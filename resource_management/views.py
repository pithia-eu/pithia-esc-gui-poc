import pymongo
from django.shortcuts import render
from django.views.generic import ListView

from common import models
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
from utils.mapping_functions import prepare_resource_for_template

_INDEX_PAGE_TITLE = 'Register & Manage Metadata'
_DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE = 'Data Collection-related Metadata'
_CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE = 'Catalogue-related Metadata'

def _create_manage_resource_page_title(resource_type_plural_readable):
    return f'Register & Manage {resource_type_plural_readable.title()}'

# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': _INDEX_PAGE_TITLE
    })

def data_collection_related_metadata_index(request):
    num_current_organsations = models.Organisation.objects.count()
    num_current_individuals = models.Individual.objects.count()
    num_current_projects = models.Project.objects.count()
    num_current_platforms = models.Platform.objects.count()
    num_current_instruments = models.Operation.objects.count()
    num_current_operations = models.Instrument.objects.count()
    num_current_acquisition_capability_sets = models.AcquisitionCapabilities.objects.count()
    num_current_acquisitions = models.Acquisition.objects.count()
    num_current_computation_capability_sets = models.ComputationCapabilities.objects.count()
    num_current_computations = models.Computation.objects.count()
    num_current_processes = models.Process.objects.count()
    num_current_data_collections = models.DataCollection.objects.count()
    # TODO: remove old code
    # num_current_organsations = CurrentOrganisation.estimated_document_count()
    # num_current_individuals = CurrentIndividual.estimated_document_count()
    # num_current_projects = CurrentProject.estimated_document_count()
    # num_current_platforms = CurrentPlatform.estimated_document_count()
    # num_current_instruments = CurrentInstrument.estimated_document_count()
    # num_current_operations = CurrentOperation.estimated_document_count()
    # num_current_acquisition_capability_sets = CurrentAcquisitionCapability.estimated_document_count()
    # num_current_acquisitions = CurrentAcquisition.estimated_document_count()
    # num_current_computation_capability_sets = CurrentComputationCapability.estimated_document_count()
    # num_current_computations = CurrentComputation.estimated_document_count()
    # num_current_processes = CurrentProcess.estimated_document_count()
    # num_current_data_collections = CurrentDataCollection.estimated_document_count()
    return render(request, 'resource_management/data_collection_index.html', {
        'num_current_organisations': num_current_organsations,
        'num_current_individuals': num_current_individuals,
        'num_current_projects': num_current_projects,
        'num_current_platforms': num_current_platforms,
        'num_current_instruments': num_current_instruments,
        'num_current_operations': num_current_operations,
        'num_current_acquisition_capability_sets': num_current_acquisition_capability_sets,
        'num_current_acquisitions': num_current_acquisitions,
        'num_current_computation_capability_sets': num_current_computation_capability_sets,
        'num_current_computations': num_current_computations,
        'num_current_processes': num_current_processes,
        'num_current_data_collections': num_current_data_collections,
        'title': _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
        'index_page_url_name_breadcrumb': 'resource_management:index',
        'index_page_title_breadcrumb': _INDEX_PAGE_TITLE,
    })

def catalogue_related_metadata_index(request):
    num_current_catalogues = models.Catalogue.objects.count()
    num_current_catalogue_entries = models.CatalogueEntry.objects.count()
    num_current_catalogue_data_subsets = models.CatalogueDataSubset.objects.count()
    # TODO: remove old code
    # num_current_catalogues = CurrentCatalogue.estimated_document_count()
    # num_current_catalogue_entries = CurrentCatalogueEntry.estimated_document_count()
    # num_current_catalogue_data_subsets = CurrentCatalogueDataSubset.estimated_document_count()
    return render(request, 'resource_management/catalogue_index.html', {
        'num_current_catalogues': num_current_catalogues,
        'num_current_catalogue_entries': num_current_catalogue_entries,
        'num_current_catalogue_data_subsets': num_current_catalogue_data_subsets,
        'title': _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
        'index_page_url_name_breadcrumb': 'resource_management:index',
        'index_page_title_breadcrumb': _INDEX_PAGE_TITLE,
    })

