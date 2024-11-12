import os
from datetime import datetime
from datetime import timezone
from dateutil.parser import parse
from django.db import transaction
from django.shortcuts import render
from pyexpat import ExpatError

from .form_to_metadata_mappers import (
    AcquisitionCapabilitiesFormFieldsToMetadataMapper,
    AcquisitionFormFieldsToMetadataMapper,
    CatalogueEntryFormFieldsToMetadataMapper,
    CatalogueFormFieldsToMetadataMapper,
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
from .forms import WorkflowEditorUpdateForm

from common import models
from datahub_management.services import WorkflowDataHubService
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

    def run_extra_actions_before_update(self):
        pass

    def update_resource(self):
        return self.model.objects.update_from_xml_string(
            self.resource_id,
            self.xml_string,
            self.owner_id
        )

    def form_valid(self, form):
        try:
            metadata_editor = self.metadata_editor_class(xml_string=self.resource.xml)
            self.add_form_data_to_metadata_editor(metadata_editor, form.cleaned_data)
            self.xml_string = metadata_editor.to_xml()
            self.run_extra_actions_before_update()
            updated_resource = self.update_resource()

            messages.success(self.request, f'Successfully updated {escape(updated_resource.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
            self.success_url += '?reset=true'
        except ExpatError as err:
            logger.exception('Could not update a resource as there was an error parsing the update XML.')
            messages.error(self.request, 'An error occurred whilst parsing the XML.')
        except Exception as err:
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


class CatalogueUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    CatalogueEditorFormView):
    model = models.Catalogue
    success_url_name = 'update:catalogue_with_editor'
    form_field_to_metadata_mapper_class = CatalogueFormFieldsToMetadataMapper


class CatalogueEntryUpdateWithEditorFormView(
    ResourceUpdateWithEditorFormView,
    CatalogueEntryEditorFormView):
    model = models.CatalogueEntry
    success_url_name = 'update:catalogue_entry_with_editor'
    form_field_to_metadata_mapper_class = CatalogueEntryFormFieldsToMetadataMapper

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'time_instant_begin_position': parse(initial.get('time_instant_begin_position', '')).replace(second=0, microsecond=0).isoformat().replace('+00:00', ''),
            'time_instant_end_position': parse(initial.get('time_instant_end_position', '')).replace(second=0, microsecond=0).isoformat().replace('+00:00', ''),
        })
        return initial


class WorkflowUpdateWithEditorFormView(
        ResourceUpdateWithEditorFormView,
        WorkflowEditorFormView):
    model = models.Workflow
    success_url_name = 'update:workflow_with_editor'
    form_class = WorkflowEditorUpdateForm
    form_field_to_metadata_mapper_class = WorkflowFormFieldsToMetadataMapper

    def run_extra_actions_before_update(self):
        super().run_extra_actions_before_update()
        if not hasattr(self, 'workflow_details_file'):
            return
        self.xml_string = self.store_workflow_details_file_and_update_xml_file_string(self.xml_string)

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def update_resource(self):
        updated_resource = super().update_resource()
        if not self.workflow_details_file_source == 'external':
            return updated_resource
        self.delete_workflow_details_file()
        return updated_resource

    def form_valid(self, form):
        self.workflow_details_file_source = form.cleaned_data.get('workflow_details_file_source')
        if self.workflow_details_file_source == 'file_upload':
            self.workflow_details_file = self.request.FILES['workflow_details_file']
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workflow_details_file_source_existing_choice_index = self.get_index_of_workflow_details_file_source_choice('existing')
        context['workflow_details_file_source_existing_choice_index'] = workflow_details_file_source_existing_choice_index
        context['disabled_workflow_details_file_source_choice_indexes'] = []
        if not self.stored_workflow_details_file:
            context['disabled_workflow_details_file_source_choice_indexes'].append(
                workflow_details_file_source_existing_choice_index
            )
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'workflow_details_file_source': 'external',
        })
        self.stored_workflow_details_file = WorkflowDataHubService.get_workflow_details_file(self.resource_id)
        if not self.stored_workflow_details_file:
            return initial
        initial.update({
            'workflow_details_file_source': 'existing',
        })
        return initial