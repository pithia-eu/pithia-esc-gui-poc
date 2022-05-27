from django.http import HttpResponseRedirect
from django.shortcuts import render
from .helpers import ONTOLOGY_COMPONENT_ENUMS
from .ontology_helpers import create_dictionary_from_pithia_ontology_component
from .search_helpers import find_matching_observation_collections

def get_tree_form_for_ontology_component(request, ontology_component):
    dictionary = create_dictionary_from_pithia_ontology_component(ontology_component)
    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': dictionary,
        'ontology_component_name': ONTOLOGY_COMPONENT_ENUMS[ontology_component]
    })

def index(request):
    if request.method == 'POST':
        observed_properties = request.POST.getlist('observedProperties')
        query_string = '?'
        if len(observed_properties) > 0:
            query_string += f'observed-properties={",".join(observed_properties)}'
        if query_string == '?':
            query_string = ''

        return HttpResponseRedirect('/search/results/' + query_string)
    else:
        return render(request, 'search/index.html', {
            'title': 'Search Models & Measurements'
        })

def foi_selection(request):
    return render(request, 'search/foi_selection.html', {
        'title': 'Step 1: Select Features of Interest'
    })

def comp_and_instr_type_selection(request):
    return render(request, 'search/comp_and_instr_type_selection.html', {
        'title': 'Step 2: Select Computation Types and Instrument Types'
    })

def op_selection(request):
    return render(request, 'search/op_selection.html', {
        'title': 'Step 3: Select Observed Properties'
    })

def results(request):
    observation_collections = find_matching_observation_collections(request)

    return render(request, 'search/results.html', {
        'title': 'Search results',
        'results': observation_collections
    })