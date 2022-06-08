import os
from requests import get
from mongodb import db
from lxml import etree

from register.resource_metadata_upload import current_resource_version_collection_names

# TODO: change current_schema_version to 2.2
# when schemas are finalised.
current_schema_version = '2.1'

def get_xml_schema_file_path_for_resource_type(resource_type):
    current_dir = os.path.dirname(__file__)
    schemas_path = os.path.join(current_dir, 'schemas', current_schema_version)
    if resource_type == 'organisation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'individual':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'project':
        return os.path.join(schemas_path, 'project.xsd')
    elif resource_type == 'platform':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'operation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'instrument':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'acquisition':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'computation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif resource_type == 'process':
        return os.path.join(schemas_path, 'process.xsd')
    elif resource_type == 'data-collection':
        return os.path.join(schemas_path, 'observationCollection.xsd')
    return 'unknown'

def parse_xml_file(xml_file):
    # Returns an ElementTree
    return etree.parse(xml_file)

def validate_xml_matches_submitted_resource_type(xml_file_parsed, resource_type):
    root = xml_file_parsed.getroot()
    root_localname = etree.QName(root).localname # Get the root tag text without the namespace
    if resource_type == 'organisation':
        expected_root_localname = 'ESPAS_Organisation'
    elif resource_type == 'individual':
        expected_root_localname = 'ESPAS_Individual'
    elif resource_type == 'project':
        expected_root_localname = 'ESPAS_Project'
    elif resource_type == 'platform':
        expected_root_localname = 'ESPAS_Platform'
    elif resource_type == 'operation':
        expected_root_localname = 'ESPAS_Procedure'
    elif resource_type == 'instrument':
        expected_root_localname = 'ESPAS_Instrument'
    elif resource_type == 'acquisition':
        expected_root_localname = 'ESPAS_Acquisition'
    elif resource_type == 'computation':
        expected_root_localname = 'ESPAS_Computation'
    elif resource_type == 'process':
        expected_root_localname = 'ESPAS_Procedure'
    elif resource_type == 'data-collection':
        expected_root_localname = 'ESPAS_ObservationCollection'
    return {
        'root_tag': f'{root_localname}',
        'expected_root_tag': f'{expected_root_localname}',
        'is_root_tag_valid': root_localname == expected_root_localname
    }

def validate_xml_against_schema(xml_file_parsed, schema_file_path):
    with open(schema_file_path, 'rb') as schema_file:
        schema_file_parsed = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_file_parsed)
        schema.assertValid(xml_file_parsed)
        return 'valid'

def validate_ontology_component_with_term(component, term_id):
    ESPAS_ONTOLOGY_URL = 'http://ontology.espas-fp7.eu/' # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
    print(f'{ESPAS_ONTOLOGY_URL}{component}/{term_id}')
    ontology_term_response = get(f'{ESPAS_ONTOLOGY_URL}{component}/{term_id}')
    return ontology_term_response.status_code == 200

def get_resource_from_xlink_href_components(resource_type, localID, namespace, version):
    find_dictionary = {
        'identifier.ESPAS_Identifier.localID': localID,
        'identifier.ESPAS_Identifier.namespace': namespace,
    }
    if version:
        find_dictionary['identifier.ESPAS_Identifier.version'] = version
    current_resource_version_collection_name = current_resource_version_collection_names.get(resource_type, None)
    if not current_resource_version_collection_name:
        return None
    return db[current_resource_version_collection_name].find_one(find_dictionary)

def get_components_from_xlink_href(href, href_section_to_remove):
    href = href.replace(href_section_to_remove, '')
    return href.split('/')

def get_unregistered_referenced_resources_and_ontology_terms_from_xml(xml_file_parsed):
    unregistered_resources_and_ontology_terms = {
        'unregistered_referenced_resource_hrefs': set(),
        'unregistered_referenced_resource_types': set(),
        'unregistered_referenced_ontology_term_hrefs': set(),
    }
    parent = xml_file_parsed.getroot()
    hrefs = parent.xpath("//@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']")
    if not len(hrefs) > 0:
        for key in unregistered_resources_and_ontology_terms:
            unregistered_resources_and_ontology_terms[key] = list(unregistered_resources_and_ontology_terms[key])
        return unregistered_resources_and_ontology_terms
    for href in hrefs:
        if 'ontology' in href:
            href_components  = get_components_from_xlink_href(href, 'http://ontology.espas-fp7.eu/')
            ontology_component = href_components[0]
            ontology_term_id = href_components[1]
            is_valid_ontology_term = validate_ontology_component_with_term(ontology_component, ontology_term_id)
            if not is_valid_ontology_term:
                unregistered_resources_and_ontology_terms['unregistered_referenced_ontology_term_hrefs'].add(href)

        if 'resources' in href:
            href_components  = get_components_from_xlink_href(href, 'http://resources.espas-fp7.eu/')
            resource_type = href_components[0]
            namespace = href_components[1]
            localID = href_components[2]
            version = None
            if len(href_components) > 3:
                version = href_components[3]
            referenced_resource = get_resource_from_xlink_href_components(resource_type, localID, namespace, version)
            if not referenced_resource:
                unregistered_resources_and_ontology_terms['unregistered_referenced_resource_hrefs'].add(href)
                unregistered_resources_and_ontology_terms['unregistered_referenced_resource_types'].add(resource_type)
    
    for key in unregistered_resources_and_ontology_terms:
        unregistered_resources_and_ontology_terms[key] = list(unregistered_resources_and_ontology_terms[key])
    return unregistered_resources_and_ontology_terms