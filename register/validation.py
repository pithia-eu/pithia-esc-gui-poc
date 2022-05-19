import os
from mongodb import db
from lxml import etree

# TODO: change current_schema_version to 2.2
# when schemas are finalised.
current_schema_version = '2.1'

def get_xml_schema_file_path_by_type(type):
    current_dir = os.path.dirname(__file__)
    schemas_path = os.path.join(current_dir, 'schemas', current_schema_version)
    if type == 'organisation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'individual':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'project':
        return os.path.join(schemas_path, 'project.xsd')
    elif type == 'platform':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'operation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'instrument':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'acquisition':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'computation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'process':
        return os.path.join(schemas_path, 'process.xsd')
    elif type == 'data-collection':
        return os.path.join(schemas_path, 'observationCollection.xsd')
    return 'unknown'

def get_collection_name_from_component(component):
    if type == 'organisation':
        return 'organisations'
    elif type == 'individual':
        return 'individuals'
    elif type == 'project':
        return 'projects'
    elif type == 'platform':
        return 'platforms'
    elif type == 'operation':
        return 'operations'
    elif type == 'instrument':
        return 'instruments'
    elif type == 'acquisition':
        return 'acquisitions'
    elif type == 'computation':
        return 'computations'
    elif type == 'process':
        return 'processes'
    elif type == 'data-collection':
        return 'data-collections'
    return 'unknown'

def parse_xml_file(xml_file):
    # Returns an ElementTree
    return etree.parse(xml_file)

def validate_xml_against_schema(xml_file_parsed, schema_file_path):
    with open(schema_file_path, 'rb') as schema_file:
        schema_file_parsed = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_file_parsed)
        schema.assertValid(xml_file_parsed)
        return 'valid'

def get_ontology_term_from_xlink_href_and_type(href, type):
    ESPAS_ONTOLOGY_URL = 'http://ontology.espas-fp7.eu/' # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
    return

def get_entities_from_xlink_href_and_type(href):
    ESPAS_RESOURCES_URL = 'http://resources.espas-fp7.eu/' # e.g. # https://resources.pithia.eu/2.2/pithia/organisation/uml/UML/1
    PITHIA_RESOURCES_URL = 'https://resources.pithia.eu/2.2/pithia/'
    href = href.replace(ESPAS_RESOURCES_URL, '')
    href_components = href.split('/')
    component_referenced = href_components[0]
    collection_for_component = get_collection_name_from_component(component_referenced)
    namespace = href_components[1]
    localID = href_components[2]
    if len(href_components) > 3:
        version = href_components[3]
    find_dictionary = {
        'identifier.ESPAS_Identifier.localID': localID,
        'identifier.ESPAS_Identifier.namespace': namespace,
    }
    if version:
        find_dictionary['identifier.ESPAS_Identifier.version'] = version
    return db[collection_for_component].find_one(find_dictionary)



def validate_xml_xlinks_by_type(xml_file_parsed, type):
    missing_xlinks = []
    parent = xml_file_parsed.getroot()
    xlinks = parent.xpath("//@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']")
    if (len(xlinks) > 0):
        for xlink in xlinks:
            xlink_reference = get_entities_from_xlink_href_and_type(xlink)
            if not xlink_reference:
                missing_xlinks.append(xlink)
    
    return missing_xlinks