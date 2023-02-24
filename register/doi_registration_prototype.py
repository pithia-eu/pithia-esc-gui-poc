from lxml import etree
from validation.metadata_validation import parse_xml_file

import json
import requests
import environ

env = environ.Env()


def get_doi_api_endpoint_url():
    return env('DOI_API_URL')

def get_doi_api_headers():
    return {
        'Content-Type': 'application/json'
    }

def get_doi_api_auth():
    return (env('DOI_API_USERNAME'), env('DOI_API_PASSWORD'))

def create_pid(landing_page_url):
    endpoint_url = get_doi_api_endpoint_url()
    headers = get_doi_api_headers()
    auth = get_doi_api_auth()
    data = json.loads(env('DOI_API_PUT_DATA'))
    data['values'][1]['data'] = landing_page_url
    print('data', data)
    response = requests.put(
        endpoint_url,
        auth=auth,
        headers=headers,
        json=data
    )
    return response

def get_pid():
    endpoint_url = get_doi_api_endpoint_url()
    headers = get_doi_api_headers()
    auth = get_doi_api_auth()
    response = requests.get(
        endpoint_url,
        auth=auth,
        headers=headers
    )
    return response

def delete_pid():
    endpoint_url = get_doi_api_endpoint_url()
    headers = get_doi_api_headers()
    auth = get_doi_api_auth()
    response = requests.delete(
        endpoint_url,
        auth=auth,
        headers=headers
    )
    return response

def generate_doi(resource_detail_url):
    doi = {
        'registrationAgencyDoiName': '10.1000/ra-5',
        'issueDate': '2015-01-07',
        'issueNumber': '7',
        'name': {
            '@primaryLanguage': 'en',
            'value': 'Test',
            'type': 'Title',
        },
        'identifier': {
            'nonUriValue': '10.5240/B94E-F500-7164-57DB-82F5-6',
            'uri': {
                '@returnType': 'text/html',
                '#text': 'https://ui.eidr.org/view/content?id=10.5240/B94E-F500-7164-57DB-82F5-6',
            },
            'type': 'EidrContentID',
        }
    }
    return doi

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