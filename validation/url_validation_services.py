import re
import validators
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from operator import itemgetter
from rdflib import (
    Graph,
    URIRef,
    RDF,
    SKOS,
)
from requests import get
from typing import List

from .file_wrappers import (
    AcquisitionCapabilitiesXMLMetadataFile,
    XMLMetadataFile,
)
from .helpers import (
    create_register_url_from_resource_type_from_resource_url,
)

from common.constants import PITHIA_METADATA_SERVER_HTTPS_URL_BASE
from common.models import (
    Instrument,
    ScientificMetadata,
)
from utils.url_helpers import (
    divide_resource_url_into_main_components,
    divide_resource_url_from_op_mode_id,
)


class MetadataFileOntologyURLReferencesValidator:
    @classmethod
    def _is_ontology_term_url_valid(cls, ontology_term_url: str):
        """Checks that the provided Space Physics Ontology URL
        has a valid HTTP response and that the response
        content is as expected.

        If the HTTP response code is 404 Not Found, the
        ontology term URL is treated as invalid.

        Any other HTTP response error code is treated
        as unexpected.
        """
        # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
        response = get(ontology_term_url)
        if response.status_code == 404:
            return False
        if response.ok:
            response_text = response.text
            g = Graph()
            g.parse(data=response_text, format='application/rdf+xml')
            ontology_term = URIRef(ontology_term_url)
            return (ontology_term, RDF['type'], SKOS['Concept']) in g
        response.raise_for_status()
        return False

    @classmethod
    def _is_each_ontology_url_valid(cls, ontology_urls: list):
        invalid_urls = []
        for url in ontology_urls:
            is_valid_ontology_term = cls._is_ontology_term_url_valid(url)
            if is_valid_ontology_term == False:
                invalid_urls.append(url)
        return invalid_urls
    
    @classmethod
    def is_each_ontology_url_in_xml_file_valid(cls, xml_file: XMLMetadataFile) -> List[str]:
        """Checks each Space Physics Ontology URL in the
        provided XML metadata file is valid.
        """
        ontology_urls = xml_file.ontology_urls
        return cls._is_each_ontology_url_valid(ontology_urls)
    
    @classmethod
    def is_each_potential_ontology_url_in_xml_file_valid(cls, xml_file: XMLMetadataFile) -> list[str]:
        """Checks each Space Physics Ontology URL in the
        provided XML metadata file is valid.
        """
        ontology_urls = xml_file.potential_ontology_urls
        return cls._is_each_ontology_url_valid(ontology_urls)


