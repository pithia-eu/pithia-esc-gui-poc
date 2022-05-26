import os
from requests import get
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import _SKOS
from pprint import pprint

ESPAS_ONTOLOGY_URL = 'https://ontology.espas-fp7.eu/'
ESPAS = Namespace('http://ontology.espas-fp7.eu/espasdefinitions#')

def get_object_names_from_triple(triple):
    s, p, o = triple
    if 'phenomenon' in o:
        return o.replace(f'{ESPAS_ONTOLOGY_URL}phenomenon/', 'phenomenon')
    if 'measurand' in o:
        return o.replace(f'{ESPAS_ONTOLOGY_URL}measurand/', 'measurand')
    if 'featureOfInterest' in o:
        return o.replace(f'{ESPAS_ONTOLOGY_URL}featureOfInterest/', 'featureOfInterest')

def map_ontology_components_to_observed_property_dictionary(op_uri, op_dict, g):
    op_phenomenons = list(map(get_object_names_from_triple, g.triples((op_uri, ESPAS.phenomenon, None))))
    op_measurands = list(map(get_object_names_from_triple, g.triples((op_uri, ESPAS.measurand, None))))
    op_featuresOfInterest = list(map(get_object_names_from_triple, g.triples((op_uri, ESPAS.featureOfInterest, None))))
    op_dict['phenomenons'] = op_phenomenons
    op_dict['measurands'] = op_measurands
    op_dict['featuresOfInterest'] = op_featuresOfInterest
    return op_dict

def create_dictionary_from_pithia_ontology_component(ontology_component):
    ontology_component_url = f'{ESPAS_ONTOLOGY_URL}{ontology_component}/'

    # Fetch ontology component of ESPAS ontology text
    try:
        ontology_response = get(ontology_component_url)
        ontology_text = ontology_response.text
    except BaseException as err:
        print(err)
        # Read ontology from file - alt method if connection to ontology server fails
        ontology_file = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),  f'search\ontology\{ontology_component.capitalize()}.xml'))
        ontology_text = ontology_file.read()

    # Create a graph object with rdflib and parse fetched text
    g = Graph()
    g.parse(data=ontology_text, format='application/rdf+xml')
    SKOS = _SKOS.SKOS

    ontology_term_properties_dictionary = {}
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

    ontology_term_properties_dictionary = {}
    for s, p, o in g.triples((None, SKOS.broader, None)):
        # s_value is the narrower value
        s_value = s.replace(ontology_component_url, '')
        # o_value is the broader value
        o_value = o.replace(ontology_component_url, '')
        # If the broader value is not in the nested list, add it and set
        # its value to an empty dictionary.
        if o_value not in ontology_term_properties_dictionary:
            ontology_term_properties_dictionary[o_value] = {
                'id': f'{ontology_component}{o_value}',
                'value': o_value,
                'pref_label': pref_label_mappings[o_value],
                'alt_label': alt_label_mappings[o_value] if o_value in alt_label_mappings else None,
                'narrowers': {},
            }
            if ontology_component == 'observedProperty':
                ontology_term_properties_dictionary[o_value] = map_ontology_components_to_observed_property_dictionary(o, ontology_term_properties_dictionary[o_value], g)

        # Add to the broader value's dictionary by putting in a narrower
        # value as a key and setting its value to '1'.
        ontology_term_properties_dictionary[o_value]['narrowers'][s_value] = {
            'id': f'{ontology_component}{s_value}',
            'value': s_value,
            'pref_label': pref_label_mappings[s_value],
            'alt_label': alt_label_mappings[s_value] if s_value in alt_label_mappings else None,
            'narrowers': {},
        }
        if ontology_component == 'observedProperty':
            ontology_term_properties_dictionary[o_value]['narrowers'][s_value] = map_ontology_components_to_observed_property_dictionary(s, ontology_term_properties_dictionary[o_value]['narrowers'][s_value], g)

    keys_to_remove_at_top_level = []
    for key in ontology_term_properties_dictionary:
        for nestedKey in ontology_term_properties_dictionary[key]['narrowers']:
            if nestedKey in ontology_term_properties_dictionary:
                ontology_term_properties_dictionary[key]['narrowers'][nestedKey] = ontology_term_properties_dictionary[nestedKey]
                keys_to_remove_at_top_level.append(nestedKey)

    for key in keys_to_remove_at_top_level:
        del ontology_term_properties_dictionary[key]

    return ontology_term_properties_dictionary