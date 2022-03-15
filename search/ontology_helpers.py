from requests import get
from rdflib import Graph
from rdflib.namespace import _SKOS

ESPAS = 'https://ontology.espas-fp7.eu/'

def nested_list_from_ontology_component(ontology_component):
    # Fetch Observed Property component of ESPAS ontology text
    ontology_component_url = f'{ESPAS}{ontology_component}/'
    r = get(ontology_component_url)
    r_text = r.text

    # Create a graph object with rdflib and parse fetched text
    g = Graph()
    g.parse(data=r_text, format='application/rdf+xml')
    SKOS = _SKOS.SKOS

    nested_list = {}
    pref_label_mappings = {}
    alt_label_mappings = {}

    for s, p, o in g.triples((None, SKOS.prefLabel, None)):
        s_value = s.replace(ontology_component_url, '')
        o_value = o.replace(ontology_component_url, '')
        pref_label_mappings[s_value] = o_value

    for s, p, o in g.triples((None, SKOS.altLabel, None)):
        s_value = s.replace(ontology_component_url, '')
        o_value = o.replace(ontology_component_url, '')
        alt_label_mappings[s_value] = o_value

    nested_list = {}
    for s, p, o in g.triples((None, SKOS.broader, None)):
        # s_value is the narrower value
        s_value = s.replace(ontology_component_url, '')
        # o_value is the broader value
        o_value = o.replace(ontology_component_url, '')
        # If the broader value is not in the nested list, add it and set
        # its value to an empty dictionary.
        if o_value not in nested_list:
            nested_list[o_value] = {
                'id': f'{ontology_component}{o_value}',
                'value': o_value,
                'pref_label': pref_label_mappings[o_value],
                'alt_label': alt_label_mappings[o_value] if o_value in alt_label_mappings else None,
                'narrowers': {}
            }
        # Add to the broader value's dictionary by putting in a narrower
        # value as a key and setting its value to '1'.
        nested_list[o_value]['narrowers'][s_value] = {
            'id': f'{ontology_component}{s_value}',
            'value': s_value,
            'pref_label': pref_label_mappings[s_value],
            'alt_label': alt_label_mappings[s_value] if s_value in alt_label_mappings else None,
            'narrowers': {}
        }

    keys_to_remove_at_top_level = []
    for key in nested_list:
        for nestedKey in nested_list[key]['narrowers']:
            if nestedKey in nested_list:
                nested_list[key]['narrowers'][nestedKey] = nested_list[nestedKey]
                keys_to_remove_at_top_level.append(nestedKey)

    for key in keys_to_remove_at_top_level:
        del nested_list[key]

    return nested_list