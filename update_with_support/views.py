import os
import tempfile
import shutil
from datetime import datetime
from datetime import timezone
from dateutil.parser import parse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from io import BufferedReader
from pyexpat import ExpatError

from .form_to_metadata_mappers import (
    AcquisitionCapabilitiesFormFieldsToMetadataMapper,
    AcquisitionFormFieldsToMetadataMapper,
    CatalogueDataSubsetFormFieldsToMetadataMapper,
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
from .forms import (
    CatalogueDataSubsetEditorUpdateForm,
    WorkflowEditorUpdateForm,
)

from common import models
from common.xml_metadata_mapping_shortcuts import (
    CatalogueDataSubsetXmlMappingShortcuts,
    WorkflowXmlMappingShortcuts,
)
from datahub_management.dataclasses import CatalogueDataSubsetOnlineResourceUpdate
from datahub_management.services import WorkflowDataHubService
from handle_management.view_mixins import (
    HandleReapplicationViewMixin,
    HandleRegistrationViewMixin,
)
from metadata_editor.editor_dataclasses import (
    CatalogueDataSubsetSourceWithExistingDataHubFileMetadataUpdate,
    PithiaIdentifierMetadataUpdate,
)
from metadata_editor.form_utils import map_catalogue_data_subset_sources_with_existing_data_hub_files_to_dataclasses
from metadata_editor.service_utils import BaseMetadataEditor
from metadata_editor.services import SimpleCatalogueDataSubsetEditor
from metadata_editor.views import *
from validation.view_mixins import WorkflowDetailsUrlValidationViewMixin


# Create your views here.

class ResourceUpdateWithEditorFormView(ResourceEditorFormView):
    model = None
    form_field_to_metadata_mapper_class: EditorFormFieldsToMetadataUtilsMixin = None
    success_url = ''
    success_url_name = ''

    error_msg = 'An unexpected error occurred whilst trying to update this resource. The update has not been applied.'

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
            if not hasattr(self, 'current_resource_xml'):
                self.current_resource_xml = self.resource.xml
            metadata_editor = self.metadata_editor_class(xml_string=self.current_resource_xml)
            self.add_form_data_to_metadata_editor(metadata_editor, form.cleaned_data)
            self.xml_string = metadata_editor.to_xml()
            self.run_extra_actions_before_update()
            self.updated_resource = self.update_resource()

            messages.success(self.request, f'Successfully updated {escape(self.updated_resource.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
            self.success_url += '?reset=true'
        except ExpatError as err:
            logger.exception('Could not update a resource as there was an error parsing the update XML.')
            messages.error(self.request, 'An error occurred whilst parsing the XML.')
        except Exception as err:
            logger.exception(f'An unexpected error occurred whilst attempting to update resource with ID "{escape(self.resource_id)}".')
            messages.error(self.request, self.error_msg)

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


class NewResourceUpdateWithEditorFormView(ResourceUpdateWithEditorFormView):
    def get(self, request, *args, **kwargs):
        if request.GET.get('success'):
            messages.success(request, f'Successfully updated {escape(self.resource.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
        return super().get(request, *args, **kwargs)

    def form_invalid(self, form):
        return HttpResponseBadRequest('The form submitted was not valid. Please check the form for any errors.')

    def form_valid(self, form):
        response = HttpResponse()

        try:
            if not hasattr(self, 'current_resource_xml'):
                self.current_resource_xml = self.resource.xml
            metadata_editor = self.metadata_editor_class(xml_string=self.current_resource_xml)
            self.add_form_data_to_metadata_editor(metadata_editor, form.cleaned_data)
            self.xml_string = metadata_editor.to_xml()
            self.run_extra_actions_before_update()
            self.updated_resource = self.update_resource()

            response.write(f'Successfully updated {escape(self.updated_resource.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
        except ExpatError:
            logger.exception('Could not update a resource as there was an error parsing the update XML.')
            response.write('''An error occurred whilst parsing the XML.
                Please try submitting the form again. If the problem
                persists, please inform our support team of the problem.
            ''')
        except Exception:
            logger.exception(f'An unexpected error occurred whilst attempting to update resource with ID "{escape(self.resource_id)}".')
            response.write(self.error_msg)

        return response


class OrganisationUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    OrganisationEditorFormView):
    model = models.Organisation
    success_url_name = 'update:organisation_with_editor'
    form_field_to_metadata_mapper_class = OrganisationFormFieldsToMetadataMapper

    def get_initial(self):
        initial = super().get_initial()
        self.set_initial_country_if_in_country_choices(initial)
        return initial


class IndividualUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    IndividualEditorFormView):
    model = models.Individual
    success_url_name = 'update:individual_with_editor'
    form_field_to_metadata_mapper_class = IndividualFormFieldsToMetadataMapper

    def get_initial(self):
        initial = super().get_initial()
        self.set_initial_country_if_in_country_choices(initial)
        return initial


class ProjectUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    ProjectEditorFormView):
    model = models.Project
    success_url_name = 'update:project_with_editor'
    form_field_to_metadata_mapper_class = ProjectFormFieldsToMetadataMapper


class PlatformUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    PlatformEditorFormView):
    model = models.Platform
    success_url_name = 'update:platform_with_editor'
    form_field_to_metadata_mapper_class = PlatformFormFieldsToMetadataMapper


class OperationUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    OperationEditorFormView):
    model = models.Operation
    success_url_name = 'update:operation_with_editor'
    form_field_to_metadata_mapper_class = OperationFormFieldsToMetadataMapper


class InstrumentUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    InstrumentEditorFormView):
    model = models.Instrument
    success_url_name = 'update:instrument_with_editor'
    form_field_to_metadata_mapper_class = InstrumentFormFieldsToMetadataWrapper


class AcquisitionCapabilitiesUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    AcquisitionCapabilitiesEditorFormView):
    model = models.AcquisitionCapabilities
    success_url_name = 'update:acquisition_capability_set_with_editor'
    form_field_to_metadata_mapper_class = AcquisitionCapabilitiesFormFieldsToMetadataMapper


class AcquisitionUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    AcquisitionEditorFormView):
    model = models.Acquisition
    success_url_name = 'update:acquisition_with_editor'
    form_field_to_metadata_mapper_class = AcquisitionFormFieldsToMetadataMapper


class ComputationCapabilitiesUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    ComputationCapabilitiesEditorFormView):
    model = models.ComputationCapabilities
    success_url_name = 'update:computation_capability_set_with_editor'
    form_field_to_metadata_mapper_class = ComputationCapabilitiesFormFieldsToMetadataMapper


class ComputationUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    ComputationEditorFormView):
    model = models.Computation
    success_url_name = 'update:computation_with_editor'
    form_field_to_metadata_mapper_class = ComputationFormFieldsToMetadataMapper


class ProcessUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    ProcessEditorFormView):
    model = models.Process
    success_url_name = 'update:process_with_editor'
    form_field_to_metadata_mapper_class = ProcessFormFieldsToMetadataMapper


class DataCollectionUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    DataCollectionEditorFormView):
    model = models.DataCollection
    success_url_name = 'update:data_collection_with_editor'
    form_field_to_metadata_mapper_class = DataCollectionFormFieldsToMetadataMapper


class CatalogueUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
    CatalogueEditorFormView):
    model = models.Catalogue
    success_url_name = 'update:catalogue_with_editor'
    form_field_to_metadata_mapper_class = CatalogueFormFieldsToMetadataMapper


