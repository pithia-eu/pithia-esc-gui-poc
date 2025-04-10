from browse.views import _INDEX_PAGE_TITLE as _BROWSE_INDEX_PAGE_TITLE
from browse.views import (
    _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
)
from common import models
from resource_management.views import _INDEX_PAGE_TITLE as _RESOURCE_MANAGEMENT_INDEX_PAGE_TITLE
from resource_management.views import (
    _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
)


class ResourceXmlDownloadFromBrowsingViewMixin:
    template_name = 'utils/from_browsing/resource_as_xml_from_browsing.html'
    resource_type_list_page_breadcrumb_text = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['browse_index_page_breadcrumb_text'] = _BROWSE_INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = self.resource_type_list_page_breadcrumb_text
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        context['resource_list_page_breadcrumb_text'] = self.model.type_plural_readable.title()
        context['resource_list_page_breadcrumb_url_name'] = self.resource_list_by_type_url_name
        context['detail_page_url_name'] = self.detail_page_url_name
        return context


class ResourceXmlDownloadFromManagementViewMixin:
    template_name = 'utils/from_management/resource_as_xml_from_management.html'
    resource_management_category_list_page_breadcrumb_text = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:data_collection_related_metadata_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_index_page_breadcrumb_text'] = _RESOURCE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = self.resource_management_category_list_page_breadcrumb_text
        context['resource_management_category_list_page_breadcrumb_url_name'] = self.resource_management_category_list_page_breadcrumb_url_name
        context['resource_management_list_page_breadcrumb_text'] = _create_manage_resource_page_title(self.model.type_plural_readable.title())
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context


class OrganisationXmlDownloadViewMixin:
    model = models.Organisation
    detail_page_url_name = 'browse:organisation_detail'
    resource_list_by_type_url_name = 'browse:list_organisations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'


class IndividualXmlDownloadViewMixin:
    model = models.Individual
    detail_page_url_name = 'browse:individual_detail'
    resource_list_by_type_url_name = 'browse:list_individuals'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'


class ProjectXmlDownloadViewMixin:
    model = models.Project
    detail_page_url_name = 'browse:project_detail'
    resource_list_by_type_url_name = 'browse:list_projects'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'


class PlatformXmlDownloadViewMixin:
    model = models.Platform
    detail_page_url_name = 'browse:platform_detail'
    resource_list_by_type_url_name = 'browse:list_platforms'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'


class OperationXmlDownloadViewMixin:
    model = models.Operation
    detail_page_url_name = 'browse:operation_detail'
    resource_list_by_type_url_name = 'browse:list_operations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'


class InstrumentXmlDownloadViewMixin:
    model = models.Instrument
    detail_page_url_name = 'browse:instrument_detail'
    resource_list_by_type_url_name = 'browse:list_instruments'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'


class AcquisitionCapabilitiesXmlDownloadViewMixin:
    model = models.AcquisitionCapabilities
    detail_page_url_name = 'browse:acquisition_capability_set_detail'
    resource_list_by_type_url_name = 'browse:list_acquisition_capability_sets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'


class AcquisitionXmlDownloadViewMixin:
    model = models.Acquisition
    detail_page_url_name = 'browse:acquisition_detail'
    resource_list_by_type_url_name = 'browse:list_acquisitions'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'


class ComputationCapabilitiesXmlDownloadViewMixin:
    model = models.ComputationCapabilities
    detail_page_url_name = 'browse:computation_capability_set_detail'
    resource_list_by_type_url_name = 'browse:list_computation_capability_sets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'


class ComputationXmlDownloadViewMixin:
    model = models.Computation
    detail_page_url_name = 'browse:computation_detail'
    resource_list_by_type_url_name = 'browse:list_computations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'


class ProcessXmlDownloadViewMixin:
    model = models.Process
    detail_page_url_name = 'browse:process_detail'
    resource_list_by_type_url_name = 'browse:list_processes'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'


class DataCollectionXmlDownloadViewMixin:
    model = models.DataCollection
    detail_page_url_name = 'browse:data_collection_detail'
    resource_list_by_type_url_name = 'browse:list_data_collections'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'


class StaticDatasetRelatedDownloadViewMixin:
    resource_management_category_list_page_breadcrumb_text = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:static_dataset_related_metadata_index'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_list_page_breadcrumb_text'] = models.StaticDataset.type_plural_readable.title()
        return context


class StaticDatasetEntryXmlDownloadViewMixin(StaticDatasetRelatedDownloadViewMixin):
    model = models.StaticDatasetEntry
    detail_page_url_name = 'browse:static_dataset_entry_detail'
    resource_list_by_type_url_name = 'browse:static_dataset_tree'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:static_dataset_entries'


class DataSubsetXmlDownloadViewMixin(StaticDatasetRelatedDownloadViewMixin):
    model = models.DataSubset
    detail_page_url_name = 'browse:data_subset_detail'
    resource_list_by_type_url_name = 'browse:static_dataset_tree'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_subsets'


class WorkflowXmlDownloadViewMixin:
    model = models.Workflow
    detail_page_url_name = 'browse:workflow_detail'
    resource_list_by_type_url_name = 'browse:list_workflows'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'