import logging
import os
import tempfile
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import (
    IntegrityError,
    transaction,
)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import FormView
from pyexpat import ExpatError

from .forms import *

from common import models
from common.decorators import login_session_institution_required
from common.xml_metadata_mapping_shortcuts import (
    DataSubsetXmlMappingShortcuts,
    WorkflowXmlMappingShortcuts,
)
from datahub_management.dataclasses import DataSubsetOnlineResource
from datahub_management.view_mixins import (
    DataSubsetDataHubViewMixin,
    WorkflowDataHubViewMixin,
)
from handle_management.view_mixins import HandleRegistrationViewMixin
from resource_management.view_mixins import DataSubsetResourceManagementViewMixin
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title
)
from user_management.services import (
    get_user_id_for_login_session,
    get_institution_id_for_login_session,
)
from validation.file_wrappers import XMLMetadataFile
from validation.view_mixins import WorkflowDetailsUrlValidationViewMixin


logger = logging.getLogger(__name__)


# Create your views here.

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceRegisterFormView(FormView):
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    new_registration = None
    xml_file_string = None
    post_url = ''

    institution_id = None
    owner_id = None

    resource_management_list_page_breadcrumb_text = ''
    resource_management_list_page_breadcrumb_url_name = ''

    def register_xml_file(self, xml_file):
        self.xml_file_string = xml_file.read()
        return self.model.objects.create_from_xml_string(
            self.xml_file_string,
            self.institution_id,
            self.owner_id,
        )
    
    def run_registration_actions(self, request, xml_file):
        return self.register_xml_file(xml_file)

    def run_actions_on_registration_failure(self):
        pass

    def run_registration_actions_safely(self, request, xml_file):
        # XML should have already been validated at
        # the template, and validation could take
        # place again, but takes a long time. Another
        # method which verifies validation took place
        # should be implemented.
        try:
            self.new_registration = self.run_registration_actions(request, xml_file)
            return messages.success(request, f'Successfully registered {escape(xml_file.name)}.')
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(request, f'An error occurred whilst parsing {escape(xml_file.name)}.')
        except IntegrityError as err:
            logger.exception('The XML file submitted for registration has been registered before.')
            messages.error(request, f'{escape(xml_file.name)} has been registered before.')
        except BaseException as err:
            logger.exception('An unexpected error occurred during metadata registration.')
            messages.error(request, 'An unexpected error occurred during metadata registration.')
        self.run_actions_on_registration_failure()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.model.type_plural_readable.title()} via File Upload'
        context['data_collection_related_index_page_title'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_type_plural_readable'] = self.model.type_plural_readable.title()
        context['expected_root_element_name'] = self.model.root_element_name
        context['inline_validation_url'] = reverse_lazy('validation:new_registration')
        context['inline_xsd_validation_url'] = reverse_lazy('validation:xsd')
        context['post_url'] = self.post_url
        if 'form' not in kwargs:
            context['form'] = self.get_form()
        context['support_url'] = f'{reverse_lazy("support")}#support-heading'
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.xml_files = self.request.FILES.getlist('files')
        for xml_file in self.xml_files:
            self.run_registration_actions_safely(self.request, xml_file)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'The form submitted was not valid.')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)


class OrganisationRegisterFormView(ResourceRegisterFormView):
    model = models.Organisation
    success_url = reverse_lazy('register:organisation')

    post_url = reverse_lazy('register:organisation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')


class IndividualRegisterFormView(ResourceRegisterFormView):
    model = models.Individual
    success_url = reverse_lazy('register:individual')

    post_url = reverse_lazy('register:individual')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')


class ProjectRegisterFormView(ResourceRegisterFormView):
    model = models.Project
    success_url = reverse_lazy('register:project')

    post_url = reverse_lazy('register:project')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('projects')


class PlatformRegisterFormView(ResourceRegisterFormView):
    model = models.Platform
    success_url = reverse_lazy('register:platform')

    post_url = reverse_lazy('register:platform')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('platforms')


