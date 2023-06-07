import logging
from bson.objectid import ObjectId
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .utils import (
    get_data_collection_related_resources_linked_through_resource_id,
    delete_current_version_and_revisions_and_xmls_of_resource_id,
    delete_current_versions_and_revisions_of_data_collection_interaction_methods,
    sort_resource_list,
    get_catalogue_related_resources_linked_through_resource_id,
)

from common import models
from common.helpers import get_interaction_methods_linked_to_data_collection_id
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
from mongodb import client
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
)

logger = logging.getLogger(__name__)

# Create your views here.

class ResourceDeleteView(TemplateView):
    resource_id = ''
    resource_mongodb_model = None
    resource_revision_mongodb_model = None
    redirect_url = ''
    template_name = 'delete/confirm_delete_resource.html'
    resource_management_list_page_breadcrumb_text = 'Register & Manage Resources'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:index'
    delete_resource_page_breadcrumb_url_name = ''
    resource_to_delete = None
    other_resources_to_delete = []

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
        # TODO: remove old code
        # self.resource_to_delete = self.resource_mongodb_model.find_one({
        #     '_id': ObjectId(self.resource_id)
        # })
        # self.other_resources_to_delete = get_data_collection_related_resources_linked_through_resource_id(self.resource_id, self.resource_type_in_resource_url, self.resource_mongodb_model)
        # self.other_resources_to_delete = sort_resource_list(self.other_resources_to_delete)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_to_delete = get_object_or_404(self.model, pk=self.resource_id)
        self.other_resources_to_delete = self.resource_to_delete.metadata_dependents
        self.all_resources_to_delete = [self.resource_to_delete] + self.other_resources_to_delete
        self.all_resource_urls_to_delete = list(set([resource.metadata_server_url for resource in self.all_resources_to_delete]))
        ScientificMetadata.objects.delete_by_metadata_server_urls(self.all_resource_urls_to_delete)

        # TODO: remove old code
        # self.resource_to_delete_old = self.resource_mongodb_model.find_one({
        #     '_id': ObjectId(self.resource_id)
        # })
        # try:
        #     with client.start_session() as s:
        #         def cb(s):
        #             # Delete the resource and resources that are referencing the resource to be deleted. These should not
        #             # be able to exist without the resource being deleted.
        #             linked_resources = get_data_collection_related_resources_linked_through_resource_id(self.resource_id, self.resource_type_in_resource_url, self.resource_mongodb_model)
        #             if 'catalogue_related_resources_to_delete' in kwargs:
        #                 linked_resources.extend(kwargs['catalogue_related_resources_to_delete'])
        #             delete_current_version_and_revisions_and_xmls_of_resource_id(self.resource_id, self.resource_mongodb_model, self.resource_revision_mongodb_model, session=s)
        #             for r in linked_resources:
        #                 delete_current_version_and_revisions_and_xmls_of_resource_id(r[0]['_id'], r[2], r[3], session=s)
        #             if self.resource_mongodb_model == CurrentDataCollection:
        #                 delete_current_versions_and_revisions_of_data_collection_interaction_methods(kwargs['data_collection_id'], session=s)
        #         s.with_transaction(cb)
        # except BaseException as e:
        #     logger.exception('An error occurred during resource deletion.')
        #     messages.error(request, 'An error occurred during resource deletion.')
        #     return HttpResponseRedirect(self.redirect_url)

        messages.success(request, f'Successfully deleted {self.resource_to_delete.name}.')
        return HttpResponseRedirect(self.redirect_url)

