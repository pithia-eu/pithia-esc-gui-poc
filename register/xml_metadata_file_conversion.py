import json
import xmltodict
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import Union

def convert_xml_metadata_file_to_dictionary(xml_file_or_string: Union[InMemoryUploadedFile, str]) -> dict:
    xml = xml_file_or_string
    if hasattr(xml_file_or_string, 'read'):
        xml_file_or_string.seek(0)
        xml = xml_file_or_string.read()
    xml_as_dict = xmltodict.parse(xml)
    xml_as_json = json.dumps(xml_as_dict)
    # Some formatting to get rid of '\n' characters and extra
    # whitespace within strings
    xml_as_json = xml_as_json.replace('\\n', '')
    xml_as_json = ' '.join(xml_as_json.split())
    # pymongo takes dictionaries when inserting new documents,
    # so convert the JSON back to a dictionary
    return json.loads(xml_as_json)