class ResourceManagementListView(ListView):
    template_name = 'resource_management/resource_management_list_by_type_outer.html'
    context_object_name = 'resources'
    
    resource_mongodb_model = None
    resource_list = []
    resource_delete_page_url_name = ''
    resource_update_page_url_name = ''
    resource_register_page_url_name = ''
    resource_xml_download_page_url_name = ''
    resource_management_category_list_page_breadcrumb_text = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:data_collection_related_metadata_index'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _create_manage_resource_page_title(self.model.type_plural_readable)
        context['resource_type_plural'] = self.model.type_plural_readable
        context['resource_list'] = self.get_resource_list()
        context['empty_resource_list_text'] = f'No {self.model.type_plural_readable.lower()} have been registered with the e-Science Centre.'
        context['resource_delete_page_url_name'] = self.resource_delete_page_url_name
        context['resource_update_page_url_name'] = self.resource_update_page_url_name
        context['resource_register_page_url_name'] = self.resource_register_page_url_name
        context['resource_xml_download_page_url_name'] = self.resource_xml_download_page_url_name
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = self.resource_management_category_list_page_breadcrumb_text
        context['resource_management_category_list_page_breadcrumb_url_name'] = self.resource_management_category_list_page_breadcrumb_url_name
        return context

    def get_resource_list(self):
        resource_list = list(self.resource_mongodb_model.find({}))
        return list(map(prepare_resource_for_template, resource_list))

class OrganisationManagementListView(ResourceManagementListView):
    model = models.Organisation
    resource_mongodb_model = CurrentOrganisation
    resource_delete_page_url_name = 'delete:organisation'
    resource_update_page_url_name = 'update:organisation'
    resource_register_page_url_name = 'register:organisation'
    resource_xml_download_page_url_name = 'utils:view_organisation_as_xml'

class IndividualManagementListView(ResourceManagementListView):
    model = models.Individual
    resource_mongodb_model = CurrentIndividual
    resource_delete_page_url_name = 'delete:individual'
    resource_update_page_url_name = 'update:individual'
    resource_register_page_url_name = 'register:individual'
    resource_xml_download_page_url_name = 'utils:view_individual_as_xml'

class ProjectManagementListView(ResourceManagementListView):
    model = models.Project
    resource_mongodb_model = CurrentProject
    resource_delete_page_url_name = 'delete:project'
    resource_update_page_url_name = 'update:project'
    resource_register_page_url_name = 'register:project'
    resource_xml_download_page_url_name = 'utils:view_project_as_xml'

