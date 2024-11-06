import logging
import os
from django.contrib import messages
from django.db import (
    IntegrityError,
    transaction,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import FormView
from pyexpat import ExpatError

from .forms import *

from common import models
from common.decorators import login_session_institution_required
from handle_management.view_mixins import HandleRegistrationViewMixin
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title
)
from user_management.services import (
    get_user_id_for_login_session,
    get_institution_id_for_login_session,
)


logger = logging.getLogger(__name__)


# Create your views here.

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceRegisterFormView(FormView):
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    new_registration = None
    xml_file_string = None
    validation_url = ''
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

    def run_registration_actions_safely(self, request, xml_file):
        # XML should have already been validated at
        # the template, and validation could take
        # place again, but takes a long time. Another
        # method which verifies validation took place
        # should be implemented.
        try:
            self.new_registration = self.run_registration_actions(request, xml_file)

            messages.success(request, f'Successfully registered {escape(xml_file.name)}.')
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(request, f'An error occurred whilst parsing {escape(xml_file.name)}.')
        except IntegrityError as err:
            logger.exception('The XML file submitted for registration has been registered before.')
            messages.error(request, f'{escape(xml_file.name)} has been registered before.')
        except BaseException as err:
            logger.exception('An unexpected error occurred during metadata registration.')
            messages.error(request, 'An unexpected error occurred during metadata registration.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.model.type_readable.title()} Metadata Files'
        context['data_collection_related_index_page_title'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_type_plural_readable'] = self.model.type_plural_readable.title()
        context['validation_url'] = self.validation_url
        context['expected_root_element_name'] = self.model.root_element_name
        context['inline_validation_url'] = reverse_lazy('validation:new_registration')
        context['inline_xsd_validation_url'] = reverse_lazy('validation:xsd')
        context['post_url'] = self.post_url
        context['form'] = self.form_class
        context['support_url'] = f'{reverse_lazy("support")}#support-heading'
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        xml_files = request.FILES.getlist('files')
        if form.is_valid():
            for xml_file in xml_files:
                self.run_registration_actions_safely(request, xml_file)
        else:
            messages.error(request, 'The form submitted was not valid.')
        return super().post(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)


class OrganisationRegisterFormView(ResourceRegisterFormView):
    model = models.Organisation
    success_url = reverse_lazy('register:organisation')

    validation_url = reverse_lazy('validation:organisation')
    post_url = reverse_lazy('register:organisation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')


class IndividualRegisterFormView(ResourceRegisterFormView):
    model = models.Individual
    success_url = reverse_lazy('register:individual')

    validation_url = reverse_lazy('validation:individual')
    post_url = reverse_lazy('register:individual')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')


class ProjectRegisterFormView(ResourceRegisterFormView):
    model = models.Project
    success_url = reverse_lazy('register:project')

    validation_url = reverse_lazy('validation:project')
    post_url = reverse_lazy('register:project')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('projects')


class PlatformRegisterFormView(ResourceRegisterFormView):
    model = models.Platform
    success_url = reverse_lazy('register:platform')

    validation_url = reverse_lazy('validation:platform')
    post_url = reverse_lazy('register:platform')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('platforms')


class OperationRegisterFormView(ResourceRegisterFormView):
    model = models.Operation
    success_url = reverse_lazy('register:operation')

    validation_url = reverse_lazy('validation:operation')
    post_url = reverse_lazy('register:operation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('operations')


class InstrumentRegisterFormView(ResourceRegisterFormView):
    model = models.Instrument
    success_url = reverse_lazy('register:instrument')

    validation_url = reverse_lazy('validation:instrument')
    post_url = reverse_lazy('register:instrument')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('instruments')


class AcquisitionCapabilitiesRegisterFormView(ResourceRegisterFormView):
    model = models.AcquisitionCapabilities
    success_url = reverse_lazy('register:acquisition_capability_set')

    validation_url = reverse_lazy('validation:acquisition_capability_set')
    post_url = reverse_lazy('register:acquisition_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisition capabilities')


class AcquisitionRegisterFormView(ResourceRegisterFormView):
    model = models.Acquisition
    success_url = reverse_lazy('register:acquisition')

    validation_url = reverse_lazy('validation:acquisition')
    post_url = reverse_lazy('register:acquisition')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisitions')


class ComputationCapabilitiesRegisterFormView(ResourceRegisterFormView):
    model = models.ComputationCapabilities
    success_url = reverse_lazy('register:computation_capability_set')

    validation_url = reverse_lazy('validation:computation_capability_set')
    post_url = reverse_lazy('register:computation_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computation capabilities')


class ComputationRegisterFormView(ResourceRegisterFormView):
    model = models.Computation
    success_url = reverse_lazy('register:computation')

    validation_url = reverse_lazy('validation:computation')
    post_url = reverse_lazy('register:computation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computations')


class ProcessRegisterFormView(ResourceRegisterFormView):
    model = models.Process
    success_url = reverse_lazy('register:process')

    validation_url = reverse_lazy('validation:process')
    post_url = reverse_lazy('register:process')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('processes')


class DataCollectionRegisterFormView(ResourceRegisterFormView):
    model = models.DataCollection
    success_url = reverse_lazy('register:data_collection')

    template_name = 'register/file_upload_data_collection.html'
    form_class = UploadDataCollectionFileForm

    validation_url = reverse_lazy('validation:data_collection')
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

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadDataCollectionFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['files']
            self.run_registration_actions_safely(request, xml_file)
            if self.new_registration is None:
                return redirect(self.success_url)
            self.register_api_interaction_method(request)
        else:
            messages.error(request, 'The form submitted was not valid.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register a {self.model.type_readable.title()} Metadata File'
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context


class CatalogueRegisterFormView(ResourceRegisterFormView):
    template_name = 'register/file_upload.html'
    model = models.Catalogue
    success_url = reverse_lazy('register:catalogue')

    validation_url = reverse_lazy('validation:catalogue')
    post_url = reverse_lazy('register:catalogue')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogues')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class CatalogueEntryRegisterFormView(ResourceRegisterFormView):
    template_name = 'register/file_upload.html'
    model = models.CatalogueEntry
    success_url = reverse_lazy('register:catalogue_entry')

    validation_url = reverse_lazy('validation:catalogue_entry')
    post_url = reverse_lazy('register:catalogue_entry')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogue entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class CatalogueDataSubsetRegisterFormView(HandleRegistrationViewMixin, ResourceRegisterFormView):
    template_name='register/file_upload_catalogue_data_subset.html'
    model = models.CatalogueDataSubset
    success_url = reverse_lazy('register:catalogue_data_subset')

    form_class = UploadCatalogueDataSubsetFileForm

    validation_url = reverse_lazy('validation:catalogue_data_subset')
    post_url = reverse_lazy('register:catalogue_data_subset')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogue data subsets')

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadCatalogueDataSubsetFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['files']
            self.run_registration_actions_safely(request, xml_file)
            self.register_doi_if_requested(request, self.new_registration, xml_file)
        else:
            messages.error(request, 'The form submitted was not valid.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register a {self.model.type_readable.title()} Metadata File'
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class WorkflowRegisterFormView(ResourceRegisterFormView):
    template_name = 'register/file_upload_workflow.html'
    model = models.Workflow
    success_url = reverse_lazy('register:workflow')
    form_class = UploadWorkflowFileForm

    validation_url = reverse_lazy('validation:workflow')
    post_url = reverse_lazy('register:workflow')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('workflows')

    def register_workflow_api_interaction_method(self, request, new_registration):
        api_specification_url = request.POST.get('api_specification_url', None)
        api_description = request.POST.get('api_description', None)
        return models.InteractionMethod.workflow_api_interaction_methods.create_api_interaction_method(
            api_specification_url,
            api_description,
            new_registration
        )

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_registration_actions(self, request, xml_file):
        new_registration = self.register_xml_file(xml_file)
        self.register_workflow_api_interaction_method(request, new_registration)

        return new_registration

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadWorkflowFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['files']
            self.run_registration_actions_safely(request, xml_file)
        else:
            messages.error(request, 'The form submitted was not valid.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register a {self.model.type_readable.title()} Metadata File'
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context