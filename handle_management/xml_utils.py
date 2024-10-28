import logging
from lxml import etree
from lxml.etree import (
    Element,
    ElementTree,
)
from pyhandle.handleexceptions import *

from .handle_api import get_date_handle_was_issued_as_string

from common.models import (
    CatalogueDataSubset,
    DataCollection,
    Individual,
    Organisation,
)

logger = logging.getLogger(__name__)

# TODO: clarify
def initialise_default_doi_kernel_metadata_dict():
    default_key_value = 'Unknown'
    return {
        'referentDoiName': default_key_value,
        'primaryReferentType': 'Creation',
        'registrationAgencyDoiName': '10.1000/0000',
        # Already stored in the handle, can just retrieve it.
        'issueDate': default_key_value,
        # issueNumber - Added manually to the handle, then incremented manually as well,
        # each time the handle is updated.
        'issueNumber': '1',
        'referentCreation': {
            'name': {
                '@primaryLanguage': 'en',
                'value': default_key_value,
                'type': 'Name',
            },
            'identifier': {
                'nonUriValue': '',
                'uri': {
                    '@returnType': 'text/html',
                    '#text': '',
                },
                'type': 'URI',
            },
            'structuralType': 'Digital',
            'mode': 'Visual',
            'character': 'Language',
            'type': 'Dataset',
            'principalAgent': {
                'name': {
                    'value': default_key_value,
                    'type': 'Name',
                },
            },
        },
    }

def get_first_related_party_name_from_data_collection(
        data_collection,
        organisation_model=Organisation,
        individual_model=Individual
    ):
    try:
        related_party_url = data_collection.first_related_party_url
    except KeyError:
        return None
    
    try:
        return organisation_model.objects.get_by_metadata_server_url(related_party_url).name
    except organisation_model.DoesNotExist:
        pass
    
    try:
        individual = individual_model.objects.get_by_metadata_server_url(related_party_url)
    except individual_model.DoesNotExist:
        return None
    organisation_url = individual.organisation_url
    
    try:
        return organisation_model.objects.get_by_metadata_server_url(organisation_url).name
    except organisation_model.DoesNotExist:
        pass
    return None

def add_data_subset_data_to_doi_metadata_kernel_dict(
    data_subset,
    doi_dict: dict,
    data_collection_model=DataCollection):
    try:
        referenced_data_collection_url = data_subset.data_collection_url
    except KeyError:
        return doi_dict
    
    try:
        referenced_data_collection = data_collection_model.objects.get_by_metadata_server_url(referenced_data_collection_url)
    except data_collection_model.DoesNotExist:
        return doi_dict
    
    doi_dict['referentCreation']['name']['value'] = referenced_data_collection.name
    principal_agent_name_value = get_first_related_party_name_from_data_collection(referenced_data_collection)
    if principal_agent_name_value is not None:
        doi_dict['referentCreation']['principalAgent']['name']['value'] = principal_agent_name_value
    return doi_dict

def add_handle_data_to_doi_metadata_kernel_dict(handle: str, doi_dict: dict):
    handle_issue_date_as_string = get_date_handle_was_issued_as_string(handle)
    doi_dict['referentDoiName'] = handle
    doi_dict['issueDate'] = handle_issue_date_as_string
    doi_dict['referentCreation']['identifier']['nonUriValue'] = handle
    doi_dict['referentCreation']['identifier']['uri']['#text'] = f'https://hdl.handle.net/{handle}'
    return doi_dict

def add_doi_metadata_kernel_to_data_subset(
    resource_id,
    doi_dict: dict,
    metadata_file_xml_string: str,
    owner_id: str
):
    doi_xml_string = create_doi_xml_string_from_dict(doi_dict)
    xml_string_with_doi = add_doi_xml_string_to_metadata_xml_string(metadata_file_xml_string, doi_xml_string)
    CatalogueDataSubset.objects.update_from_xml_string(
        resource_id,
        xml_string_with_doi,
        owner_id
    )
    return xml_string_with_doi

def create_lxml_utf8_parser():
    return etree.XMLParser(remove_blank_text=True, encoding='utf-8')

def create_doi_xml_string_from_dict(doi_dict: dict) -> str:
    doi_xml_string = '''
    <doi xmlns:doi="http://www.doi.org/2010/DOISchema">
        <doi:referentDoiName>{referentDoiName}</doi:referentDoiName>
        <doi:primaryReferentType>{primaryReferentType}</doi:primaryReferentType>
        <!-- The registrationAgencyDoiName used is a placeholder -->
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
                    <doi:value>{principalAgentNameValue}</doi:value>
                    <doi:type>{principalAgentNameType}</doi:type>
                </doi:name>
            </doi:principalAgent>
        </doi:referentCreation>
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

def parse_xml_string(xml_string: str):
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    # Use lxml to append a new filled in doi element
    parser = create_lxml_utf8_parser()
    return etree.fromstring(xml_string, parser)

def is_doi_element_present_in_xml_file(xml_file) -> bool:
    xml_file.seek(0)
    xml_string_parsed = parse_xml_string(xml_file.read())
    return xml_string_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}doi') != None

def get_last_result_time_element(data_subset_xml_string_parsed: ElementTree) -> Element:
    result_time_elements_found = data_subset_xml_string_parsed.findall('.//{https://metadata.pithia.eu/schemas/2.2}resultTime')
    if len(result_time_elements_found) == 0:
        return None
    return result_time_elements_found[-1]

def get_last_source_element(data_subset_xml_string_parsed: ElementTree) -> Element:
    source_elements_found = data_subset_xml_string_parsed.findall('.//{https://metadata.pithia.eu/schemas/2.2}source')
    if len(source_elements_found) == 0:
        return None
    return source_elements_found[-1]

def add_doi_xml_string_to_metadata_xml_string(metadata_xml_string: str, doi_xml_string: str) -> str:
    if isinstance(metadata_xml_string, str):
        metadata_xml_string = metadata_xml_string.encode('utf-8')
    # Use lxml to append a new filled in doi element
    parser = create_lxml_utf8_parser()
    root = etree.fromstring(metadata_xml_string, parser)
    doi_xml_string_parsed = etree.fromstring(doi_xml_string)
    element_to_insert_after = get_last_source_element(root)
    if element_to_insert_after is None:
        element_to_insert_after = get_last_result_time_element(root)
    parent_of_element_to_insert_after = element_to_insert_after.getparent()
    parent_of_element_to_insert_after.insert(parent_of_element_to_insert_after.index(element_to_insert_after) + 1, doi_xml_string_parsed)
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