class CatalogueRelatedResourceDeleteView(TemplateView):
    resource_id = ''
    resource_mongodb_model = None
    resource_revision_mongodb_model = None
    redirect_url = ''
    template_name = 'delete/confirm_delete_resource.html'
    resource_management_list_page_breadcrumb_text = 'Register & Manage Resources'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:index'
    delete_resource_page_breadcrumb_url_name = ''
    resource_to_delete = None
    other_resources_to_delete = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Delete Metadata Confirmation'
        context['resource_id'] = self.resource_id
        context['resource_to_delete'] = self.resource_to_delete
        context['other_resources_to_delete'] = self.other_resources_to_delete
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        context['delete_resource_page_breadcrumb_url_name'] = self.delete_resource_page_breadcrumb_url_name
        return context

    def get(self, request, *args, **kwargs):
        self.resource_to_delete = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        if 'entryName' in self.resource_to_delete:
            self.resource_to_delete['name'] = self.resource_to_delete['entryName']
        if 'dataSubsetName' in self.resource_to_delete:
            self.resource_to_delete['name'] = self.resource_to_delete['dataSubsetName']
        self.other_resources_to_delete = get_catalogue_related_resources_linked_through_resource_id(self.resource_id, self.resource_mongodb_model)
        self.other_resources_to_delete = sort_resource_list(self.other_resources_to_delete)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            with client.start_session() as s:
                def cb(s):
                    # Delete the resource and resources that are referencing the resource to be deleted. These should not
                    # be able to exist without the resource being deleted.
                    linked_resources = get_catalogue_related_resources_linked_through_resource_id(self.resource_id, self.resource_mongodb_model)
                    delete_current_version_and_revisions_and_xmls_of_resource_id(self.resource_id, self.resource_mongodb_model, self.resource_revision_mongodb_model, session=s)
                    for r in linked_resources:
                        delete_current_version_and_revisions_and_xmls_of_resource_id(r[0]['_id'], r[2], r[3], session=s)
                s.with_transaction(cb)
        except BaseException as e:
            print(e)
            messages.error(request, 'An error occurred during resource deletion.')
        return HttpResponseRedirect(self.redirect_url)


class OrganisationDeleteView(ResourceDeleteView):
    model = models.Organisation

    resource_mongodb_model = CurrentOrganisation
    resource_revision_mongodb_model = OrganisationRevision
    redirect_url = reverse_lazy('resource_management:organisations')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Organisations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    delete_resource_page_breadcrumb_url_name = 'delete:organisation'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)

