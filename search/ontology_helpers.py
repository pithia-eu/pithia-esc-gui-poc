import os
from requests import get
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace._SKOS import SKOS
from rdflib.resource import Resource

ONTOLOGY_SERVER_BASE_URL = 'https://metadata.pithia.eu/ontology/2.2/'
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
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/{node_id}'), SKOS.broader, None)):
        parent_node_ids.append(o.split('/')[-1])
    return parent_node_ids

def create_dictionary_from_pithia_ontology_component(ontology_component):
    ontology_component_url = f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/'
    g = get_graph_of_pithia_ontology_component(ontology_component)
    ontology_dictionary = {}
    for s, p, o in g.triples((None, SKOS.member, None)):
        # o_value is the localID after the ontology_component_url
        o_value = o.split('/')[-1]
        if o_value not in ontology_dictionary:
            ontology_dictionary[o_value] = {
                'id': f'{ontology_component}{o_value}',
                'value': o_value,
                'narrowers': {},
                'iri': f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/{o_value}',
            }
            o_resource = Resource(g, o)
            for op in o_resource.predicates():
                op_identifier_no_prefix = op.identifier.split('#')[-1]
                if len(op.identifier.split('#')) == 1:
                    op_identifier_no_prefix = op.identifier.split('/')[-1]
                if op_identifier_no_prefix not in ontology_dictionary[o_value] and (op_identifier_no_prefix == 'phenomenon' or op_identifier_no_prefix == 'featureOfInterest' or op_identifier_no_prefix == 'measurand'):
                    ontology_dictionary[o_value][op_identifier_no_prefix] = []
                    if op_identifier_no_prefix == 'phenomenon':
                        for ops, opp, opo in g.triples((o, op.identifier, None)):
                            opo_value_with_prefix = f'phenomenon{opo.split("/")[-1]}'
                            ontology_dictionary[o_value][op_identifier_no_prefix].append(opo_value_with_prefix)
                    if op_identifier_no_prefix == 'featureOfInterest':
                        for ops, opp, opo in g.triples((o, op.identifier, None)):
                            opo_value_with_prefix = f'featureOfInterest{opo.split("/")[-1]}'
                            ontology_dictionary[o_value][op_identifier_no_prefix].append(opo_value_with_prefix)
                    if op_identifier_no_prefix == 'measurand':
                        for ops, opp, opo in g.triples((o, op.identifier, None)):
                            opo_value_with_prefix = f'measurand{opo.split("/")[-1]}'
                            ontology_dictionary[o_value][op_identifier_no_prefix].append(opo_value_with_prefix)
                elif op_identifier_no_prefix not in ontology_dictionary[o_value]:
                    if len(list(g.triples((o, op.identifier, None)))) > 1:
                        ontology_dictionary[o_value][op_identifier_no_prefix] = []
                        for ops, opp, opo in g.triples((o, op.identifier, None)):
                            ontology_dictionary[o_value][op_identifier_no_prefix].append(str(opo))
                    else:
                        ontology_dictionary[o_value][op_identifier_no_prefix] = str(list(g.triples((o, op.identifier, None)))[0][2])

            # SKOS.broader covers more than SKOS.narrower
            for broader_s, broader_p, broader_o in g.triples((None, SKOS.broader, o)):
                broader_o_value = broader_o.split('/')[-1]
                broader_s_value = broader_s.split('/')[-1]
                if broader_o_value != broader_s_value and broader_s_value not in ontology_dictionary[o_value]['narrowers']:
                    ontology_dictionary[o_value]['narrowers'][broader_s_value] = {
                        'id': f'{ontology_component}{broader_s_value}',
                        'value': broader_s_value,
                        'narrowers': {},
                    }

            # Do SKOS.narrower JIC
            for narrower_s, narrower_p, narrower_o in g.triples((o, SKOS.narrower, None)):
                narrower_s_value = narrower_s.split('/')[-1]
                narrower_o_value = narrower_o.split('/')[-1]
                if narrower_o_value != narrower_s_value and narrower_o_value not in ontology_dictionary[o_value]['narrowers']:
                    ontology_dictionary[o_value]['narrowers'][narrower_o_value] = {
                        'id': f'{ontology_component}{narrower_o_value}',
                        'value': narrower_o_value,
                        'narrowers': {},
                    }
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
            else:
                print(nestedKey)
    
    for key in keys_to_remove_at_top_level:
        ontology_dictionary.pop(key, None)

    return ontology_dictionary

def get_localid_from_ontology_node_uri(ontology_node_uri):
    return ontology_node_uri.split('/')[-1]