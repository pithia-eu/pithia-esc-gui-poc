import os
from requests import get
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace._SKOS import SKOS
from rdflib.resource import Resource

ONTOLOGY_SERVER_BASE_URL = 'https://metadata.pithia.eu/ontology/2.2/'
PITHIA = Namespace('https://metadata.pithia.eu/ontology/2.2/')

def get_object_names_from_triple(triple):
    s, p, o = triple
    if 'phenomenon' in o:
        return o.replace(f'{ONTOLOGY_SERVER_BASE_URL}phenomenon/', 'phenomenon')
    if 'measurand' in o:
        return o.replace(f'{ONTOLOGY_SERVER_BASE_URL}measurand/', 'measurand')
    if 'featureOfInterest' in o:
        return o.replace(f'{ONTOLOGY_SERVER_BASE_URL}featureOfInterest/', 'featureOfInterest')

def map_ontology_components_to_observed_property_dictionary(op_uri, op_dict, g):
    op_phenomenons = list(map(get_object_names_from_triple, g.triples((op_uri, PITHIA.phenomenon, None))))
    op_measurands = list(map(get_object_names_from_triple, g.triples((op_uri, PITHIA.measurand, None))))
    op_featuresOfInterest = list(map(get_object_names_from_triple, g.triples((op_uri, PITHIA.featureOfInterest, None))))
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
    for s, p, o in g.triples((None, PITHIA.featureOfInterest, None)):
        if any(x in str(o) for x in features_of_interest):
            op_hrefs.append(str(s))
    return op_hrefs

def get_feature_of_interest_ids_from_observed_property_id(observed_property_id, g, feature_of_interest_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}observedProperty/{observed_property_id}'), PITHIA.featureOfInterest, None)):
        feature_of_interest_ids.append(o.split('/')[-1])
    return feature_of_interest_ids

def get_phenomenon_ids_from_observed_property_id(observed_property_id, g, phenomenon_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}observedProperty/{observed_property_id}'), PITHIA.phenomenon, None)):
        phenomenon_ids.append(o.split('/')[-1])
    return phenomenon_ids

def get_measurand_ids_from_observed_property_id(observed_property_id, g, measurand_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}observedProperty/{observed_property_id}'), PITHIA.measurand, None)):
        measurand_ids.append(o.split('/')[-1])
    return measurand_ids

def get_parent_node_ids_of_node_id(node_id, ontology_component, g, parent_node_ids):
    for s, p, o in g.triples((URIRef(f'{ONTOLOGY_SERVER_BASE_URL}{ontology_component}/{node_id}'), SKOS.broader, None)):
        parent_node_ids.append(o.split('/')[-1])
    return parent_node_ids

def get_localid_from_ontology_node_iri(ontology_node_iri):
    return ontology_node_iri.split('/')[-1]

def get_pref_label_from_ontology_node_iri(ontology_node_iri, g=None):
    if g is None:
        ontology_term_category = ontology_node_iri.split('/')[-2]
        g = get_graph_of_pithia_ontology_component(ontology_term_category)
    return str(g.value(URIRef(ontology_node_iri), SKOS.prefLabel))

# Credit for get_path: https://stackoverflow.com/a/22171182
def getpath(nested_dict, value, prepath=()):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if value in v: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = getpath(v, value, path) # recursive call
            if p is not None:
                return p

# Credit for gen_dict_extract: https://stackoverflow.com/a/29652561
def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

def get_nested_phenomenons_in_observed_property(observed_property):
    all_phenomenons_of_observed_property = list(gen_dict_extract('phenomenon', observed_property))
    # Credit for list flattening code: https://stackoverflow.com/a/952952
    all_phenomenons_of_observed_property_flattened = [item for sublist in all_phenomenons_of_observed_property for item in sublist]
    return all_phenomenons_of_observed_property_flattened

def categorise_observed_property_dict_by_top_level_phenomenons(observed_property_dict):
    categorised_observed_property_dict = {}
    phenomen_dict = create_dictionary_from_pithia_ontology_component('phenomenon')
    added_observed_properties = []

    def add_observed_property_to_category(key, observed_property, category):
        if category not in categorised_observed_property_dict:
            categorised_observed_property_dict[category] = {}
        if (category != 'None' and
            'None' in categorised_observed_property_dict and
            key in categorised_observed_property_dict['None'] and
            key in added_observed_properties):
            categorised_observed_property_dict[category][key] = observed_property
            categorised_observed_property_dict['None'].pop(key)
        if key not in added_observed_properties:
            categorised_observed_property_dict[category][key] = observed_property
            added_observed_properties.append(key)

    for key, value in observed_property_dict.items():
        all_phenomenons_for_observed_property = get_nested_phenomenons_in_observed_property(value)
        if len(all_phenomenons_for_observed_property) == 0:
            add_observed_property_to_category(key, value, 'None')
            continue
        for phenomenon in all_phenomenons_for_observed_property:
            path_of_phenomenon = getpath(phenomen_dict, phenomenon.replace('phenomenon', ''))
            if path_of_phenomenon is None:
                add_observed_property_to_category(key, value, 'None')
            else:
                top_level_phenomenon = path_of_phenomenon[0]
                add_observed_property_to_category(key, value, top_level_phenomenon)
    if 'None' in categorised_observed_property_dict and len(categorised_observed_property_dict['None']) == 0:
        categorised_observed_property_dict.pop('None', None)
    return categorised_observed_property_dict

def create_dictionary_from_pithia_ontology_component(
    ontology_component,
    instrument_types_grouped_by_observed_property={},
    computation_types_grouped_by_observed_property={}
):
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

    if instrument_types_grouped_by_observed_property != {}:
        for op, value in instrument_types_grouped_by_observed_property.items():
            if op not in ontology_dictionary:
                continue
            ontology_dictionary[op]['instrumentType'] = value

    if computation_types_grouped_by_observed_property != {}:
        for op, value in computation_types_grouped_by_observed_property.items():
            if op not in ontology_dictionary:
                continue
            ontology_dictionary[op]['computationType'] = value

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
            # else:
            #     print('nested key in ontology dict found', nestedKey)
    
    for key in keys_to_remove_at_top_level:
        ontology_dictionary.pop(key, None)

    return ontology_dictionary