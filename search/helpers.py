import re

ONTOLOGY_COMPONENT_ENUMS = {
    'measurand': 'measurands',
    'observedProperty': 'observed_properties',
    'phenomenon': 'phenomenons',
    'qualifier': 'qualifiers'
}

def convert_list_to_regex_list(list):
    return [re.compile(x) for x in list]

def map_ontology_components_to_local_ids(list):
    local_ids_list = []
    for x in list:
        local_ids_list.append(x['content']['identifier']['pithia:Identifier']['localID'])
    return local_ids_list