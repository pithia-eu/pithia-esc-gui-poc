import os

import xmlschema
current_schema_version = '2.2'

def get_xml_schema_by_type(type):
    current_dir = os.path.dirname(__file__)
    schemas_path = os.path.join(current_dir, 'schemas', current_schema_version)
    if type == 'organisation':
        return open(os.path.join(schemas_path, 'utilities.xsd')) 

def validate_xml_files_by_type(files, type):
    valid_xmls = []
    invalid_xmls = []
    schema_file = get_xml_schema_by_type(type)
    print('test')
    schema = xmlschema.XMLSchema(schema_file)
    print('schema', schema)
    for xsd_component in schema.iter_components():
        print(xsd_component)
    for f in files:
        try:
            if not schema.is_valid(f):
                invalid_xmls.append(f)
            else:
                valid_xmls.append(f)
        except BaseException as err:
            print(err)
    return valid_xmls, invalid_xmls
