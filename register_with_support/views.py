import logging
import os
from datetime import datetime
from datetime import timezone
from django.contrib import messages
from django.db import (
    IntegrityError,
    transaction,
)
from django.urls import reverse_lazy
from django.utils.html import escape
from pyexpat import ExpatError

from .forms import *
from .metadata_builder.metadata_structures import *
from .metadata_builder.utils import *

from common import models
from metadata_editor.editor_dataclasses import PithiaIdentifierMetadataUpdate
from metadata_editor.views import *
from validation.view_mixins import WorkflowDetailsUrlValidationViewMixin


logger = logging.getLogger(__name__)


# Create your views here.
class ResourceRegisterWithEditorFormView(ResourceEditorFormView):
    submit_button_text = 'Validate and Register'
    editor_registration_setup_script_path = 'register_with_support/editor_registration_setup.js'

    def get_namespaces_by_organisation(self):
        return {o.metadata_server_url: clean_localid_or_namespace(o.short_name) for o in models.Organisation.objects.all()}

    def register_xml_string(self, xml_string):
        new_registration = self.model.objects.create_from_xml_string(
            xml_string,
            self.institution_id,
            self.owner_id,
        )
        self.success_url += '?reset=true'
        return new_registration

    def run_registration_actions(self, request, xml_string):
        return self.register_xml_string(xml_string)

    def add_form_data_to_metadata_editor(self, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        namespace = self.namespace if hasattr(self, 'namespace') else form_cleaned_data.get('namespace')
        last_modification_date = datetime.now(timezone.utc).replace(second=0, microsecond=0).isoformat().replace('+00:00', 'Z')
        pithia_identifier_update = PithiaIdentifierMetadataUpdate(
            localid=f'{self.model.localid_base}_{form_cleaned_data.get("localid")}',
            namespace=namespace,
            version=form_cleaned_data.get('identifier_version'),
            creation_date=last_modification_date,
            last_modification_date=last_modification_date
        )
        metadata_editor.update_pithia_identifier(pithia_identifier_update)

    def process_form(self, form_cleaned_data):
        # Make copy of cleaned data
        processed_form = form_cleaned_data
        processed_form['localid'] = f'{self.model.localid_base}_{processed_form["localid"]}'
        processed_form['namespace'] = processed_form['namespace']
        return processed_form

    def convert_form_to_validated_xml(self, form):
        result = {}

        try:
            metadata_editor = self.metadata_editor_class()
            self.add_form_data_to_metadata_editor(metadata_editor, form.cleaned_data)
            xml_string = metadata_editor.to_xml()
            result['xml_string'] = xml_string
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(self.request, 'An error occurred whilst parsing the XML.')
            result['error'] = err
            return result
        except BaseException as err:
            logger.exception('An unexpected error occurred during XML generation.')
            messages.error(self.request, 'An unexpected error occurred during XML generation.')
            result['error'] = err

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'New {self.model.type_readable.title()}'
        context['localid_base'] = self.model.localid_base
        context['localid_validation_url'] = reverse_lazy('validation:new_localid')
        context['namespaces_by_organisation'] = self.get_namespaces_by_organisation()
        context['editor_registration_setup_script_path'] = self.editor_registration_setup_script_path
        return context

    def form_valid(self, form):
        xml_result = self.convert_form_to_validated_xml(form)
        if 'error' in xml_result:
            return self.render_to_response(self.get_context_data(form=form))

        try:
            xml_string = xml_result['xml_string']
            registration_name = form.cleaned_data.get('name', '')
            self.run_registration_actions(self.request, xml_string)
            messages.success(self.request, f'Successfully registered {escape(registration_name)}.')
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(self.request, f'There was a problem during XML generation. Please report this error to our support team.')
            return self.render_to_response(self.get_context_data(form=form))
        except IntegrityError as err:
            logger.exception('The local ID submitted is already in use.')
            messages.error(self.request, 'The local ID submitted is already in use.')
            return self.render_to_response(self.get_context_data(form=form))
        except BaseException as err:
            logger.exception('An unexpected error occurred during registration.')
            messages.error(self.request, 'An unexpected error occurred during registration.')
            return self.render_to_response(self.get_context_data(form=form))
        
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        return kwargs


class OrganisationRegisterWithEditorFormView(
    OrganisationEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = OrganisationEditorRegistrationForm
    success_url = reverse_lazy('register:organisation_with_editor')

    file_upload_registration_url = reverse_lazy('register:organisation')
    save_data_local_storage_key = 'organisation_r_wizard_save_data'
    namespace = 'pithia'
    editor_registration_setup_script_path = 'register_with_support/organisation_editor_registration_setup.js'

    def get_organisation_choices_for_form(self):
        return []

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'namespace': 'pithia'}
        return kwargs


class IndividualRegisterWithEditorFormView(
    IndividualEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = IndividualEditorRegistrationForm
    success_url = reverse_lazy('register:individual_with_editor')

    file_upload_registration_url = reverse_lazy('register:individual')
    save_data_local_storage_key = 'individual_r_wizard_save_data'


class ProjectRegisterWithEditorFormView(
    ProjectEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = ProjectEditorRegistrationForm
    success_url = reverse_lazy('register:project_with_editor')

    file_upload_registration_url = reverse_lazy('register:project')
    save_data_local_storage_key = 'project_r_wizard_save_data'
    new = True


class PlatformRegisterWithEditorFormView(
    PlatformEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = PlatformEditorRegistrationForm
    success_url = reverse_lazy('register:platform_with_editor')

    file_upload_registration_url = reverse_lazy('register:platform')
    save_data_local_storage_key = 'platform_r_wizard_save_data'


class OperationRegisterWithEditorFormView(
    OperationEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = OperationEditorRegistrationForm
    success_url = reverse_lazy('register:operation_with_editor')

    file_upload_registration_url = reverse_lazy('register:operation')
    save_data_local_storage_key = 'operation_r_wizard_save_data'


class InstrumentRegisterWithEditorFormView(
    InstrumentEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = InstrumentEditorRegistrationForm
    success_url = reverse_lazy('register:instrument_with_editor')

    file_upload_registration_url = reverse_lazy('register:instrument')
    save_data_local_storage_key = 'instrument_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['operational_modes'] = process_operational_modes(form_cleaned_data)

        return processed_form


class AcquisitionCapabilitiesRegisterWithEditorFormView(
    AcquisitionCapabilitiesEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = AcquisitionCapabilitiesEditorRegistrationForm
    success_url = reverse_lazy('register:acquisition_capability_set_with_editor')

    file_upload_registration_url = reverse_lazy('register:acquisition_capability_set')
    save_data_local_storage_key = 'acquisition_capabilities_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['capabilities'] = process_capabilities(form_cleaned_data)
        processed_form['instrument_mode_pair'] = process_instrument_mode_pair(form_cleaned_data)
        processed_form['quality_assessment'] = process_quality_assessment(form_cleaned_data)

        return processed_form


class AcquisitionRegisterWithEditorFormView(
    AcquisitionEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = AcquisitionEditorRegistrationForm
    success_url = reverse_lazy('register:acquisition_with_editor')

    file_upload_registration_url = reverse_lazy('register:acquisition')
    save_data_local_storage_key = 'acquisition_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        processed_form['capability_links'] = process_acquisition_capability_links(form_cleaned_data)
        return processed_form


class ComputationCapabilitiesRegisterWithEditorFormView(
    ComputationCapabilitiesEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = ComputationCapabilitiesEditorRegistrationForm
    success_url = reverse_lazy('register:computation_capability_set_with_editor')

    file_upload_registration_url = reverse_lazy('register:computation_capability_set')
    save_data_local_storage_key = 'computation_capabilities_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        
        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['capabilities'] = process_capabilities(form_cleaned_data)
        processed_form['quality_assessment'] = process_quality_assessment(form_cleaned_data)
        processed_form['processing_inputs'] = process_processing_inputs(form_cleaned_data)
        processed_form['software_reference'] = process_software_reference(form_cleaned_data)
        
        return processed_form


class ComputationRegisterWithEditorFormView(
    ComputationEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = ComputationEditorRegistrationForm
    success_url = reverse_lazy('register:computation_with_editor')

    file_upload_registration_url = reverse_lazy('register:computation')
    save_data_local_storage_key = 'computation_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['capability_links'] = process_computation_capability_links(form_cleaned_data)

        return processed_form


class ProcessRegisterWithEditorFormView(
    ProcessEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = ProcessEditorRegistrationForm
    success_url = reverse_lazy('register:process_with_editor')

    file_upload_registration_url = reverse_lazy('register:process')
    save_data_local_storage_key = 'process_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        
        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['capabilities'] = process_capabilities(form_cleaned_data)
        processed_form['quality_assessment'] = process_quality_assessment(form_cleaned_data)

        return processed_form


class DataCollectionRegisterWithEditorFormView(
    DataCollectionEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = DataCollectionEditorRegistrationForm
    success_url = reverse_lazy('register:data_collection_with_editor')

    file_upload_registration_url = reverse_lazy('register:data_collection')
    save_data_local_storage_key = 'data_collection_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['quality_assessment'] = process_quality_assessment(form_cleaned_data)
        processed_form['collection_results'] = process_sources(form_cleaned_data)

        return processed_form

    def register_api_interaction_method(self, request, new_registration):
        try:
            api_specification_url = request.POST.get('api_specification_url', None)
            api_description = request.POST.get('api_description', '')
            if not api_specification_url:
                return
            models.InteractionMethod.api_interaction_methods.create_api_interaction_method(
                api_specification_url,
                api_description,
                new_registration
            )
            messages.success(request, f'<p>Added an API interaction method for {escape(new_registration.name)}.</p><p class="mb-0">It can be viewed and/or updated from the <a href="{reverse_lazy("update:data_collection_interaction_methods", kwargs={"resource_id": new_registration.pk})}">interaction methods page</a> for this data collection.</p>')
        except BaseException as err:
            logger.exception('An unexpected error occurred during API interaction method registration.')
            messages.error(request, 'An unexpected error occurred during API interaction method registration.')
    
    def run_registration_actions(self, request, xml_string):
        new_registration = self.register_xml_string(xml_string)
        self.register_api_interaction_method(request, new_registration)
        return new_registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context


class CatalogueRegisterWithEditorFormView(
    CatalogueEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = CatalogueEditorRegistrationForm
    success_url = reverse_lazy('register:catalogue_with_editor')

    file_upload_registration_url = reverse_lazy('register:catalogue')
    save_data_local_storage_key = 'catalogue_r_wizard_save_data'


class CatalogueEntryRegisterWithEditorFormView(
    CatalogueEntryEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = CatalogueEntryEditorRegistrationForm
    success_url = reverse_lazy('register:catalogue_entry_with_editor')

    file_upload_registration_url = reverse_lazy('register:catalogue_entry')
    save_data_local_storage_key = 'catalogue_entry_r_wizard_save_data'


class CatalogueDataSubsetRegisterWithEditorFormView(
    CatalogueDataSubsetEditorFormView,
    ResourceRegisterWithEditorFormView):
    form_class = CatalogueDataSubsetEditorRegistrationForm
    success_url = reverse_lazy('register:catalogue_data_subset_with_editor')

    file_upload_registration_url = reverse_lazy('register:catalogue_data_subset')
    save_data_local_storage_key = 'catalogue_data_subset_r_wizard_save_data'


class WorkflowRegisterWithEditorFormView(
        WorkflowDetailsUrlValidationViewMixin,
        WorkflowEditorFormView,
        ResourceRegisterWithEditorFormView):
    form_class = WorkflowEditorRegistrationForm
    success_url = reverse_lazy('register:workflow_with_editor')

    file_upload_registration_url = reverse_lazy('register:workflow')
    save_data_local_storage_key = 'workflow_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        processed_form['data_collections'] = process_workflow_data_collections(form_cleaned_data)
        return processed_form

    def register_workflow_api_interaction_method(self, request, new_registration):
        api_specification_url = request.POST.get('api_specification_url', None)
        api_description = request.POST.get('api_description', None)
        return models.InteractionMethod.workflow_api_interaction_methods.create_api_interaction_method(
            api_specification_url,
            api_description,
            new_registration
        )

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_registration_actions(self, request, xml_string):
        if hasattr(self, 'workflow_details_file'):
            xml_string = self.store_workflow_details_file_and_update_xml_file_string(xml_string)
        new_registration = self.register_xml_string(xml_string)
        self.register_workflow_api_interaction_method(request, new_registration)
        return new_registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context

    def form_valid(self, form):
        self.workflow_details_file_source = form.cleaned_data.get('workflow_details_file_source')
        if self.workflow_details_file_source == 'file_upload':
            self.workflow_details_file = self.request.FILES['workflow_details_file']
        if not self.workflow_details_file_source == 'external':
            return super().form_valid(form)
        workflow_details_file_url = form.cleaned_data.get('workflow_details')
        workflow_details_url_error = self.check_workflow_details_url(workflow_details_file_url)
        if workflow_details_url_error:
            messages.error(self.request, workflow_details_url_error)
            form.add_error('workflow_details', workflow_details_url_error)
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'workflow_details_file_source': 'file_upload'
        }
        return kwargs
