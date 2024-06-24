import logging
import os
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import (
    IntegrityError,
    transaction,
)
from django.urls import reverse_lazy
from django.utils.html import escape
from pyexpat import ExpatError
from xmlschema import XMLSchemaException

from .forms import *
from .metadata_builder.metadata_structures import *
from .metadata_builder.utils import *

from common import models
from metadata_editor.services import *
from metadata_editor.views import *
from validation.file_wrappers import XMLMetadataFile
from validation.services import MetadataFileXSDValidator


logger = logging.getLogger(__name__)


# Create your views here.

class ResourceRegisterWithEditorFormView(ResourceEditorFormView):
    def process_form(self, form_cleaned_data):
        # Make copy of cleaned data
        processed_form = super().process_form(form_cleaned_data)
        processed_form['localid'] = f'{self.model.localid_base}_{processed_form["localid"]}'
        processed_form['namespace'] = processed_form['namespace']
        return processed_form

    def register_xml_file(self, request, xml_file, name):
        new_registration = self.model.objects.create_from_xml_string(
            xml_file.read(),
            self.institution_id,
            self.owner_id,
        )
        messages.success(request, f'Successfully registered {escape(name)}.')
        self.success_url += '?reset=true'
        return new_registration

    def run_registration_actions(self, request, xml_file, name):
        return self.register_xml_file(request, xml_file, name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'New {self.model.type_readable.title()}'
        context['localid_validation_url'] = reverse_lazy('validation:new_localid')
        return context

    def form_valid(self, form):
        try:
            processed_form = self.process_form(form.cleaned_data)
            metadata_editor = self.metadata_editor_class()
            metadata_editor.add_properties_to_xml_document(processed_form)
            xml = metadata_editor.xml
            localid = processed_form['localid']
            name = processed_form['name']
            xml_file = SimpleUploadedFile(f'{localid}.xml', xml.encode('utf-8'))
        except BaseException as err:
            logger.exception('An unexpected error occurred during XML generation.')
            messages.error(self.request, 'An unexpected error occurred during XML generation.')
            return self.render_to_response(self.get_context_data(form=form))

        try:
            MetadataFileXSDValidator.validate(XMLMetadataFile.from_file(xml_file))
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
            return self.render_to_response(self.get_context_data(form=form))
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
            return self.render_to_response(self.get_context_data(form=form))
        
        try:
            xml_file.seek(0)
            self.run_registration_actions(self.request, xml_file, name)
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
    success_url = reverse_lazy('register:organisation_with_editor')
    file_upload_registration_url = reverse_lazy('register:organisation')
    save_data_local_storage_key = 'organisation_r_wizard_save_data'

    def get_organisation_choices_for_form(self):
        return []

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        processed_form['namespace'] = 'pithia'
        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'namespace': 'pithia'}
        return kwargs

class IndividualRegisterWithEditorFormView(
    IndividualEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:individual_with_editor')
    file_upload_registration_url = reverse_lazy('register:individual')
    save_data_local_storage_key = 'individual_r_wizard_save_data'

class ProjectRegisterWithEditorFormView(
    ProjectEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:project_with_editor')
    file_upload_registration_url = reverse_lazy('register:project')
    save_data_local_storage_key = 'project_r_wizard_save_data'

class PlatformRegisterWithEditorFormView(
    PlatformEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:platform_with_editor')
    file_upload_registration_url = reverse_lazy('register:platform')
    save_data_local_storage_key = 'platform_r_wizard_save_data'


class OperationRegisterWithEditorFormView(
    OperationEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:operation_with_editor')
    file_upload_registration_url = reverse_lazy('register:operation')
    save_data_local_storage_key = 'operation_r_wizard_save_data'


class InstrumentRegisterWithEditorFormView(
    InstrumentEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:instrument_with_editor')
    file_upload_registration_url = reverse_lazy('register:instrument')
    save_data_local_storage_key = 'instrument_r_wizard_save_data'


class AcquisitionCapabilitiesRegisterWithEditorFormView(
    AcquisitionCapabilitiesEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:acquisition_capability_set_with_editor')
    file_upload_registration_url = reverse_lazy('register:acquisition_capability_set')
    save_data_local_storage_key = 'acquisition_capabilities_r_wizard_save_data'


class AcquisitionRegisterWithEditorFormView(
    AcquisitionEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:acquisition_with_editor')
    file_upload_registration_url = reverse_lazy('register:acquisition')
    save_data_local_storage_key = 'acquisition_r_wizard_save_data'


class ComputationCapabilitiesRegisterWithEditorFormView(
    ComputationCapabilitiesEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:computation_capability_set_with_editor')
    file_upload_registration_url = reverse_lazy('register:computation_capability_set')
    save_data_local_storage_key = 'computation_capabilities_r_wizard_save_data'


class ComputationRegisterWithEditorFormView(
    ComputationEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:computation_with_editor')
    file_upload_registration_url = reverse_lazy('register:computation')
    save_data_local_storage_key = 'computation_r_wizard_save_data'


class ProcessRegisterWithEditorFormView(
    ProcessEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:process_with_editor')
    file_upload_registration_url = reverse_lazy('register:process')
    save_data_local_storage_key = 'process_r_wizard_save_data'


class DataCollectionRegisterWithEditorFormView(
    DataCollectionEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:data_collection_with_editor')
    file_upload_registration_url = reverse_lazy('register:data_collection')
    save_data_local_storage_key = 'data_collection_r_wizard_save_data'

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
    
    def run_registration_actions(self, request, xml_file, name):
        new_registration = self.register_xml_file(request, xml_file, name)
        self.register_api_interaction_method(request, new_registration)
        return new_registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context


class WorkflowRegisterWithEditorFormView(
    WorkflowEditorFormView,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:workflow_with_editor')
    file_upload_registration_url = reverse_lazy('register:workflow')
    save_data_local_storage_key = 'workflow_r_wizard_save_data'

    def register_workflow_api_interaction_method(self, request, new_registration):
        api_specification_url = request.POST.get('api_specification_url', None)
        api_description = request.POST.get('api_description', None)
        return models.InteractionMethod.workflow_api_interaction_methods.create_api_interaction_method(
            api_specification_url,
            api_description,
            new_registration
        )

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_registration_actions(self, request, xml_file, name):
        new_registration = self.register_xml_file(request, xml_file, name)
        self.register_workflow_api_interaction_method(request, new_registration)
        return new_registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context
