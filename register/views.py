import dateutil.parser
import json
import logging
import os
from django.contrib import messages
from django.db import (
    IntegrityError,
    transaction,
)
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from pyexpat import ExpatError

from .forms import *
from .metadata_builder.metadata_structures import (
    IndividualMetadata,
    OrganisationMetadata,
)
from .metadata_builder.utils import *
from common import models
from common.decorators import login_session_institution_required
from handle_management.handle_api import (
    add_doi_metadata_kernel_to_handle,
    create_and_register_handle_for_resource_url,
    delete_handle,
)
from handle_management.utils import (
    add_handle_to_url_mapping,
)
from handle_management.xml_utils import (
    add_data_subset_data_to_doi_metadata_kernel_dict,
    add_doi_metadata_kernel_to_data_subset,
    add_handle_data_to_doi_metadata_kernel_dict,
    initialise_default_doi_kernel_metadata_dict,
    is_doi_element_present_in_xml_file,
)
from pithiaesc.settings import BASE_DIR
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
from utils.url_helpers import create_data_subset_detail_page_url
from validation.errors import FileRegisteredBefore


logger = logging.getLogger(__name__)


# Create your views here.

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceRegisterWithoutFileFormView(FormView):
    success_url = ''
    form_class = None
    template_name = ''

    model = None
    metadata_builder_class = None
    resource_management_list_page_breadcrumb_url_name = ''
    resource_management_list_page_breadcrumb_text = ''

    institution_id = None
    owner_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['success_url'] = self.success_url
        context['localid_base'] = self.model.localid_base
        context['title'] = f'New {self.model.type_readable.title()}'
        context['organisation_short_names'] = {o.metadata_server_url: o.short_name for o in models.Organisation.objects.all()}
        context['localid_validation_url'] = reverse_lazy('validation:new_localid')
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def process_form(self, form_cleaned_data):
        # Make copy of cleaned data
        processed_form = form_cleaned_data
        processed_form['localid'] = f'{self.model.localid_base}_{processed_form["localid"]}'
        return processed_form
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            processed_form = self.process_form(form.cleaned_data)
            metadata_builder = self.metadata_builder_class(processed_form)
            print('metadata_builder.xml', metadata_builder.xml)
        else:
            messages.error(request, 'The form submitted was not valid.')
        return super().post(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)

class OrganisationRegisterWithoutFileFormView(ResourceRegisterWithoutFileFormView):
    success_url = reverse_lazy('register:organisation_no_file')
    form_class = OrganisationInputSupportForm
    template_name = 'register/metadata_form_templates/organisation_form.html'

    model = models.Organisation
    metadata_builder_class = OrganisationMetadata

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['namespace'] = 'pithia'

        # Hours of service
        hours_of_service = process_hours_of_service_in_form(form_cleaned_data)
        processed_form['hours_of_service'] = hours_of_service
        
        # Contact info
        processed_form['contact_info'] = process_contact_info_in_form(form_cleaned_data)

        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(initial={'namespace': 'pithia'})
        return context

class IndividualRegisterWithoutFileFormView(ResourceRegisterWithoutFileFormView):
    success_url = reverse_lazy('register:individual_no_file')
    form_class = IndividualInputSupportForm
    template_name = 'register/metadata_form_templates/individual_form.html'

    model = models.Individual
    metadata_builder_class = IndividualMetadata

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'


@method_decorator(login_session_institution_required, name='dispatch')
class ResourceRegisterFormView(FormView):
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    resource_id = None
    new_registration = None
    xml_file_string = None
    handle = None
    handle_api_client = None
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

            messages.success(request, f'Successfully registered {xml_file.name}.')
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(request, f'An error occurred whilst parsing {xml_file.name}.')
        except (FileRegisteredBefore, IntegrityError) as err:
            logger.exception('The XML file submitted for registration has been registered before.')
            messages.error(request, f'{xml_file.name} has been registered before.')
        except BaseException as err:
            logger.exception('An unexpected error occurred during metadata registration.')
            messages.error(request, 'An unexpected error occurred during metadata registration.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.model.type_plural_readable.title()}'
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

class CatalogueDataSubsetRegisterFormView(ResourceRegisterFormView):
    template_name='register/file_upload_catalogue_data_subset.html'
    model = models.CatalogueDataSubset
    success_url = reverse_lazy('register:catalogue_data_subset')

    form_class = UploadCatalogueDataSubsetFileForm

    validation_url = reverse_lazy('validation:catalogue_data_subset')
    post_url = reverse_lazy('register:catalogue_data_subset')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogue data subsets')

    def register_doi(self, request, xml_file):
        try:
            # POST RESOURCE REGISTRATION
            # Get the DOI
            # Update the actual "xml_file" variable by adding the DOI to the XML
            # Perform an update on the resource
            # Continue with registration as normal
            if 'register_doi' not in request.POST:
                return
            with transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME']):
                is_doi_in_file_already = is_doi_element_present_in_xml_file(xml_file)
                if is_doi_in_file_already == True:
                    logger.exception('A DOI has already been issued for this metadata file.')
                    messages.error(request, f'A DOI has already been issued for this metadata file.')
                    return
                
                # Create and register a handle
                data_subset_url = create_data_subset_detail_page_url(self.new_registration.pk)
                handle, handle_api_client, credentials = create_and_register_handle_for_resource_url(data_subset_url)
                self.handle_api_client = handle_api_client
                self.handle = handle

                # Create a dict storing DOI metadata kernel information.
                # This information in this dict will be added to the
                # Handle to store data that a DOI would normally handle.
                doi_dict = initialise_default_doi_kernel_metadata_dict()
                # Add the handle metadata to the DOI dict
                doi_dict = add_handle_data_to_doi_metadata_kernel_dict(handle, doi_dict)
                add_data_subset_data_to_doi_metadata_kernel_dict(self.new_registration, doi_dict)

                # Add DOI metadata kernel to Handle and Data Subset
                add_doi_metadata_kernel_to_handle(self.handle, doi_dict, self.handle_api_client)
                add_doi_metadata_kernel_to_data_subset(
                    self.new_registration.pk,
                    doi_dict,
                    self.xml_file_string,
                    self.owner_id
                )
                # Handle to Data Subset URL mapping, to be able to
                # retrieve information from the Handle in case the
                # Data Subset ever gets deleted.
                add_handle_to_url_mapping(handle, data_subset_url)

            messages.success(request, f'A DOI with name "{self.handle}" has been registered for this data subset.')
        except ExpatError as err:
            logger.exception('Expat error occurred during DOI registration process.')
            messages.error(request, f'An error occurred whilst parsing {xml_file.name} during the DOI registration process.')
        except BaseException as err:
            logger.exception('An unexpected error occurred during DOI registration.')
            messages.error(request, 'An unexpected error occurred during DOI registration.')
            if self.handle != None:
                try:
                    delete_handle(self.handle, self.handle_api_client)
                    logger.info(f'Deleted handle {self.handle} due to an error that occurred during DOI registration.')
                except BaseException as err:
                    logger.exception(f'Could not delete handle {self.handle} due to an error.')

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadCatalogueDataSubsetFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['files']
            self.run_registration_actions_safely(request, xml_file)
            self.register_doi(request, xml_file)
        else:
            messages.error(request, 'The form submitted was not valid.')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context