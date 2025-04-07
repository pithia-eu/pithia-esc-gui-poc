import json
import logging
import os
import requests
import urllib.parse
from dateutil import parser
from django.db import transaction
from django.urls import reverse_lazy
from lxml import etree
from pathlib import Path
from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.handleclient import (
    PyHandleClient,
    RESTHandleClient
)

from common.models import (
    DataSubset,
    DataCollection,
    HandleURLMapping,
    Individual,
    Organisation,
)
from metadata_editor.editor_dataclasses import (
    DoiKernelMetadataUpdate,
)
from metadata_editor.services import (
    DataSubsetEditor,
    SimpleDataSubsetEditor,
)
from metadata_editor.service_utils import (
    Namespace,
    NamespacePrefix,
)
from utils.dict_helpers import flatten


logger = logging.getLogger(__name__)


class HandleRegistrationProcessForDataSubset:
    data_subset: DataSubset
    data_subset_url_in_handle_record: str
    data_collection: DataCollection
    doi_kernel_metadata: DoiKernelMetadataUpdate
    doi_kernel_metadata_xml_string: str
    handle_name: str
    owner_id: str
    principal_agent_name: str
    xml_string_with_doi_kernel_metadata: str

    def __init__(self, data_subset: DataSubset, owner_id: str) -> None:
        self.handle_client = HandleClient()
        self.data_subset = data_subset
        self.owner_id = owner_id
        try:
            self.data_collection = DataCollection.objects.get_by_metadata_server_url(self.data_subset.data_collection_url)
        except DataCollection.DoesNotExist:
            pass
        except KeyError:
            pass

    def _get_organisation_for_related_party(
            self,
            related_parties,
            role: str = '',
            related_party_data: dict = None):
        if role:
            related_party_data = next(
                (
                    rp
                    for rp in related_parties
                    if rp.get('role') == role
                ),
                {}
            )
        party_urls = related_party_data.get('parties', [])
        if not party_urls:
            return None

        organisation = None
        for party_url in party_urls:
            try:
                individual = Individual.objects.get_by_metadata_server_url(party_url)
                party_url = individual.organisation_url
            except Individual.DoesNotExist:
                pass
            except KeyError:
                continue

            try:
                organisation = Organisation.objects.get_by_metadata_server_url(party_url)
                return organisation
            except Organisation.DoesNotExist:
                pass

        return None

    def _get_organisation_responsible_for_data_collection(self):
        try:
            related_parties = self.data_collection.properties.related_parties
        except AttributeError:
            return None
        if not related_parties:
            return None
        
        # Find the organisation responsible in order
        # of importance.
        # Data provider
        data_provider = self._get_organisation_for_related_party(
            related_parties,
            role='https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider'
        )
        if data_provider:
            return data_provider
        # Point of contact
        point_of_contact = self._get_organisation_for_related_party(
            related_parties,
            role='https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact'
        )
        if point_of_contact:
            return point_of_contact
        # If a data provider or point of contact
        # does not exist, then the first related
        # party found is returned, or None if none
        # are still not found.
        for related_party in related_parties:
            related_party_organisation = self._get_organisation_for_related_party(
                related_parties,
                related_party_data=related_party
            )
            if not related_party_organisation:
                continue
            return related_party_organisation
        
        return None
    
    def _get_principal_agent_name_from_data_collection(self):
        organisation = self._get_organisation_responsible_for_data_collection()
        if not organisation or not organisation.name:
            return 'Unknown'
        return organisation.name
    
    def _register_handle_for_data_subset(self):
        # The eSC website domain is pre-pended to
        # the reversed URL name for the data subset
        # detail page.
        return self.handle_client.create_and_register_handle_for_resource_url(
            self.data_subset_url_in_handle_record
        )

    def _create_doi_kernel_metadata_with_spoofed_doi_details_for_data_subset(self):
        # referent_doi_name and registration_agency_doi_name
        # are changed so the doi kernel metadata will pass
        # XSD validation.
        # referent_doi_name will be changed after the data
        # subset XML is generated.
        return DoiKernelMetadataUpdate(
            referent_doi_name='10.000/000',
            primary_referent_type='Creation',
            registration_agency_doi_name='10.000/000',
            doi_issue_date=self.handle_client.get_date_handle_was_issued_as_string(self.handle_name),
            doi_issue_number=1,
            rc_name_primary_language='en',
            rc_name_value=self.data_subset.name,
            rc_name_type='Name',
            rc_identifier_non_uri_value=self.handle_name,
            rc_identifier_uri_return_type='text/html',
            rc_identifier_uri_value=f'https://hdl.handle.net/{self.handle_name}',
            rc_identifier_type='URI',
            rc_structural_type='Digital',
            rc_mode='Visual',
            rc_character='Language',
            rc_type='Dataset',
            rc_principal_agent_name_value=self.principal_agent_name,
            rc_principal_agent_name_type='Name'
        )
    
    def _get_data_subset_xml_with_spoofed_doi_kernel_metadata(self):
        data_subset_editor = DataSubsetEditor(self.data_subset.xml)
        data_subset_editor.update_doi_kernel_metadata(self.doi_kernel_metadata)
        return data_subset_editor.to_xml()
    
    def _replace_referent_doi_name_with_handle_name(self):
        simple_data_subset_editor = SimpleDataSubsetEditor(
            self.xml_string_with_doi_kernel_metadata
        )
        simple_data_subset_editor.update_referent_doi_name_if_exists(
            self.handle_name
        )
        return simple_data_subset_editor.to_xml()
    
    def _get_doi_kernel_metadata_from_data_subset_xml(self):
        xml_string_parsed = etree.fromstring(
            self.xml_string_with_doi_kernel_metadata
        )
        doi_element = xml_string_parsed.find('.//{%s}doi' % Namespace.PITHIA)
        doi_element_reduced_namespaces = etree.Element('doi', nsmap={
            None: Namespace.PITHIA,
            NamespacePrefix.DOI: Namespace.DOI,
        })
        for child in doi_element:
            doi_element_reduced_namespaces.append(child)
        etree.indent(doi_element_reduced_namespaces, space='\t')
        return etree.tostring(
            doi_element_reduced_namespaces,
            doctype='<?xml version="1.0" encoding="UTF-8"?>'
        ).decode()
    
    def _update_data_subset_with_doi_kernel_metadata_in_database(self):
        with transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME']):
            DataSubset.objects.update_from_xml_string(
                self.data_subset.pk,
                self.xml_string_with_doi_kernel_metadata,
                self.owner_id
            )
            handle_url_mapping = HandleURLMapping(
                id=self.handle_name,
                handle_name=self.handle_name,
                url=self.data_subset_url_in_handle_record
            )
            handle_url_mapping.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])

    def _update_handle_with_doi_kernel_metadata(self):
        return self.handle_client.add_doi_kernel_metadata_to_handle(
            self.handle_name,
            self.doi_kernel_metadata_xml_string
        )
    
    def run(self):
        try:
            data_subset_detail_page_url = reverse_lazy(
                'browse:data_subset_detail',
                kwargs={
                    'data_subset_id': self.data_subset.pk,
                }
            )
            self.data_subset_url_in_handle_record = f'{os.environ["HANDLE_URL_PREFIX"]}{str(data_subset_detail_page_url)}'
            self.handle_name = self._register_handle_for_data_subset()
            self.principal_agent_name = self._get_principal_agent_name_from_data_collection()
            self.doi_kernel_metadata = self._create_doi_kernel_metadata_with_spoofed_doi_details_for_data_subset()
            self.xml_string_with_doi_kernel_metadata = self._get_data_subset_xml_with_spoofed_doi_kernel_metadata()
            self.xml_string_with_doi_kernel_metadata = self._replace_referent_doi_name_with_handle_name()
            self.doi_kernel_metadata_xml_string = self._get_doi_kernel_metadata_from_data_subset_xml()
            self._update_handle_with_doi_kernel_metadata()
            self._update_data_subset_with_doi_kernel_metadata_in_database()
            return self.handle_name
        except Exception:
            logger.exception('An unexpected error occurred whilst registering a handle with a data subset.')
        
        if not self.handle_client or not self.handle_name:
            return None

        try:
            logger.info(f'Attempting to delete handle {self.handle_name} after error occurred...')
            self.handle_client.delete_handle(self.handle_name)
            logger.info(f'Deleted handle {self.handle_name}.')
        except Exception:
            logger.exception(f'An unexpected error occurred whilst trying to delete incomplete handle {self.handle_name}.')

        return None


