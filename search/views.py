import logging
from django.http import HttpResponseServerError
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .services import get_parents_of_registered_ontology_terms

from ontology.services import (
    categorise_observed_property_dict_by_top_level_phenomenons,
    create_dictionary_from_pithia_ontology_component,
)


logger = logging.getLogger(__file__)


# Create your views here.

class SearchByContentTemplateView(TemplateView):
    template_name = 'search/ontology_tree_template_outer.html'
    terms_load_error_msg = render_to_string('search/search_form_load_error.html', {})

    def get_dict_of_ontology_branch(self):
        return create_dictionary_from_pithia_ontology_component(self.ontology_branch_name)

    def get_registered_ontology_terms(self):
        return []

    def _get_parents_of_registered_ontology_terms(self):
        return get_parents_of_registered_ontology_terms(
            self.registered_ontology_terms,
            self.ontology_branch_name,
            []
        )

    def _on_server_error(self):
            return HttpResponseServerError(self.terms_load_error_msg)

    def get(self, request, *args, **kwargs):
        # Get a nested dict of the ontology tree for a given branch.
        try:
            self.ontology_branch_dict = self.get_dict_of_ontology_branch()
        except FileNotFoundError:
            logger.exception(f'An error occurred attempting to load from the {self.ontology_branch_name} ontology file.')
            return self._on_server_error()
        except Exception:
            logger.exception(f'An error occurred whilst attempting to load the {self.ontology_branch_name} ontology branch.')
            return self._on_server_error()

        # Get the terms registered with whatever is being searched
        # for, for that ontology branch.
        try:
            self.registered_ontology_terms = self.get_registered_ontology_terms()
        except FileNotFoundError:
            logger.exception(f'An error occurred attempting to load from the {self.ontology_branch_name} ontology file.')
            return self._on_server_error()
        except Exception:
            logger.exception(f'An error occurred whilst getting registered {self.ontology_branch_name} terms.')
            return self._on_server_error()

        # Get the parents terms of the registered terms to help with
        # layout in the Django template.
        try:
            self.parents_of_registered_ontology_terms = self._get_parents_of_registered_ontology_terms()
        except Exception:
            logger.exception(f'An error occurred whilst getting parents of registered {self.ontology_branch_name} terms.')
            return self._on_server_error()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'ontology_component': self.ontology_branch_dict,
            'ontology_component_name': self.ontology_branch_name,
            'registered_ontology_terms': self.registered_ontology_terms,
            'parents_of_registered_ontology_terms': self.parents_of_registered_ontology_terms,
        })
        return context


class BaseAnnotationTypeSearchByContentTemplateView(SearchByContentTemplateView):
    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'annotationType'
        return super().get(request, *args, **kwargs)


class BaseComputationTypeSearchByContentTemplateView(SearchByContentTemplateView):
    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'computationType'
        return super().get(request, *args, **kwargs)


class BaseFeatureOfInterestSearchByContentTemplateView(SearchByContentTemplateView):
    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'featureOfInterest'
        return super().get(request, *args, **kwargs)


class BaseInstrumentTypeSearchByContentTemplateView(SearchByContentTemplateView):
    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'instrumentType'
        return super().get(request, *args, **kwargs)


class BaseMeasurandSearchByContentTemplateView(SearchByContentTemplateView):
    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'measurand'
        return super().get(request, *args, **kwargs)


class BaseObservedPropertySearchByContentTemplateView(SearchByContentTemplateView):
    template_name = 'search/observed_property_tree_categories_template.html'

    def get_dict_of_ontology_branch(self, **kwargs):
        return categorise_observed_property_dict_by_top_level_phenomenons(create_dictionary_from_pithia_ontology_component(
            self.ontology_branch_name,
            **kwargs
        ))

    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'observedProperty'
        return super().get(request, *args, **kwargs)


class BasePhenomenonSearchByContentTemplateView(SearchByContentTemplateView):
    def get(self, request, *args, **kwargs):
        self.ontology_branch_name = 'phenomenon'
        return super().get(request, *args, **kwargs)