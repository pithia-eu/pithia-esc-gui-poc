import os
from mongodb import db
from lxml import etree

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

def get_mongodb_collection_name_for_resource_type(resource_type):
    if resource_type == 'organisation':
        return 'organisations'
    elif resource_type == 'individual':
        return 'individuals'
    elif resource_type == 'project':
        return 'projects'
    elif resource_type == 'platform':
        return 'platforms'
    elif resource_type == 'operation':
        return 'operations'
    elif resource_type == 'instrument':
        return 'instruments'
    elif resource_type == 'acquisition':
        return 'acquisitions'
    elif resource_type == 'computation':
        return 'computations'
    elif resource_type == 'process':
        return 'processes'
    elif resource_type == 'data-collection':
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

def get_ontology_term_from_xlink_href(href):
    ESPAS_ONTOLOGY_URL = 'http://ontology.espas-fp7.eu/' # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
    return

def get_resource_from_xlink_href_components(resource_type, localID, namespace, version):
    find_dictionary = {
        'identifier.ESPAS_Identifier.localID': localID,
        'identifier.ESPAS_Identifier.namespace': namespace,
    }
    if version:
        find_dictionary['identifier.ESPAS_Identifier.version'] = version
    collection_name_for_resource_type = get_mongodb_collection_name_for_resource_type(resource_type)
    return db[collection_name_for_resource_type].find_one(find_dictionary)

def get_components_from_xlink_href(href):
    ESPAS_RESOURCES_URL = 'http://resources.espas-fp7.eu/' # e.g. # https://resources.pithia.eu/2.2/pithia/organisation/uml/UML/1
    PITHIA_RESOURCES_URL = 'https://resources.pithia.eu/2.2/pithia/'
    href = href.replace(ESPAS_RESOURCES_URL, '')
    href_components = href.split('/')
    resource_type = href_components[0]
    namespace = href_components[1]
    localID = href_components[2]
    if len(href_components) > 3:
        version = href_components[3]
    return resource_type, localID, namespace, version



def get_unregistered_referenced_resources_from_xml(xml_file_parsed):
    unregistered_referenced_resource_hrefs = []
    unregistered_referenced_resource_types = set()
    parent = xml_file_parsed.getroot()
    hrefs = parent.xpath("//@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']")
    if (len(hrefs) > 0):
        for href in hrefs:
            resource_type, localID, namespace, version  = get_components_from_xlink_href(href)
            referenced_resource = get_resource_from_xlink_href_components(resource_type, localID, namespace, version)
            if not referenced_resource:
                unregistered_referenced_resource_hrefs.append(href)
                unregistered_referenced_resource_types.add(resource_type)
    
    return unregistered_referenced_resource_hrefs, list(unregistered_referenced_resource_types)