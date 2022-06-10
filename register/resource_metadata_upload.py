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

resource_revision_collection_names = {
    ORGANISATION: 'organisation-revisions',
    INDIVIDUAL: 'individual-revisions',
    PROJECT: 'project-revisions',
    PLATFORM: 'platform-revisions',
    INSTRUMENT: 'instrument-revisions',
    OPERATION: 'operation-revisions',
    ACQUISITION: 'acquisition-revisions',
    COMPUTATION: 'computation-revisions',
    PROCESS: 'process-revisions',
    DATA_COLLECTION: 'data-collection-revisions',
}

current_resource_version_collection_names = {
    ORGANISATION: 'current-organisations',
    INDIVIDUAL: 'current-individuals',
    PROJECT: 'current-projects',
    PLATFORM: 'current-platforms',
    INSTRUMENT: 'current-instruments',
    OPERATION: 'current-operations',
    ACQUISITION: 'current-acquisitions',
    COMPUTATION: 'current-computations',
    PROCESS: 'current-processes',
    DATA_COLLECTION: 'current-data-collections',
}

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
def copy_current_version_of_resource_to_revisions_collection(resource_pithia_identifier, current_resource_version_collection_name, resource_revisions_collection_name):
    current_version_of_resource = db[current_resource_version_collection_name].find_one({
        'identifier.ESPAS_Identifier.localID': resource_pithia_identifier['localID'],
        'identifier.ESPAS_Identifier.namespace': resource_pithia_identifier['namespace'],
    })
    if not current_version_of_resource:
        return
    return db[resource_revisions_collection_name].insert_one(current_version_of_resource)

def replace_current_version_of_resource_with_newer_version(newer_resource_version, current_resource_version_collection_name):
    # The resource version is expected to be added
    # by data owners, but if not, may need to add
    # it here.
    db[current_resource_version_collection_name].delete_many({})
    return db[current_resource_version_collection_name].insert_one(newer_resource_version)

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
    elif resource_type  == PROCESS:
        format_process_dictionary(xml_as_dict)
    elif resource_type  == DATA_COLLECTION:
        format_data_collection_dictionary(xml_as_dict)
    
    current_resource_version_collection_name = current_resource_version_collection_names.get(resource_type, None)
    resource_revision_collection_name = resource_revision_collection_names.get(resource_type, None)
    if not current_resource_version_collection_name and not resource_revision_collection_name:
        return 'Resource type not supported.'
    copy_current_version_of_resource_to_revisions_collection(xml_as_dict['identifier']['pithia:Identifier'], current_resource_version_collection_name, resource_revision_collection_name)
    return replace_current_version_of_resource_with_newer_version(xml_as_dict, current_resource_version_collection_name)