class CatalogueEntryUpdateWithEditorFormView(
    NewResourceUpdateWithEditorFormView,
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


class CatalogueDataSubsetUpdateWithEditorFormView(
        HandleReapplicationViewMixin,
        HandleRegistrationViewMixin,
        NewResourceUpdateWithEditorFormView,
        CatalogueDataSubsetEditorFormView):
    template_name = 'update_with_support/catalogue_data_subset_update_editor.html'
    model = models.CatalogueDataSubset
    success_url_name = 'update:catalogue_data_subset_with_editor'
    
    form_class = CatalogueDataSubsetEditorUpdateForm
    form_field_to_metadata_mapper_class = CatalogueDataSubsetFormFieldsToMetadataMapper

    def get_sources_tab_pane_content_template_path(self):
        return 'update_with_support/components/catalogue_data_subset/sources_tab_pane_content_template.html'

    def _get_file_for_online_resource(self, online_resource: CatalogueDataSubsetOnlineResourceUpdate|CatalogueDataSubsetSourceWithExistingDataHubFileMetadataUpdate):
        if not online_resource.is_existing_datahub_file_used:
            return super()._get_file_for_online_resource(online_resource)
        file_name_with_no_extension, file_extension = os.path.splitext(online_resource.datahub_file_name)
        return self.get_online_resource_file_for_catalogue_data_subset_by_file_name(
            file_name_with_no_extension
        )

    def run_extra_actions_before_update(self):
        if not self.current_doi_name:
            return super().run_extra_actions_before_update()
        simple_catalogue_data_subset_editor = SimpleCatalogueDataSubsetEditor(self.xml_string)
        # Replace temp DOI name used to pass
        # XSD validation with real DOI name.
        simple_catalogue_data_subset_editor.update_referent_doi_name(self.current_doi_name)
        self.xml_string = simple_catalogue_data_subset_editor.to_xml()
        return super().run_extra_actions_before_update()

    def add_source_file_to_temporary_directory(self, source_file: InMemoryUploadedFile|BufferedReader, source_file_write_path: str):
        try:
            return super().add_source_file_to_temporary_directory(
                source_file,
                source_file_write_path
            )
        except AttributeError as err:
            logger.exception(err)
        return shutil.copyfile(source_file.name, source_file_write_path)

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def update_resource(self):
        if not self.is_file_uploaded_for_each_online_resource:
            try:
                self.delete_catalogue_data_subset_directory()
            except FileNotFoundError:
                logger.exception(f'The directory for Catalogue Data Subset {self.resource_id} has already been deleted.')
            return super().update_resource()

        with tempfile.TemporaryDirectory() as temp_dirname:
            self.configure_and_add_source_files_to_temporary_directory(temp_dirname)
            updated_resource = super().update_resource()
            self.copy_temporary_directory_to_datahub(
                temp_dirname,
                self.get_catalogue_data_subset_datahub_directory_path()
            )
        return updated_resource

    def map_sources_to_dataclasses(
            self,
            form_cleaned_data,
            is_file_uploaded_for_each_online_resource):
        return map_catalogue_data_subset_sources_with_existing_data_hub_files_to_dataclasses(
            form_cleaned_data,
            is_file_uploaded_for_each_online_resource=is_file_uploaded_for_each_online_resource
        )

    def form_valid(self, form):
        self.source_files = self.request.FILES
        if not self.check_source_names(form):
            form.add_error('sources_json', self.SIMILAR_SOURCE_NAMES_ERROR)
            return self.form_invalid(form)

        self.current_resource_xml = self.resource.xml
        self.is_file_uploaded_for_each_online_resource = form.cleaned_data.get('is_file_uploaded_for_each_online_resource')
        try:
            xml_shortcuts = CatalogueDataSubsetXmlMappingShortcuts(self.current_resource_xml)
            self.current_doi_name = xml_shortcuts.doi_kernel_metadata.get('referent_doi_name')
            temp_doi_name = '10.000/000'
            simple_catalogue_data_subset_editor = SimpleCatalogueDataSubsetEditor(self.current_resource_xml)
            simple_catalogue_data_subset_editor.update_referent_doi_name(temp_doi_name)
            self.current_resource_xml = simple_catalogue_data_subset_editor.to_xml()
        except Exception as err:
            logger.exception(err)

        response = super().form_valid(form)

        try:
            self.handle_name = self.register_doi_if_requested(self.request, self.resource, xml_file_string=self.xml_string)
            # RE-INSERT PRE-EXISTING DOI KERNEL METADATA
            # Refresh self.resource if a DOI was added
            # so the new DOI kernel metadata is added to
            # the submitted XML file.
            self.resource = self.model.objects.get(pk=self.resource_id)
            self.xml_string = self.reinsert_pre_existing_doi_kernel_metadata_into_updated_xml_file_if_needed(
                self.updated_resource,
                xml_file_string=self.xml_string
            )
        except Exception:
            logger.exception(self.error_msg)
            messages.error(self.request, 'An unexpected error occurred whilst handling the DOI request.')
        return response

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'time_instant_begin_position': parse(initial.get('time_instant_begin_position', '')).replace(second=0, microsecond=0).isoformat().replace('+00:00', ''),
            'time_instant_end_position': parse(initial.get('time_instant_end_position', '')).replace(second=0, microsecond=0).isoformat().replace('+00:00', ''),
        })
        if not self.get_online_resource_files_for_catalogue_data_subset():
            initial.update({
                'is_file_uploaded_for_each_online_resource': False,
            })
        return initial


class WorkflowUpdateWithEditorFormView(
        NewResourceUpdateWithEditorFormView,
        WorkflowDetailsUrlValidationViewMixin,
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
        # User may choose the external details file
        # source by mistake, but still use the eSC
        # details file URL. If this is true, do not
        # delete the details file from DataHub.
        updated_workflow_details_url = WorkflowXmlMappingShortcuts(self.xml_string).workflow_details_url
        if updated_workflow_details_url == self.get_workflow_details_file_url():
            return updated_resource
        try:
            self.delete_workflow_details_file()
        except FileNotFoundError:
            logger.exception('Workflow details file was not found.')
        return updated_resource

    def form_valid(self, form):
        self.workflow_details_file_source = form.cleaned_data.get('workflow_details_file_source')
        if self.workflow_details_file_source == 'file_upload':
            self.workflow_details_file = self.request.FILES['workflow_details_file']

        if not form.cleaned_data.get('workflow_details_file_source') == 'external':
            return super().form_valid(form)

        workflow_details_file_url = form.cleaned_data.get('workflow_details')
        workflow_details_url_error = self.check_workflow_details_url(workflow_details_file_url)
        if workflow_details_url_error:
            messages.error(self.request, workflow_details_url_error)
            form.add_error('workflow_details', workflow_details_url_error)
            return super().form_invalid(form)
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
            'workflow_details': '',
        })
        return initial