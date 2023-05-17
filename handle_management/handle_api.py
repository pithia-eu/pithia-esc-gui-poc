import json
import logging
import os
import requests
import urllib.parse
from dateutil import parser
from django.urls import reverse_lazy
from pyhandle.clientcredentials import PIDClientCredentials
from pyhandle.handleclient import PyHandleClient, RESTHandleClient
from utils.dict_helpers import flatten

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

def generate_and_register_handle(handle_value: str, credentials: PIDClientCredentials, client: RESTHandleClient, initial_doi_dict_values: dict = {}) -> str:
    flat_initial_doi_dict_values = flatten(initial_doi_dict_values, number_list_items=False)
    new_handle_name = client.generate_and_register_handle(credentials.get_prefix(), handle_value, **flat_initial_doi_dict_values)
    
    return new_handle_name

def register_handle(handle: str, handle_value: str, client: RESTHandleClient, initial_doi_dict_values: dict = {}):
    logger.info(f'Registering handle {handle}')
    flat_initial_doi_dict_values = flatten(initial_doi_dict_values, number_list_items=False)
    register_result = client.register_handle(handle, handle_value, **flat_initial_doi_dict_values)

    if register_result == handle:
        logger.info('OK: Register handle successful.')
    else:
        logger.info('PROBLEM: Register handle returned unexpected response.')

    return register_result

def create_and_register_handle_for_resource(resource_id: str, initial_doi_dict_values: dict = {}) -> tuple[str, RESTHandleClient, PIDClientCredentials]:
    client, credentials = instantiate_client_and_load_credentials()
    resource_details_page_url = reverse_lazy('browse:catalogue_data_subset_detail', kwargs={ 'catalogue_data_subset_id': resource_id })
    resource_details_page_url_string = f'{os.environ["HANDLE_URL_PREFIX"]}{str(resource_details_page_url)}'
    handle = generate_and_register_handle(resource_details_page_url_string, credentials, client, initial_doi_dict_values=initial_doi_dict_values)
    return handle, client, credentials

def delete_handle(handle: str, client: RESTHandleClient):
    delete_result = client.delete_handle(handle)
    logger.info('OK: Delete handle successful.')
    return delete_result

def get_handle_url(handle: str, client: RESTHandleClient) -> str:
    key = 'URL'
    read_value = client.get_value_from_handle(handle, key)

    return read_value

def get_handle_issue_number(handle: str, client: RESTHandleClient) -> str:
    key = 'issueNumber'
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
    issue_number_key = 'issueNumber'
    url_key = 'URL'
    issue_number = client.get_value_from_handle(handle, issue_number_key)
    new_issue_number = int(issue_number) + 1
    update_dict = {
        url_key: new_handle_value,
        issue_number_key: new_issue_number,
    }
    modify_result = client.modify_handle_value(handle, **update_dict)
    get_url_result = client.get_value_from_handle(handle, url_key)
    get_issue_number_result = client.get_value_from_handle(handle, issue_number_key)

    if (get_url_result == new_handle_value and
        str(get_issue_number_result) == str(new_issue_number)):
        logger.info('OK: Update handle URL successful.')
    else:
        logger.critical('CRITICAL: Modify handle URL returned unexpected value.')
        logger.info(f'Expected URL: {new_handle_value}')
        logger.info(f'Returned URL: {get_url_result}')
        logger.info(f'Expected issue number: {str(new_issue_number)}')
        logger.info(f'Returned issue number: {str(get_issue_number_result)}')
    
    return modify_result

def get_handles_with_prefix(prefix):
    handle_api_endpoint = os.environ['HANDLE_API_ENDPOINT_URL']
    response = requests.get(
        f'{handle_api_endpoint}/api/handles?prefix={prefix}',
        auth=(urllib.parse.quote_plus(os.environ['HANDLE_API_USERNAME']), os.environ['HANDLE_API_KEY'])
    )
    handles_with_prefix = response.json()
    return handles_with_prefix

def add_doi_metadata_kernel_to_handle(handle: str, doi_dict: dict, client: RESTHandleClient):
    flat_doi_dict = flatten(doi_dict, number_list_items=False)
    modify_result = client.modify_handle_value(handle, **flat_doi_dict, add_if_not_exist=True)
    return modify_result