class IndividualDeleteView(ResourceDeleteView):
    model = models.Individual

    resource_mongodb_model = CurrentIndividual
    resource_revision_mongodb_model = IndividualRevision
    redirect_url = reverse_lazy('resource_management:individuals')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Individuals'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    delete_resource_page_breadcrumb_url_name = 'delete:individual'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class ProjectDeleteView(ResourceDeleteView):
    model = models.Project

    resource_mongodb_model = CurrentProject
    resource_revision_mongodb_model = ProjectRevision
    redirect_url = reverse_lazy('resource_management:projects')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Projects'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    delete_resource_page_breadcrumb_url_name = 'delete:project'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class PlatformDeleteView(ResourceDeleteView):
    model = models.Platform

    resource_mongodb_model = CurrentPlatform
    resource_revision_mongodb_model = PlatformRevision
    redirect_url = reverse_lazy('resource_management:platforms')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Platforms'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    delete_resource_page_breadcrumb_url_name = 'delete:platform'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class InstrumentDeleteView(ResourceDeleteView):
    model = models.Instrument

    resource_mongodb_model = CurrentInstrument
    resource_revision_mongodb_model = InstrumentRevision
    redirect_url = reverse_lazy('resource_management:instruments')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Instruments'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    delete_resource_page_breadcrumb_url_name = 'delete:instrument'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class OperationDeleteView(ResourceDeleteView):
    model = models.Operation

    resource_mongodb_model = CurrentOperation
    resource_revision_mongodb_model = OperationRevision
    redirect_url = reverse_lazy('resource_management:operations')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Operations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    delete_resource_page_breadcrumb_url_name = 'delete:operation'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class AcquisitionCapabilitiesDeleteView(ResourceDeleteView):
    model = models.AcquisitionCapabilities

    resource_mongodb_model = CurrentAcquisitionCapability
    resource_revision_mongodb_model = AcquisitionCapabilityRevision
    redirect_url = reverse_lazy('resource_management:acquisition_capability_sets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Acquisition Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    delete_resource_page_breadcrumb_url_name = 'delete:acquisition_capability_set'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().dispatch(request, *args, **kwargs)

class AcquisitionDeleteView(ResourceDeleteView):
    model = models.Acquisition

    resource_mongodb_model = CurrentAcquisition
    resource_revision_mongodb_model = AcquisitionRevision
    redirect_url = reverse_lazy('resource_management:acquisitions')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Acquisitions'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    delete_resource_page_breadcrumb_url_name = 'delete:acquisition'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class ComputationCapabilitiesDeleteView(ResourceDeleteView):
    model = models.ComputationCapabilities

    resource_mongodb_model = CurrentComputationCapability
    resource_revision_mongodb_model = ComputationCapabilityRevision
    redirect_url = reverse_lazy('resource_management:computation_capability_sets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Computation Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    delete_resource_page_breadcrumb_url_name = 'delete:computation_capability_set'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().dispatch(request, *args, **kwargs)

class ComputationDeleteView(ResourceDeleteView):
    model = models.Computation

    resource_mongodb_model = CurrentComputation
    resource_revision_mongodb_model = ComputationRevision
    redirect_url = reverse_lazy('resource_management:computations')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Computations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    delete_resource_page_breadcrumb_url_name = 'delete:computation'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class ProcessDeleteView(ResourceDeleteView):
    model = models.Process

    resource_mongodb_model = CurrentProcess
    resource_revision_mongodb_model = ProcessRevision
    redirect_url = reverse_lazy('resource_management:processes')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Processes'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    delete_resource_page_breadcrumb_url_name = 'delete:process'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class DataCollectionDeleteView(ResourceDeleteView):
    model = models.DataCollection

    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    redirect_url = reverse_lazy('resource_management:data_collections')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Collections'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    delete_resource_page_breadcrumb_url_name = 'delete:data_collection'
    template_name = 'delete/confirm_delete_data_collection.html'
    catalogue_related_resources_to_delete = []

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_resources_to_delete'].extend(self.catalogue_related_resources_to_delete)
        context['linked_interaction_methods'] = get_interaction_methods_linked_to_data_collection_id(self.resource_id)
        return context

    def get(self, request, *args, **kwargs):
        self.catalogue_related_resources_to_delete = get_catalogue_related_resources_linked_through_resource_id(self.resource_id, self.resource_mongodb_model)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        kwargs['catalogue_related_resources_to_delete'] = get_catalogue_related_resources_linked_through_resource_id(self.resource_id, self.resource_mongodb_model)
        return super().post(request, *args, **kwargs)

class CatalogueDeleteView(CatalogueRelatedResourceDeleteView):
    model = models.Catalogue

    resource_type = 'catalogue'
    resource_mongodb_model = CurrentCatalogue
    resource_revision_mongodb_model = CatalogueRevision
    redirect_url = reverse_lazy('resource_management:catalogues')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogues'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class CatalogueEntryDeleteView(CatalogueRelatedResourceDeleteView):
    model = models.CatalogueEntry

    resource_type = 'catalogue entry'
    resource_mongodb_model = CurrentCatalogueEntry
    resource_revision_mongodb_model = CatalogueEntryRevision
    redirect_url = reverse_lazy('resource_management:catalogue_entries')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogue Entries'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_entry'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class CatalogueDataSubsetDeleteView(CatalogueRelatedResourceDeleteView):
    model = models.CatalogueDataSubset

    resource_type = 'catalogue data subset'
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_revision_mongodb_model = CatalogueDataSubsetRevision
    redirect_url = reverse_lazy('resource_management:catalogue_data_subsets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogue Data Subsets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_data_subset'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context
