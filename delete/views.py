from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from bson.objectid import ObjectId
from common.helpers import get_interaction_methods_linked_to_data_collection_id
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
from django.views.generic import TemplateView
from resource_management.views import _INDEX_PAGE_TITLE, _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE, _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
from .utils import (
    get_resources_linked_through_resource_id,
    delete_current_version_and_revisions_of_resource_id,
    delete_current_versions_and_revisions_of_data_collection_interaction_methods,
    sort_resource_list,
)

# Create your views here.

class ResourceDeleteView(TemplateView):
    resource_id = ''
    resource_type_in_resource_url = ''
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

    def get(self, request, *args, **kwargs):
        self.resource_to_delete = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        self.other_resources_to_delete = get_resources_linked_through_resource_id(self.resource_id, self.resource_type_in_resource_url, self.resource_mongodb_model)
        self.other_resources_to_delete = sort_resource_list(self.other_resources_to_delete)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Delete the resource and resources that are referencing the resource to be deleted. These should not
        # be able to exist without the resource being deleted.
        linked_resources = get_resources_linked_through_resource_id(self.resource_id, self.resource_type_in_resource_url, self.resource_mongodb_model)
        delete_current_version_and_revisions_of_resource_id(self.resource_id, self.resource_mongodb_model, self.resource_revision_mongodb_model)
        for r in linked_resources:
            delete_current_version_and_revisions_of_resource_id(r[0]['_id'], r[2], r[3])
        return HttpResponseRedirect(self.redirect_url)

class DeleteCatalogueResourceView(TemplateView):
    resource_id = ''
    resource_type = ''
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
        context['resource_type'] = self.resource_type
        if self.resource_type.lower() == 'catalogueentry':
            context['resource_type'] = 'catalogue entry'
        if self.resource_type.lower() == 'cataloguedatasubset':
            context['resource_type'] = 'catalogue data subset'
        context['title'] = f'Confirm Deletion of Metadata'
        context['resource_management_index_page_title'] = _INDEX_PAGE_TITLE
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        context['delete_resource_page_breadcrumb_url_name'] = self.delete_resource_page_breadcrumb_url_name
        context['resource_id'] = self.resource_id
        context['resource_to_delete'] = self.resource_to_delete
        context['other_resources_to_delete'] = self.other_resources_to_delete
        return context

    def get(self, request, *args, **kwargs):
        self.resource_to_delete = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        self.other_resources_to_delete = _get_resources_linked_through_resource_id(self.resource_id, self.resource_type, self.resource_mongodb_model)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Delete the resource and resources that are referencing the resource to be deleted. These should not
        # be able to exist without the resource being deleted.
        linked_resources = _get_resources_linked_through_resource_id(self.resource_id, self.resource_type, self.resource_mongodb_model)
        _delete_current_version_and_revisions_of_resource_id(self.resource_id, self.resource_mongodb_model, self.resource_revision_mongodb_model)
        for r in linked_resources:
            _delete_current_version_and_revisions_of_resource_id(r[0]['_id'], r[2], r[3])
        return HttpResponseRedirect(self.redirect_url)


class OrganisationDeleteView(ResourceDeleteView):
    resource_type_in_resource_url = 'organisation'
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
    resource_type_in_resource_url = 'individual'
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
    resource_type_in_resource_url = 'project'
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
    resource_type_in_resource_url = 'platform'
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
    resource_type_in_resource_url = 'instrument'
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
    resource_type_in_resource_url = 'operation'
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
    resource_type_in_resource_url = 'acquisitionCapabilities'
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
    resource_type_in_resource_url = 'acquisition'
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
    resource_type_in_resource_url = 'computationCapabilities'
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
    resource_type_in_resource_url = 'computation'
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
    resource_type_in_resource_url = 'process'
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
    resource_type_in_resource_url = 'collection'
    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    redirect_url = reverse_lazy('resource_management:data_collections')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Collections'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    delete_resource_page_breadcrumb_url_name = 'delete:data_collection'
    template_name = 'delete/confirm_delete_data_collection.html'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['linked_interaction_methods'] = get_interaction_methods_linked_to_data_collection_id(self.resource_id)
        return context

    def post(self, request, *args, **kwargs):
        # Delete interaction methods (current versions and
        # revisions) before deleting the actual data collection,
        # not sure if the order should be changed around...
        delete_current_versions_and_revisions_of_data_collection_interaction_methods(self.resource_id)
        return super().post(request, *args, **kwargs)

class catalogue(DeleteCatalogueResourceView):
    resource_type = 'catalogue'
    resource_mongodb_model = CurrentCatalogue
    resource_revision_mongodb_model = CatalogueRevision
    redirect_url = reverse_lazy('resource_management:catalogues')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogues'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class catalogue_entry(DeleteCatalogueResourceView):
    resource_type = 'catalogueentry'
    resource_mongodb_model = CurrentCatalogueEntry
    resource_revision_mongodb_model = CatalogueEntryRevision
    redirect_url = reverse_lazy('resource_management:catalogue_entries')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogue Entries'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class catalogue_data_subset(DeleteCatalogueResourceView):
    resource_type = 'cataloguedatasubset'
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_revision_mongodb_model = CatalogueDataSubsetRevision
    redirect_url = reverse_lazy('resource_management:catalogue_data_subsets')
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Catalogue Data Subsets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    delete_resource_page_breadcrumb_url_name = 'delete:catalogue_data_subset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context
