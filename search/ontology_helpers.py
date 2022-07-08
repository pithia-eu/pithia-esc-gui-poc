import os
from requests import get
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import _SKOS

ONTOLOGY_SERVER_BASE_URL = 'https://ontology.espas-fp7.eu/'
ESPAS = Namespace('http://ontology.espas-fp7.eu/espasdefinitions#')

def get_object_names_from_triple(triple):
    s, p, o = triple
    if 'phenomenon' in o:
        return o.replace(f'{ONTOLOGY_SERVER_BASE_URL}phenomenon/', 'phenomenon')
    if 'measurand' in o:
        return o.replace(f'{ONTOLOGY_SERVER_BASE_URL}measurand/', 'measurand')
    if 'featureOfInterest' in o:
        return o.replace(f'{ONTOLOGY_SERVER_BASE_URL}featureOfInterest/', 'featureOfInterest')

def map_ontology_components_to_observed_property_dictionary(op_uri, op_dict, g):
    op_phenomenons = list(map(get_object_names_from_triple, g.triples((op_uri, ESPAS.phenomenon, None))))
    op_measurands = list(map(get_object_names_from_triple, g.triples((op_uri, ESPAS.measurand, None))))
    op_featuresOfInterest = list(map(get_object_names_from_triple, g.triples((op_uri, ESPAS.featureOfInterest, None))))
    op_dict['phenomenons'] = op_phenomenons
    op_dict['measurands'] = op_measurands
    op_dict['featuresOfInterest'] = op_featuresOfInterest
    return op_dict

def get_rdf_text_remotely(ontology_component):
    ontology_component_url = f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/'
    ontology_response = get(ontology_component_url)
    return ontology_response.text

def get_rdf_text_locally(ontology_component):
    ontology_file = open(os.path.join(os.path.dirname(os.path.dirname(__file__)),  f'search/ontology/{ontology_component.lower()}.xml'))
    return ontology_file.read()


def get_rdf_text_for_ontology_component(ontology_component):
    # Fetch ontology component of ESPAS ontology text
    if ontology_component.lower() == 'featureofinterest':
        # Current solution as PITHIA ontology server is not ready
        # yet.
        ontology_text = get_rdf_text_locally(ontology_component)
    else:
        try:
            ontology_text = get_rdf_text_remotely(ontology_component)
        except BaseException as err:
            print(err)
            # Read ontology from file - alt method if connection to ontology server fails
            ontology_text = get_rdf_text_locally(ontology_component)

    return ontology_text

def get_graph_of_pithia_ontology_component(ontology_component):
    ontology_text = get_rdf_text_for_ontology_component(ontology_component)

    # Create a graph object with rdflib and parse fetched text
    g = Graph()
    return g.parse(data=ontology_text, format='application/rdf+xml')

def get_observed_property_hrefs_from_features_of_interest(features_of_interest):
    op_hrefs = []
    g = get_graph_of_pithia_ontology_component('observedProperty')
    for s, p, o in g.triples((None, ESPAS.featureOfInterest, None)):
        if any(x in str(o) for x in features_of_interest):
            op_hrefs.append(str(s))
    return op_hrefs

def get_feature_of_interest_ids_from_observed_property_id(observed_property_id, g, feature_of_interest_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}observedProperty/{observed_property_id}'), ESPAS.featureOfInterest, None)):
        feature_of_interest_ids.append(o.split('/')[-1])
    return feature_of_interest_ids

def get_phenomenon_ids_from_observed_property_id(observed_property_id, g, phenomenon_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}observedProperty/{observed_property_id}'), ESPAS.phenomenon, None)):
        phenomenon_ids.append(o.split('/')[-1])
    return phenomenon_ids

def get_measurand_ids_from_observed_property_id(observed_property_id, g, measurand_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}observedProperty/{observed_property_id}'), ESPAS.measurand, None)):
        measurand_ids.append(o.split('/')[-1])
    return measurand_ids

def get_parent_node_ids_of_node_id(node_id, ontology_component, g, parent_node_ids):
    SKOS = _SKOS.SKOS
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/{node_id}'), SKOS.broader, None)):
        parent_node_ids.append(o.split('/')[-1])
    return parent_node_ids

def create_dictionary_from_pithia_ontology_component(ontology_component):
    ontology_component_url = f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/'
    g = get_graph_of_pithia_ontology_component(ontology_component)
    SKOS = _SKOS.SKOS
    ontology_dictionary = {}
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

    ontology_dictionary = {}
    for s, p, o in g.triples((None, SKOS.broader, None)):
        # s_value is the narrower value
        s_value = s.replace(ontology_component_url, '')
        # o_value is the broader value
        o_value = o.replace(ontology_component_url, '')
        # If the broader value is not in the nested list, add it and set
        # its value to an empty dictionary.
        if o_value not in ontology_dictionary:
            ontology_dictionary[o_value] = {
                'id': f'{ontology_component}{o_value}',
                'value': o_value,
                'pref_label': pref_label_mappings[o_value],
                'alt_label': alt_label_mappings[o_value] if o_value in alt_label_mappings else None,
                'narrowers': {},
            }
            if ontology_component == 'observedProperty':
                ontology_dictionary[o_value] = map_ontology_components_to_observed_property_dictionary(o, ontology_dictionary[o_value], g)

        # Add to the broader value's dictionary by putting in a narrower
        # value as a key and setting its value to '1'.
        ontology_dictionary[o_value]['narrowers'][s_value] = {
            'id': f'{ontology_component}{s_value}',
            'value': s_value,
            'pref_label': pref_label_mappings[s_value],
            'alt_label': alt_label_mappings[s_value] if s_value in alt_label_mappings else None,
            'narrowers': {},
        }
        if ontology_component == 'observedProperty':
            ontology_dictionary[o_value]['narrowers'][s_value] = map_ontology_components_to_observed_property_dictionary(s, ontology_dictionary[o_value]['narrowers'][s_value], g)

    # Property dictionaries for child terms are nested within
    # the property dictionaries for parent terms, but the keys
    # for the child terms will still be present at the top level
    # of the ontology dictionary and should be removed.
    keys_to_remove_at_top_level = []
    for key in ontology_dictionary:
        for nestedKey in ontology_dictionary[key]['narrowers']:
            if nestedKey in ontology_dictionary:
                ontology_dictionary[key]['narrowers'][nestedKey] = ontology_dictionary[nestedKey]
                keys_to_remove_at_top_level.append(nestedKey)

    for key in keys_to_remove_at_top_level:
        del ontology_dictionary[key]

    return ontology_dictionary

def get_localid_from_ontology_node_uri(ontology_node_uri):
    return ontology_node_uri.split('/')[-1]