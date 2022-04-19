from mongodb import db
from enum import Enum
import json
import xmltodict

class DataModelComponent(Enum):
    ACQUISITION = 'Acquisition'
    COMPUTATION = 'Computation'
    OBSERVATION_COLLECTION = 'ObservationCollection'
    PROCESS = 'Process'

def validate_acquisition_dictionary(dict):
    # Check if the 'capability' property is an
    # array-type property
    if 'capability' in dict and not isinstance(dict['capability'], list):
        dict['capability'] = [dict['capability']]
    return dict

def validate_computation_dictionary(dict):
    # Check if the 'capability' property is an
    # array-type property
    if 'capability' in dict and not isinstance(dict['capability'], list):
        dict['capability'] = [dict['capability']]
    return dict

def validate_observation_collection_dictionary(dict):
    # Check if the 'relatedParty' property is an
    # array-type property
    if not isinstance(dict['relatedParty'], list):
        dict['relatedParty'] = [dict['relatedParty']]
    # Check if the 'om:parameter' property exists and
    # if it is an array-type property
    if 'om:paramater' in dict and not isinstance(dict['om:paramater'], list):
        dict['om:paramater'] = [dict['om:paramater']]
    # Check if nested 'source' property is an
    # array-type property
    if not isinstance(dict['result']['pithia:CollectionResults']['source'], list):
        dict['result']['pithia:CollectionResults']['source'] = [dict['result']['pithia:CollectionResults']['source']]
    return dict

def validate_process_dictionary(dict):
    # Check if the 'acquisitionComponent' property exists and
    # if it is an array-type property
    if 'acquisitionComponent' in dict and not isinstance(dict['acquisitionComponent'], list):
        dict['acquisitionComponent'] = [dict['acquisitionComponent']]
    # Check if the 'computationComponent' property exists and
    # if it is an array-type property
    if 'computationComponent' in dict and not isinstance(dict['computationComponent'], list):
        dict['computationComponent'] = [dict['computationComponent']]
    return dict


def handle_uploaded_metadata(files, form):
    # Dictionaries for the different metadata types
    num_acquisition_files = 0
    num_computation_files = 0
    num_observation_collection_files = 0
    num_process_files = 0
    new_resources = []
    i = 0
    for f in files:
        xml = f.read()
        # Convert XML to a dictionary to be able to convert it JSON
        xml_as_dict = xmltodict.parse(xml)
        # Convert the dictionary to JSON
        xml_as_json = json.dumps(xml_as_dict)
        # Some formatting to get rid of '\n' characters and extra
        # whitespace within strings
        xml_as_json = xml_as_json.replace('\\n', '')
        xml_as_json = ' '.join(xml_as_json.split())
        # pymongo takes dictionaries when inserting new documents,
        # so convert the JSON back to a dictionary
        xml_as_dict = json.loads(xml_as_json)
        resource = {
            'content': '',
            'dataModelType': '',
            'executable': f'is-file{i}-executable' in form,
            'metadataType': form[f'file{i}-metadata-type'],
        }
        valid_resource_uploaded = False
        # Add the dictionary to the relevant dictionary list
        if DataModelComponent.ACQUISITION.value in xml_as_dict:
            xml_as_dict[DataModelComponent.ACQUISITION.value] = validate_acquisition_dictionary(xml_as_dict[DataModelComponent.ACQUISITION.value])
            resource['content'] = xml_as_dict[DataModelComponent.ACQUISITION.value]
            resource['dataModelType'] = DataModelComponent.ACQUISITION.value.lower()
            valid_resource_uploaded = True
            num_acquisition_files += 1
        elif DataModelComponent.COMPUTATION.value in xml_as_dict:
            xml_as_dict[DataModelComponent.COMPUTATION.value] = validate_computation_dictionary(xml_as_dict[DataModelComponent.COMPUTATION.value])
            resource['content'] = xml_as_dict[DataModelComponent.COMPUTATION.value]
            resource['dataModelType'] = DataModelComponent.COMPUTATION.value.lower()
            valid_resource_uploaded = True
            num_computation_files += 1
        elif DataModelComponent.OBSERVATION_COLLECTION.value in xml_as_dict:
            xml_as_dict[DataModelComponent.OBSERVATION_COLLECTION.value] = validate_observation_collection_dictionary(xml_as_dict[DataModelComponent.OBSERVATION_COLLECTION.value])
            resource['content'] = xml_as_dict[DataModelComponent.OBSERVATION_COLLECTION.value]
            resource['dataModelType'] = DataModelComponent.OBSERVATION_COLLECTION.value.lower()
            valid_resource_uploaded = True
            num_observation_collection_files += 1
        elif DataModelComponent.PROCESS.value in xml_as_dict:
            xml_as_dict[DataModelComponent.PROCESS.value] = validate_process_dictionary(xml_as_dict[DataModelComponent.PROCESS.value])
            resource['content'] = xml_as_dict[DataModelComponent.PROCESS.value]
            resource['dataModelType'] = DataModelComponent.PROCESS.value.lower()
            valid_resource_uploaded = True
            num_process_files += 1

        if valid_resource_uploaded:
            new_resources.append(resource)
        # DEBUG: Print out the resulting dictionary
        # print(json.dumps(xml_as_dict, indent=2, sort_keys=True))
        i += 1
    # Insert the dictionaries into the database
    if len(new_resources) > 0:
        db['resources'].insert_many(new_resources)
    # Return number of files uploaded from each category
    return {
        'acq_files_uploaded': num_acquisition_files,
        'comp_files_uploaded': num_computation_files,
        'op_files_uploaded': num_observation_collection_files,
        'proc_files_uploaded': num_process_files,
    }