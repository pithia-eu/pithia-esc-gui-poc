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

def format_data_collection_dictionary(dictionary):
    # Check if the 'relatedParty' property is an
    # array-type property
    if 'relatedParty' in dictionary and not isinstance(dictionary['relatedParty'], list):
        dictionary['relatedParty'] = [dictionary['relatedParty']]
    # Check if the 'om:parameter' property exists and
    # if it is an array-type property
    if 'om:paramater' in dictionary and not isinstance(dictionary['om:paramater'], list):
        dictionary['om:paramater'] = [dictionary['om:paramater']]
    # Check if nested 'source' property is an
    # array-type property
    if 'result' in dictionary and 'pithia:CollectionResults' in dictionary['result'] and 'source' in dictionary['result']['pithia:CollectionResults'] and not isinstance(dictionary['result']['pithia:CollectionResults']['source'], list):
        dictionary['result']['pithia:CollectionResults']['source'] = [dictionary['result']['pithia:CollectionResults']['source']]
    return dictionary