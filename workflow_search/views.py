from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse

from .services import (
    OntologyTermsRegisteredWithWorkflows,
    WorkflowSearchService,
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


_INDEX_PAGE_TITLE = 'Search Workflows by Content'


# Create your views here.

class AnnotationTypeSearchByContentTemplateView(BaseAnnotationTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_annotation_types()


class ComputationTypeSearchByContentTemplateView(BaseComputationTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_computation_types()


class FeatureOfInterestSearchByContentTemplateView(BaseFeatureOfInterestSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_features_of_interest()


class InstrumentTypeSearchByContentTemplateView(BaseInstrumentTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_instrument_types()


class MeasurandSearchByContentTemplateView(BaseMeasurandSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_measurands()


class ObservedPropertySearchByContentTemplateView(BaseObservedPropertySearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_observed_properties()


class PhenomenonSearchByContentTemplateView(BasePhenomenonSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_phenomenons()


def index(request):
    if request.method == 'POST':
        request.session.update({
            'wf_features_of_interest': request.POST.getlist('featureOfInterest'),
            'wf_computation_types': request.POST.getlist('computationType'),
            'wf_instrument_types': request.POST.getlist('instrumentType'),
            'wf_annotation_types': request.POST.getlist('annotationType'),
            'wf_observed_properties': request.POST.getlist('observedProperty'),
        })
        return redirect('workflow_search:results')
    return render(request, 'workflow_search/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'annotation_type_form_url': reverse('workflow_search:forms:annotation_types'),
        'computation_type_form_url': reverse('workflow_search:forms:computation_types'),
        'feature_of_interest_form_url': reverse('workflow_search:forms:features_of_interest'),
        'instrument_type_form_url': reverse('workflow_search:forms:instrument_types'),
        'measurand_form_url': reverse('workflow_search:forms:measurands'),
        'observed_property_form_url': reverse('workflow_search:forms:observed_properties'),
        'phenomenon_form_url': reverse('workflow_search:forms:phenomenons'),
    })


def results(request):
    results = WorkflowSearchService.search(
        annotation_type_urls=[
            f'{ANNOTATION_TYPE_URL_BASE}/{annotation_type_localid}'
            for annotation_type_localid in request.session.get(
                'wf_annotation_types',
                []
            )
        ],
        computation_type_urls=[
            f'{COMPUTATION_TYPE_URL_BASE}/{computation_type_localid}'
            for computation_type_localid in request.session.get(
                'wf_computation_types',
                []
            )
        ],
        feature_of_interest_urls=[
            f'{FEATURE_OF_INTEREST_URL_BASE}/{feature_of_interest_localid}'
            for feature_of_interest_localid in request.session.get(
                'wf_features_of_interest',
                []
            )
        ],
        instrument_type_urls=[
            f'{INSTRUMENT_TYPE_URL_BASE}/{instrument_type_localid}'
            for instrument_type_localid in request.session.get(
                'wf_instrument_types',
                []
            )
        ],
        observed_property_urls=[
            f'{OBSERVED_PROPERTY_URL_BASE}/{op_localid}'
            for op_localid in request.session.get(
                'wf_observed_properties',
                []
            )
            ]
    )
    print('results', results)
    return render(request, 'workflow_search/results.html', {
        'title': 'Workflow Search by Content Results',
        'results': results,
        'search_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })