from mongodb import db
import json
import xmltodict

def validate_acquisition_dictionary(dict):
    # Check if the 'capability' property is an
    # array-type property
    if not isinstance(dict['capability'], list):
        dict['capability'] = [dict['capability']]
    return dict

def validate_computation_dictionary(dict):
    # Check if the 'capability' property is an
    # array-type property
    if not isinstance(dict['capability'], list):
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


def handle_uploaded_metadata(files):
    # Dictionaries for the different metadata types
    acquisition_dicts = []
    computation_dicts = []
    observation_collection_dicts = []
    process_dicts = []
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
        # Add the dictionary to the relevant dictionary list
        if 'Acquisition' in xml_as_dict:
            xml_as_dict['Acquisition'] = validate_acquisition_dictionary(xml_as_dict['Acquisition'])
            acquisition_dicts.append(xml_as_dict['Acquisition'])
        elif 'Computation' in xml_as_dict:
            xml_as_dict['Computation'] = validate_computation_dictionary(xml_as_dict['Computation'])
            computation_dicts.append(xml_as_dict['Computation'])
        elif 'ObservationCollection' in xml_as_dict:
            xml_as_dict['ObservationCollection'] = validate_observation_collection_dictionary(xml_as_dict['ObservationCollection'])
            observation_collection_dicts.append(xml_as_dict['ObservationCollection'])
        elif 'Process' in xml_as_dict:
            xml_as_dict['Process'] = validate_process_dictionary(xml_as_dict['Process'])
            process_dicts.append(xml_as_dict['Process'])
        
        # DEBUG: Print out the resulting dictionary
        # print(json.dumps(xml_as_dict, indent=2, sort_keys=True))
    # Insert the dictionaries into the database
    if len(acquisition_dicts) > 0:
        db['acquisitions'].insert_many(acquisition_dicts)
    if len(computation_dicts) > 0:
        db['computations'].insert_many(computation_dicts)
    if len(observation_collection_dicts) > 0:
        db['observation_collections'].insert_many(observation_collection_dicts)
    if len(process_dicts) > 0:
        db['processes'].insert_many(process_dicts)
    # Return number of files uploaded from each category
    return {
        'acq_files_uploaded': len(acquisition_dicts),
        'comp_files_uploaded': len(computation_dicts),
        'op_files_uploaded': len(observation_collection_dicts),
        'proc_files_uploaded': len(process_dicts),
    }