from requests import get
from django.shortcuts import render

from functools import reduce
from rdflib import Graph
from rdflib.namespace import _SKOS

ESPAS = 'https://ontology.espas-fp7.eu/'

# Create your views here.
def construct_html_from_human_readable_list(human_readable_list):
    html = '<ul>'
    for key in human_readable_list:
        html += f'<li><input type="checkbox"> {key}'
        if human_readable_list[key] != 1:
            html += f'{construct_html_from_human_readable_list(human_readable_list[key])}'
        html += '</li>'
    html += '</ul>'
    return html

def create_human_readable_nested_list(nested_list, pref_label_mappings, alt_label_mappings):
    human_readable_nested_list = {}
    for key in nested_list:
        if (key not in alt_label_mappings):
            human_readable_key = pref_label_mappings[key]
        else:
            human_readable_key = f'{pref_label_mappings[key]} ({alt_label_mappings[key]})'
        human_readable_nested_list[human_readable_key] = nested_list[key]
        if human_readable_nested_list[human_readable_key] != 1:
            human_readable_nested_list[human_readable_key] = create_human_readable_nested_list(nested_list[key], pref_label_mappings, alt_label_mappings)
    return human_readable_nested_list

def nested_list_from_ontology_component(ontology_component):
    # Fetch Observed Property component of ESPAS ontology text
    ontology_component_url = f'{ESPAS}{ontology_component}'
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

    for s, p, o in g.triples((None, SKOS.broader, None)):
        s_value = s.replace(ontology_component_url, '')
        o_value = o.replace(ontology_component_url, '')
        if o_value not in nested_list:
            nested_list[o_value] = {}
        nested_list[o_value][s_value] = 1

    keys_to_remove_at_top_level = []
    for key in nested_list:
        for nestedKey in nested_list[key]:
            if nestedKey in nested_list:
                nested_list[key][nestedKey] = nested_list[nestedKey]
                keys_to_remove_at_top_level.append(nestedKey)

    for key in keys_to_remove_at_top_level:
        del nested_list[key]

    return create_human_readable_nested_list(nested_list, pref_label_mappings, alt_label_mappings)

def index(request):
    observed_properties = nested_list_from_ontology_component('observedProperty')
    qualifiers = nested_list_from_ontology_component('qualifier')
    measurands = nested_list_from_ontology_component('measurand')
    phenomenons = nested_list_from_ontology_component('phenomenon')

    observed_properties_html = construct_html_from_human_readable_list(observed_properties)
    qualifiers_html = construct_html_from_human_readable_list(qualifiers)
    measurands_html = construct_html_from_human_readable_list(measurands)
    phenomenons_html = construct_html_from_human_readable_list(phenomenons)

    return render(request, 'search/index.html', {
        'observed_properties_html': observed_properties_html,
        'qualifiers_html': qualifiers_html,
        'measurands_html': measurands_html,
        'phenomenons_html': phenomenons_html,
    })