class OperationRegisterFormView(ResourceRegisterFormView):
    model = models.Operation
    success_url = reverse_lazy('register:operation')

    post_url = reverse_lazy('register:operation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('operations')


class InstrumentRegisterFormView(ResourceRegisterFormView):
    model = models.Instrument
    success_url = reverse_lazy('register:instrument')

    post_url = reverse_lazy('register:instrument')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('instruments')


class AcquisitionCapabilitiesRegisterFormView(ResourceRegisterFormView):
    model = models.AcquisitionCapabilities
    success_url = reverse_lazy('register:acquisition_capability_set')

    post_url = reverse_lazy('register:acquisition_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisition capabilities')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inline_validation_url'] = reverse_lazy('validation:new_acquisition_capabilities_registration')
        return context


class AcquisitionRegisterFormView(ResourceRegisterFormView):
    model = models.Acquisition
    success_url = reverse_lazy('register:acquisition')

    post_url = reverse_lazy('register:acquisition')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisitions')


class ComputationCapabilitiesRegisterFormView(ResourceRegisterFormView):
    model = models.ComputationCapabilities
    success_url = reverse_lazy('register:computation_capability_set')

    post_url = reverse_lazy('register:computation_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computation capabilities')


class ComputationRegisterFormView(ResourceRegisterFormView):
    model = models.Computation
    success_url = reverse_lazy('register:computation')

    post_url = reverse_lazy('register:computation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computations')


class ProcessRegisterFormView(ResourceRegisterFormView):
    model = models.Process
    success_url = reverse_lazy('register:process')

    post_url = reverse_lazy('register:process')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('processes')


class DataCollectionRegisterFormView(ResourceRegisterFormView):
    model = models.DataCollection
    success_url = reverse_lazy('register:data_collection')

    template_name = 'register/file_upload_data_collection.html'
    form_class = UploadDataCollectionFileForm

    post_url = reverse_lazy('register:data_collection')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('data collections')
    
    def register_api_interaction_method(self, request):
        try:
            is_api_selected = 'api_selected' in request.POST
            api_specification_url = request.POST.get('api_specification_url', None)
            api_description = request.POST.get('api_description', '')
            if is_api_selected is False:
                return
            models.InteractionMethod.api_interaction_methods.create_api_interaction_method(
                api_specification_url,
                api_description,
                self.new_registration
            )
            messages.success(request, f'<p>Added an API interaction method for {escape(self.new_registration.name)}.</p><p class="mb-0">It can be viewed and/or updated from the <a href="{reverse_lazy("update:data_collection_interaction_methods", kwargs={"resource_id": self.new_registration.pk})}">interaction methods page</a> for this data collection.</p>')
        except BaseException as err:
            logger.exception('An unexpected error occurred during API interaction method registration.')
            messages.error(request, 'An unexpected error occurred during API interaction method registration.')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.new_registration is None:
            return response
        self.register_api_interaction_method(self.request)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register a {self.model.type_readable.title()} via File Upload'
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context


class StaticDatasetEntryRegisterFormView(ResourceRegisterFormView):
    template_name = 'register/file_upload.html'
    model = models.StaticDatasetEntry
    success_url = reverse_lazy('register:static_dataset_entry')

    post_url = reverse_lazy('register:static_dataset_entry')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:static_dataset_entries'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('static dataset entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:static_dataset_related_metadata_index'
        return context


class DataSubsetRegisterFormView(
        DataSubsetDataHubViewMixin,
        DataSubsetResourceManagementViewMixin,
        HandleRegistrationViewMixin,
        ResourceRegisterFormView):
    template_name='register/file_upload_data_subset.html'
    model = models.DataSubset
    success_url = reverse_lazy('register:data_subset')

    form_class = UploadDataSubsetFileForm

    post_url = reverse_lazy('register:data_subset')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_subsets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('data subsets')

    def register_xml_file(self, xml_file):
        # This method is overridden to use
        # self.xml_string (instead of xml_file.read())
        # as self.xml_string keeps track of
        # whether external URLs or DataHub
        # URLs are used or not.
        return self.model.objects.create_from_xml_string(
            self.xml_string,
            self.institution_id,
            self.owner_id,
        )

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_registration_actions(self, request, xml_file):
        if not self.is_file_uploaded_for_each_online_resource:
            xml_file.seek(0)
            return self.register_xml_file(xml_file)

        with tempfile.TemporaryDirectory() as temp_dirname:
            wrapped_xml_file = XMLMetadataFile.from_file(xml_file)
            self.resource_id = wrapped_xml_file.localid
            self.configure_and_add_source_files_to_temporary_directory(temp_dirname)
            xml_file.seek(0)
            new_registration = self.register_xml_file(xml_file)
            self.copy_temporary_directory_to_datahub(
                temp_dirname,
                self.get_data_subset_datahub_directory_path()
            )
            return new_registration

    def form_valid(self, form):
        # Run before registering the data subset
        self.is_file_uploaded_for_each_online_resource = form.cleaned_data.get('is_file_uploaded_for_each_online_resource')
        self.source_files = self.request.FILES

        try:
            if not self.check_source_names(form):
                messages.error(self.request, self.SIMILAR_SOURCE_NAMES_ERROR)
                return self.form_invalid(form)
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'An unexpected error occurred.')
            return self.form_invalid(form)

        try:
            self.temp_xml_file.seek(0)
            self.xml_string = self.temp_xml_file.read().decode()
            data_subset_shortcutted = DataSubsetXmlMappingShortcuts(self.xml_string)
            self.valid_sources = [
                DataSubsetOnlineResource(
                    name=online_resource.get('name'),
                    file_input_name=f'online_resource_file__{online_resource.get("name")}'
                )
                for online_resource in data_subset_shortcutted.online_resources
            ]
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'An unexpected error occurred during metadata registration.')
            return self.form_invalid(form)

        response = super().form_valid(form)

        # Run after registering the data subset
        xml_file = self.xml_files[0]
        xml_file.seek(0)
        self.register_doi_if_requested(self.request, self.new_registration, xml_file=xml_file)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register a {self.model.type_readable.title()} via File Upload'
        context['resource_management_category_list_page_breadcrumb_text'] = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:static_dataset_related_metadata_index'
        context['source_file_list_item_template'] = render_to_string(
            'register/components/source_file_list_item_template.html',
            context=context
        )
        return context


class WorkflowRegisterFormView(
        ResourceRegisterFormView,
        WorkflowDataHubViewMixin,
        WorkflowDetailsUrlValidationViewMixin):
    template_name = 'register/file_upload_workflow.html'
    model = models.Workflow
    success_url = reverse_lazy('register:workflow')
    form_class = UploadWorkflowFileForm

    post_url = reverse_lazy('register:workflow')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('workflows')

    def store_workflow_details_file_and_update_xml_file(self, xml_file):
        xml_file.seek(0)
        updated_xml_file_string = self.store_workflow_details_file_and_update_xml_file_string(xml_file.read().decode())
        return SimpleUploadedFile(xml_file.name, updated_xml_file_string.encode('utf-8'))

    def register_workflow_api_interaction_method(self, request, new_registration):
        api_specification_url = request.POST.get('api_specification_url', None)
        api_description = request.POST.get('api_description', None)
        return models.InteractionMethod.workflow_api_interaction_methods.create_api_interaction_method(
            api_specification_url,
            api_description,
            new_registration
        )

    def run_actions_on_registration_failure(self):
        if not hasattr(self, 'resource_id'):
            return
        try:
            self.delete_workflow_details_file()
        except FileNotFoundError:
            logger.exception('Workflow details file already deleted.')
        return super().run_actions_on_registration_failure()

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_registration_actions(self, request, xml_file):
        wrapped_xml_file = XMLMetadataFile.from_file(xml_file)
        self.resource_id = wrapped_xml_file.localid
        xml_file.seek(0)
        if not hasattr(self, 'workflow_details_file'):
            new_registration = self.register_xml_file(xml_file)
            self.register_workflow_api_interaction_method(request, new_registration)
            return new_registration
        xml_file_with_details_file_url = self.store_workflow_details_file_and_update_xml_file(xml_file)
        # Register the updated XML
        new_registration = self.register_xml_file(xml_file_with_details_file_url)
        self.register_workflow_api_interaction_method(request, new_registration)
        return new_registration

    def form_valid(self, form):
        if form.cleaned_data['is_workflow_details_file_input_used']:
            self.workflow_details_file = self.request.FILES['workflow_details_file']
            # Skip validating workflow details file in XML
            # as will be overwritten anyway.
            return super().form_valid(form)
        try:
            xml_file = self.request.FILES.getlist('files')[0]
            workflow_xml = WorkflowXmlMappingShortcuts(xml_file.read().decode())
            workflow_details_url_error = self.check_workflow_details_url(workflow_xml.workflow_details_url)
            if workflow_details_url_error:
                messages.error(self.request, workflow_details_url_error)
                return super().form_invalid(form)
            xml_file.seek(0)
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'An unexpected error occurred during registration.')
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register a {self.model.type_readable.title()} via File Upload'
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context