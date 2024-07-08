from django.shortcuts import render

from .xml_metadata_to_form import (
    IndividualXmlMetadataToFormConverter,
    OrganisationXmlMetadataToFormConverter,
)

from common import models
from metadata_editor.utils import (
    BaseMetadataEditor,
    IndividualEditor,
    OrganisationEditor,
)
from metadata_editor.views import *


# Create your views here.

class ResourceUpdateWithEditorFormView(ResourceEditorFormView):
    model = None
    xml_metadata_to_form_field_converter: BaseMetadataEditor = None

    def add_form_to_metadata(self, form):
        self.metadata_editor.update_name(form.get('name'))

    def form_valid(self, form):
        try:
            self.processed_form = self.process_form(form.cleaned_data)
            self.metadata_editor = self.metadata_editor_class(xml_string=self.resource.xml)
        except BaseException:
            messages.error(self.request, 'An unexpected error occurred. Please try again later.')
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs.get('resource_id')
        self.resource = self.model.objects.get(pk=self.resource_id)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()

        initial.update(self.xml_metadata_to_form_field_converter(self.resource.xml).convert())
        if 'namespace' in initial:
            organisations_by_namespace = {value.lower(): key for key, value in self.get_namespaces_by_organisation().items()}
            organisation = organisations_by_namespace.get(initial['namespace'].lower(), '')
            initial.update({'organisation': organisation})

        return initial

class OrganisationUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    OrganisationEditorFormView):
    model = models.Organisation
    metadata_editor_class = OrganisationEditor
    xml_metadata_to_form_field_converter = OrganisationXmlMetadataToFormConverter

class IndividualUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    IndividualEditorFormView):
    model = models.Individual
    metadata_editor_class = IndividualEditor
    xml_metadata_to_form_field_converter = IndividualXmlMetadataToFormConverter