import json
import os
import requests
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
    resource_details_page_url_string = str(resource_details_page_url)
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
    doi = map_handle_to_doi(handle, handle_url)
    print(type(xml_file))
    xml_file.seek(0)
    xml_string = xml_file.read()
    xml_string_with_doi = add_doi_to_xml_string(xml_string, doi)
    update_current_version_of_resource(
        resource_id,
        xml_string_with_doi,
        resource_mongodb_model,
        resource_conversion_validate_and_correct_function,
        session=session
    )
    return xml_string_with_doi

def map_handle_to_doi(handle: str, handle_url: str):
    handle_issue_date_as_string = get_date_handle_was_issued_as_string(handle)

    doi = {
        'registrationAgencyDoiName': os.environ['HANDLE_API_USERNAME'],
        'issueDate': handle_issue_date_as_string,
        'issueNumber': '0', # issue number is not known
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
        }
    }
    return doi

def add_doi_to_xml_string(xml_string: str, doi: dict) -> str:
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    # Use lxml to append a new filled in doi element
    parser = etree.XMLParser(remove_blank_text=True, encoding='utf-8')
    root = etree.fromstring(xml_string, parser)
    doi_element_content = '''
    <doi xmlns:doi="http://www.doi.org/2010/DOISchema">
        <doi:kernelMetadata>
            <doi:registrationAgencyDoiName>%s</doi:registrationAgencyDoiName>
            <doi:issueDate>%s</doi:issueDate>
            <doi:issueNumber>%s</doi:issueNumber>
            <doi:referentCreation>
                <doi:name primaryLanguage="%s">
                    <value>%s</value>
                    <type>%s</type>
                </doi:name>
                <doi:identifier>
                    <doi:nonUriValue>%s</doi:nonUriValue>
                    <doi:uri returnType="%s">%s</doi:uri>
                    <doi:type>%s</doi:type>
                </doi:identifier>
            </doi:referentCreation>
        </doi:kernelMetadata>
    </doi>
    ''' % (
        doi['registrationAgencyDoiName'],
        doi['issueDate'],
        doi['issueNumber'],
        doi['name']['@primaryLanguage'],
        doi['name']['value'],
        doi['name']['type'],
        doi['identifier']['nonUriValue'],
        doi['identifier']['uri']['@returnType'],
        doi['identifier']['uri']['#text'],
        doi['identifier']['type']
    )
    doi_element_content = (' '.join(doi_element_content.split())).replace('> <', '><')
    doi_element = etree.fromstring(doi_element_content)
    root.append(doi_element)
    etree.indent(root, space='    ')
    updated_xml_string = etree.tostring(root, pretty_print=True)
    updated_xml_string = updated_xml_string.decode('utf-8')
    return updated_xml_string