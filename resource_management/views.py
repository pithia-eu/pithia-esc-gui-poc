import pymongo
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from common.mongodb_models import (
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
    CurrentCatalogue,
    CurrentCatalogueEntry,
    CurrentCatalogueDataSubset,
)

from search.helpers import remove_underscore_from_id_attribute

_INDEX_PAGE_TITLE = 'Register & Manage Metadata'
_DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE = 'Data Collection-related Metadata'
_CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE = 'Catalogue-related Metadata'

def _create_manage_resource_page_title(resource_type_plural):
    return f'Register & Manage {resource_type_plural.title()}'

# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': _INDEX_PAGE_TITLE
    })

def data_collection_related_metadata_index(request):
    num_current_organsations = CurrentOrganisation.count_documents({})
    num_current_individuals = CurrentIndividual.count_documents({})
    num_current_projects = CurrentProject.count_documents({})
    num_current_platforms = CurrentPlatform.count_documents({})
    num_current_instruments = CurrentInstrument.count_documents({})
    num_current_operations = CurrentOperation.count_documents({})
    num_current_acquisition_capabilities = CurrentAcquisitionCapability.count_documents({})
    num_current_acquisitions = CurrentAcquisition.count_documents({})
    num_current_computation_capabilities = CurrentComputationCapability.count_documents({})
    num_current_computations = CurrentComputation.count_documents({})
    num_current_processes = CurrentProcess.count_documents({})
    num_current_data_collections = CurrentDataCollection.count_documents({})
    return render(request, 'resource_management/data_collection_index.html', {
        'num_current_organisations': num_current_organsations,
        'num_current_individuals': num_current_individuals,
        'num_current_projects': num_current_projects,
        'num_current_platforms': num_current_platforms,
        'num_current_instruments': num_current_instruments,
        'num_current_operations': num_current_operations,
        'num_current_acquisition_capabilities': num_current_acquisition_capabilities,
        'num_current_acquisitions': num_current_acquisitions,
        'num_current_computation_capabilities': num_current_computation_capabilities,
        'num_current_computations': num_current_computations,
        'num_current_processes': num_current_processes,
        'num_current_data_collections': num_current_data_collections,
        'title': _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
        'index_page_url_name_breadcrumb': 'resource_management:index',
        'index_page_title_breadcrumb': _INDEX_PAGE_TITLE,
    })

def catalogue_related_metadata_index(request):
    num_current_catalogues = CurrentCatalogue.count_documents({})
    num_current_catalogue_entries = CurrentCatalogueEntry.count_documents({})
    num_current_catalogue_data_subsets = CurrentCatalogueDataSubset.count_documents({})
    return render(request, 'resource_management/catalogue_index.html', {
        'num_current_catalogues': num_current_catalogues,
        'num_current_catalogue_entries': num_current_catalogue_entries,
        'num_current_catalogue_data_subsets': num_current_catalogue_data_subsets,
        'title': _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
        'index_page_url_name_breadcrumb': 'resource_management:index',
        'index_page_title_breadcrumb': _INDEX_PAGE_TITLE,
    })

