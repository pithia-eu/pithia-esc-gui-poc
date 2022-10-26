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
    # Check if the 'type' property (which maps to both instrumentTypes and computationTypes)
    # exists and if it is an array-type property
    if 'type' in dictionary and not isinstance(dictionary['type'], list):
        dictionary['type'] = [dictionary['type']]
    # Check if the 'om:parameter' property exists and
    # if it is an array-type property
    if 'om:parameter' in dictionary and not isinstance(dictionary['om:parameter'], list):
        dictionary['om:parameter'] = [dictionary['om:parameter']]
    # Check if the nested 'namedRegion' property is an array-type property
    if 'om:featureOfInterest' in dictionary and 'FeatureOfInterest' in dictionary['om:featureOfInterest'] and 'namedRegion' in dictionary['om:featureOfInterest']['FeatureOfInterest'] and not isinstance(dictionary['om:featureOfInterest']['FeatureOfInterest']['namedRegion'], list):
        dictionary['om:featureOfInterest']['FeatureOfInterest']['namedRegion'] = [dictionary['om:featureOfInterest']['FeatureOfInterest']['namedRegion']]
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