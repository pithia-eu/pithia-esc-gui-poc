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
            'features_of_interest': request.POST.getlist('featureOfInterest'),
            'computation_types': request.POST.getlist('computationType'),
            'instrument_types': request.POST.getlist('instrumentType'),
            'annotation_types': request.POST.getlist('annotationType'),
            'observed_properties': request.POST.getlist('observedProperty'),
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
    data_collections = get_data_collections_for_search(
        annotation_type_urls=[f'{ANNOTATION_TYPE_URL_BASE}/{annotation_type_localid}' for annotation_type_localid in request.session.get('annotation_types', [])],
        computation_type_urls=[f'{COMPUTATION_TYPE_URL_BASE}/{computation_type_localid}' for computation_type_localid in request.session.get('computation_types', [])],
        feature_of_interest_urls=[f'{FEATURE_OF_INTEREST_URL_BASE}/{feature_of_interest_localid}' for feature_of_interest_localid in request.session.get('features_of_interest', [])],
        instrument_type_urls=[f'{INSTRUMENT_TYPE_URL_BASE}/{instrument_type_localid}' for instrument_type_localid in request.session.get('instrument_types', [])],
        observed_property_urls=[f'{OBSERVED_PROPERTY_URL_BASE}/{op_localid}' for op_localid in request.session.get('observed_properties', [])]
    )

    return render(request, 'data_collection_search/results.html', {
        'title': 'Data Collection Search by Content Results',
        'results': data_collections,
        'search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })