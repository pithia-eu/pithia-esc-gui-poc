import pymongo
from django.shortcuts import render
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
_DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE = 'Register & Manage Data Collection-related Metadata'
_CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE = 'Register & Manage Catalogue-related Metadata'

def _create_manage_resource_page_title(resource_type_plural):
    return f'Register & Manage {resource_type_plural.title()}'

# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': _INDEX_PAGE_TITLE
    })

def data_collection_related_registrations_index(request):
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
    })

def catalogue_related_registrations_index(request):
    num_current_catalogues = CurrentCatalogue.count_documents({})
    num_current_catalogue_entries = CurrentCatalogueEntry.count_documents({})
    num_current_catalogue_data_subsets = CurrentCatalogueDataSubset.count_documents({})
    return render(request, 'resource_management/catalogue_index.html', {
        'num_current_catalogues': num_current_catalogues,
        'num_current_catalogue_entries': num_current_catalogue_entries,
        'num_current_catalogue_data_subsets': num_current_catalogue_data_subsets,
        'title': _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
    })

class ResourceManagementListView(TemplateView):
    template_name = 'resource_management/list_resources_of_type.html'
    resource_mongodb_model = None
    resource_type_plural = 'Resources'
    title = f'Manage {resource_type_plural}'
    resources_list = []
    delete_resource_view_name = ''
    update_resource_view_name = ''
    register_resource_view_name = ''
    view_as_xml_view_name = ''

    def get_resources_list(self):
        resources_list = list(self.resource_mongodb_model.find({}))
        return list(map(remove_underscore_from_id_attribute, resources_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['resource_type_plural'] = self.resource_type_plural
        context['resources_list'] = self.get_resources_list()
        context['delete_resource_view_name'] = self.delete_resource_view_name
        context['update_resource_view_name'] = self.update_resource_view_name
        context['register_resource_view_name'] = self.register_resource_view_name
        context['index_page_title'] = _INDEX_PAGE_TITLE
        context['view_as_xml_view_name'] = self.view_as_xml_view_name
        return context

class organisations(ResourceManagementListView):
    title = _create_manage_resource_page_title('organisations')
    resource_mongodb_model = CurrentOrganisation
    resource_type_plural = 'Organisations'
    delete_resource_view_name = 'delete:organisation'
    update_resource_view_name = 'update:organisation'
    register_resource_view_name = 'register:organisation'
    view_as_xml_view_name = 'utils:view_organisation_as_xml'

class individuals(ResourceManagementListView):
    title = _create_manage_resource_page_title('individuals')
    resource_mongodb_model = CurrentIndividual
    resource_type_plural = 'Individuals'
    delete_resource_view_name = 'delete:individual'
    update_resource_view_name = 'update:individual'
    register_resource_view_name = 'register:individual'
    view_as_xml_view_name = 'utils:view_individual_as_xml'

class projects(ResourceManagementListView):
    title = _create_manage_resource_page_title('projects')
    resource_mongodb_model = CurrentProject
    resource_type_plural = 'Projects'
    delete_resource_view_name = 'delete:project'
    update_resource_view_name = 'update:project'
    register_resource_view_name = 'register:project'
    view_as_xml_view_name = 'utils:view_project_as_xml'

class platforms(ResourceManagementListView):
    template_name = 'resource_management/list_platforms.html'
    title = _create_manage_resource_page_title('platforms')
    resource_mongodb_model = CurrentPlatform
    resource_type_plural = 'PLatforms'
    delete_resource_view_name = 'delete:platform'
    update_resource_view_name = 'update:platform'
    register_resource_view_name = 'register:platform'
    view_as_xml_view_name = 'utils:view_platform_as_xml'

    def get_resources_list(self):
        resources_list = list(self.resource_mongodb_model.find({}).sort([
            ('name', pymongo.ASCENDING)
        ]))
        return list(map(remove_underscore_from_id_attribute, resources_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pithia_platforms, non_pithia_platforms = [], []
        for p in context['resources_list']:
            pithia_platforms.append(p) if p['identifier']['PITHIA_Identifier']['namespace'] == 'pithia' else non_pithia_platforms.append(p)
        context['pithia_platforms'] = pithia_platforms
        context['non_pithia_platforms'] = non_pithia_platforms
        return context

class operations(ResourceManagementListView):
    title = _create_manage_resource_page_title('operations')
    resource_mongodb_model = CurrentOperation
    resource_type_plural = 'Operations'
    delete_resource_view_name = 'delete:operation'
    update_resource_view_name = 'update:operation'
    register_resource_view_name = 'register:operation'
    view_as_xml_view_name = 'utils:view_operation_as_xml'

class instruments(ResourceManagementListView):
    title = _create_manage_resource_page_title('instruments')
    resource_mongodb_model = CurrentInstrument
    resource_type_plural = 'Instruments'
    delete_resource_view_name = 'delete:instrument'
    update_resource_view_name = 'update:instrument'
    register_resource_view_name = 'register:instrument'
    view_as_xml_view_name = 'utils:view_instrument_as_xml'

class acquisition_capabilities(ResourceManagementListView):
    title = _create_manage_resource_page_title('acquisition capabilities')
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    delete_resource_view_name = 'delete:acquisition_capability'
    update_resource_view_name = 'update:acquisition_capability'
    register_resource_view_name = 'register:acquisition_capability'
    view_as_xml_view_name = 'utils:view_acquisition_capability_as_xml'

class acquisitions(ResourceManagementListView):
    title = _create_manage_resource_page_title('acquisitions')
    resource_mongodb_model = CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    delete_resource_view_name = 'delete:acquisition'
    update_resource_view_name = 'update:acquisition'
    register_resource_view_name = 'register:acquisition'
    view_as_xml_view_name = 'utils:view_acquisition_as_xml'

class computation_capabilities(ResourceManagementListView):
    title = _create_manage_resource_page_title('computation capabilities')
    resource_mongodb_model = CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    delete_resource_view_name = 'delete:computation_capability'
    update_resource_view_name = 'update:computation_capability'
    register_resource_view_name = 'register:computation_capability'
    view_as_xml_view_name = 'utils:view_computation_capability_as_xml'

class computations(ResourceManagementListView):
    title = _create_manage_resource_page_title('computations')
    resource_mongodb_model = CurrentComputation
    resource_type_plural = 'Computations'
    delete_resource_view_name = 'delete:computation'
    update_resource_view_name = 'update:computation'
    register_resource_view_name = 'register:computation'
    view_as_xml_view_name = 'utils:view_computation_as_xml'

class processes(ResourceManagementListView):
    title = _create_manage_resource_page_title('processes')
    resource_mongodb_model = CurrentProcess
    resource_type_plural = 'Processes'
    delete_resource_view_name = 'delete:process'
    update_resource_view_name = 'update:process'
    register_resource_view_name = 'register:process'
    view_as_xml_view_name = 'utils:view_process_as_xml'

class data_collections(ResourceManagementListView):
    title = _create_manage_resource_page_title('data collections')
    resource_mongodb_model = CurrentDataCollection
    resource_type_plural = 'Data Collections'
    delete_resource_view_name = 'delete:data_collection'
    update_resource_view_name = 'update:data_collection'
    register_resource_view_name = 'register:data_collection'
    view_as_xml_view_name = 'utils:view_data_collection_as_xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_interaction_methods_view_name'] = 'update:data_collection_interaction_methods'
        return context

class catalogues(ResourceManagementListView):
    title = _create_manage_resource_page_title('catalogues')
    resource_mongodb_model = CurrentCatalogue
    resource_type_plural = 'Catalogues'
    delete_resource_view_name = 'delete:catalogue'
    update_resource_view_name = 'update:catalogue'
    register_resource_view_name = 'register:catalogue'
    view_as_xml_view_name = 'utils:view_catalogue_as_xml'

class catalogue_entries(ResourceManagementListView):
    title = _create_manage_resource_page_title('catalogue entries')
    resource_mongodb_model = CurrentCatalogueEntry
    resource_type_plural = 'Catalogue Entries'
    delete_resource_view_name = 'delete:catalogue_entry'
    update_resource_view_name = 'update:catalogue_entry'
    register_resource_view_name = 'register:catalogue_entry'
    view_as_xml_view_name = 'utils:view_catalogue_entry_as_xml'

class catalogue_data_subsets(ResourceManagementListView):
    title = _create_manage_resource_page_title('catalogue data subsets')
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_type_plural = 'Catalogue Data Subsets'
    delete_resource_view_name = 'delete:catalogue_data_subset'
    update_resource_view_name = 'update:catalogue_data_subset'
    register_resource_view_name = 'register:catalogue_data_subset'
    view_as_xml_view_name = 'utils:view_catalogue_data_subset_as_xml'
