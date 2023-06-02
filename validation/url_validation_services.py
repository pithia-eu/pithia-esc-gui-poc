import re
import validators
from operator import itemgetter
from rdflib import (
    Graph,
    URIRef,
    RDF,
    SKOS,
)
from requests import get
from typing import Optional

from .services import XMLMetadataFile
from .url_validation_utils import (
    get_resource_by_pithia_identifier_components,
    get_resource_by_pithia_identifier_components_and_op_mode_id,
)

from common.helpers import (
    get_mongodb_model_by_resource_type_from_resource_url,
    get_mongodb_model_from_catalogue_related_resource_url,
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


class MetadataFileMetadataURLReferencesValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        pass

class MetadataFileOntologyURLReferencesValidator:
    @classmethod
    def _validate_ontology_term_url(self, ontology_term_url: str):
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
            is_valid_ontology_term = cls._validate_ontology_term_url(url)
            if is_valid_ontology_term == False:
                invalid_urls.append(url)
        if len(invalid_urls) > 0:
            return invalid_urls

# Resource url validation
def is_resource_url_base_structure_valid(resource_url):
    if not validators.url(resource_url):
        return False

    return all([
        resource_url.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE),
        resource_url.count(PITHIA_METADATA_SERVER_HTTPS_URL_BASE) == 1,
    ])

def is_data_collection_related_url_structure_valid(resource_url):
    url_base, resource_type_in_resource_url, namespace, localid = itemgetter('url_base', 'resource_type', 'namespace', 'localid')(divide_resource_url_into_main_components(resource_url))
    resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type_in_resource_url)
    
    localid_base = resource_type_in_resource_url.capitalize()
    # Exceptions to localid starting with resource_type_in_resource_url.capitalize():
    if resource_type_in_resource_url == 'collection':
        localid_base = 'DataCollection'
    elif resource_type_in_resource_url == 'acquisitionCapabilities':
        localid_base = 'AcquisitionCapabilities'
    elif resource_type_in_resource_url == 'computationCapabilities':
        localid_base = 'ComputationCapabilities'
    elif resource_type_in_resource_url == 'process':
        localid_base = 'CompositeProcess'
    is_localid_base_matching_resource_type_in_resource_url = localid.startswith(localid_base)

    return all([
        resource_mongodb_model != 'unknown',
        url_base == PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
        len(re.findall(f'(?=/{resource_type_in_resource_url}/)', resource_url)) == 1,
        len(re.findall(f'(?=/{namespace}/)', resource_url)) == 1,
        len(re.findall(f'(?=/{localid})', resource_url)) == 1,
        resource_url.endswith(localid),
        is_localid_base_matching_resource_type_in_resource_url,
    ])

def is_catalogue_related_url_structure_valid(resource_url):
    url_base, resource_type_in_resource_url, namespace, localid = itemgetter('url_base', 'resource_type', 'namespace', 'localid')(divide_catalogue_related_resource_url_into_main_components(resource_url))
    resource_mongodb_model = get_mongodb_model_from_catalogue_related_resource_url(resource_url)

    return all([
        resource_mongodb_model != 'unknown', # 'unknown' means that the catalogue-metadata type is unsupported
        url_base == PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
        resource_type_in_resource_url == 'catalogue',
        len(re.findall(f'(?=/{resource_type_in_resource_url}/)', resource_url)) == 1,
        len(re.findall(f'(?=/{namespace}/)', resource_url)) == 1,
        len(re.findall(f'(?=/{localid})', resource_url)) == 1,
        resource_url.endswith(localid),
    ])

