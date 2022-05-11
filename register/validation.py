import os
import xmlschema
from lxml import etree

current_schema_version = '2.2'

def get_xml_schema_file_path_by_type(type):
    current_dir = os.path.dirname(__file__)
    schemas_path = os.path.join(current_dir, 'schemas', current_schema_version)
    if type == 'organisation':
        return os.path.join(schemas_path, 'utilities.xsd')
    elif type == 'process':
        return os.path.join(schemas_path, 'procedure.xsd')
    return 'unknown';

def validate_xml_files_by_type(files, type):
    valid_xmls = []
    invalid_xmls = []
    schema_file_path = get_xml_schema_file_path_by_type(type)
    with open(schema_file_path, 'rb') as schema_file:
        schema_root = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_root)
        for f in files:
            with open(f, 'rb') as metadata_file:
                metadata_file_parsed = etree.parse(metadata_file)
                is_metadata_file_valid = schema.validate(metadata_file_parsed)
                if not is_metadata_file_valid:
                    print(f'{metadata_file.name} is not valid', is_metadata_file_valid)
                    invalid_xmls.append(metadata_file)
                else:
                    print(f'{metadata_file.name} is valid', is_metadata_file_valid)
                    valid_xmls.append(metadata_file)
    return valid_xmls, invalid_xmls
 