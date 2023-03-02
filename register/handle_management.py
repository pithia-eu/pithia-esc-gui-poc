import json
import os
import requests
from bson import ObjectId
from common.mongodb_models import OriginalMetadataXml
from dateutil import parser
from django.urls import reverse_lazy
from lxml import etree
from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.handleclient import PyHandleClient, RESTHandleClient
from pyhandle.handleexceptions import *
from update.update import update_current_version_of_resource
import urllib.parse

import logging

logger = logging.getLogger(__name__)

def instantiate_client_and_load_credentials() -> tuple[RESTHandleClient, PIDClientCredentials]:
    handle_api_url = os.environ['HANDLE_API_ENDPOINT_URL']
    credentials = None
    with open('credentials.json', 'w+') as credentials_json_file:
        credentials_data = {
            'client': os.environ['HANDLE_API_CLIENT'],
            'handle_server_url': handle_api_url,
            'baseuri': handle_api_url,
            'username': os.environ['HANDLE_API_USERNAME'],
            'password': os.environ['HANDLE_API_KEY'],
            'prefix': os.environ['HANDLE_PREFIX'],
        }
        json.dump(credentials_data, credentials_json_file, indent=4)
    credentials = PIDClientCredentials.load_from_JSON('credentials.json')
    client = PyHandleClient('rest').instantiate_with_credentials(credentials)
    return client, credentials

def create_handle(credentials: PIDClientCredentials, handle_suffix: str) -> str:
    return f'{credentials.get_prefix()}/{handle_suffix}'

def register_handle(handle: str, handle_value: str, client: RESTHandleClient):
    logger.info(f'Registering handle {handle}')
    register_result = client.register_handle(handle, handle_value)

    if register_result == handle:
        logger.info('OK: Register handle successful.')
    else:
        logger.info('PROBLEM: Register handle returned unexpected response.')

    return register_result

def create_and_register_handle_for_resource(resource_id: str) -> tuple[str, RESTHandleClient, PIDClientCredentials]:
    client, credentials = instantiate_client_and_load_credentials()
    handle = create_handle(credentials, resource_id)
    resource_details_page_url = reverse_lazy('browse:catalogue_data_subset_detail', kwargs={ 'catalogue_data_subset_id': resource_id })
    resource_details_page_url_string = f'{os.environ["HANDLE_URL_PREFIX"]}{str(resource_details_page_url)}'
    register_handle(handle, resource_details_page_url_string, client)
    return handle, client, credentials

def delete_handle(handle: str, client: RESTHandleClient):
    delete_result = client.delete_handle(handle)
    logger.info('OK: Delete handle successful.')
    return delete_result

def get_handle_url(handle: str, client: RESTHandleClient) -> str:
    key = 'URL'
    read_value = client.get_value_from_handle(handle, key)

    return read_value

def get_handle_record(handle: str, client: RESTHandleClient) -> dict:
    handle_record = client.retrieve_handle_record(handle)

    if handle_record != None:
        logger.info('OK: Handle exists.')
    else:
        logger.error('PROBLEM: Retrieving handle record returned unexpected response.')

    return handle_record

def get_handle_raw(handle: str) -> dict:
    handle_api_endpoint = os.environ['HANDLE_API_ENDPOINT_URL']
    response = requests.get(f'{handle_api_endpoint}/api/handles/{handle}')
    handle_raw = response.json()
    return handle_raw

def get_time_handle_was_issued_as_string(handle: str) -> str:
    handle_raw = get_handle_raw(handle)
    date_issued = handle_raw['values'][0]['timestamp']
    return date_issued

def get_date_handle_was_issued_as_string(handle: str) -> str:
    handle_issue_time_string = get_time_handle_was_issued_as_string(handle)
    print('handle_issue_time_string', handle_issue_time_string)
    handle_issue_date = parser.isoparse(handle_issue_time_string).strftime('%Y-%m-%d')
    return handle_issue_date

def update_handle_url(handle: str, new_handle_value: str, client: RESTHandleClient):
    key = 'URL'
    modify_result = client.modify_handle_value(handle, **{ key: new_handle_value })
    get_value_result = client.get_value_from_handle(handle, key)

    if get_value_result == new_handle_value:
        logger.info('OK: Update handle URL successful.')
    else:
        logger.critical('CRITICAL: Modify handle URL returned unexpected value.')
        logger.info(f'Expected: {new_handle_value}')
        logger.info(f'Returned: {get_value_result}')
    
    return modify_result

def get_handles_with_prefix(prefix):
    handle_api_endpoint = os.environ['HANDLE_API_ENDPOINT_URL']
    response = requests.get(
        f'{handle_api_endpoint}/api/handles?prefix={prefix}',
        auth=(urllib.parse.quote_plus(os.environ['HANDLE_API_USERNAME']), os.environ['HANDLE_API_KEY'])
    )
    handles_with_prefix = response.json()
    return handles_with_prefix

def add_handle_to_metadata_and_return_updated_xml_string(
    handle,
    client,
    resource_id,
    xml_file,
    resource_mongodb_model,
    resource_conversion_validate_and_correct_function=None,
    session=None
):
    handle_url = get_handle_url(handle, client)
    doi_dict = map_handle_to_doi_dict(handle, handle_url)
    doi_xml_string = create_doi_xml_string_from_dict(doi_dict)
    xml_file.seek(0)
    metadata_xml_string = xml_file.read()
    xml_string_with_doi = add_doi_xml_string_to_metadata_xml_string(metadata_xml_string, doi_xml_string)
    update_current_version_of_resource(
        resource_id,
        xml_string_with_doi,
        resource_mongodb_model,
        resource_conversion_validate_and_correct_function,
        session=session
    )
    return xml_string_with_doi

def create_lxml_utf8_parser():
    return etree.XMLParser(remove_blank_text=True, encoding='utf-8')

def map_handle_to_doi_dict(handle: str, handle_url: str):
    handle_issue_date_as_string = get_date_handle_was_issued_as_string(handle)

    doi = {
        'referentDoiName': handle,
        'primaryReferentType': 'Creation',
        'registrationAgencyDoiName': os.environ['HANDLE_API_USERNAME'],
        'issueDate': handle_issue_date_as_string,
        'issueNumber': '0', # issue number is not known
        'referentCreation': {
            'name': {
                '@primaryLanguage': 'en',
                'value': handle_url,
                'type': 'URL',
            },
            'identifier': {
                'nonUriValue': handle,
                'uri': {
                    '@returnType': 'text/html',
                    '#text': f'{os.environ["HANDLE_API_ENDPOINT_URL"]}/api/handles/{handle}',
                },
                'type': 'epicId',
            },
            'structuralType': 'Digital',
            'mode': 'Visual',
            'character': 'Image',
            'type': 'Dataset',
            'principalAgent': {
                'name': {
                    'value': 'Lowell GIRO Data Center',
                    'type': 'Name',
                },
            },
        },
    }
    return doi

def create_doi_xml_string_from_dict(doi_dict: dict) -> str:
    doi_xml_string = '''
    <doi xmlns:doi="http://www.doi.org/2010/DOISchema">
        <doi:kernelMetadata>
            <doi:referentDoiName>{referentDoiName}</doi:referentDoiName>
            <doi:primaryReferentType>{primaryReferentType}</doi:primaryReferentType>
            <doi:registrationAgencyDoiName>{registrationAgencyDoiName}</doi:registrationAgencyDoiName>
            <doi:issueDate>{issueDate}</doi:issueDate>
            <doi:issueNumber>{issueNumber}</doi:issueNumber>
            <doi:referentCreation>
                <doi:name primaryLanguage="{primaryLanguage}">
                    <doi:value>{nameValue}</doi:value>
                    <doi:type>{nameType}</doi:type>
                </doi:name>
                <doi:identifier>
                    <doi:nonUriValue>{identifierNonUriValue}</doi:nonUriValue>
                    <doi:uri returnType="{identifierUriReturnType}">{identifierUriText}</doi:uri>
                    <doi:type>{identifierType}</doi:type>
                </doi:identifier>
                <doi:structuralType>{structuralType}</doi:structuralType>
                <doi:mode>{mode}</doi:mode>
                <doi:character>{character}</doi:character>
                <doi:type>{type}</doi:type>
                <doi:principalAgent>
                    <doi:name>
                        <doi:value>{principalAgentNameValue}</doi:value> <!-- Proper name of organisation?? -->
                        <doi:type>{principalAgentNameType}</doi:type>
                    </doi:name>
                </doi:principalAgent>
            </doi:referentCreation>
        </doi:kernelMetadata>
    </doi>
    '''.format(
        referentDoiName=doi_dict['referentDoiName'],
        primaryReferentType=doi_dict['primaryReferentType'],
        registrationAgencyDoiName=doi_dict['registrationAgencyDoiName'],
        issueDate=doi_dict['issueDate'],
        issueNumber=doi_dict['issueNumber'],
        primaryLanguage=doi_dict['referentCreation']['name']['@primaryLanguage'],
        nameValue=doi_dict['referentCreation']['name']['value'],
        nameType=doi_dict['referentCreation']['name']['type'],
        identifierNonUriValue=doi_dict['referentCreation']['identifier']['nonUriValue'],
        identifierUriReturnType=doi_dict['referentCreation']['identifier']['uri']['@returnType'],
        identifierUriText=doi_dict['referentCreation']['identifier']['uri']['#text'],
        identifierType=doi_dict['referentCreation']['identifier']['type'],
        structuralType=doi_dict['referentCreation']['structuralType'],
        mode=doi_dict['referentCreation']['mode'],
        character=doi_dict['referentCreation']['character'],
        type=doi_dict['referentCreation']['type'],
        principalAgentNameValue=doi_dict['referentCreation']['principalAgent']['name']['value'],
        principalAgentNameType=doi_dict['referentCreation']['principalAgent']['name']['type']
    )
    doi_xml_string = (' '.join(doi_xml_string.split())).replace('> <', '><')
    return doi_xml_string

def add_doi_xml_string_to_metadata_xml_string(metadata_xml_string: str, doi_xml_string: str) -> str:
    if isinstance(metadata_xml_string, str):
        metadata_xml_string = metadata_xml_string.encode('utf-8')
    # Use lxml to append a new filled in doi element
    parser = create_lxml_utf8_parser()
    root = etree.fromstring(metadata_xml_string, parser)
    doi_xml_string_parsed = etree.fromstring(doi_xml_string)
    root.append(doi_xml_string_parsed)
    etree.indent(root, space='    ')
    updated_xml_string = etree.tostring(root, pretty_print=True)
    updated_xml_string = updated_xml_string.decode('utf-8')
    return updated_xml_string

def remove_doi_element_from_metadata_xml_string(xml_string):
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    parser = create_lxml_utf8_parser()
    root = etree.fromstring(xml_string, parser)
    for doi in root.findall('.//{https://metadata.pithia.eu/schemas/2.2}doi'):
        doi.getparent().remove(doi)
    updated_xml_string = etree.tostring(root, pretty_print=True)
    updated_xml_string = updated_xml_string.decode('utf-8')
    return updated_xml_string

def get_doi_xml_string_from_metadata_xml_string(xml_string):
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    parser = create_lxml_utf8_parser()
    root = etree.fromstring(xml_string, parser)
    doi_element = root.find('.//{https://metadata.pithia.eu/schemas/2.2}doi')
    if doi_element is None:
        return None
    doi_element_string = etree.tostring(doi_element, pretty_print=True)
    doi_element_string = doi_element_string.decode('utf-8')
    return doi_element_string

def get_doi_xml_string_for_resource_id(resource_id):
    original_metadata_xml = OriginalMetadataXml.find_one({
        'resourceId': ObjectId(resource_id),
    }, { 'value': 1 })
    xml_string = original_metadata_xml['value']
    return get_doi_xml_string_from_metadata_xml_string(xml_string)