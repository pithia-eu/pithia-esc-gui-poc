def format_instrument_dictionary(self, dictionary):
    # Check if 'operationalMode' property is an
    # array-type property
    if 'operationalMode' in dictionary and not isinstance(dictionary['operationalMode'], list):
        dictionary['operationalMode'] = [dictionary['operationalMode']]
    return dictionary

def format_acquisition_dictionary(self, dictionary):
    # Check if the 'capability' property is an
    # array-type property
    if 'capability' in dictionary and not isinstance(dictionary['capability'], list):
        dictionary['capability'] = [dictionary['capability']]
    return dictionary

def format_computation_dictionary(self, dictionary):
    # Check if the 'capability' property is an
    # array-type property
    if 'capability' in dictionary and not isinstance(dictionary['capability'], list):
        dictionary['capability'] = [dictionary['capability']]
    return dictionary

def format_process_dictionary(self, dictionary):
    # Check if the 'acquisitionComponent' property exists and
    # if it is an array-type property
    if 'acquisitionComponent' in dictionary and not isinstance(dictionary['acquisitionComponent'], list):
        dictionary['acquisitionComponent'] = [dictionary['acquisitionComponent']]
    # Check if the 'computationComponent' property exists and
    # if it is an array-type property
    if 'computationComponent' in dictionary and not isinstance(dictionary['computationComponent'], list):
        dictionary['computationComponent'] = [dictionary['computationComponent']]
    return dictionary

def format_data_collection_dictionary(self, dictionary):
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
    if 'collectionResults' in dictionary and 'source' in dictionary['collectionResults'] and not isinstance(dictionary['collectionResults']['source'], list):
        dictionary['collectionResults']['source'] = [dictionary['collectionResults']['source']]
    # Check if nested 'dataFormat' property is an
    # array-type property
    if 'collectionResults' in dictionary and 'source' in dictionary['collectionResults']:
        for s in dictionary['collectionResults']['source']:
            if 'dataFormat' in s['OnlineResource'] and not isinstance(s['OnlineResource']['dataFormat'], list):
                s['OnlineResource']['dataFormat'] = [s['OnlineResource']['dataFormat']]
    return dictionary