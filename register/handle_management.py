import os
import json
from lxml import etree
from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.handleclient import PyHandleClient, RESTHandleClient
from pyhandle.handleexceptions import *

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

def update_handle_url(handle: str, new_handle_value: str, client: RESTHandleClient):
    key = 'URL'
    client.modify_handle_value(handle, **{ key: new_handle_value })
    get_value_result = client.get_value_from_handle(handle, key)

    if get_value_result == new_handle_value:
        logger.info('OK: Update handle URL successful.')
    else:
        logger.critical('CRITICAL: Modify handle URL returned unexpected value.')
        logger.info(f'Expected: {new_handle_value}')
        logger.info(f'Returned: {get_value_result}')

def add_doi_to_xml_file(xml_file, doi):
    # Use lxml to append a new filled in doi element
    # The passed in xml_file should be open in 'wb' mode,
    # so it can be written to.
    parser = etree.XMLParser(remove_blank_text=True)
    xml_file_parsed = etree.parse(xml_file, parser)
    root = xml_file_parsed.getroot()
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
    with open(xml_file.name, 'wb') as xml_file:
        xml_file_parsed.write(xml_file.name, pretty_print=True)
    return xml_file