class ResourceManagementListView(TemplateView):
    template_name = 'resource_management/list_resources_of_type.html'
    resource_mongodb_model = None
    resource_type_plural = 'Resources'
    title = f'Manage {resource_type_plural}'
    resource_list = []
    resource_delete_page_url_name = ''
    resource_update_page_url_name = ''
    resource_register_page_url_name = ''
    resource_xml_download_page_url_name = ''
    resource_management_category_list_breadcrumb_text = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_breadcrumb_url_name = 'resource_management:data_collection_related_metadata_index'

    def get_resource_list(self):
        resource_list = list(self.resource_mongodb_model.find({}))
        return list(map(remove_underscore_from_id_attribute, resource_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['resource_type_plural'] = self.resource_type_plural
        context['resource_list'] = self.get_resource_list()
        context['empty_resource_list_text'] = f'No {self.resource_type_plural.lower()} have been registered with the e-Science Centre.'
        context['resource_delete_page_url_name'] = self.resource_delete_page_url_name
        context['resource_update_page_url_name'] = self.resource_update_page_url_name
        context['resource_register_page_url_name'] = self.resource_register_page_url_name
        context['resource_xml_download_page_url_name'] = self.resource_xml_download_page_url_name
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_breadcrumb_text'] = self.resource_management_category_list_breadcrumb_text
        context['resource_management_category_list_breadcrumb_url_name'] = self.resource_management_category_list_breadcrumb_url_name
        return context

class organisations(ResourceManagementListView):
    title = _create_manage_resource_page_title('organisations')
    resource_mongodb_model = CurrentOrganisation
    resource_type_plural = 'Organisations'
    resource_delete_page_url_name = 'delete:organisation'
    resource_update_page_url_name = 'update:organisation'
    resource_register_page_url_name = 'register:organisation'
    resource_xml_download_page_url_name = 'utils:view_organisation_as_xml'

class individuals(ResourceManagementListView):
    title = _create_manage_resource_page_title('individuals')
    resource_mongodb_model = CurrentIndividual
    resource_type_plural = 'Individuals'
    resource_delete_page_url_name = 'delete:individual'
    resource_update_page_url_name = 'update:individual'
    resource_register_page_url_name = 'register:individual'
    resource_xml_download_page_url_name = 'utils:view_individual_as_xml'

class projects(ResourceManagementListView):
    title = _create_manage_resource_page_title('projects')
    resource_mongodb_model = CurrentProject
    resource_type_plural = 'Projects'
    resource_delete_page_url_name = 'delete:project'
    resource_update_page_url_name = 'update:project'
    resource_register_page_url_name = 'register:project'
    resource_xml_download_page_url_name = 'utils:view_project_as_xml'

class platforms(ResourceManagementListView):
    template_name = 'resource_management/list_platforms.html'
    title = _create_manage_resource_page_title('platforms')
    resource_mongodb_model = CurrentPlatform
    resource_type_plural = 'Platforms'
    resource_delete_page_url_name = 'delete:platform'
    resource_update_page_url_name = 'update:platform'
    resource_register_page_url_name = 'register:platform'
    resource_xml_download_page_url_name = 'utils:view_platform_as_xml'

    def get_resource_list(self):
        resource_list = list(self.resource_mongodb_model.find({}).sort([
            ('name', pymongo.ASCENDING)
        ]))
        return list(map(remove_underscore_from_id_attribute, resource_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pithia_platforms, non_pithia_platforms = [], []
        for p in context['resource_list']:
            pithia_platforms.append(p) if p['identifier']['PITHIA_Identifier']['namespace'] == 'pithia' else non_pithia_platforms.append(p)
        context['pithia_platforms'] = pithia_platforms
        context['non_pithia_platforms'] = non_pithia_platforms
        return context

class operations(ResourceManagementListView):
    title = _create_manage_resource_page_title('operations')
    resource_mongodb_model = CurrentOperation
    resource_type_plural = 'Operations'
    resource_delete_page_url_name = 'delete:operation'
    resource_update_page_url_name = 'update:operation'
    resource_register_page_url_name = 'register:operation'
    resource_xml_download_page_url_name = 'utils:view_operation_as_xml'

class instruments(ResourceManagementListView):
    title = _create_manage_resource_page_title('instruments')
    resource_mongodb_model = CurrentInstrument
    resource_type_plural = 'Instruments'
    resource_delete_page_url_name = 'delete:instrument'
    resource_update_page_url_name = 'update:instrument'
    resource_register_page_url_name = 'register:instrument'
    resource_xml_download_page_url_name = 'utils:view_instrument_as_xml'

class acquisition_capabilities(ResourceManagementListView):
    title = _create_manage_resource_page_title('acquisition capabilities')
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    resource_delete_page_url_name = 'delete:acquisition_capability'
    resource_update_page_url_name = 'update:acquisition_capability'
    resource_register_page_url_name = 'register:acquisition_capability'
    resource_xml_download_page_url_name = 'utils:view_acquisition_capability_as_xml'

class acquisitions(ResourceManagementListView):
    title = _create_manage_resource_page_title('acquisitions')
    resource_mongodb_model = CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    resource_delete_page_url_name = 'delete:acquisition'
    resource_update_page_url_name = 'update:acquisition'
    resource_register_page_url_name = 'register:acquisition'
    resource_xml_download_page_url_name = 'utils:view_acquisition_as_xml'

class computation_capabilities(ResourceManagementListView):
    title = _create_manage_resource_page_title('computation capabilities')
    resource_mongodb_model = CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    resource_delete_page_url_name = 'delete:computation_capability'
    resource_update_page_url_name = 'update:computation_capability'
    resource_register_page_url_name = 'register:computation_capability'
    resource_xml_download_page_url_name = 'utils:view_computation_capability_as_xml'

class computations(ResourceManagementListView):
    title = _create_manage_resource_page_title('computations')
    resource_mongodb_model = CurrentComputation
    resource_type_plural = 'Computations'
    resource_delete_page_url_name = 'delete:computation'
    resource_update_page_url_name = 'update:computation'
    resource_register_page_url_name = 'register:computation'
    resource_xml_download_page_url_name = 'utils:view_computation_as_xml'

class processes(ResourceManagementListView):
    title = _create_manage_resource_page_title('processes')
    resource_mongodb_model = CurrentProcess
    resource_type_plural = 'Processes'
    resource_delete_page_url_name = 'delete:process'
    resource_update_page_url_name = 'update:process'
    resource_register_page_url_name = 'register:process'
    resource_xml_download_page_url_name = 'utils:view_process_as_xml'

class data_collections(ResourceManagementListView):
    title = _create_manage_resource_page_title('data collections')
    resource_mongodb_model = CurrentDataCollection
    resource_type_plural = 'Data Collections'
    resource_delete_page_url_name = 'delete:data_collection'
    resource_update_page_url_name = 'update:data_collection'
    resource_register_page_url_name = 'register:data_collection'
    resource_xml_download_page_url_name = 'utils:view_data_collection_as_xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_method_update_page_url_name'] = 'update:data_collection_interaction_methods'
        return context

class catalogues(ResourceManagementListView):
    title = _create_manage_resource_page_title('catalogues')
    resource_mongodb_model = CurrentCatalogue
    resource_type_plural = 'Catalogues'
    resource_delete_page_url_name = 'delete:catalogue'
    resource_update_page_url_name = 'update:catalogue'
    resource_register_page_url_name = 'register:catalogue'
    resource_xml_download_page_url_name = 'utils:view_catalogue_as_xml'
    resource_management_category_list_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'

class catalogue_entries(ResourceManagementListView):
    title = _create_manage_resource_page_title('catalogue entries')
    resource_mongodb_model = CurrentCatalogueEntry
    resource_type_plural = 'Catalogue Entries'
    resource_delete_page_url_name = 'delete:catalogue_entry'
    resource_update_page_url_name = 'update:catalogue_entry'
    resource_register_page_url_name = 'register:catalogue_entry'
    resource_xml_download_page_url_name = 'utils:view_catalogue_entry_as_xml'
    resource_management_category_list_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'

class catalogue_data_subsets(ResourceManagementListView):
    title = _create_manage_resource_page_title('catalogue data subsets')
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_type_plural = 'Catalogue Data Subsets'
    resource_delete_page_url_name = 'delete:catalogue_data_subset'
    resource_update_page_url_name = 'update:catalogue_data_subset'
    resource_register_page_url_name = 'register:catalogue_data_subset'
    resource_xml_download_page_url_name = 'utils:view_catalogue_data_subset_as_xml'
    resource_management_category_list_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'