class MetadataFileMetadataURLReferencesValidator:
    # Keys to access invalid URL categories
    INCORRECTLY_STRUCTURED_URLS_KEY = 'urls_with_incorrect_structure'
    UNREGISTERED_RESOURCE_URLS_KEY = 'urls_pointing_to_unregistered_resources'
    UNREGISTERED_RESOURCE_URL_TYPES_KEY = 'types_of_missing_resources'
    UNREGISTERED_OPERATIONAL_MODE_URLS_KEY = 'urls_pointing_to_registered_resources_with_missing_op_modes'

    @classmethod
    def _is_resource_url_well_formed(cls, resource_url):
        return validators.url(resource_url)
    
    @classmethod
    def _divide_resource_url_into_components(cls, resource_url):
        return divide_resource_url_into_main_components(resource_url)

    @classmethod
    def _is_resource_url_structure_valid(cls, resource_url):
        url_base, resource_type_in_resource_url, namespace, localid = itemgetter('url_base', 'resource_type', 'namespace', 'localid')(cls._divide_resource_url_into_components(resource_url))
        if any(
            component is None
            for component in [
                url_base,
                resource_type_in_resource_url,
                namespace,
                localid
            ]):
            return False

        # Verify resource type in resource URL is valid
        scientific_metadata_subclasses = ScientificMetadata.__subclasses__()
        is_resource_type_in_resource_url_valid = any(resource_type_in_resource_url == cls.type_in_metadata_server_url for cls in scientific_metadata_subclasses)

        # Verify that the localID base used in the resource
        # URL is valid (matches the resource type used in
        # the resource URL).
        localid_base = localid.split('_')[0]
        is_localid_base_valid = any(
            localid_base == cls.localid_base
            for cls in scientific_metadata_subclasses
        )
        is_resource_type_in_resource_url_matching_with_localid_base = any(
            (
                resource_type_in_resource_url == cls.type_in_metadata_server_url
                and localid_base == cls.localid_base
            )
            for cls in scientific_metadata_subclasses
        )

        return all([
            resource_url.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE),
            resource_url.count(PITHIA_METADATA_SERVER_HTTPS_URL_BASE) == 1,
            is_resource_type_in_resource_url_valid,
            is_localid_base_valid,
            is_resource_type_in_resource_url_matching_with_localid_base,
            url_base == PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
            len(re.findall(f'(?=/{resource_type_in_resource_url}/)', resource_url)) == 1,
            len(re.findall(f'(?=/{namespace}/)', resource_url)) == 1,
            len(re.findall(f'(?=/{localid})', resource_url)) == 1,
            resource_url.endswith(localid),
        ])

    @classmethod
    def _is_resource_url_valid(cls, resource_url):
        validation_summary_for_metadata_server_url = {
            'is_structure_valid': False,
            'is_pointing_to_registered_resource': False,
            'type_of_missing_resource': None,
        }
        if not cls._is_resource_url_well_formed(resource_url):
            return validation_summary_for_metadata_server_url
        
        if not cls._is_resource_url_structure_valid(resource_url):
            return validation_summary_for_metadata_server_url
        validation_summary_for_metadata_server_url['is_structure_valid'] = True

        try:
            ScientificMetadata.objects.get_by_metadata_server_url(resource_url)
        except ObjectDoesNotExist:
            resource_type_in_resource_url, localid = itemgetter('resource_type', 'localid')(cls._divide_resource_url_into_components(resource_url))
            validation_summary_for_metadata_server_url['type_of_missing_resource'] = resource_type_in_resource_url
            if resource_type_in_resource_url == 'catalogue':
                validation_summary_for_metadata_server_url['type_of_missing_resource'] = ('catalogue', localid)
            return validation_summary_for_metadata_server_url
        validation_summary_for_metadata_server_url['is_pointing_to_registered_resource'] = True

        return validation_summary_for_metadata_server_url

    @classmethod
    def _is_each_resource_url_valid(cls, resource_urls: List[str]) -> dict:
        """Checks that each metadata server URL is well-formed and that each URL
        corresponds with a metadata registration in the e-Science Centre.
        """
        invalid_urls_dict = {
            cls.INCORRECTLY_STRUCTURED_URLS_KEY: [],
            cls.UNREGISTERED_RESOURCE_URLS_KEY: [],
            cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY: [],
        }
        for resource_url in resource_urls:
            is_structure_valid, is_pointing_to_registered_resource, type_of_missing_resource = itemgetter(
                'is_structure_valid',
                'is_pointing_to_registered_resource',
                'type_of_missing_resource'
            )(cls._is_resource_url_valid(resource_url))
            if not is_structure_valid:
                invalid_urls_dict[cls.INCORRECTLY_STRUCTURED_URLS_KEY].append(
                    resource_url
                )
            elif not is_pointing_to_registered_resource:
                invalid_urls_dict[cls.UNREGISTERED_RESOURCE_URLS_KEY].append(resource_url)
                invalid_urls_dict[cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY].append(type_of_missing_resource)
        # Remove duplicate resource URL types
        invalid_urls_dict[cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY] = list(set(invalid_urls_dict[cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY]))
        
        return invalid_urls_dict

    @classmethod
    def is_each_resource_url_valid(cls, xml_file: XMLMetadataFile) -> dict:
        """Checks that each metadata server URL is valid by
        meeting a specified set of criteria.
        """
        resource_urls = xml_file.metadata_urls
        return cls._is_each_resource_url_valid(resource_urls)

    @classmethod
    def is_each_potential_resource_url_valid(cls, xml_file: XMLMetadataFile) -> dict:
        """Checks that each potential metadata server URL is valid by
        meeting a specified set of criteria.
        """
        resource_urls = xml_file.potential_metadata_urls
        return cls._is_each_resource_url_valid(resource_urls)

    @classmethod
    def is_each_operational_mode_url_valid(cls, xml_file: AcquisitionCapabilitiesXMLMetadataFile) -> dict:
        """Checks that each operational mode URL is well-formed and that
        each URL corresponds with a metadata registration in the
        e-Science Centre.
        """
        try:
            resource_urls_with_op_mode_ids = xml_file.operational_mode_urls
        except:
            return cls._is_each_resource_url_valid([])
        resource_urls = [itemgetter('resource_url')(divide_resource_url_from_op_mode_id(url)) for url in resource_urls_with_op_mode_ids]
        invalid_urls_dict = cls._is_each_resource_url_valid(resource_urls)
        invalid_urls_dict[cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY] = []

        for url in resource_urls_with_op_mode_ids:
            try:
                Instrument.objects.get_by_operational_mode_url(url)
            except ObjectDoesNotExist:
                invalid_urls_dict[cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY].append(url)
        
        return invalid_urls_dict

    @classmethod
    def is_each_potential_operational_mode_url_valid(cls, xml_file: AcquisitionCapabilitiesXMLMetadataFile) -> dict:
        """Checks that each potential operational mode URL is well-formed
        and that each URL corresponds with a metadata registration in the
        e-Science Centre.
        """
        try:
            resource_urls_with_op_mode_ids = xml_file.potential_operational_mode_urls
        except:
            # Only Acquisition Capabilities XML files
            # have potential operational mode URLs.
            return cls._is_each_resource_url_valid([])
        resource_urls = [
            itemgetter('resource_url')(divide_resource_url_from_op_mode_id(url))
            for url in resource_urls_with_op_mode_ids
        ]
        invalid_urls_dict = cls._is_each_resource_url_valid(resource_urls)
        invalid_urls_dict[cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY] = []
        invalid_urls = []
        for key in invalid_urls_dict.keys():
            if key == cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY:
                # UNREGISTERED_RESOURCE_URL_TYPES_KEY only
                # contains types found in resource URLs.
                continue
            invalid_urls += invalid_urls_dict[key]
        invalid_urls = list(set(invalid_urls))
        safe_resource_urls_with_op_mode_ids = resource_urls_with_op_mode_ids
        for safe_url in safe_resource_urls_with_op_mode_ids:
            for invalid_url in invalid_urls:
                if invalid_url not in safe_url:
                    continue
                safe_resource_urls_with_op_mode_ids.remove(safe_url)
        safe_resource_urls_with_op_mode_ids = list(set(safe_resource_urls_with_op_mode_ids))

        for url in safe_resource_urls_with_op_mode_ids:
            try:
                Instrument.objects.get_by_operational_mode_url(url)
            except ObjectDoesNotExist:
                invalid_urls_dict[cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY].append(url)
        
        return invalid_urls_dict

    @classmethod
    def validate_and_return_errors(cls, xml_metadata_file: XMLMetadataFile):
        incorrectly_structured_url_errors = []
        unregistered_resource_url_errors = []
        unregistered_operational_mode_url_errors = []

        # Resource URL validation
        # Check which resource URLs are valid and return
        # the invalid ones.
        invalid_resource_urls = cls.is_each_potential_resource_url_valid(xml_metadata_file)
        invalid_operational_mode_urls = cls.is_each_potential_operational_mode_url_valid(xml_metadata_file)

        # Process the returned invalid resource URLs.
        incorrectly_structured_urls = invalid_resource_urls.get(cls.INCORRECTLY_STRUCTURED_URLS_KEY, []) + invalid_operational_mode_urls.get(cls.INCORRECTLY_STRUCTURED_URLS_KEY, [])
        unregistered_resource_urls = invalid_resource_urls.get(cls.UNREGISTERED_RESOURCE_URLS_KEY, []) + invalid_operational_mode_urls.get(cls.UNREGISTERED_RESOURCE_URLS_KEY, [])
        unregistered_resource_url_types = invalid_resource_urls.get(cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY, []) + invalid_operational_mode_urls.get(cls.UNREGISTERED_RESOURCE_URL_TYPES_KEY, [])
        unregistered_operational_mode_urls = invalid_operational_mode_urls.get(cls.UNREGISTERED_OPERATIONAL_MODE_URLS_KEY, [])
        
        if len(incorrectly_structured_urls) > 0:
            error_msg = render_to_string(
                'validation/error_incorrectly_structured_urls.html',
                context={
                    'incorrectly_structured_urls': incorrectly_structured_urls,
                }
            )
            incorrectly_structured_url_errors.append(error_msg)

        if len(unregistered_resource_urls) > 0:
            file_upload_registration_url_and_url_texts = list(map(
                create_register_url_from_resource_type_from_resource_url,
                unregistered_resource_url_types
            ))
            error_msg = render_to_string(
                'validation/error_unregistered_resource_urls.html',
                context={
                    'unregistered_resource_urls': unregistered_resource_urls,
                    'file_upload_registration_url_and_url_texts': file_upload_registration_url_and_url_texts,
                }
            )
            unregistered_resource_url_errors.append(error_msg)

        if len(unregistered_operational_mode_urls) > 0:
            file_upload_registration_url_and_url_texts = list(map(
                create_register_url_from_resource_type_from_resource_url,
                unregistered_resource_url_types
            ))
            error_msg = render_to_string(
                'validation/error_unregistered_operational_mode_urls.html',
                context={
                    'unregistered_resource_urls': unregistered_operational_mode_urls,
                    'file_upload_registration_url_and_url_texts': file_upload_registration_url_and_url_texts,
                }
            )
            unregistered_operational_mode_url_errors.append(error_msg)

        # Ontology URL validation
        invalid_ontology_urls = MetadataFileOntologyURLReferencesValidator.is_each_potential_ontology_url_in_xml_file_valid(xml_metadata_file)
        invalid_ontology_url_errors = []
        if len(invalid_ontology_urls) > 0:
            error_msg = render_to_string(
                'validation/error_invalid_ontology_urls.html',
                context={
                    'invalid_ontology_urls': invalid_ontology_urls,
                }
            )
            invalid_ontology_url_errors.append(error_msg)

        return {
            'incorrectly_structured_url_errors': incorrectly_structured_url_errors,
            'unregistered_resource_url_errors': unregistered_resource_url_errors,
            'unregistered_operational_mode_url_errors': unregistered_operational_mode_url_errors,
            'invalid_ontology_url_errors': invalid_ontology_url_errors,
        }