def validate_resource_url(resource_url):
    validation_details = {
        'is_structure_valid': False,
        'is_pointing_to_registered_resource': False,
        'type_of_missing_resource': None,
    }
    resource_type_in_resource_url = ''
    namespace = ''
    localid = ''
    resource_mongodb_model = None
    referenced_resource = None
    if not is_resource_url_base_structure_valid(resource_url):
        return validation_details
    
    if '/catalogue/' in resource_url:
        resource_type_in_resource_url, namespace, localid = itemgetter('resource_type', 'namespace', 'localid')(divide_catalogue_related_resource_url_into_main_components(resource_url))
        resource_mongodb_model = get_mongodb_model_from_catalogue_related_resource_url(resource_url)
        if not is_catalogue_related_url_structure_valid(resource_url):
            return validation_details
    else:
        resource_type_in_resource_url, namespace, localid = itemgetter('resource_type', 'namespace', 'localid')(divide_resource_url_into_main_components(resource_url))
        resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type_in_resource_url)
        if not is_data_collection_related_url_structure_valid(resource_url):
            return validation_details
    validation_details['is_structure_valid'] = True

    if resource_mongodb_model != 'unknown':
        referenced_resource = get_resource_by_pithia_identifier_components(resource_mongodb_model, localid, namespace)
    if referenced_resource == None:
        validation_details['type_of_missing_resource'] = resource_type_in_resource_url
        if resource_type_in_resource_url == 'catalogue':
            validation_details['type_of_missing_resource'] += f'_{localid}'
        return validation_details
    validation_details['is_pointing_to_registered_resource'] = True

    return validation_details

def get_invalid_resource_urls_from_parsed_xml(xml_file_parsed):
    invalid_urls = {
        'urls_with_incorrect_structure': [],
        'urls_pointing_to_unregistered_resources': [],
        'types_of_missing_resources': [],
    }
    root = xml_file_parsed.getroot()
    resource_urls = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and not(contains(@xlink:href, '#'))]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for resource_url in resource_urls:
        is_structure_valid, is_pointing_to_registered_resource, type_of_missing_resource = itemgetter('is_structure_valid', 'is_pointing_to_registered_resource', 'type_of_missing_resource')(validate_resource_url(resource_url))
        if not is_structure_valid:
            invalid_urls['urls_with_incorrect_structure'].append(resource_url)
        elif not is_pointing_to_registered_resource:
            invalid_urls['urls_pointing_to_unregistered_resources'].append(resource_url)
            invalid_urls['types_of_missing_resources'].append(type_of_missing_resource)
            invalid_urls['types_of_missing_resources'] = list(set(invalid_urls['types_of_missing_resources']))

    return invalid_urls

def get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml(xml_file_parsed):
    invalid_urls = {
        'urls_with_incorrect_structure': [],
        'urls_pointing_to_unregistered_resources': [],
        'urls_pointing_to_registered_resources_with_missing_op_modes': [],
        'types_of_missing_resources': [],
    }
    root = xml_file_parsed.getroot()
    resource_urls_with_op_mode_ids = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and contains(@xlink:href, '#')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for resource_url_with_op_mode_id in resource_urls_with_op_mode_ids:
        resource_url, op_mode_id = itemgetter('resource_url', 'op_mode_id')(divide_resource_url_from_op_mode_id(resource_url_with_op_mode_id))
        is_structure_valid, is_pointing_to_registered_resource, type_of_missing_resource = itemgetter('is_structure_valid', 'is_pointing_to_registered_resource', 'type_of_missing_resource')(validate_resource_url(resource_url))
        if not is_structure_valid:
            invalid_urls['urls_with_incorrect_structure'].append(resource_url_with_op_mode_id)
        elif not is_pointing_to_registered_resource:
            invalid_urls['urls_pointing_to_unregistered_resources'].append(resource_url_with_op_mode_id)
            invalid_urls['types_of_missing_resources'].append(type_of_missing_resource)
            invalid_urls['types_of_missing_resources'] = list(set(invalid_urls['types_of_missing_resources']))
            
        if is_pointing_to_registered_resource:
            resource_type_in_resource_url, namespace, localid = itemgetter('resource_type', 'namespace', 'localid')(divide_resource_url_into_main_components(resource_url))
            resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type_in_resource_url)
            resource_with_op_mode_id = get_resource_by_pithia_identifier_components_and_op_mode_id(resource_mongodb_model, localid, namespace, op_mode_id)
            if resource_with_op_mode_id == None:
                invalid_urls['urls_pointing_to_registered_resources_with_missing_op_modes'].append(resource_url_with_op_mode_id)
            
    return invalid_urls