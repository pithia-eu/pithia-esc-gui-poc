import os
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
    logger.info('Registering handle ', handle)
    register_result = client.register_handle(handle, handle_value)

    if register_result == handle:
        logger.info('OK: Register handle successful.')
    else:
        logger.info('PROBLEM: Register handle returned unexpected response.')

def delete_handle(handle: str, client: RESTHandleClient):
    delete_result = client.delete_handle(handle)
    logger.info('OK: Delete handle successful.')

def get_handle_url(handle: str, client: RESTHandleClient) -> str:
    key = 'URL'
    read_value = client.get_value_from_handle(handle, key)

    return read_value

def get_handle_record(handle: str, client: RESTHandleClient):
    handle_record= client.retrieve_handle_record(handle)

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
        logger.info('Expected: ', new_handle_value)
        logger.info('Returned: ', get_value_result)