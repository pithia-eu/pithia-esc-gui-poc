from django.http import (
    HttpResponseRedirect,
    HttpResponseServerError,
)
from django.shortcuts import render
from django.urls import reverse

from .services import (
    get_data_collections_for_search,
    get_parents_of_registered_ontology_terms,
    get_registered_annotation_types,
    get_registered_computation_types,
    get_registered_features_of_interest,
    get_registered_instrument_types,
    get_registered_measurands,
    get_registered_observed_properties,
    get_registered_phenomenons,
    setup_computation_types_for_observed_property_search_form,
    setup_instrument_types_for_observed_property_search_form,
)

from common.constants import (
    ANNOTATION_TYPE_URL_BASE,
    COMPUTATION_TYPE_URL_BASE,
    FEATURE_OF_INTEREST_URL_BASE,
    INSTRUMENT_TYPE_URL_BASE,
    OBSERVED_PROPERTY_URL_BASE,
)
from ontology.services import (
    create_dictionary_from_pithia_ontology_component,
    categorise_observed_property_dict_by_top_level_phenomenons,
)

_INDEX_PAGE_TITLE = 'Search Data Collections by Content'

def get_tree_form_for_ontology_component(request, ontology_component):
    terms_load_error_msg = '<span class="text-body-secondary">The form could not be loaded due to a server error.</span>'

    instrument_types_grouped_by_observed_property = {}
    computation_types_grouped_by_observed_property = {}
    if ontology_component == 'observedProperty':
        instrument_types_grouped_by_observed_property = setup_instrument_types_for_observed_property_search_form()
        computation_types_grouped_by_observed_property = setup_computation_types_for_observed_property_search_form()
    try:
        dictionary = create_dictionary_from_pithia_ontology_component(
            ontology_component,
            instrument_types_grouped_by_observed_property=instrument_types_grouped_by_observed_property,
            computation_types_grouped_by_observed_property=computation_types_grouped_by_observed_property
        )
    except FileNotFoundError:
        return HttpResponseServerError(terms_load_error_msg)
    
    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []

    if ontology_component.lower() == 'observedproperty':
        registered_ontology_terms = get_registered_observed_properties()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
        return render(request, 'search/observed_property_tree_categories_template.html', {
            'observed_property_categories': categorise_observed_property_dict_by_top_level_phenomenons(dictionary),
            'ontology_component_name': ontology_component,
            'registered_ontology_terms': registered_ontology_terms,
            'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
        })
    elif ontology_component.lower() == 'annotationtype':
        registered_ontology_terms = get_registered_annotation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
    elif ontology_component.lower() == 'computationtype':
        registered_ontology_terms = get_registered_computation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
    elif ontology_component.lower() == 'featureofinterest':
        try:
            registered_observed_property_ids = get_registered_observed_properties()
            registered_ontology_terms = get_registered_features_of_interest(registered_observed_property_ids)
            parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
        except FileNotFoundError:
            return HttpResponseServerError(terms_load_error_msg)
    elif ontology_component.lower() == 'instrumenttype':
        registered_ontology_terms = get_registered_instrument_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
    elif ontology_component.lower() == 'measurand':
        try:
            registered_observed_property_ids = get_registered_observed_properties()
            registered_ontology_terms = get_registered_measurands(registered_observed_property_ids)
            parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
        except FileNotFoundError:
            return HttpResponseServerError(terms_load_error_msg)
    elif ontology_component.lower() == 'phenomenon':
        try:
            registered_observed_property_ids = get_registered_observed_properties()
            registered_ontology_terms = get_registered_phenomenons(registered_observed_property_ids)
            parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, [])
        except FileNotFoundError:
            return HttpResponseServerError(terms_load_error_msg)
    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': dictionary,
        'ontology_component_name': ontology_component,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })

def index(request):
    if request.method == 'POST':
        features_of_interests = request.POST.getlist('featureOfInterest')
        request.session['features_of_interest'] = features_of_interests
        computation_types = request.POST.getlist('computationType')
        request.session['computation_types'] = computation_types
        instrument_types = request.POST.getlist('instrumentType')
        request.session['instrument_types'] = instrument_types
        annotation_types = request.POST.getlist('annotationType')
        request.session['annotation_types'] = annotation_types
        observed_properties = request.POST.getlist('observedProperty')
        request.session['observed_properties'] = observed_properties
        return HttpResponseRedirect(reverse('search:results'))
    return render(request, 'search/index.html', {
        'title': _INDEX_PAGE_TITLE
    })

def results_from_foi(request):
    feature_of_interest_url = request.GET.get('feature_of_interest')
    request.session['features_of_interest'] = [feature_of_interest_url]
    return HttpResponseRedirect(reverse('search:results'))

def results(request):
    observed_property_urls = [f'{OBSERVED_PROPERTY_URL_BASE}/{op_localid}' for op_localid in request.session.get('observed_properties', [])]
    computation_type_urls = [f'{COMPUTATION_TYPE_URL_BASE}/{computation_type_localid}' for computation_type_localid in request.session.get('computation_types', [])]
    instrument_type_urls = [f'{INSTRUMENT_TYPE_URL_BASE}/{instrument_type_localid}' for instrument_type_localid in request.session.get('instrument_types', [])]
    annotation_type_urls = [f'{ANNOTATION_TYPE_URL_BASE}/{annotation_type_localid}' for annotation_type_localid in request.session.get('annotation_types', [])]
    feature_of_interest_urls = [f'{FEATURE_OF_INTEREST_URL_BASE}/{feature_of_interest_localid}' for feature_of_interest_localid in request.session.get('features_of_interest', [])]
    
    data_collections = get_data_collections_for_search(
        feature_of_interest_urls=feature_of_interest_urls,
        instrument_type_urls=instrument_type_urls,
        computation_type_urls=computation_type_urls,
        annotation_type_urls=annotation_type_urls,
        observed_property_urls=observed_property_urls
    )

    return render(request, 'search/results.html', {
        'title': 'Search Results',
        'results': data_collections,
        'search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })