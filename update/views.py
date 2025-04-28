import logging
import os
import shutil
import tempfile
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.text import slugify
from django.views.generic.edit import FormView
from io import BufferedReader
from pyexpat import ExpatError

from common import models
from common.decorators import (
    login_session_institution_required,
    institution_ownership_required
)
from common.xml_metadata_mapping_shortcuts import (
    DataSubsetXmlMappingShortcuts,
    WorkflowXmlMappingShortcuts,
)
from datahub_management.dataclasses import DataSubsetOnlineResourceUpdate
from datahub_management.view_mixins import (
    DataSubsetDataHubViewMixin,
    WorkflowDataHubViewMixin,
)
from handle_management.view_mixins import (
    HandleRegistrationViewMixin,
    HandleReapplicationViewMixin,
)
from resource_management.forms import (
    UpdateDataCollectionInteractionMethodsForm,
    UpdateWorkflowOpenAPISpecificationURLForm,
    UploadUpdatedDataSubsetFileForm,
    UploadUpdatedDataCollectionFileForm,
    UploadUpdatedFileForm,
    UploadUpdatedWorkflowFileForm,
)
from resource_management.view_mixins import DataSubsetResourceManagementViewMixin
from resource_management.views import (
    _create_manage_resource_page_title,
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE,
)
from user_management.services import get_user_id_for_login_session
from validation.view_mixins import WorkflowDetailsUrlValidationViewMixin


logger = logging.getLogger(__name__)


# Create your views here.


@method_decorator(login_session_institution_required, name='dispatch')
@method_decorator(institution_ownership_required, name='dispatch')
class ResourceUpdateFormView(FormView):
    # Registration variables
    resource = None
    resource_id = ''

    # Template variables
    resource_update_page_url_name = ''
    # resource_to_update_name = '' # Set in dispatch() function
    resource_management_list_page_breadcrumb_url_name = ''

    # Class variables
    template_name = 'update/file_upload_update.html'
    form_class = UploadUpdatedFileForm
    success_url = ''
    xml_string = None

    def update_resource(self):
        return self.model.objects.update_from_xml_string(
            self.resource_id,
            self.xml_string,
            self.owner_id
        )

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['resource_id']
        self.resource = self.model.objects.get(pk=self.resource_id)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.resource.name}'
        context['title_short'] = 'Update'
        if 'form' not in kwargs:
            context['form'] = self.get_form()
        context['resource'] = self.resource
        context['resource_id'] = self.resource_id
        context['expected_root_element_name'] = self.model.root_element_name
        context['inline_validation_url'] = reverse_lazy('validation:update')
        context['inline_xsd_validation_url'] = reverse_lazy('validation:xsd')
        context['support_url'] = f'{reverse_lazy("support")}#support-heading'
        context['post_url'] = reverse_lazy(self.resource_update_page_url_name, args=[self.resource_id])
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = _create_manage_resource_page_title(self.model.type_plural_readable.title())
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        xml_file = self.request.FILES['files']
        try:
            if self.xml_string is None:
                xml_file.seek(0)
                self.xml_string = xml_file.read()
            self.update_resource()

            messages.success(self.request, f'Successfully updated {escape(xml_file.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
        except ExpatError:
            logger.exception('Could not update a resource as there was an error parsing the update XML.')
            messages.error(self.request, 'An error occurred whilst parsing the XML.')
        except Exception:
            logger.exception(f'An unexpected error occurred whilst attempting to update resource with ID "{escape(self.resource_id)}".')
            messages.error(self.request, 'An unexpected error occurred.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'The form submitted was not valid.')
        return response


class OrganisationUpdateFormView(ResourceUpdateFormView):
    model = models.Organisation

    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    resource_update_page_url_name = 'update:organisation'
    success_url = reverse_lazy('resource_management:organisations')


class IndividualUpdateFormView(ResourceUpdateFormView):
    model = models.Individual

    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_update_page_url_name = 'update:individual'
    success_url = reverse_lazy('resource_management:individuals')


class ProjectUpdateFormView(ResourceUpdateFormView):
    model = models.Project

    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_update_page_url_name = 'update:project'
    success_url = reverse_lazy('resource_management:projects')


class PlatformUpdateFormView(ResourceUpdateFormView):
    model = models.Platform

    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_update_page_url_name = 'update:platform'
    success_url = reverse_lazy('resource_management:platforms')


class OperationUpdateFormView(ResourceUpdateFormView):
    model = models.Operation

    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_update_page_url_name = 'update:operation'
    success_url = reverse_lazy('resource_management:operations')


class InstrumentUpdateFormView(ResourceUpdateFormView):
    template_name = 'update/file_upload_instrument_update.html'
    model = models.Instrument

    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_update_page_url_name = 'update:instrument'
    success_url = reverse_lazy('resource_management:instruments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inline_validation_url'] = reverse_lazy('validation:instrument_update')
        return context


class AcquisitionCapabilitiesUpdateFormView(ResourceUpdateFormView):
    model = models.AcquisitionCapabilities

    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    success_url = reverse_lazy('resource_management:acquisition_capability_sets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inline_validation_url'] = reverse_lazy('validation:acquisition_capabilities_update')
        return context


class AcquisitionUpdateFormView(ResourceUpdateFormView):
    model = models.Acquisition

    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_update_page_url_name = 'update:acquisition'
    success_url = reverse_lazy('resource_management:acquisitions')


class ComputationCapabilitiesUpdateFormView(ResourceUpdateFormView):
    model = models.ComputationCapabilities

    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_update_page_url_name = 'update:computation_capability_set'
    success_url = reverse_lazy('resource_management:computation_capability_sets')


class ComputationUpdateFormView(ResourceUpdateFormView):
    model = models.Computation

    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_update_page_url_name = 'update:computation'
    success_url = reverse_lazy('resource_management:computations')


class ProcessUpdateFormView(ResourceUpdateFormView):
    model = models.Process

    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_update_page_url_name = 'update:process'
    success_url = reverse_lazy('resource_management:processes')


class DataCollectionUpdateFormView(ResourceUpdateFormView):
    model = models.DataCollection
    form_class = UploadUpdatedDataCollectionFileForm

    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    resource_update_page_url_name = 'update:data_collection'
    success_url = reverse_lazy('resource_management:data_collections')


@method_decorator(login_session_institution_required, name='dispatch')
@method_decorator(institution_ownership_required, name='dispatch')
class DataCollectionInteractionMethodsUpdateView(FormView):
    form_class = UpdateDataCollectionInteractionMethodsForm
    template_name = 'update/interaction_methods_update.html'
    success_url_name = 'update:data_collection_interaction_methods'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['resource_id']
        self.success_url = reverse_lazy(self.success_url_name, args=[self.resource_id])
        self.data_collection = get_object_or_404(models.DataCollection, pk=self.resource_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_values = {}
        try:
            api_interaction_method = models.APIInteractionMethod.objects.get(
                scientific_metadata=self.data_collection
            )
            initial_values.update({
                'api_selected': True,
                'api_specification_url': api_interaction_method.specification_url,
                'api_description': api_interaction_method.description,
            })
            form = self.form_class(initial=initial_values)
        except models.APIInteractionMethod.DoesNotExist:
            form = self.form_class()

        context.update({
            'data_collection': self.data_collection,
            'data_collection_id': self.data_collection.pk,
            'form': form,
            'api_specification_validation_url': reverse_lazy('validation:api_specification_url'),
            'title': f'Update Interaction Methods for {self.data_collection.name}',
            'resource_management_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
            'resource_management_category_list_page_breadcrumb_url_name': 'resource_management:data_collection_related_metadata_index',
            'resource_management_category_list_page_breadcrumb_text': _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
            'resource_management_list_page_breadcrumb_url_name': 'resource_management:data_collections',
            'resource_management_list_page_breadcrumb_text': _create_manage_resource_page_title(models.DataCollection.type_plural_readable.title())
        })
        return context


class StaticDatasetEntryUpdateFormView(ResourceUpdateFormView):
    model = models.StaticDatasetEntry

    resource_management_list_page_breadcrumb_url_name = 'resource_management:static_dataset_entries'
    resource_update_page_url_name = 'update:static_dataset_entry'
    success_url = reverse_lazy('resource_management:static_dataset_entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:static_dataset_related_metadata_index'
        return context


class DataSubsetUpdateFormView(
        DataSubsetDataHubViewMixin,
        DataSubsetResourceManagementViewMixin,
        HandleReapplicationViewMixin,
        HandleRegistrationViewMixin,
        ResourceUpdateFormView):
    model = models.DataSubset
    template_name = 'update/file_upload_data_subset_update.html'
    form_class = UploadUpdatedDataSubsetFileForm

    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_subsets'
    resource_update_page_url_name = 'update:data_subset'
    success_url = reverse_lazy('resource_management:data_subsets')

    error_msg = 'An unexpected error occurred whilst trying to update this resource. The update has not been applied.'

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def update_resource(self):
        if not self.is_file_uploaded_for_each_online_resource:
            try:
                self.delete_data_subset_directory()
            except FileNotFoundError:
                logger.exception(f'The directory for Data Subset {self.resource_id} has already been deleted.')
            return super().update_resource()

        with tempfile.TemporaryDirectory() as temp_dirname:
            self.configure_and_add_source_files_to_temporary_directory(temp_dirname)
            updated_resource = super().update_resource()
            self.copy_temporary_directory_to_datahub(
                temp_dirname,
                self.get_data_subset_datahub_directory_path()
            )
            return updated_resource

    def add_source_file_to_temporary_directory(self, source_file: InMemoryUploadedFile|BufferedReader, source_file_write_path: str):
        try:
            return super().add_source_file_to_temporary_directory(
                source_file,
                source_file_write_path
            )
        except AttributeError as err:
            logger.exception(err)
        return shutil.copyfile(source_file.name, source_file_write_path)

    def get_names_of_online_resources_with_files(self):
        # Get list of online resources from resource
        data_subset_shortcutted = DataSubsetXmlMappingShortcuts(self.resource.xml)
        online_resources = data_subset_shortcutted.online_resources

        names_of_online_resources_with_files = []
        for online_resource in online_resources:
            online_resource_name = online_resource.get('name')
            # Find files for each slugified online resource
            # name and store in a dictionary to pass to
            # template context later
            online_resource_file = self.get_online_resource_file_for_data_subset_by_file_name(
                online_resource_name
            )
            if not online_resource_file:
                continue
            names_of_online_resources_with_files.append(online_resource_name)
        return names_of_online_resources_with_files

    def _get_file_for_online_resource(self, online_resource: DataSubsetOnlineResourceUpdate):
        if not online_resource.is_existing_datahub_file_used:
            return super()._get_file_for_online_resource(online_resource)
        file_name_with_no_extension, file_extension = os.path.splitext(online_resource.datahub_file_name)
        return self.get_online_resource_file_for_data_subset_by_file_name(
            file_name_with_no_extension
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:static_dataset_related_metadata_index'
        context['names_of_online_resources_with_files'] = self.get_names_of_online_resources_with_files()
        context['source_file_list_item_template'] = render_to_string(
            'update/source_file_update_list_item_template.html',
            context=context
        )
        return context

    def form_valid(self, form):
        self.is_file_uploaded_for_each_online_resource = form.cleaned_data.get('is_file_uploaded_for_each_online_resource')
        self.source_files = self.request.FILES
        xml_file = self.request.FILES['files']
        
        try:
            if not self.check_source_names(form):
                messages.error(self.request, self.SIMILAR_SOURCE_NAMES_ERROR)
                return self.form_invalid(form)
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'An unexpected error occurred.')
            return super().form_invalid(form)

        try:
            self.temp_xml_file.seek(0)
            self.xml_string = self.temp_xml_file.read().decode()
            data_subset_shortcutted = DataSubsetXmlMappingShortcuts(self.xml_string)
            datahub_file_usage_for_each_source = form.cleaned_data.get('online_resource_datahub_file_usage')
            self.valid_sources = [
                DataSubsetOnlineResourceUpdate(
                    name=online_resource.get('name'),
                    file_input_name=f'online_resource_file__{online_resource.get("name")}',
                    datahub_file_name=slugify(online_resource.get('name')),
                    is_existing_datahub_file_used=datahub_file_usage_for_each_source.get(online_resource.get('name'), False)
                )
                for online_resource in data_subset_shortcutted.online_resources
            ]
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'An unexpected error occurred during metadata registration.')
            return self.form_invalid(form)

        try:
            self.handle_name = self.register_doi_if_requested(self.request, self.resource, xml_file=xml_file)
            # RE-INSERT PRE-EXISTING DOI KERNEL METADATA
            # Refresh self.resource if a DOI was added
            # so the new DOI kernel metadata is added to
            # the submitted XML file.
            self.resource = self.model.objects.get(pk=self.resource_id)
            self.xml_string = self.reinsert_pre_existing_doi_kernel_metadata_into_updated_xml_file_if_needed(
                self.resource,
                xml_file
            )
            return super().form_valid(form)
        except Exception:
            logger.exception(self.error_msg)
            messages.error(self.request, self.error_msg)
        
        return redirect(self.resource_update_page_url_name, resource_id=self.resource_id)


class WorkflowUpdateFormView(
        ResourceUpdateFormView,
        WorkflowDataHubViewMixin,
        WorkflowDetailsUrlValidationViewMixin):
    template_name = 'update/file_upload_workflow_update.html'
    model = models.Workflow
    form_class = UploadUpdatedWorkflowFileForm

    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
    resource_update_page_url_name = 'update:workflow'
    success_url = reverse_lazy('resource_management:workflows')

    error_msg = 'An unexpected error occurred whilst trying to update this resource. The update has not been applied.'
    
    def get_index_of_workflow_details_file_source_choice(self, choice_value: str):
        try:
            return [
                choice[0]
                for choice in self.form_class().fields.get('workflow_details_file_source').choices
            ].index(choice_value)
        except ValueError:
            logger.exception(f'Workflow details source choice, "{choice_value}" does not exist!')
        return None

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def update_resource(self):
        updated_resource = super().update_resource()
        if not self.workflow_details_file_source == 'external':
            return updated_resource
        # User may choose the external details file
        # source by mistake, but still use the eSC
        # details file URL. If this is true, do not
        # delete the details file from DataHub.
        updated_workflow_details_url = WorkflowXmlMappingShortcuts(self.xml_string.decode()).workflow_details_url
        if updated_workflow_details_url == self.get_workflow_details_file_url():
            return updated_resource
        try:
            self.delete_workflow_details_file()
        except FileNotFoundError:
            logger.exception('Workflow details file was not found.')
        return updated_resource

    def form_valid(self, form):
        xml_file = self.request.FILES['files']
        try:
            self.workflow_details_file_source = form.cleaned_data.get('workflow_details_file_source')
            if self.workflow_details_file_source == 'existing':
                xml_file.seek(0)
                self.xml_string = self.add_workflow_details_file_link_to_workflow_xml_file_string(xml_file.read().decode())
            elif self.workflow_details_file_source == 'external':
                xml_file.seek(0)
                workflow_xml = WorkflowXmlMappingShortcuts(xml_file.read().decode())
                workflow_details_url_error = self.check_workflow_details_url(workflow_xml.workflow_details_url)
                if workflow_details_url_error:
                    messages.error(self.request, workflow_details_url_error)
                    return super().form_invalid(form)
                xml_file.seek(0)
            elif self.workflow_details_file_source == 'file_upload':
                self.workflow_details_file = self.request.FILES['workflow_details_file']
                xml_file.seek(0)
                self.xml_string = self.store_workflow_details_file_and_update_xml_file_string(xml_file.read().decode())
            return super().form_valid(form)
        except Exception:
            logger.exception(self.error_msg)
            messages.error(self.request, self.error_msg)
        
        return redirect(self.resource_update_page_url_name, resource_id=self.resource_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workflow_details_file_source_file_upload_choice_index'] = self.get_index_of_workflow_details_file_source_choice('file_upload')
        context['workflow_details_file_source_external_choice_index'] = self.get_index_of_workflow_details_file_source_choice('external')
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
        self.stored_workflow_details_file = self.get_workflow_details_file()
        if not self.stored_workflow_details_file:
            return initial
        initial.update({
            'workflow_details_file_source': 'existing',
        })
        return initial


@login_session_institution_required
@institution_ownership_required
def workflow_openapi_specification_url(request, resource_id):
    workflow = get_object_or_404(models.Workflow, pk=resource_id)
    workflow_interaction_method = workflow.interactionmethod_set.first()
    if request.method == 'POST':
        form = UpdateWorkflowOpenAPISpecificationURLForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'The form submitted was not valid.')
            return redirect('update:workflow_openapi_specification_url', resource_id=workflow.id)
        try:
            if workflow_interaction_method:
                models.WorkflowAPIInteractionMethod.objects.update_config(
                    workflow_interaction_method.id,
                    request.POST.get('api_specification_url'),
                    request.POST.get('api_description')
                )
            else:
                models.WorkflowAPIInteractionMethod.objects.create_api_interaction_method(
                    request.POST.get('api_specification_url'),
                    request.POST.get('api_description'),
                    workflow
                )
            messages.success(request, f'Successfully updated OpenAPI specification for {escape(workflow.name)}.')
        except Exception:
            logger.exception('An unexpected error occurred whilst trying to update an OpenAPI specification for a workflow.')
            messages.error(request, 'An unexpected error occurred.')
        return redirect('update:workflow_openapi_specification_url', resource_id=workflow.id)
    if workflow_interaction_method:
        form = UpdateWorkflowOpenAPISpecificationURLForm(
            initial={
                'api_specification_url': workflow_interaction_method.config.get('specification_url'),
                'api_description': workflow_interaction_method.config.get('description'),
            }
        )
    else:
        form = UpdateWorkflowOpenAPISpecificationURLForm()
    return render(request, 'update/workflow_openapi_specification_url_update.html', {
        'title': 'Update Workflow OpenAPI Specification',
        'workflow': workflow,
        'form': form,
        'api_specification_validation_url': reverse_lazy('validation:api_specification_url'),
        'resource_management_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
        'resource_management_list_page_breadcrumb_url_name': 'resource_management:workflows',
        'resource_management_list_page_breadcrumb_text': _create_manage_resource_page_title(models.Workflow.type_plural_readable.title())
    })