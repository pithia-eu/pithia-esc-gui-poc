import logging
import os
from django.contrib import messages
from django.db import (
    IntegrityError,
    transaction,
)
from django.urls import reverse_lazy
from django.utils.html import escape
from pyexpat import ExpatError
from xmlschema import XMLSchemaException

from .metadata_builder.metadata_structures import *
from .metadata_builder.utils import *

from common import models
from metadata_editor.editor_dataclasses import PithiaIdentifierMetadataUpdate
from metadata_editor.views import *
from validation.file_wrappers import XMLMetadataFile
from validation.services import MetadataFileXSDValidator


logger = logging.getLogger(__name__)


# Create your views here.

class ResourceRegisterWithEditorFormView(ResourceEditorFormView):
    submit_button_text = 'Validate and Register'
    editor_registration_setup_script_path = 'register_with_support/editor_registration_setup.js'

    def process_form(self, form_cleaned_data):
        # Make copy of cleaned data
        processed_form = form_cleaned_data
        processed_form['localid'] = f'{self.model.localid_base}_{processed_form["localid"]}'
        processed_form['namespace'] = processed_form['namespace']
        return processed_form

    def convert_form_to_validated_xml(self, form):
        result = {}
        xml_string = None
        localid = None

        try:
            processed_form = self.process_form(form.cleaned_data)
            metadata_editor = self.metadata_editor_class()
            metadata_editor.add_properties_to_xml_document(processed_form)
            xml_string = metadata_editor.xml
            localid = processed_form['localid']
            result['xml_string'] = xml_string
        except BaseException as err:
            logger.exception('An unexpected error occurred during XML generation.')
            messages.error(self.request, 'An unexpected error occurred during XML generation.')
            result['error'] = err

        try:
            MetadataFileXSDValidator.validate(XMLMetadataFile(xml_string, f'{localid}.xml'))
        except XMLSchemaException as err:
            logger.exception('Generated XML failed schema validation.')
            form_error_msg = f'''
            This form was unable to be processed into schema-valid XML due to an error.
            Please try submitting the form again, or if the issue persists,
            <a href="{reverse_lazy('support')}" target="_blank">let our support team know</a>.
            <br><br>
            If this functionality is down, the <a href="{self.file_upload_registration_url}">file upload functionality</a>
            may alternatively be used to register your metadata.
            <br><br>
            We apologise for any inconvenience caused.
            <details>
                <summary class="mt-4">
                    <small>Validation feedback</small>
                </summary>
                <p class="mt-2 mb-0">
                    <small style="white-space: pre-wrap;">{escape(err).strip()}</small>
                </p>
            </details>
            '''
            messages.error(self.request, form_error_msg)
            result['error'] = err
        except BaseException as err:
            logger.exception('An unexpected error occurred whilst running XSD validation on generated XML.')
            form_error_msg = f'''
            An unexpected error occurred whilst validating the generated XML against the schema.
            Please try submitting the form again, or if the issue persists,
            <a href="{reverse_lazy('support')}" target="_blank">let our support team know</a>.
            <br><br>
            If this functionality is down, the <a href="{self.file_upload_registration_url}">file upload functionality</a>
            may alternatively be used to register your metadata.
            <br><br>
            We apologise for any inconvenience caused.
            '''
            messages.error(self.request, form_error_msg)
            result['error'] = err
        
        return result

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'New {self.model.type_readable.title()}'
        context['localid_validation_url'] = reverse_lazy('validation:new_localid')
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


class NewResourceRegisterWithEditorFormView(ResourceRegisterWithEditorFormView):
    def add_form_data_to_metadata_editor(self, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        namespace = self.namespace if hasattr(self, 'namespace') else form_cleaned_data.get('namespace')
        pithia_identifier_update = PithiaIdentifierMetadataUpdate(
            localid=form_cleaned_data.get('localid'),
            namespace=namespace,
            version=form_cleaned_data.get('identifier_version'),
        )
        pithia_identifier_update.creation_date = pithia_identifier_update.last_modification_date
        metadata_editor.update_pithia_identifier(pithia_identifier_update)

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
        except BaseException as err:
            logger.exception('An unexpected error occurred during XML generation.')
            messages.error(self.request, 'An unexpected error occurred during XML generation.')
            result['error'] = err

        return result


class OrganisationRegisterWithEditorFormView(
    OrganisationEditorFormView,
    NewResourceRegisterWithEditorFormView):
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
    NewResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:individual_with_editor')
    file_upload_registration_url = reverse_lazy('register:individual')
    save_data_local_storage_key = 'individual_r_wizard_save_data'

class ProjectRegisterWithEditorFormView(
    ProjectEditorFormView,
    ResourceRegisterWithEditorFormView):
    metadata_editor_class = ProjectMetadata
    success_url = reverse_lazy('register:project_with_editor')
    file_upload_registration_url = reverse_lazy('register:project')
    save_data_local_storage_key = 'project_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        # processed_form['keyword_dict_list'] = process_project_keywords(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)

        return processed_form

class PlatformRegisterWithEditorFormView(
    PlatformEditorFormView,
    ResourceRegisterWithEditorFormView):
    metadata_editor_class = PlatformMetadata
    success_url = reverse_lazy('register:platform_with_editor')
    file_upload_registration_url = reverse_lazy('register:platform')
    save_data_local_storage_key = 'platform_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['location'] = process_location(form_cleaned_data)
        processed_form['standard_identifiers'] = form_cleaned_data['standard_identifiers_json']

        return processed_form


class OperationRegisterWithEditorFormView(
    OperationEditorFormView,
    ResourceRegisterWithEditorFormView):
    metadata_editor_class = OperationMetadata
    success_url = reverse_lazy('register:operation_with_editor')
    file_upload_registration_url = reverse_lazy('register:operation')
    save_data_local_storage_key = 'operation_r_wizard_save_data'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['location'] = process_location(form_cleaned_data)
        processed_form['operation_time'] = process_operation_time(form_cleaned_data)

        return processed_form


class InstrumentRegisterWithEditorFormView(
    InstrumentEditorFormView,
    ResourceRegisterWithEditorFormView):
    metadata_editor_class = InstrumentMetadata
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
    metadata_editor_class = AcquisitionCapabilitiesMetadata
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
    metadata_editor_class = AcquisitionMetadata
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
    metadata_editor_class = ComputationCapabilitiesMetadata
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
    metadata_editor_class = ComputationMetadata
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
    metadata_editor_class = ProcessMetadata
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
    metadata_editor_class = DataCollectionMetadata
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


class WorkflowRegisterWithEditorFormView(
    WorkflowEditorFormView,
    ResourceRegisterWithEditorFormView):
    metadata_editor_class = WorkflowMetadata
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
        new_registration = self.register_xml_string(xml_string)
        self.register_workflow_api_interaction_method(request, new_registration)
        return new_registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context
