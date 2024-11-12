import logging
import os
from django.contrib import messages
from django.shortcuts import (
    get_object_or_404,
    render,
    redirect,
)
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic.edit import FormView
from pyexpat import ExpatError

from common import models
from common.decorators import (
    login_session_institution_required,
    institution_ownership_required
)
from datahub_management.view_mixins import WorkflowDataHubViewMixin
from handle_management.view_mixins import (
    HandleRegistrationViewMixin,
    HandleReapplicationViewMixin,
)
from resource_management.forms import (
    UpdateDataCollectionInteractionMethodsForm,
    UpdateWorkflowOpenAPISpecificationURLForm,
    UploadUpdatedCatalogueDataSubsetFileForm,
    UploadUpdatedDataCollectionFileForm,
    UploadUpdatedFileForm,
    UploadUpdatedWorkflowFileForm,
)
from resource_management.views import (
    _create_manage_resource_page_title,
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
)
from user_management.services import get_user_id_for_login_session


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
    validation_url = ''
    # resource_to_update_name = '' # Set in dispatch() function
    resource_management_list_page_breadcrumb_url_name = ''

    # Class variables
    template_name = 'update/file_upload_update.html'
    form_class = UploadUpdatedFileForm
    success_url = ''
    xml_file_string = None

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
        context['validation_url'] = self.validation_url
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
            if self.xml_file_string is None:
                xml_file.seek(0)
                self.xml_file_string = xml_file.read()
            resource_id_temp = self.resource_id
            self.model.objects.update_from_xml_string(
                resource_id_temp,
                self.xml_file_string,
                self.owner_id
            )

            messages.success(self.request, f'Successfully updated {escape(xml_file.name)}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
        except ExpatError as err:
            logger.exception('Could not update a resource as there was an error parsing the update XML.')
            messages.error(self.request, 'An error occurred whilst parsing the XML.')
        except BaseException as err:
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
    validation_url = reverse_lazy('validation:organisation')
    success_url = reverse_lazy('resource_management:organisations')


class IndividualUpdateFormView(ResourceUpdateFormView):
    model = models.Individual

    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_update_page_url_name = 'update:individual'
    validation_url = reverse_lazy('validation:individual')
    success_url = reverse_lazy('resource_management:individuals')


class ProjectUpdateFormView(ResourceUpdateFormView):
    model = models.Project

    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_update_page_url_name = 'update:project'
    validation_url = reverse_lazy('validation:project')
    success_url = reverse_lazy('resource_management:projects')


class PlatformUpdateFormView(ResourceUpdateFormView):
    model = models.Platform

    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_update_page_url_name = 'update:platform'
    validation_url = reverse_lazy('validation:platform')
    success_url = reverse_lazy('resource_management:platforms')


class OperationUpdateFormView(ResourceUpdateFormView):
    model = models.Operation

    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_update_page_url_name = 'update:operation'
    validation_url = reverse_lazy('validation:operation')
    success_url = reverse_lazy('resource_management:operations')


class InstrumentUpdateFormView(ResourceUpdateFormView):
    template_name = 'update/file_upload_instrument_update.html'
    model = models.Instrument

    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_update_page_url_name = 'update:instrument'
    validation_url = reverse_lazy('validation:instrument')
    success_url = reverse_lazy('resource_management:instruments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inline_validation_url'] = reverse_lazy('validation:instrument_update')
        return context


class AcquisitionCapabilitiesUpdateFormView(ResourceUpdateFormView):
    model = models.AcquisitionCapabilities

    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    validation_url = reverse_lazy('validation:acquisition_capability_set')
    success_url = reverse_lazy('resource_management:acquisition_capability_sets')


class AcquisitionUpdateFormView(ResourceUpdateFormView):
    model = models.Acquisition

    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_update_page_url_name = 'update:acquisition'
    validation_url = reverse_lazy('validation:acquisition')
    success_url = reverse_lazy('resource_management:acquisitions')


class ComputationCapabilitiesUpdateFormView(ResourceUpdateFormView):
    model = models.ComputationCapabilities

    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_update_page_url_name = 'update:computation_capability_set'
    validation_url = reverse_lazy('validation:computation_capability_set')
    success_url = reverse_lazy('resource_management:computation_capability_sets')


class ComputationUpdateFormView(ResourceUpdateFormView):
    model = models.Computation

    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_update_page_url_name = 'update:computation'
    validation_url = reverse_lazy('validation:computation')
    success_url = reverse_lazy('resource_management:computations')


class ProcessUpdateFormView(ResourceUpdateFormView):
    model = models.Process

    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_update_page_url_name = 'update:process'
    validation_url = reverse_lazy('validation:process')
    success_url = reverse_lazy('resource_management:processes')


class DataCollectionUpdateFormView(ResourceUpdateFormView):
    model = models.DataCollection
    form_class = UploadUpdatedDataCollectionFileForm

    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    resource_update_page_url_name = 'update:data_collection'
    validation_url = reverse_lazy('validation:data_collection')
    success_url = reverse_lazy('resource_management:data_collections')


@login_session_institution_required
@institution_ownership_required
def data_collection_interaction_methods(request, resource_id):
    data_collection = get_object_or_404(models.DataCollection, pk=resource_id)
    if request.method == 'POST':
        form = UpdateDataCollectionInteractionMethodsForm(request.POST)
        if form.is_valid():
            try:
                is_api_selected = 'api_selected' in request.POST
                api_specification_url = request.POST.get('api_specification_url')
                api_description = request.POST.get('api_description')
                
                if is_api_selected == False:
                    try:
                        models.APIInteractionMethod.objects.get(scientific_metadata=data_collection).delete(using=os.environ['DJANGO_RW_DATABASE_NAME'])
                    except models.APIInteractionMethod.DoesNotExist:
                        pass
                    messages.success(request, f'Successfully updated interaction methods for {escape(data_collection.name)}.')
                    return redirect('update:data_collection_interaction_methods', resource_id=resource_id)

                try:
                    api_interaction_method = models.APIInteractionMethod.objects.get(scientific_metadata=data_collection)
                    models.APIInteractionMethod.objects.update_config(
                        api_interaction_method.pk,
                        api_specification_url,
                        api_description
                    )
                except models.APIInteractionMethod.DoesNotExist:
                    models.APIInteractionMethod.objects.create_api_interaction_method(
                        api_specification_url,
                        api_description,
                        data_collection
                    )
                messages.success(request, f'Successfully updated interaction methods for {escape(data_collection.name)}.')
            except BaseException as err:
                logger.exception('An unexpected error occurred whilst trying to update a Data Collection interaction method.')
                messages.error(request, 'An unexpected error occurred.')
        else:
            messages.error(request, 'The form submitted was not valid.')
        return redirect('update:data_collection_interaction_methods', resource_id=resource_id)
        
    # request.method == 'GET'
    form = UpdateDataCollectionInteractionMethodsForm()
    form_data = {}
    try:
        api_interaction_method = models.APIInteractionMethod.objects.get(scientific_metadata=data_collection)
        form_data['api_selected'] = True
        form_data['api_specification_url'] = api_interaction_method.specification_url
        form_data['api_description'] = api_interaction_method.description
        form = UpdateDataCollectionInteractionMethodsForm(initial=form_data)
    except models.APIInteractionMethod.DoesNotExist:
        pass
    return render(request, 'update/interaction_methods_update.html', {
        'data_collection': data_collection,
        'data_collection_id': data_collection.pk,
        'form': form,
        'api_specification_validation_url': reverse_lazy('validation:api_specification_url'),
        'title': f'Update Interaction Methods for {data_collection.name}',
        'resource_management_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
        'resource_management_category_list_page_breadcrumb_url_name': 'resource_management:data_collection_related_metadata_index',
        'resource_management_category_list_page_breadcrumb_text': _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
        'resource_management_list_page_breadcrumb_url_name': 'resource_management:data_collections',
        'resource_management_list_page_breadcrumb_text': _create_manage_resource_page_title(models.DataCollection.type_plural_readable.title())
    })


class CatalogueUpdateFormView(ResourceUpdateFormView):
    model = models.Catalogue

    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    resource_update_page_url_name = 'update:catalogue'
    validation_url = reverse_lazy('validation:catalogue')
    success_url = reverse_lazy('resource_management:catalogues')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class CatalogueEntryUpdateFormView(ResourceUpdateFormView):
    model = models.CatalogueEntry

    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    resource_update_page_url_name = 'update:catalogue_entry'
    validation_url = reverse_lazy('validation:catalogue_entry')
    success_url = reverse_lazy('resource_management:catalogue_entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class CatalogueDataSubsetUpdateFormView(
    HandleReapplicationViewMixin,
    HandleRegistrationViewMixin,
    ResourceUpdateFormView):
    model = models.CatalogueDataSubset
    template_name = 'update/file_upload_catalogue_data_subset_update.html'
    form_class = UploadUpdatedCatalogueDataSubsetFileForm

    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    resource_update_page_url_name = 'update:catalogue_data_subset'
    validation_url = reverse_lazy('validation:catalogue_data_subset')
    success_url = reverse_lazy('resource_management:catalogue_data_subsets')

    error_msg = 'An unexpected error occurred whilst trying to update this resource. The update has not been applied.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

    def form_valid(self, form):
        xml_file = self.request.FILES['files']
        try:
            self.handle_name = self.register_doi_if_requested(self.request, self.resource, xml_file)
            # RE-INSERT PRE-EXISTING DOI KERNEL METADATA
            # Refresh self.resource if a DOI was added
            # so the new DOI kernel metadata is added to
            # the submitted XML file.
            self.resource = self.model.objects.get(pk=self.resource_id)
            self.xml_file_string = self.reinsert_pre_existing_doi_kernel_metadata_into_updated_xml_file_if_needed(
                self.resource,
                xml_file
            )
            return super().form_valid(form)
        except Exception:
            logger.exception(self.error_msg)
            messages.error(self.request, self.error_msg)
        
        return redirect(self.resource_update_page_url_name, resource_id=self.resource_id)


class WorkflowUpdateFormView(ResourceUpdateFormView, WorkflowDataHubViewMixin):
    template_name = 'update/file_upload_workflow_update.html'
    model = models.Workflow
    form_class = UploadUpdatedWorkflowFileForm

    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
    resource_update_page_url_name = 'update:workflow'
    validation_url = reverse_lazy('validation:workflow')
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

    def form_valid(self, form):
        xml_file = self.request.FILES['files']
        try:
            workflow_details_file_source = form.cleaned_data.get('workflow_details_file_source')
            # Do nothing for workflow_details_file_source == 'external'
            if workflow_details_file_source == 'existing':
                xml_file.seek(0)
                self.xml_file_string = self.add_workflow_details_file_link_to_workflow_xml_file_string(xml_file.read().decode())
            elif workflow_details_file_source == 'file_upload':
                self.details_file = self.request.FILES['workflow_details_file']
                xml_file.seek(0)
                self.xml_file_string = self.store_workflow_details_file_and_update_xml_file_string(xml_file.read().decode())
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
        except BaseException as err:
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