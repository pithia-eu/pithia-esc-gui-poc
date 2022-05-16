import os
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
    elif type == 'instrument':
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
    return 'unknown';

def parse_xml_file(xml_file):
    # Returns an ElementTree
    return etree.parse(xml_file)

def validate_xml_against_schema(xml_file_parsed, schema_file_path):
    with open(schema_file_path, 'rb') as schema_file:
        schema_file_parsed = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_file_parsed)
        return schema.validate(xml_file_parsed)

def validate_xml_xlinks_by_type(xml_file_parsed, type):
    missing_xlinks = []
    XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
    XLINK = '{%s}' % XLINK_NAMESPACE
    
    return missing_xlinks