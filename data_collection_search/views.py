from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .services import (
    get_data_collections_for_search,
    get_registered_annotation_types,
    get_registered_computation_types,
    get_registered_features_of_interest,
    get_registered_instrument_types,
    get_registered_measurands,
    get_registered_observed_properties,
    get_registered_phenomenons,
)

from common.constants import (
    ANNOTATION_TYPE_URL_BASE,
    COMPUTATION_TYPE_URL_BASE,
    FEATURE_OF_INTEREST_URL_BASE,
    INSTRUMENT_TYPE_URL_BASE,
    OBSERVED_PROPERTY_URL_BASE,
)
from search.views import (
    BaseAnnotationTypeSearchByContentTemplateView,
    BaseComputationTypeSearchByContentTemplateView,
    BaseFeatureOfInterestSearchByContentTemplateView,
    BaseInstrumentTypeSearchByContentTemplateView,
    BaseMeasurandSearchByContentTemplateView,
    BaseObservedPropertySearchByContentTemplateView,
    BasePhenomenonSearchByContentTemplateView,
)


_INDEX_PAGE_TITLE = 'Search Data Collections by Content'


class AnnotationTypeSearchByContentTemplateView(BaseAnnotationTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return get_registered_annotation_types()


class ComputationTypeSearchByContentTemplateView(BaseComputationTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return get_registered_computation_types()


class FeatureOfInterestSearchByContentTemplateView(BaseFeatureOfInterestSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return get_registered_features_of_interest()


class InstrumentTypeSearchByContentTemplateView(BaseInstrumentTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return get_registered_instrument_types()


class MeasurandSearchByContentTemplateView(BaseMeasurandSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        registered_observed_property_ids = get_registered_observed_properties()
        return get_registered_measurands(registered_observed_property_ids)


class ObservedPropertySearchByContentTemplateView(BaseObservedPropertySearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return get_registered_observed_properties()


class PhenomenonSearchByContentTemplateView(BasePhenomenonSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        registered_observed_property_ids = get_registered_observed_properties()
        return get_registered_phenomenons(registered_observed_property_ids)


def index(request):
    if request.method == 'POST':
        request.session.update({
            'data_collection_search': {
                'features_of_interest': request.POST.getlist('featureOfInterest'),
                'computation_types': request.POST.getlist('computationType'),
                'instrument_types': request.POST.getlist('instrumentType'),
                'annotation_types': request.POST.getlist('annotationType'),
                'observed_properties': request.POST.getlist('observedProperty'),
            }
        })
        return HttpResponseRedirect(reverse('data_collection_search:results'))
    return render(request, 'data_collection_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'annotation_type_form_url': reverse('data_collection_search:forms:annotation_types'),
        'computation_type_form_url': reverse('data_collection_search:forms:computation_types'),
        'feature_of_interest_form_url': reverse('data_collection_search:forms:features_of_interest'),
        'instrument_type_form_url': reverse('data_collection_search:forms:instrument_types'),
        'measurand_form_url': reverse('data_collection_search:forms:measurands'),
        'observed_property_form_url': reverse('data_collection_search:forms:observed_properties'),
        'phenomenon_form_url': reverse('data_collection_search:forms:phenomenons'),
    })

def results(request):
    local_ids = request.session.get('data_collection_search', {})
    feature_of_interest_local_ids = local_ids.get('features_of_interest', [])
    computation_type_local_ids = local_ids.get('computation_types', [])
    instrument_type_local_ids = local_ids.get('instrument_types', [])
    annotation_type_local_ids = local_ids.get('annotation_types', [])
    observed_property_local_ids = local_ids.get('observed_properties', [])

    data_collections = get_data_collections_for_search(
        feature_of_interest_urls=[
            f'{FEATURE_OF_INTEREST_URL_BASE}/{local_id}'
            for local_id in feature_of_interest_local_ids
        ],
        computation_type_urls=[
            f'{COMPUTATION_TYPE_URL_BASE}/{local_id}'
            for local_id in computation_type_local_ids
        ],
        instrument_type_urls=[
            f'{INSTRUMENT_TYPE_URL_BASE}/{local_id}'
            for local_id in instrument_type_local_ids
        ],
        annotation_type_urls=[
            f'{ANNOTATION_TYPE_URL_BASE}/{local_id}'
            for local_id in annotation_type_local_ids
        ],
        observed_property_urls=[
            f'{OBSERVED_PROPERTY_URL_BASE}/{local_id}'
            for local_id in observed_property_local_ids
        ]
    )

    # Display parameters user inputted in case they want to refine for the next search.
    parameters = dict()
    if len(feature_of_interest_local_ids):
        parameters.update({
            'Features of Interest': [
                f'{FEATURE_OF_INTEREST_URL_BASE}/{local_id}'
                for local_id in feature_of_interest_local_ids
            ],
        })
    if len(computation_type_local_ids):
        parameters.update({
            'Computation Types': [
                f'{COMPUTATION_TYPE_URL_BASE}/{local_id}'
                for local_id in computation_type_local_ids
            ],
        })
    if len(instrument_type_local_ids):
        parameters.update({
            'Instrument Types': [
                f'{INSTRUMENT_TYPE_URL_BASE}/{local_id}'
                for local_id in instrument_type_local_ids
            ],
        })
    if len(annotation_type_local_ids):
        parameters.update({
            'Annotation Types': [
                f'{ANNOTATION_TYPE_URL_BASE}/{local_id}'
                for local_id in annotation_type_local_ids
            ],
        })
    if len(observed_property_local_ids):
        parameters.update({
            'Observed Properties': [
                f'{OBSERVED_PROPERTY_URL_BASE}/{local_id}'
                for local_id in observed_property_local_ids
            ],
        })

    return render(request, 'data_collection_search/results.html', {
        'title': 'Data Collection Search by Content Results',
        'parameters': parameters,
        'results': data_collections,
        'search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })