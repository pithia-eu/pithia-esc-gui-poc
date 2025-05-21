from django.shortcuts import render
from django.urls import reverse

from .services import OntologyTermsRegisteredWithWorkflows

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

def index(request):
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
    return render(request, 'workflow_search/results.html', {

    })


class AnnotationTypeSearchByContentTemplateView(BaseAnnotationTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return []


class ComputationTypeSearchByContentTemplateView(BaseComputationTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return []


class FeatureOfInterestSearchByContentTemplateView(BaseFeatureOfInterestSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return OntologyTermsRegisteredWithWorkflows.get_registered_features_of_interest()


class InstrumentTypeSearchByContentTemplateView(BaseInstrumentTypeSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return []


class MeasurandSearchByContentTemplateView(BaseMeasurandSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return []


class ObservedPropertySearchByContentTemplateView(BaseObservedPropertySearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return []


class PhenomenonSearchByContentTemplateView(BasePhenomenonSearchByContentTemplateView):
    def get_registered_ontology_terms(self):
        return []

