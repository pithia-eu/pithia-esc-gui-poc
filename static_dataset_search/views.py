from django.http import (
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from .services import get_registered_features_of_interest


from common.constants import FEATURE_OF_INTEREST_URL_BASE
from common.models import StaticDatasetEntry
from ontology.services import create_dictionary_from_pithia_ontology_component
from search.services import get_parents_of_registered_ontology_terms


_INDEX_PAGE_TITLE = 'Search Static Dataset Entries by Content'


# Create your views here.

def index(request):
    if request.method == 'POST':
        features_of_interests = request.POST.getlist('featureOfInterest')
        request.session['sde_features_of_interest'] = features_of_interests
        return HttpResponseRedirect(reverse('static_dataset_search:results'))
    return render(request, 'static_dataset_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'feature_of_interest_form_url': reverse('static_dataset_search:foi_form_template'),
    })


def results(request):
    feature_of_interest_urls = [
        f'{FEATURE_OF_INTEREST_URL_BASE}/{feature_of_interest_localid}'
        for feature_of_interest_localid in request.session.get('sde_features_of_interest', [])
    ]
    results = StaticDatasetEntry.objects.for_search(feature_of_interest_urls)
    return render(request, 'static_dataset_search/results.html', {
        'title': 'Search Results',
        'results': results,
        'search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })


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