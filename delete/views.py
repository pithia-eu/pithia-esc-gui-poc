import logging
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .pymongo_api import (
    delete_catalogue_related_resource_with_pymongo_transaction_if_possible,
    delete_data_collection_related_resource_with_pymongo_transaction_if_possible,
)

from common import models
from common.models import ScientificMetadata
from common.mongodb_models import (
    AcquisitionCapabilityRevision,
    AcquisitionRevision,
    ComputationCapabilityRevision,
    ComputationRevision,
    CurrentAcquisition,
    CurrentAcquisitionCapability,
    CurrentComputation,
    CurrentComputationCapability,
    CurrentDataCollection,
    CurrentIndividual,
    CurrentInstrument,
    CurrentOperation,
    CurrentOrganisation,
    CurrentPlatform,
    CurrentProcess,
    CurrentProject,
    DataCollectionRevision,
    IndividualRevision,
    InstrumentRevision,
    OperationRevision,
    OrganisationRevision,
    PlatformRevision,
    ProcessRevision,
    ProjectRevision,
    CurrentCatalogue,
    CatalogueRevision,
    CurrentCatalogueEntry,
    CatalogueEntryRevision,
    CurrentCatalogueDataSubset,
    CatalogueDataSubsetRevision,
)
from common.views import (
    LoginInstitutionRequiredView,
)
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
)

logger = logging.getLogger(__name__)

# Create your views here.

class ResourceDeleteView(LoginInstitutionRequiredView, TemplateView):
    """
    The deletion confirmation page for a
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

    resource_management_list_page_breadcrumb_text = 'Register & Manage Resources'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:index'
    delete_resource_page_breadcrumb_url_name = ''

    # TODO: remove old code
    resource_mongodb_model = None
    resource_revision_mongodb_model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Metadata Confirmation'
        context['resource_id'] = self.resource_id
        context['resource_to_delete'] = self.resource_to_delete
        context['other_resources_to_delete'] = self.other_resources_to_delete
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        context['delete_resource_page_breadcrumb_url_name'] = self.delete_resource_page_breadcrumb_url_name
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_type_in_resource_url = self.model.type_in_metadata_server_url
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.resource_to_delete = get_object_or_404(self.model, pk=self.resource_id)
        self.other_resources_to_delete = self.resource_to_delete.metadata_dependents
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_to_delete = get_object_or_404(self.model, pk=self.resource_id)
        # TODO: remove old code
        # In case the localid getter isn't available after
        # the resource is deleted.
        resource_localid = self.resource_to_delete.localid

        try:
            with transaction.atomic():
                self.other_resources_to_delete = self.resource_to_delete.metadata_dependents
                self.all_resources_to_delete = [self.resource_to_delete] + self.other_resources_to_delete
                self.all_resource_urls_to_delete = list(set([resource.metadata_server_url for resource in self.all_resources_to_delete]))
                ScientificMetadata.objects.delete_by_metadata_server_urls(self.all_resource_urls_to_delete)

                # TODO: remove old code
                delete_data_collection_related_resource_with_pymongo_transaction_if_possible(resource_localid, self.resource_mongodb_model, self.resource_revision_mongodb_model, self.resource_type_in_resource_url)
            messages.success(request, f'Successfully deleted {self.resource_to_delete.name}.')
        except BaseException as e:
            logger.exception('An error occurred during resource deletion.')
            messages.error(request, 'An error occurred during resource deletion.')
            return HttpResponseRedirect(self.redirect_url)

        return HttpResponseRedirect(self.redirect_url)

class CatalogueRelatedResourceDeleteView(ResourceDeleteView):
    """
    A subclass of ResourceDeleteView.

    Maps Data Collection-related features (e.g., breadcrumbs)
    to Catalogue-related features.

    This view is intended to be subclassed and to not
    be called directly.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

    def post(self, request, *args, **kwargs):
        self.resource_to_delete = get_object_or_404(self.model, pk=self.resource_id)
        # TODO: remove old code
        # In case the localid getter isn't available after
        # the resource is deleted.
        resource_localid = self.resource_to_delete.localid

        try:
            with transaction.atomic():
                self.other_resources_to_delete = self.resource_to_delete.metadata_dependents
                self.all_resources_to_delete = [self.resource_to_delete] + self.other_resources_to_delete
                self.all_resource_urls_to_delete = list(set([resource.metadata_server_url for resource in self.all_resources_to_delete]))
                ScientificMetadata.objects.delete_by_metadata_server_urls(self.all_resource_urls_to_delete)
                
                # TODO: remove old code
                delete_catalogue_related_resource_with_pymongo_transaction_if_possible(resource_localid, self.resource_mongodb_model, self.resource_revision_mongodb_model)
            messages.success(request, f'Successfully deleted {self.resource_to_delete.name}.')
        except BaseException as e:
            print(e)
            messages.error(request, 'An error occurred during resource deletion.')
        return HttpResponseRedirect(self.redirect_url)


class OrganisationDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for an Organisation
    registration.
    """
    model = models.Organisation

    redirect_url = reverse_lazy('resource_management:organisations')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Organisations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    delete_resource_page_breadcrumb_url_name = 'delete:organisation'

    # TODO: remove old code
    resource_mongodb_model = CurrentOrganisation
    resource_revision_mongodb_model = OrganisationRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)

class IndividualDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for an Individual
    registration.
    """
    model = models.Individual

    redirect_url = reverse_lazy('resource_management:individuals')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Individuals'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    delete_resource_page_breadcrumb_url_name = 'delete:individual'

    # TODO: remove old code
    resource_mongodb_model = CurrentIndividual
    resource_revision_mongodb_model = IndividualRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class ProjectDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for a Project
    registration.
    """
    model = models.Project

    redirect_url = reverse_lazy('resource_management:projects')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Projects'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    delete_resource_page_breadcrumb_url_name = 'delete:project'

    # TODO: remove old code
    resource_mongodb_model = CurrentProject
    resource_revision_mongodb_model = ProjectRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class PlatformDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for a Platform
    registration.
    """
    model = models.Platform

    redirect_url = reverse_lazy('resource_management:platforms')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Platforms'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    delete_resource_page_breadcrumb_url_name = 'delete:platform'

    # TODO: remove old code
    resource_mongodb_model = CurrentPlatform
    resource_revision_mongodb_model = PlatformRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class InstrumentDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for an Instrument
    registration.
    """
    model = models.Instrument

    redirect_url = reverse_lazy('resource_management:instruments')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Instruments'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    delete_resource_page_breadcrumb_url_name = 'delete:instrument'

    # TODO: remove old code
    resource_mongodb_model = CurrentInstrument
    resource_revision_mongodb_model = InstrumentRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class OperationDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for an Operation
    registration.
    """
    model = models.Operation

    redirect_url = reverse_lazy('resource_management:operations')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Operations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    delete_resource_page_breadcrumb_url_name = 'delete:operation'

    # TODO: remove old code
    resource_mongodb_model = CurrentOperation
    resource_revision_mongodb_model = OperationRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class AcquisitionCapabilitiesDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for an Acquisition
    Capabilities registration.
    """
    model = models.AcquisitionCapabilities

    redirect_url = reverse_lazy('resource_management:acquisition_capability_sets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Acquisition Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    delete_resource_page_breadcrumb_url_name = 'delete:acquisition_capability_set'

    # TODO: remove old code
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_revision_mongodb_model = AcquisitionCapabilityRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().dispatch(request, *args, **kwargs)

class AcquisitionDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for an Acquisition
    registration.
    """
    model = models.Acquisition

    redirect_url = reverse_lazy('resource_management:acquisitions')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Acquisitions'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    delete_resource_page_breadcrumb_url_name = 'delete:acquisition'

    # TODO: remove old code
    resource_mongodb_model = CurrentAcquisition
    resource_revision_mongodb_model = AcquisitionRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class ComputationCapabilitiesDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for a Computation
    Capabilities registration.
    """
    model = models.ComputationCapabilities

    redirect_url = reverse_lazy('resource_management:computation_capability_sets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Computation Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    delete_resource_page_breadcrumb_url_name = 'delete:computation_capability_set'

    # TODO: remove old code
    resource_mongodb_model = CurrentComputationCapability
    resource_revision_mongodb_model = ComputationCapabilityRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().dispatch(request, *args, **kwargs)

class ComputationDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for a Computation
    registration.
    """
    model = models.Computation

    redirect_url = reverse_lazy('resource_management:computations')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Computations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    delete_resource_page_breadcrumb_url_name = 'delete:computation'

    # TODO: remove old code
    resource_mongodb_model = CurrentComputation
    resource_revision_mongodb_model = ComputationRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class ProcessDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for a Process
    registration.
    """
    model = models.Process

    redirect_url = reverse_lazy('resource_management:processes')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Processes'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    delete_resource_page_breadcrumb_url_name = 'delete:process'

    # TODO: remove old code
    resource_mongodb_model = CurrentProcess
    resource_revision_mongodb_model = ProcessRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class DataCollectionDeleteView(ResourceDeleteView):
    """
    The deletion confirmation page for a Data
    Collection registration.
    """
    template_name = 'delete/confirm_delete_data_collection.html'
    model = models.DataCollection

    redirect_url = reverse_lazy('resource_management:data_collections')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Collections'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    delete_resource_page_breadcrumb_url_name = 'delete:data_collection'

    # TODO: remove old code
    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    catalogue_related_resources_to_delete = []

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['linked_interaction_methods'] = list(self.resource_to_delete.interactionmethod_set.all())
        return context

class CatalogueDeleteView(CatalogueRelatedResourceDeleteView):
    """
    The deletion confirmation page for a Catalogue
    registration.
    """
    model = models.Catalogue

    redirect_url = reverse_lazy('resource_management:catalogues')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogues'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue'

    # TODO: remove old code
    resource_mongodb_model = CurrentCatalogue
    resource_revision_mongodb_model = CatalogueRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().dispatch(request, *args, **kwargs)

class CatalogueEntryDeleteView(CatalogueRelatedResourceDeleteView):
    """
    The deletion confirmation page for a Catalogue
    Entry registration.
    """
    model = models.CatalogueEntry

    redirect_url = reverse_lazy('resource_management:catalogue_entries')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogue Entries'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_entry'

    # TODO: remove old code
    resource_mongodb_model = CurrentCatalogueEntry
    resource_revision_mongodb_model = CatalogueEntryRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().dispatch(request, *args, **kwargs)

class CatalogueDataSubsetDeleteView(CatalogueRelatedResourceDeleteView):
    """
    The deletion confirmation page for a Catalogue
    Data Subset registration.
    """
    model = models.CatalogueDataSubset

    redirect_url = reverse_lazy('resource_management:catalogue_data_subsets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogue Data Subsets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_data_subset'

    # TODO: remove old code
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_revision_mongodb_model = CatalogueDataSubsetRevision

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        return super().dispatch(request, *args, **kwargs)
