from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
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
    return render(request, 'search/index.html', {
        'title': 'Search Models & Measurements'
    })

def foi_selection(request):
    if request.method == 'POST':
        features_of_interests = request.POST.getlist('featuresOfInterest')
        request.session['features_of_interest'] = features_of_interests
        return HttpResponseRedirect(reverse('search:comp_and_instr_type_selection'))
    return render(request, 'search/foi_selection.html', {
        'title': 'Step 1: Select Features of Interest'
    })

def comp_and_instr_type_selection(request):
    if request.method == 'POST':
        computation_types = request.POST.getlist('computationTypes')
        request.session['computation_types'] = computation_types
        instrument_types = request.POST.getlist('instrumentTypes')
        request.session['instrument_types'] = instrument_types
        return HttpResponseRedirect(reverse('search:op_selection'))
    return render(request, 'search/comp_and_instr_type_selection.html', {
        'title': 'Step 2: Select Computation Types and Instrument Types'
    })

def op_selection(request):
    if request.method == 'POST':
        observed_properties = request.POST.getlist('observedProperties')
        request.session['observed_properties'] = observed_properties
        return HttpResponseRedirect(reverse('search:results'))
    return render(request, 'search/op_selection.html', {
        'title': 'Step 3: Select Observed Properties'
    })

def results(request):
    observation_collections = find_matching_observation_collections(request)

    return render(request, 'search/results.html', {
        'title': 'Search results',
        'results': observation_collections
    })

def get_observed_properties_from_data_collections(request):
    return