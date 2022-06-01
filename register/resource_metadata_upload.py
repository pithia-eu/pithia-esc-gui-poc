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

CURRENT_ORGANISATIONS = 'current-organisations'
CURRENT_INDIVIDUALS = 'current-individuals'
CURRENT_PROJECTS = 'current-projects'
CURRENT_PLATFORMS = 'current-platforms'
CURRENT_INSTRUMENTS = 'current-instruments'
CURRENT_OPERATIONS = 'current-operations'
CURRENT_ACQUISITIONS = 'current-acquisitions'
CURRENT_COMPUTATIONS = 'current-computations'
CURRENT_PROCESSES = 'current-processes'
CURRENT_DATA_COLLECTIONS = 'current-data-collections'

ORGANISATION_REVISIONS = 'organisation-revisions'
INDIVIDUAL_REVISIONS = 'individual-revisions'
PROJECT_REVISIONS = 'project-revisions'
PLATFORM_REVISIONS = 'platform-revisions'
INSTRUMENT_REVISIONS = 'instrument-revisions'
OPERATION_REVISIONS = 'operation-revisions'
ACQUISITION_REVISIONS = 'acquisition-revisions'
COMPUTATION_REVISIONS = 'computation-revisions'
PROCESS_REVISIONS = 'processe-revisions'
DATA_COLLECTION_REVISIONS = 'data-collection-revisions'

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

def get_collection_names_from_resource_type(resource_type):
    if resource_type  == ACQUISITION:
        current_resource_version_collection = CURRENT_ACQUISITIONS
        resource_revisions_collection = ACQUISITION_REVISIONS
    elif resource_type  == COMPUTATION:
        current_resource_version_collection = CURRENT_COMPUTATIONS
        resource_revisions_collection = COMPUTATION_REVISIONS
    elif resource_type  == DATA_COLLECTION:
        current_resource_version_collection = CURRENT_DATA_COLLECTIONS
        resource_revisions_collection = DATA_COLLECTION_REVISIONS
    elif resource_type  == INDIVIDUAL:
        current_resource_version_collection = CURRENT_INDIVIDUALS
        resource_revisions_collection = INDIVIDUAL_REVISIONS
    elif resource_type  == INSTRUMENT:
        current_resource_version_collection = CURRENT_INSTRUMENTS
        resource_revisions_collection = INSTRUMENT_REVISIONS
    elif resource_type  == OPERATION:
        current_resource_version_collection = CURRENT_OPERATIONS
        resource_revisions_collection = OPERATION_REVISIONS
    elif resource_type  == ORGANISATION:
        current_resource_version_collection = CURRENT_ORGANISATIONS
        resource_revisions_collection = ORGANISATION_REVISIONS
    elif resource_type  == PLATFORM:
        current_resource_version_collection = CURRENT_PLATFORMS
        resource_revisions_collection = PLATFORM_REVISIONS
    elif resource_type  == PROCESS:
        current_resource_version_collection = CURRENT_PROCESSES
        resource_revisions_collection = PROCESS_REVISIONS
    elif resource_type  == PROJECT:
        current_resource_version_collection = CURRENT_PROJECTS
        resource_revisions_collection = PROJECT_REVISIONS
    return current_resource_version_collection or 'unknown', resource_revisions_collection or 'unknown'

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

# TODO: Replace ESPAS_Identifier with pithia:Identifier
def copy_current_version_of_resource_to_revisions_collection(resource_pithia_identifier, current_resource_version_collection, resource_revisions_collection):
    current_version_of_resource = db[current_resource_version_collection].find_one({
        'identifier.ESPAS_Identifier.localID': resource_pithia_identifier['localID'],
        'identifier.ESPAS_Identifier.namespace': resource_pithia_identifier['namespace'],
    })
    print(current_version_of_resource)
    if not current_version_of_resource:
        return
    return db[resource_revisions_collection].insert_one(current_version_of_resource)

def replace_current_version_of_resource_with_newer_version(newer_resource_version, current_resource_version_collection):
    # The resource version is expected to be added
    # by data owners, but if not, may need to add
    # it here.
    db[current_resource_version_collection].delete_many({})
    return db[current_resource_version_collection].insert_one(newer_resource_version)

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
    elif resource_type  == COMPUTATION:
        format_computation_dictionary(xml_as_dict)
    elif resource_type  == DATA_COLLECTION:
        format_data_collection_dictionary(xml_as_dict)
    elif resource_type  == PROCESS:
        format_process_dictionary(xml_as_dict)
    
    current_resource_version_collection, resource_revisions_collection = get_collection_names_from_resource_type(resource_type)
    if not current_resource_version_collection and not resource_revisions_collection:
        return 'Resource type not supported.'
    copy_current_version_of_resource_to_revisions_collection(xml_as_dict['identifier']['ESPAS_Identifier'], current_resource_version_collection, resource_revisions_collection)
    return replace_current_version_of_resource_with_newer_version(xml_as_dict, current_resource_version_collection)