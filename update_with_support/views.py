from datetime import datetime
from datetime import timezone
from django.shortcuts import render
from pyexpat import ExpatError

from .form_to_metadata_mappers import (
    AcquisitionCapabilitiesFormFieldsToMetadataMapper,
    AcquisitionFormFieldsToMetadataMapper,
    ComputationCapabilitiesFormFieldsToMetadataMapper,
    ComputationFormFieldsToMetadataMapper,
    DataCollectionFormFieldsToMetadataMapper,
    InstrumentFormFieldsToMetadataWrapper,
    IndividualFormFieldsToMetadataMapper,
    OperationFormFieldsToMetadataMapper,
    OrganisationFormFieldsToMetadataMapper,
    PlatformFormFieldsToMetadataMapper,
    ProcessFormFieldsToMetadataMapper,
    ProjectFormFieldsToMetadataMapper,
    WorkflowFormFieldsToMetadataMapper,
)
from .form_to_metadata_mapper_components import EditorFormFieldsToMetadataUtilsMixin

from common import models
from metadata_editor.editor_dataclasses import PithiaIdentifierMetadataUpdate
from metadata_editor.service_utils import BaseMetadataEditor
from metadata_editor.views import *


# Create your views here.

class ResourceUpdateWithEditorFormView(ResourceEditorFormView):
    model = None
    form_field_to_metadata_mapper_class: EditorFormFieldsToMetadataUtilsMixin = None
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
            self.success_url += '?reset=true'
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
        context['save_data_local_storage_key'] = f'{self.model.type_readable}_u_{escape(self.resource_id).lower()}_wizard_save_data'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs.get('resource_id')
        self.resource = self.model.objects.get(pk=self.resource_id)
        self.success_url = reverse_lazy(self.success_url_name, args=[self.resource_id])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        form_field_to_metadata_mapper = self.form_field_to_metadata_mapper_class(self.resource.xml)
        initial_from_metadata = form_field_to_metadata_mapper.get_initial_form_values()
        initial.update(initial_from_metadata)
        return initial


class OrganisationUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    OrganisationEditorFormView):
    model = models.Organisation
    success_url_name = 'update:organisation_with_editor'
    form_field_to_metadata_mapper_class = OrganisationFormFieldsToMetadataMapper

    def get_initial(self):
        initial = super().get_initial()
        self.set_initial_country_if_in_country_choices(initial)
        return initial


class IndividualUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    IndividualEditorFormView):
    model = models.Individual
    success_url_name = 'update:individual_with_editor'
    form_field_to_metadata_mapper_class = IndividualFormFieldsToMetadataMapper

    def get_initial(self):
        initial = super().get_initial()
        self.set_initial_country_if_in_country_choices(initial)
        return initial


class ProjectUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    ProjectEditorFormView):
    model = models.Project
    success_url_name = 'update:project_with_editor'
    form_field_to_metadata_mapper_class = ProjectFormFieldsToMetadataMapper


class PlatformUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    PlatformEditorFormView):
    model = models.Platform
    success_url_name = 'update:platform_with_editor'
    form_field_to_metadata_mapper_class = PlatformFormFieldsToMetadataMapper


class OperationUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    OperationEditorFormView):
    model = models.Operation
    success_url_name = 'update:operation_with_editor'
    form_field_to_metadata_mapper_class = OperationFormFieldsToMetadataMapper


class InstrumentUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    InstrumentEditorFormView):
    model = models.Instrument
    success_url_name = 'update:instrument_with_editor'
    form_field_to_metadata_mapper_class = InstrumentFormFieldsToMetadataWrapper


class AcquisitionCapabilitiesUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    AcquisitionCapabilitiesEditorFormView):
    model = models.AcquisitionCapabilities
    success_url_name = 'update:acquisition_capability_set_with_editor'
    form_field_to_metadata_mapper_class = AcquisitionCapabilitiesFormFieldsToMetadataMapper


class AcquisitionUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    AcquisitionEditorFormView):
    model = models.Acquisition
    success_url_name = 'update:acquisition_with_editor'
    form_field_to_metadata_mapper_class = AcquisitionFormFieldsToMetadataMapper


class ComputationCapabilitiesUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    ComputationCapabilitiesEditorFormView):
    model = models.ComputationCapabilities
    success_url_name = 'update:computation_capability_set_with_editor'
    form_field_to_metadata_mapper_class = ComputationCapabilitiesFormFieldsToMetadataMapper


class ComputationUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    ComputationEditorFormView):
    model = models.Computation
    success_url_name = 'update:computation_with_editor'
    form_field_to_metadata_mapper_class = ComputationFormFieldsToMetadataMapper


class ProcessUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    ProcessEditorFormView):
    model = models.Process
    success_url_name = 'update:process_with_editor'
    form_field_to_metadata_mapper_class = ProcessFormFieldsToMetadataMapper


class DataCollectionUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    DataCollectionEditorFormView):
    model = models.DataCollection
    success_url_name = 'update:data_collection_with_editor'
    form_field_to_metadata_mapper_class = DataCollectionFormFieldsToMetadataMapper


class WorkflowUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    WorkflowEditorFormView):
    model = models.Workflow
    success_url_name = 'update:workflow_with_editor'
    form_field_to_metadata_mapper_class = WorkflowFormFieldsToMetadataMapper