class HandleClient:
    credentials: PIDClientCredentials
    client: RESTHandleClient

    def __init__(self) -> None:
        # Create
        self._create_credentials_json_file_if_needed()
        self.credentials = PIDClientCredentials.load_from_JSON('credentials.json')
        self.handle_prefix = self.credentials.get_prefix()
        self.client = PyHandleClient('rest').instantiate_with_credentials(self.credentials)

    def _create_credentials_json_file_if_needed(self):
        credentials_json_file = Path('credentials.json')
        if credentials_json_file.is_file():
            return
        with open('credentials.json', 'w+') as credentials_json_file:
            credentials_data = {
                'client': os.environ['HANDLE_API_CLIENT'],
                'handle_server_url': os.environ['HANDLE_API_ENDPOINT_URL'],
                'baseuri': os.environ['HANDLE_API_ENDPOINT_URL'],
                'username': os.environ['HANDLE_API_USERNAME'],
                'password': os.environ['HANDLE_API_KEY'],
                'prefix': os.environ['HANDLE_PREFIX'],
            }
            json.dump(credentials_data, credentials_json_file, indent=4)

    def _create_handle_name_with_suffix(self, handle_suffix: str) -> str:
        return f'{self.handle_prefix}/{handle_suffix}'
    
    def _get_value_from_handle(self, handle_name: str, key: str):
        return self.client.get_value_from_handle(handle_name, key)

    def _get_handles_with_prefix(self, prefix):
        handle_api_endpoint = os.environ['HANDLE_API_ENDPOINT_URL']
        response = requests.get(
            f'{handle_api_endpoint}/api/handles?prefix={prefix}',
            auth=(urllib.parse.quote_plus(os.environ['HANDLE_API_USERNAME']), os.environ['HANDLE_API_KEY'])
        )
        handles_with_prefix = response.json()
        return handles_with_prefix

    def register_handle(
            self,
            handle_name: str,
            handle_value: str) -> str:
        logger.info(f'Registering handle {handle_name}')
        register_result = self.client.register_handle(handle_name, handle_value)

        if register_result == handle_name:
            logger.info('OK: Register handle successful.')
        else:
            logger.info('PROBLEM: Register handle returned unexpected response.')

        return register_result

    def create_and_register_handle_for_resource_url(
            self,
            resource_url: str) -> str:
        # Registers a randomly-generated handle name
        # for the resource URL.
        new_handle_name = self.client.generate_and_register_handle(
            self.handle_prefix,
            resource_url
        )
        return new_handle_name

    def create_and_register_handle_for_resource(
            self,
            resource_id: str) -> str:
        handle = self._create_handle_name_with_suffix(resource_id)
        resource_details_page_url = reverse_lazy(
            'browse:data_subset_detail',
            kwargs={
                'data_subset_id': resource_id
            }
        )
        # Prefixes the domain name to the details page URL.
        resource_details_page_url_string = f'{os.environ["HANDLE_URL_PREFIX"]}{str(resource_details_page_url)}'
        self.register_handle(handle, resource_details_page_url_string)
        return handle

    def delete_handle(self, handle_name: str):
        delete_result = self.client.delete_handle(handle_name)
        logger.info('OK: Delete handle successful.')
        return delete_result
    
    def get_registered_handles(self):
        return self._get_handles_with_prefix(self.handle_prefix)

    def get_handle_record(self, handle_name: str) -> dict:
        handle_record = self.client.retrieve_handle_record(handle_name)

        if handle_record != None:
            logger.info('OK: Handle exists.')
        else:
            logger.error('PROBLEM: Retrieving handle record returned unexpected response.')

        return handle_record

    def get_handle_raw(self, handle_name: str) -> dict:
        handle_api_endpoint = os.environ['HANDLE_API_ENDPOINT_URL']
        response = requests.get(f'{handle_api_endpoint}/api/handles/{handle_name}')
        handle_raw = response.json()
        return handle_raw

    def get_data_subset_detail_page_url_from_handle(self, handle_name: str) -> str:
        return self._get_value_from_handle(handle_name, 'URL')

    def get_handle_issue_number(self, handle_name: str) -> str:
        return self._get_value_from_handle(handle_name, 'issueNumber')

    def get_time_handle_was_issued_as_string(self, handle_name: str) -> str:
        handle_raw = self.get_handle_raw(handle_name)
        date_issued = handle_raw['values'][0]['timestamp']
        return date_issued

    def get_date_handle_was_issued_as_string(self, handle_name: str) -> str:
        handle_issue_time_string = self.get_time_handle_was_issued_as_string(handle_name)
        handle_issue_date = parser.isoparse(handle_issue_time_string).strftime('%Y-%m-%d')
        return handle_issue_date

    def add_doi_kernel_metadata_to_handle(
            self,
            handle: str,
            doi_kernel_metadata_xml_string: str):
        modify_result = self.client.modify_handle_value(
            handle,
            DOI_KERNEL_METADATA=doi_kernel_metadata_xml_string,
            add_if_not_exist=True
        )
        return modify_result

    def update_data_subset_detail_page_url_for_handle(
            self,
            handle_name: str,
            new_handle_value: str):
        # Increment current handle issue number
        issue_number = self.get_handle_issue_number(handle_name)
        if not issue_number:
            issue_number = 1
        new_issue_number = int(issue_number) + 1
        update_dict = {
            'URL': new_handle_value,
            'issueNumber': new_issue_number,
        }
        # Pass updated URL and issue number as kw args
        modify_result = self.client.modify_handle_value(handle_name, **update_dict)
        get_url_result = self.get_data_subset_detail_page_url_from_handle(handle_name)
        get_issue_number_result = self.get_handle_issue_number(handle_name)
        # If both handle and issue number not updated,
        # assume something went wrong.
        if (not (get_url_result == new_handle_value
            and str(get_issue_number_result) == str(new_issue_number))):
            logger.critical('CRITICAL: Modify handle URL returned unexpected value.')
            logger.info(f'Expected URL: {new_handle_value}')
            logger.info(f'Returned URL: {get_url_result}')
            logger.info(f'Expected issue number: {str(new_issue_number)}')
            logger.info(f'Returned issue number: {str(get_issue_number_result)}')
            return modify_result

        logger.info('OK: Update handle URL successful.')
        return modify_result