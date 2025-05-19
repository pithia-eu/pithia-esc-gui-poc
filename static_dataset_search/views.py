from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template.loader import render_to_string

from .services import get_registered_features_of_interest

from ontology.services import create_dictionary_from_pithia_ontology_component
from search.services import get_parents_of_registered_ontology_terms


# Create your views here.

def index(request):
    return render(request, 'static_dataset_search/index.html', {})


def results(request):
    return render(request, 'static_dataset_search/results.html', {})


def foi_form_template(request):
    terms_load_error_msg = render_to_string('search/search_form_load_error.html', {})

    foi_ontology_branch_name = 'featureOfInterest'
    try:
        dictionary = create_dictionary_from_pithia_ontology_component(foi_ontology_branch_name)
    except FileNotFoundError:
        return HttpResponseServerError(terms_load_error_msg)

    registered_features_of_interest = []
    parents_of_registered_features_of_interest = []

    try:
        registered_features_of_interest = get_registered_features_of_interest()
        parents_of_registered_features_of_interest = get_parents_of_registered_ontology_terms(
            registered_features_of_interest,
            foi_ontology_branch_name,
            []
        )
    except FileNotFoundError:
        return HttpResponseServerError(terms_load_error_msg)

    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': dictionary,
        'ontology_component_name': foi_ontology_branch_name,
        'registered_ontology_terms': registered_features_of_interest,
        'parents_of_registered_ontology_terms': parents_of_registered_features_of_interest,
    })