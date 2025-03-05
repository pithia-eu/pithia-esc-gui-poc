import logging
import os
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import TemplateView

from common import models
from common.decorators import (
    login_session_institution_required,
    institution_ownership_required,
)
from common.models import ScientificMetadata
from datahub_management.view_mixins import (
    CatalogueDataSubsetDataHubViewMixin,
    WorkflowDataHubViewMixin,
)
from resource_management.views import (
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _INDEX_PAGE_TITLE,
)


logger = logging.getLogger(__name__)


# Create your views here.


@method_decorator(login_session_institution_required, name='dispatch')
@method_decorator(institution_ownership_required, name='dispatch')
class ResourceDeleteView(TemplateView):
    """The deletion confirmation page for a
    scientific metadata registration.

    Displays (if any) the scientific metadata
    dependents of the registration being
    deleted.

    For Data Collections, the page also informs
    of whether any associated interaction
    methods will be deleted as well.

    If any scientific metadata dependents exist,
    the deletion of the resource is prevented,
    else the deletion of the resource is allowed.

    This view is intended to be subclassed and to not
    be called directly.
    """
    template_name = 'delete/confirm_delete_resource.html'

    resource_id = ''
    resource_to_delete = None
    other_resources_to_delete = []
    redirect_url = ''

    resource_management_list_page_breadcrumb_text = ''
    resource_management_list_page_breadcrumb_url_name = 'resource_management:index'
    delete_resource_page_breadcrumb_url_name = ''

    def run_delete_actions(self):
        self.other_resources_to_delete = self.resource_to_delete.metadata_dependents
        self.all_resources_to_delete = [self.resource_to_delete] + self.other_resources_to_delete
        self.all_resource_urls_to_delete = list(set([resource.metadata_server_url for resource in self.all_resources_to_delete]))
        ScientificMetadata.objects.delete_by_metadata_server_urls(self.all_resource_urls_to_delete)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete {self.resource_to_delete.name}'
        context['resource_id'] = self.resource_id
        context['resource_to_delete'] = self.resource_to_delete
        context['other_resources_to_delete'] = self.other_resources_to_delete
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = _create_manage_resource_page_title(self.model.type_plural_readable.title())
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        context['delete_resource_page_breadcrumb_url_name'] = self.delete_resource_page_breadcrumb_url_name
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['resource_id']
        self.resource_type_in_resource_url = self.model.type_in_metadata_server_url
        self.resource_to_delete = get_object_or_404(self.model, pk=self.resource_id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.other_resources_to_delete = self.resource_to_delete.metadata_dependents
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.run_delete_actions()
            messages.success(request, f'Successfully deleted {escape(self.resource_to_delete.name)}.')
        except BaseException as e:
            logger.exception('An error occurred during resource deletion.')
            messages.error(request, 'An error occurred during resource deletion.')
            return HttpResponseRedirect(self.redirect_url)

        return HttpResponseRedirect(self.redirect_url)


class CatalogueRelatedResourceDeleteView(ResourceDeleteView):
    """A subclass of ResourceDeleteView.

    Maps Data Collection-related features (e.g., breadcrumbs)
    to Static Dataset-related features.

    This view is intended to be subclassed and to not
    be called directly.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class OrganisationDeleteView(ResourceDeleteView):
    """The deletion confirmation page for an Organisation
    registration.
    """
    model = models.Organisation

    redirect_url = reverse_lazy('resource_management:organisations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    delete_resource_page_breadcrumb_url_name = 'delete:organisation'


class IndividualDeleteView(ResourceDeleteView):
    """The deletion confirmation page for an Individual
    registration.
    """
    model = models.Individual

    redirect_url = reverse_lazy('resource_management:individuals')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    delete_resource_page_breadcrumb_url_name = 'delete:individual'


class ProjectDeleteView(ResourceDeleteView):
    """The deletion confirmation page for a Project
    registration.
    """
    model = models.Project

    redirect_url = reverse_lazy('resource_management:projects')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    delete_resource_page_breadcrumb_url_name = 'delete:project'


class PlatformDeleteView(ResourceDeleteView):
    """The deletion confirmation page for a Platform
    registration.
    """
    model = models.Platform

    redirect_url = reverse_lazy('resource_management:platforms')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    delete_resource_page_breadcrumb_url_name = 'delete:platform'


class InstrumentDeleteView(ResourceDeleteView):
    """The deletion confirmation page for an Instrument
    registration.
    """
    model = models.Instrument

    redirect_url = reverse_lazy('resource_management:instruments')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    delete_resource_page_breadcrumb_url_name = 'delete:instrument'


class OperationDeleteView(ResourceDeleteView):
    """The deletion confirmation page for an Operation
    registration.
    """
    model = models.Operation

    redirect_url = reverse_lazy('resource_management:operations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    delete_resource_page_breadcrumb_url_name = 'delete:operation'


class AcquisitionCapabilitiesDeleteView(ResourceDeleteView):
    """The deletion confirmation page for an Acquisition
    Capabilities registration.
    """
    model = models.AcquisitionCapabilities

    redirect_url = reverse_lazy('resource_management:acquisition_capability_sets')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    delete_resource_page_breadcrumb_url_name = 'delete:acquisition_capability_set'


class AcquisitionDeleteView(ResourceDeleteView):
    """The deletion confirmation page for an Acquisition
    registration.
    """
    model = models.Acquisition

    redirect_url = reverse_lazy('resource_management:acquisitions')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    delete_resource_page_breadcrumb_url_name = 'delete:acquisition'


class ComputationCapabilitiesDeleteView(ResourceDeleteView):
    """The deletion confirmation page for a Computation
    Capabilities registration.
    """
    model = models.ComputationCapabilities

    redirect_url = reverse_lazy('resource_management:computation_capability_sets')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    delete_resource_page_breadcrumb_url_name = 'delete:computation_capability_set'


class ComputationDeleteView(ResourceDeleteView):
    """The deletion confirmation page for a Computation
    registration.
    """
    model = models.Computation

    redirect_url = reverse_lazy('resource_management:computations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    delete_resource_page_breadcrumb_url_name = 'delete:computation'


class ProcessDeleteView(ResourceDeleteView):
    """The deletion confirmation page for a Process
    registration.
    """
    model = models.Process

    redirect_url = reverse_lazy('resource_management:processes')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    delete_resource_page_breadcrumb_url_name = 'delete:process'

class DataCollectionDeleteView(ResourceDeleteView):
    """The deletion confirmation page for a Data
    Collection registration.
    """
    template_name = 'delete/confirm_delete_data_collection.html'
    model = models.DataCollection

    redirect_url = reverse_lazy('resource_management:data_collections')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    delete_resource_page_breadcrumb_url_name = 'delete:data_collection'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['linked_interaction_methods'] = list(self.resource_to_delete.interactionmethod_set.all())
        return context


class CatalogueDeleteView(CatalogueRelatedResourceDeleteView):
    """The deletion confirmation page for a Static Dataset
    registration.
    """
    model = models.Catalogue

    redirect_url = reverse_lazy('resource_management:catalogues')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue'


class CatalogueEntryDeleteView(CatalogueRelatedResourceDeleteView):
    """The deletion confirmation page for a Static Dataset
    Entry registration.
    """
    model = models.CatalogueEntry

    redirect_url = reverse_lazy('resource_management:catalogue_entries')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_entry'


class CatalogueDataSubsetDeleteView(
        CatalogueDataSubsetDataHubViewMixin,
        CatalogueRelatedResourceDeleteView):
    """The deletion confirmation page for a Static
    Data Subset registration.
    """
    template_name = 'delete/confirm_delete_catalogue_data_subset.html'
    model = models.CatalogueDataSubset

    redirect_url = reverse_lazy('resource_management:catalogue_data_subsets')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_data_subset'

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_delete_actions(self):
        super().run_delete_actions()
        try:
            self.delete_catalogue_data_subset_directory()
        except FileNotFoundError:
            logger.exception(f'The directory for Static Data Subset {self.resource_id} has already been deleted.')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_datahub_used'] = self.is_catalogue_data_subset_directory_created()
        return context


class WorkflowDeleteView(ResourceDeleteView, WorkflowDataHubViewMixin):
    """The deletion confirmation page for a Workflow.
    """
    template_name = 'delete/confirm_delete_workflow.html'
    model = models.Workflow

    redirect_url = reverse_lazy('resource_management:workflows')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'
    delete_resource_page_breadcrumb_url_name = 'delete:workflow'

    @transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME'])
    def run_delete_actions(self):
        super().run_delete_actions()
        stored_workflow_details_file = self.get_workflow_details_file()
        if not stored_workflow_details_file:
            return
        try:
            self.delete_workflow_details_file()
        except FileNotFoundError:
            logger.exception('Workflow details file already deleted.')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stored_workflow_details_file'] = self.get_workflow_details_file()
        return context
