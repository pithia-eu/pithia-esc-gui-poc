import validators
from operator import itemgetter
from requests import get
from rdflib import Graph, URIRef, RDF, SKOS
from common.helpers import get_mongodb_model_by_resource_type_from_resource_url
from .url_validation_utils import get_resource_by_pithia_identifier_components, get_resource_by_pithia_identifier_components_and_op_mode_id, divide_resource_url_into_main_components, divide_resource_url_from_op_mode_id


PITHIA_METADATA_SERVER_URL_BASE = 'metadata.pithia.eu/resources/2.2'
SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE = 'metadata.pithia.eu/ontology/2.2'
PITHIA_METADATA_SERVER_HTTPS_URL_BASE = f'https://{PITHIA_METADATA_SERVER_URL_BASE}'
SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE = f'https://{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE}'

# Ontology url validation
def validate_ontology_term_url(ontology_term_url):
    response = get(ontology_term_url) # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
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

def get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed):
    invalid_urls = []
    root = xml_file_parsed.getroot()
    ontology_urls = root.xpath(f"//*[contains(@xlink:href, '{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE}')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for url in ontology_urls:
        is_valid_ontology_term = validate_ontology_term_url(url)
        if is_valid_ontology_term == False:
            invalid_urls.append(url)
    return invalid_urls

# Resource url validation
def is_resource_url_structure_valid(resource_url):
    if not validators.url(resource_url):
        return False
    resource_type, namespace, localID = itemgetter('resource_type', 'namespace', 'localID')(divide_resource_url_into_main_components(resource_url))

    is_start_of_localid_equal_to_resource_type = localID.startswith(resource_type.capitalize())
    # Exceptions to localID starting with resource_type.capitalize():
    if resource_type == 'collection':
        is_start_of_localid_equal_to_resource_type = localID.startswith('DataCollection')
    elif resource_type == 'acquisitionCapabilities':
        is_start_of_localid_equal_to_resource_type = localID.startswith('AcquisitionCapabilities')
    elif resource_type == 'computationCapabilities':
        is_start_of_localid_equal_to_resource_type = localID.startswith('ComputationCapabilities')
    elif resource_type == 'process':
        is_start_of_localid_equal_to_resource_type = localID.startswith('CompositeProcess')

    return all([
        get_mongodb_model_by_resource_type_from_resource_url(resource_type) != 'unknown',
        resource_url.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE),
        resource_url.count(PITHIA_METADATA_SERVER_HTTPS_URL_BASE) == 1,
        resource_url.count(f'/{resource_type}/') == 1,
        resource_url.count(f'/{namespace}/') == 1,
        resource_url.count(f'/{localID}') == 1,
        resource_url.endswith(localID),
        is_start_of_localid_equal_to_resource_type,
    ])

def validate_resource_url(resource_url):
    validation_details = {
        'is_structure_valid': False,
        'is_pointing_to_registered_resource': False,
        'type_of_missing_resource': None,
    }

    if not is_resource_url_structure_valid(resource_url):
        # The URL was formatted incorrectly.
        return validation_details
    validation_details['is_structure_valid'] = True
    resource_type, namespace, localID = itemgetter('resource_type', 'namespace', 'localID')(divide_resource_url_into_main_components(resource_url))
    resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type)

    referenced_resource = get_resource_by_pithia_identifier_components(resource_mongodb_model, localID, namespace)
    if referenced_resource == None:
        validation_details['type_of_missing_resource'] = resource_type
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
        'urls_with_unregistered_op_modes': [],
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
            
        resource_type, namespace, localID = itemgetter('resource_type', 'namespace', 'localID')(divide_resource_url_into_main_components(resource_url))
        resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type)
        resource_with_op_mode_id = get_resource_by_pithia_identifier_components_and_op_mode_id(resource_mongodb_model, localID, namespace, op_mode_id)
        if resource_with_op_mode_id == None:
            invalid_urls['urls_with_unregistered_op_modes'].append(resource_url_with_op_mode_id)
            
    return invalid_urls