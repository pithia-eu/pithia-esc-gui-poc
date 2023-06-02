import re
import validators
from django.core.exceptions import ObjectDoesNotExist
from operator import itemgetter
from rdflib import (
    Graph,
    URIRef,
    RDF,
    SKOS,
)
from requests import get
from typing import Optional

from .services import (
    AcquisitionCapabilitiesXMLMetadataFile,
    XMLMetadataFile,
)

from common.models import (
    Instrument,
    ScientificMetadata,
)
from utils.url_helpers import (
    divide_resource_url_into_main_components,
    divide_resource_url_from_op_mode_id,
    divide_catalogue_related_resource_url_into_main_components,
)


PITHIA_METADATA_SERVER_URL_BASE = 'metadata.pithia.eu/resources/2.2'
SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE = 'metadata.pithia.eu/ontology/2.2'
PITHIA_METADATA_SERVER_HTTPS_URL_BASE = f'https://{PITHIA_METADATA_SERVER_URL_BASE}'
SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE = f'https://{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE}'


class MetadataFileOntologyURLReferencesValidator:
    def _is_ontology_term_url_valid(self, ontology_term_url: str):
        """
        Checks that the provided Space Physics Ontology URL
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
    def is_each_url_valid(cls, xml_file: XMLMetadataFile) -> Optional(list[str]):
        """
        Checks each Space Physics Ontology URL in the
        provided XML metadata file is valid.
        """
        invalid_urls = []
        ontology_urls = xml_file.ontology_urls
        for url in ontology_urls:
            is_valid_ontology_term = cls._is_ontology_term_url_valid(url)
            if is_valid_ontology_term == False:
                invalid_urls.append(url)
        if len(invalid_urls) > 0:
            return invalid_urls

class MetadataFileMetadataURLReferencesValidator:
    def _is_resource_url_well_formed(self, resource_url):
        return validators.url(resource_url)
    
    def _divide_resource_url_into_components(self, resource_url):
        try:
            return divide_catalogue_related_resource_url_into_main_components(resource_url)
        except IndexError:
            return divide_resource_url_into_main_components(resource_url)

    def _is_resource_url_structure_valid(self, resource_url):
        url_base, resource_type_in_resource_url, namespace, localid = itemgetter('url_base', 'resource_type', 'namespace', 'localid')(self._divide_resource_url_into_components(resource_url))

        # Verify resource type in resource URL is valid
        scientific_metadata_subclasses = ScientificMetadata.__subclasses__
        is_resource_type_in_resource_url_valid = any(resource_type_in_resource_url == cls.type_in_metadata_server_url for cls in scientific_metadata_subclasses)

        # Verify that the localID base used in the resource
        # URL is valid (matches the resource type used in
        # the resource URL).
        localid_base = localid.split('_')[0]
        is_localid_base_valid = any(localid_base == cls.localid_base for cls in scientific_metadata_subclasses)
        is_resource_type_in_resource_url_matching_with_localid_base = any(resource_type_in_resource_url == cls.type_in_metadata_server_url and localid_base == cls.localid_base for cls in scientific_metadata_subclasses)

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

    def _is_resource_url_valid(self, resource_url):
        validation_summary_for_metadata_server_url = {
            'is_structure_valid': False,
            'is_pointing_to_registered_resource': False,
            'type_of_missing_resource': None,
        }
        if not self._is_resource_url_well_formed(resource_url):
            return validation_summary_for_metadata_server_url
        
        if not self._is_resource_url_structure_valid(resource_url):
            return validation_summary_for_metadata_server_url
        validation_summary_for_metadata_server_url['is_structure_valid'] = True

        try:
            ScientificMetadata.objects.get_by_metadata_server_url(resource_url)
        except ObjectDoesNotExist:
            resource_type_in_resource_url, localid = itemgetter('resource_type', 'localid')(self._divide_resource_url_into_components(resource_url))
            validation_summary_for_metadata_server_url['type_of_missing_resource'] = resource_type_in_resource_url
            if resource_type_in_resource_url == 'catalogue':
                validation_summary_for_metadata_server_url['type_of_missing_resource'] += f'_{localid}'
            return validation_summary_for_metadata_server_url
        validation_summary_for_metadata_server_url['is_pointing_to_registered_resource'] = True

        return validation_summary_for_metadata_server_url

    @classmethod
    def is_each_url_valid(cls, xml_file: XMLMetadataFile) -> Optional(list[str]):
        """
        Checks that each metadata server URL is well-formed and that each URL
        corresponds with a metadata registration in the e-Science Centre.
        """
        invalid_urls_dict = {
            'urls_with_incorrect_structure': [],
            'urls_pointing_to_unregistered_resources': [],
            'types_of_missing_resources': [],
        }
        resource_urls = xml_file.metadata_urls
        for resource_url in resource_urls:
            is_structure_valid, is_pointing_to_registered_resource, type_of_missing_resource = itemgetter('is_structure_valid', 'is_pointing_to_registered_resource', 'type_of_missing_resource')(cls._is_resource_url_valid(resource_url))
            if not is_structure_valid:
                invalid_urls_dict['urls_with_incorrect_structure'].append(resource_url)
            elif not is_pointing_to_registered_resource:
                invalid_urls_dict['urls_pointing_to_unregistered_resources'].append(resource_url)
                invalid_urls_dict['types_of_missing_resources'].append(type_of_missing_resource)
                invalid_urls_dict['types_of_missing_resources'] = list(set(invalid_urls_dict['types_of_missing_resources']))

        if any(len(l) > 0 for l in invalid_urls_dict.values()):
            return invalid_urls_dict

    @classmethod
    def is_each_operation_mode_url_valid(cls, xml_file: AcquisitionCapabilitiesXMLMetadataFile) -> Optional(list[str]):
        """
        Checks that each metadata server URL is well-formed and that each URL
        corresponds with a metadata registration in the e-Science Centre.
        """
        invalid_urls_dict = {
            'urls_with_incorrect_structure': [],
            'urls_pointing_to_unregistered_resources': [],
            'urls_pointing_to_registered_resources_with_missing_op_modes': [],
            'types_of_missing_resources': [],
        }
        resource_urls_with_op_mode_ids = xml_file.operational_mode_urls
        for resource_url_with_op_mode_id in resource_urls_with_op_mode_ids:
            resource_url, op_mode_id = itemgetter('resource_url', 'op_mode_id')(divide_resource_url_from_op_mode_id(resource_url_with_op_mode_id))
            is_structure_valid, is_pointing_to_registered_resource, type_of_missing_resource = itemgetter('is_structure_valid', 'is_pointing_to_registered_resource', 'type_of_missing_resource')(cls._is_resource_url_valid(resource_url))
            if not is_structure_valid:
                invalid_urls_dict['urls_with_incorrect_structure'].append(resource_url_with_op_mode_id)
            elif not is_pointing_to_registered_resource:
                invalid_urls_dict['urls_pointing_to_unregistered_resources'].append(resource_url_with_op_mode_id)
                invalid_urls_dict['types_of_missing_resources'].append(type_of_missing_resource)
                invalid_urls_dict['types_of_missing_resources'] = list(set(invalid_urls_dict['types_of_missing_resources']))
                
            if is_pointing_to_registered_resource:
                resource_with_op_mode_id = Instrument.objects.get_by_operational_mode_url(resource_url_with_op_mode_id)
                if resource_with_op_mode_id == None:
                    invalid_urls_dict['urls_pointing_to_registered_resources_with_missing_op_modes'].append(resource_url_with_op_mode_id)
        
        if any(len(l) > 0 for l in invalid_urls_dict.values()):
            return invalid_urls_dict