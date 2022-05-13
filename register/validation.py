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
    elif type == 'process':
        return os.path.join(schemas_path, 'procedure.xsd')
    return 'unknown';

def validate_xml_file_by_type(xml_file, type):
    file_path_of_schema_for_type = get_xml_schema_file_path_by_type(type)
    with open(file_path_of_schema_for_type, 'rb') as schema_file:
        schema_file_parsed = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_file_parsed)
        xml_file_parsed = etree.parse(xml_file)
        return schema.validate(xml_file_parsed)