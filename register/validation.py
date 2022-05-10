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
    with open(schema_file_path, "r") as schema_file:
        schema_file_text = schema_file.read()
        schema_root = etree.XML()
        schema = etree.XMLSchema(schema_root)
        for f in files:
            xml = f.read()
            doc = etree.parse(xml)
            try:
                schema.validate(doc)
                print(f'{f.name} is valid')
                valid_xmls.append(f)
            except BaseException as err:
                print(err)
                print(f'{f.name} is not valid')
                invalid_xmls.append(f)
    return valid_xmls, invalid_xmls
