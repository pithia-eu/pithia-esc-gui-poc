import validators
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
    resource_url_components = divide_resource_url_into_main_components(resource_url)

    is_start_of_localid_equal_to_resource_type = resource_url_components['localID'].startswith(resource_url_components['resource_type'].capitalize())
    # Exceptions to localID starting with resource_type.capitalize():
    if resource_url_components['resource_type'] == 'collection':
        is_start_of_localid_equal_to_resource_type = resource_url_components['localID'].startswith('DataCollection')
    elif resource_url_components['resource_type'] == 'acquisitionCapabilities':
        is_start_of_localid_equal_to_resource_type = resource_url_components['localID'].startswith('AcquisitionCapabilities')
    elif resource_url_components['resource_type'] == 'computationCapabilities':
        is_start_of_localid_equal_to_resource_type = resource_url_components['localID'].startswith('ComputationCapabilities')
    elif resource_url_components['resource_type'] == 'process':
        is_start_of_localid_equal_to_resource_type = resource_url_components['localID'].startswith('CompositeProcess')

    return all([
        get_mongodb_model_by_resource_type_from_resource_url(resource_url_components['resource_type']) != 'unknown',
        resource_url.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE),
        resource_url.count(PITHIA_METADATA_SERVER_HTTPS_URL_BASE) == 1,
        resource_url.count(f'/{resource_url_components["resource_type"]}/') == 1,
        resource_url.count(f'/{resource_url_components["namespace"]}/') == 1,
        resource_url.count(f'/{resource_url_components["localID"]}') == 1,
        resource_url.endswith(resource_url_components["localID"]),
        is_start_of_localid_equal_to_resource_type,
    ])

def validate_resource_url(resource_url):
    if not is_resource_url_structure_valid(resource_url):
        # The URL was formatted incorrectly.
        return {
            'is_valid': False,
            'error_msg': 'The URL was formatted incorrectly.',
        }
    url_components = divide_resource_url_into_main_components(resource_url)
    resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(url_components['resource_type'])

    referenced_resource = get_resource_by_pithia_identifier_components(resource_mongodb_model, url_components['localID'], url_components['namespace'])
    if referenced_resource == None:
        return {
            'is_valid': False,
            'error_msg': 'The resource this URL refers to was not found.',
            'resource_type': url_components['resource_type'],
        }

    return {
        'is_valid': True
    }

def get_invalid_resource_urls_from_parsed_xml(xml_file_parsed):
    invalid_urls = []
    root = xml_file_parsed.getroot()
    resource_urls = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and not(contains(@xlink:href, '#'))]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for resource_url in resource_urls:
        resource_url_validation_result = validate_resource_url(resource_url)
        if resource_url_validation_result['is_valid'] == False:
            invalid_urls.append((resource_url, resource_url_validation_result['error_msg'], resource_url_validation_result['resource_type']))
    return invalid_urls

def get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml(xml_file_parsed):
    invalid_urls = []
    root = xml_file_parsed.getroot()
    resource_urls = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and contains(@xlink:href, '#')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for resource_url in resource_urls:
        resource_url_and_op_mode_id = divide_resource_url_from_op_mode_id
        resource_url = resource_url_and_op_mode_id[:-1]
        op_mode_id = resource_url_and_op_mode_id[-1]
        resource_url_validation_result = validate_resource_url(resource_url)
        if resource_url_validation_result['is_valid'] == False:
            invalid_urls.append((resource_url, resource_url_validation_result['error_msg'], resource_url_validation_result['resource_type']))
            
        url_components = divide_resource_url_into_main_components(resource_url)
        resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(url_components['resource_type'])
        resource_with_op_mode_id = get_resource_by_pithia_identifier_components_and_op_mode_id(resource_mongodb_model, url_components['localID'], url_components['namespace'], op_mode_id)
        if resource_with_op_mode_id == None:
            hashtag_index = resource_url.index('#')
            invalid_url = resource_url[:hashtag_index] + '<b>' + resource_url[hashtag_index:] + '</b>'
            invalid_urls.append((invalid_url, 'The operational mode this URL is referencing was not found.'))
    return invalid_urls