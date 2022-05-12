import os
import xmlschema
from lxml import etree

current_schema_version = '2.2'

def get_xml_schema_file_path_by_type(type):
    current_dir = os.path.dirname(__file__)
    test_schemas_path = os.path.join(current_dir, 'schemas', 'testing', 'testschema.xsd')
    return test_schemas_path
    schemas_path = os.path.join(current_dir, 'schemas', current_schema_version)
    if type == 'organisation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'process':
        return os.path.join(schemas_path, 'procedure.xsd')
    return 'unknown';

def validate_xml_files_by_type(xml_files, type):
    valid_xmls = []
    invalid_xmls = []
    schema_file_path = get_xml_schema_file_path_by_type(type)
    with open(schema_file_path, 'rb') as schema_file:
        schema_doc = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_doc)
        for xml_file in xml_files:
            xml_file_parsed = etree.parse(xml_file)
            print(etree.tostring(xml_file_parsed))
            print(schema)
            is_xml_file_valid = schema.validate(xml_file_parsed)
            if not is_xml_file_valid:
                print(f'{xml_file.name} is not valid', is_xml_file_valid)
                log = schema.error_log
                error = log.last_error
                print(error)
                invalid_xmls.append(xml_file)
            else:
                print(f'{xml_file.name} is valid', is_xml_file_valid)
                valid_xmls.append(xml_file)
    return valid_xmls, invalid_xmls