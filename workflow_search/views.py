from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template.loader import render_to_string

from .services import get_registered_features_of_interest

from ontology.services import create_dictionary_from_pithia_ontology_component
from search.services import get_parents_of_registered_ontology_terms


_INDEX_PAGE_TITLE = 'Search Workflows by Content'


# Create your views here.

def index(request):
    return render(request, 'workflow_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
    })


def results(request):
    return render(request, 'workflow_search/results.html', {

    })


def search_form_template(request, ontology_branch_name):
    terms_load_error_msg = render_to_string('search/search_form_load_error.html', {})

    try:
        dictionary = create_dictionary_from_pithia_ontology_component(ontology_branch_name)
    except FileNotFoundError:
        return HttpResponseServerError(terms_load_error_msg)

    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []

    try:
        registered_ontology_terms = get_registered_features_of_interest()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(
            registered_ontology_terms,
            ontology_branch_name,
            []
        )
    except FileNotFoundError:
        return HttpResponseServerError(terms_load_error_msg)

    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': dictionary,
        'ontology_component_name': ontology_branch_name,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })