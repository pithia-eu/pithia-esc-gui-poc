from datetime import datetime
from datetime import timezone
from django.shortcuts import render
from pyexpat import ExpatError

from .xml_metadata_to_form import (
    IndividualXmlMetadataToFormConverter,
    OrganisationXmlMetadataToFormConverter,
)

from common import models
from metadata_editor.editor_dataclasses import PithiaIdentifierMetadataUpdate
from metadata_editor.utils import BaseMetadataEditor
from metadata_editor.views import *


# Create your views here.

class ResourceUpdateWithEditorFormView(ResourceEditorFormView):
    model = None
    xml_metadata_to_form_field_converter: BaseMetadataEditor = None
    success_url = ''
    success_url_name = ''

    submit_button_text = 'Validate and Update'

    def add_form_data_to_metadata_editor(self, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        last_modification_date = datetime.now(timezone.utc).replace(second=0, microsecond=0).isoformat().replace('+00:00', 'Z')
        pithia_identifier_update = PithiaIdentifierMetadataUpdate(
            version=form_cleaned_data.get('identifier_version'),
            last_modification_date=last_modification_date
        )
        metadata_editor.update_pithia_identifier(pithia_identifier_update)

    def form_valid(self, form):
        try:
            metadata_editor = self.metadata_editor_class(xml_string=self.resource.xml)
            self.add_form_data_to_metadata_editor(metadata_editor, form.cleaned_data)
            xml_string = metadata_editor.to_xml()
            resource_id_temp = self.resource_id
            resource = self.model.objects.update_from_xml_string(
                resource_id_temp,
                xml_string,
                self.owner_id
            )

            messages.success(self.request, f'Successfully updated {escape(resource.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
        except ExpatError as err:
            logger.exception('Could not update a resource as there was an error parsing the update XML.')
            messages.error(self.request, 'An error occurred whilst parsing the XML.')
        except BaseException as err:
            logger.exception(f'An unexpected error occurred whilst attempting to update resource with ID "{escape(self.resource_id)}".')
            messages.error(self.request, 'An unexpected error occurred.')

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_url'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs.get('resource_id')
        self.resource = self.model.objects.get(pk=self.resource_id)
        self.success_url = reverse_lazy(self.success_url_name, args=[self.resource_id])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(self.xml_metadata_to_form_field_converter(self.resource.xml).convert())
        return initial

class OrganisationUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    OrganisationEditorFormView):
    model = models.Organisation
    success_url_name = 'update:organisation_with_editor'
    xml_metadata_to_form_field_converter = OrganisationXmlMetadataToFormConverter

class IndividualUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    IndividualEditorFormView):
    model = models.Individual
    success_url_name = 'update:individual_with_editor'
    xml_metadata_to_form_field_converter = IndividualXmlMetadataToFormConverter