class PlatformManagementListView(ResourceManagementListView):
    model = models.Platform
    template_name = 'resource_management/platform_management_list.html'
    resource_mongodb_model = CurrentPlatform
    resource_delete_page_url_name = 'delete:platform'
    resource_update_page_url_name = 'update:platform'
    resource_register_page_url_name = 'register:platform'
    resource_xml_download_page_url_name = 'utils:view_platform_as_xml'

    def get_resource_list(self):
        resource_list = list(self.resource_mongodb_model.find({}).sort([
            ('name', pymongo.ASCENDING)
        ]))
        return list(map(prepare_resource_for_template, resource_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pithia_platforms, non_pithia_platforms = [], []
        for p in context['resource_list']:
            pithia_platforms.append(p) if p['identifier']['PITHIA_Identifier']['namespace'] == 'pithia' else non_pithia_platforms.append(p)
        context['pithia_platforms'] = pithia_platforms
        context['non_pithia_platforms'] = non_pithia_platforms
        return context

class OperationManagementListView(ResourceManagementListView):
    model = models.Operation
    resource_mongodb_model = CurrentOperation
    resource_delete_page_url_name = 'delete:operation'
    resource_update_page_url_name = 'update:operation'
    resource_register_page_url_name = 'register:operation'
    resource_xml_download_page_url_name = 'utils:view_operation_as_xml'

class InstrumentManagementListView(ResourceManagementListView):
    model = models.Instrument
    resource_mongodb_model = CurrentInstrument
    resource_delete_page_url_name = 'delete:instrument'
    resource_update_page_url_name = 'update:instrument'
    resource_register_page_url_name = 'register:instrument'
    resource_xml_download_page_url_name = 'utils:view_instrument_as_xml'

class AcquisitionCapabilitiesManagementListView(ResourceManagementListView):
    model = models.AcquisitionCapabilities
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_delete_page_url_name = 'delete:acquisition_capability_set'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    resource_register_page_url_name = 'register:acquisition_capability_set'
    resource_xml_download_page_url_name = 'utils:view_acquisition_capability_set_as_xml'

class AcquisitionManagementListView(ResourceManagementListView):
    model = models.Acquisition
    resource_mongodb_model = CurrentAcquisition
    resource_delete_page_url_name = 'delete:acquisition'
    resource_update_page_url_name = 'update:acquisition'
    resource_register_page_url_name = 'register:acquisition'
    resource_xml_download_page_url_name = 'utils:view_acquisition_as_xml'

class ComputationCapabilitiesManagementListView(ResourceManagementListView):
    model = models.ComputationCapabilities
    resource_mongodb_model = CurrentComputationCapability
    resource_delete_page_url_name = 'delete:computation_capability_set'
    resource_update_page_url_name = 'update:computation_capability_set'
    resource_register_page_url_name = 'register:computation_capability_set'
    resource_xml_download_page_url_name = 'utils:view_computation_capability_set_as_xml'

class ComputationManagementListView(ResourceManagementListView):
    model = models.Computation
    resource_mongodb_model = CurrentComputation
    resource_delete_page_url_name = 'delete:computation'
    resource_update_page_url_name = 'update:computation'
    resource_register_page_url_name = 'register:computation'
    resource_xml_download_page_url_name = 'utils:view_computation_as_xml'

class ProcessManagementListView(ResourceManagementListView):
    model = models.Process
    resource_mongodb_model = CurrentProcess
    resource_delete_page_url_name = 'delete:process'
    resource_update_page_url_name = 'update:process'
    resource_register_page_url_name = 'register:process'
    resource_xml_download_page_url_name = 'utils:view_process_as_xml'

class DataCollectionManagementListView(ResourceManagementListView):
    model = models.DataCollection
    resource_mongodb_model = CurrentDataCollection
    resource_delete_page_url_name = 'delete:data_collection'
    resource_update_page_url_name = 'update:data_collection'
    resource_register_page_url_name = 'register:data_collection'
    resource_xml_download_page_url_name = 'utils:view_data_collection_as_xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_method_update_page_url_name'] = 'update:data_collection_interaction_methods'
        return context

class CatalogueManagementListView(ResourceManagementListView):
    model = models.Catalogue
    resource_mongodb_model = CurrentCatalogue
    resource_delete_page_url_name = 'delete:catalogue'
    resource_update_page_url_name = 'update:catalogue'
    resource_register_page_url_name = 'register:catalogue'
    resource_xml_download_page_url_name = 'utils:view_catalogue_as_xml'
    resource_management_category_list_page_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'

class CatalogueEntryManagementListView(ResourceManagementListView):
    model = models.CatalogueEntry
    resource_mongodb_model = CurrentCatalogueEntry
    resource_delete_page_url_name = 'delete:catalogue_entry'
    resource_update_page_url_name = 'update:catalogue_entry'
    resource_register_page_url_name = 'register:catalogue_entry'
    resource_xml_download_page_url_name = 'utils:view_catalogue_entry_as_xml'
    resource_management_category_list_page_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'

class CatalogueDataSubsetManagementListView(ResourceManagementListView):
    model = models.CatalogueDataSubset
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_delete_page_url_name = 'delete:catalogue_data_subset'
    resource_update_page_url_name = 'update:catalogue_data_subset'
    resource_register_page_url_name = 'register:catalogue_data_subset'
    resource_xml_download_page_url_name = 'utils:view_catalogue_data_subset_as_xml'
    resource_management_category_list_page_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'
