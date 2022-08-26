import re

ONTOLOGY_COMPONENT_ENUMS = {
    'computationType': 'computationTypes',
    'featureOfInterest': 'featuresOfInterest',
    'instrumentType': 'instrumentTypes',
    'measurand': 'measurands',
    'observedProperty': 'observedProperties',
    'phenomenon': 'phenomenons',
}

def convert_list_to_regex_list(list):
    return [re.compile(x) for x in list]

def map_ontology_components_to_local_ids(list):
    local_ids_list = []
    for x in list:
        local_ids_list.append(x['identifier']['PITHIA_Identifier']['localID'])
    return local_ids_list

def remove_underscore_from_id_attribute(resource):
    resource['id'] = resource['_id']
    return resource