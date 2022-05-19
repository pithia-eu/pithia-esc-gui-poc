from mongodb import db
import json
import xmltodict

ORGANISATION = 'organisation'
INDIVIDUAL = 'individual'
PROJECT = 'project'
PLATFORM = 'platform'
INSTRUMENT = 'instrument'
OPERATION = 'operation'
ACQUISITION = 'acquisition'
COMPUTATION = 'computation'
PROCESS = 'process'
DATA_COLLECTION = 'data-collection'

ORGANISATION_COLLECTION = 'organisations'
INDIVIDUAL_COLLECTION = 'individuals'
PROJECT_COLLECTION = 'projects'
PLATFORM_COLLECTION = 'platforms'
INSTRUMENT_COLLECTION = 'instruments'
OPERATION_COLLECTION = 'operations'
ACQUISITION_COLLECTION = 'acquisitions'
COMPUTATION_COLLECTION = 'computations'
PROCESS_COLLECTION = 'processes'
DATA_COLLECTION_COLLECTION = 'data-collections'



def format_acquisition_dictionary(dictionary):
    # Check if the 'capability' property is an
    # array-type property
    if 'capability' in dictionary and not isinstance(dictionary['capability'], list):
        dictionary['capability'] = [dictionary['capability']]
    return dictionary

def format_computation_dictionary(dictionary):
    # Check if the 'capability' property is an
    # array-type property
    if 'capability' in dictionary and not isinstance(dictionary['capability'], list):
        dictionary['capability'] = [dictionary['capability']]
    return dictionary

def format_data_collection_dictionary(dictionary):
    # Check if the 'relatedParty' property is an
    # array-type property
    if not isinstance(dictionary['relatedParty'], list):
        dictionary['relatedParty'] = [dictionary['relatedParty']]
    # Check if the 'om:parameter' property exists and
    # if it is an array-type property
    if 'om:paramater' in dictionary and not isinstance(dictionary['om:paramater'], list):
        dictionary['om:paramater'] = [dictionary['om:paramater']]
    # Check if nested 'source' property is an
    # array-type property
    if not isinstance(dictionary['result']['pithia:CollectionResults']['source'], list):
        dictionary['result']['pithia:CollectionResults']['source'] = [dictionary['result']['pithia:CollectionResults']['source']]
    return dictionary

def format_process_dictionary(dictionary):
    # Check if the 'acquisitionComponent' property exists and
    # if it is an array-type property
    if 'acquisitionComponent' in dictionary and not isinstance(dictionary['acquisitionComponent'], list):
        dictionary['acquisitionComponent'] = [dictionary['acquisitionComponent']]
    # Check if the 'computationComponent' property exists and
    # if it is an array-type property
    if 'computationComponent' in dictionary and not isinstance(dictionary['computationComponent'], list):
        dictionary['computationComponent'] = [dictionary['computationComponent']]
    return dictionary

def convert_xml_file_to_dictionary(xml_file):
    xml = xml_file.read()
    xml_as_dict = xmltodict.parse(xml)
    xml_as_json = json.dumps(xml_as_dict)
    # Some formatting to get rid of '\n' characters and extra
    # whitespace within strings
    xml_as_json = xml_as_json.replace('\\n', '')
    xml_as_json = ' '.join(xml_as_json.split())
    # pymongo takes dictionaries when inserting new documents,
    # so convert the JSON back to a dictionary
    return json.loads(xml_as_json)

def add_dictionary_to_mongodb_collection(dictionary, collection_name):
    return db[collection_name].insert_one(dictionary)

def convert_and_upload_xml_file(xml_file, resource_type):
    xml_as_dict = convert_xml_file_to_dictionary(xml_file)
    # Remove the top-level tag
    xml_as_dict = xml_as_dict[(list(xml_as_dict)[0])]
    if resource_type  == ACQUISITION:
        format_acquisition_dictionary(xml_as_dict)
        return add_dictionary_to_mongodb_collection(xml_as_dict, ACQUISITION_COLLECTION)
    elif resource_type  == COMPUTATION:
        format_computation_dictionary(xml_as_dict)
        return add_dictionary_to_mongodb_collection(xml_as_dict, COMPUTATION_COLLECTION)
    elif resource_type  == DATA_COLLECTION:
        format_data_collection_dictionary(xml_as_dict)
        return add_dictionary_to_mongodb_collection(xml_as_dict, DATA_COLLECTION_COLLECTION)
    elif resource_type  == INDIVIDUAL:
        return add_dictionary_to_mongodb_collection(xml_as_dict, INDIVIDUAL_COLLECTION)
    elif resource_type  == INSTRUMENT:
        return add_dictionary_to_mongodb_collection(xml_as_dict, INSTRUMENT_COLLECTION)
    elif resource_type  == OPERATION:
        return add_dictionary_to_mongodb_collection(xml_as_dict, OPERATION_COLLECTION)
    elif resource_type  == ORGANISATION:
        return add_dictionary_to_mongodb_collection(xml_as_dict, ORGANISATION_COLLECTION)
    elif resource_type  == PLATFORM:
        return add_dictionary_to_mongodb_collection(xml_as_dict, PLATFORM_COLLECTION)
    elif resource_type  == PROCESS:
        format_process_dictionary(xml_as_dict)
        return add_dictionary_to_mongodb_collection(xml_as_dict, PROCESS_COLLECTION)
    elif resource_type  == PROJECT:
        return add_dictionary_to_mongodb_collection(xml_as_dict, PROJECT_COLLECTION)
    return 'Resource type not supported.'