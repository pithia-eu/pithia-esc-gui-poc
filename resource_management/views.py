from django.shortcuts import render
from django.views.generic import ListView

from common import models
from user_management.services import (
    get_logged_in_user_institution_id,
)

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
    institution_id = get_logged_in_user_institution_id(request)

    num_current_organsations = models.Organisation.objects.owned_by_institution(institution_id).count()
    num_current_individuals = models.Individual.objects.owned_by_institution(institution_id).count()
    num_current_projects = models.Project.objects.owned_by_institution(institution_id).count()
    num_current_platforms = models.Platform.objects.owned_by_institution(institution_id).count()
    num_current_operations = models.Operation.objects.owned_by_institution(institution_id).count()
    num_current_instruments = models.Instrument.objects.owned_by_institution(institution_id).count()
    num_current_acquisition_capability_sets = models.AcquisitionCapabilities.objects.owned_by_institution(institution_id).count()
    num_current_acquisitions = models.Acquisition.objects.owned_by_institution(institution_id).count()
    num_current_computation_capability_sets = models.ComputationCapabilities.objects.owned_by_institution(institution_id).count()
    num_current_computations = models.Computation.objects.owned_by_institution(institution_id).count()
    num_current_processes = models.Process.objects.owned_by_institution(institution_id).count()
    num_current_data_collections = models.DataCollection.objects.owned_by_institution(institution_id).count()
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
    institution_id = get_logged_in_user_institution_id(request)
    
    num_current_catalogues = models.Catalogue.objects.owned_by_institution(institution_id).count()
    num_current_catalogue_entries = models.CatalogueEntry.objects.owned_by_institution(institution_id).count()
    num_current_catalogue_data_subsets = models.CatalogueDataSubset.objects.owned_by_institution(institution_id).count()
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
    
    resource_delete_page_url_name = ''
    resource_update_page_url_name = ''
    resource_register_page_url_name = ''
    resource_xml_download_page_url_name = ''
    resource_management_category_list_page_breadcrumb_text = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:data_collection_related_metadata_index'

    def get(self, request, *args, **kwargs):
        self.institution_id = get_logged_in_user_institution_id(request)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.owned_by_institution(self.institution_id).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _create_manage_resource_page_title(self.model.type_plural_readable)
        context['resource_type_plural'] = self.model.type_plural_readable
        context['empty_resource_list_text'] = f'No {self.model.type_plural_readable.lower()} have been registered with the e-Science Centre.'
        context['resource_delete_page_url_name'] = self.resource_delete_page_url_name
        context['resource_update_page_url_name'] = self.resource_update_page_url_name
        context['resource_register_page_url_name'] = self.resource_register_page_url_name
        context['resource_xml_download_page_url_name'] = self.resource_xml_download_page_url_name
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = self.resource_management_category_list_page_breadcrumb_text
        context['resource_management_category_list_page_breadcrumb_url_name'] = self.resource_management_category_list_page_breadcrumb_url_name
        return context

class OrganisationManagementListView(ResourceManagementListView):
    model = models.Organisation

    resource_delete_page_url_name = 'delete:organisation'
    resource_update_page_url_name = 'update:organisation'
    resource_register_page_url_name = 'register:organisation'
    resource_xml_download_page_url_name = 'utils:view_organisation_as_xml'

class IndividualManagementListView(ResourceManagementListView):
    model = models.Individual

    resource_delete_page_url_name = 'delete:individual'
    resource_update_page_url_name = 'update:individual'
    resource_register_page_url_name = 'register:individual'
    resource_xml_download_page_url_name = 'utils:view_individual_as_xml'

class ProjectManagementListView(ResourceManagementListView):
    model = models.Project

    resource_delete_page_url_name = 'delete:project'
    resource_update_page_url_name = 'update:project'
    resource_register_page_url_name = 'register:project'
    resource_xml_download_page_url_name = 'utils:view_project_as_xml'

class PlatformManagementListView(ResourceManagementListView):
    model = models.Platform
    template_name = 'resource_management/platform_management_list.html'

    resource_delete_page_url_name = 'delete:platform'
    resource_update_page_url_name = 'update:platform'
    resource_register_page_url_name = 'register:platform'
    resource_xml_download_page_url_name = 'utils:view_platform_as_xml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pithia_platforms, non_pithia_platforms = [], []
        for r in context['resources']:
            if r.namespace == 'pithia':
                pithia_platforms.append(r)
            else:
                non_pithia_platforms.append(r)
        context['pithia_platforms'] = pithia_platforms
        context['non_pithia_platforms'] = non_pithia_platforms
        context['no_platform_networks_message'] = 'No platform networks have been registered with the e-Science Centre.'
        context['no_platforms_message'] = 'No individual platforms have been registered with the e-Science Centre.'
        return context

class OperationManagementListView(ResourceManagementListView):
    model = models.Operation

    resource_delete_page_url_name = 'delete:operation'
    resource_update_page_url_name = 'update:operation'
    resource_register_page_url_name = 'register:operation'
    resource_xml_download_page_url_name = 'utils:view_operation_as_xml'

class InstrumentManagementListView(ResourceManagementListView):
    model = models.Instrument

    resource_delete_page_url_name = 'delete:instrument'
    resource_update_page_url_name = 'update:instrument'
    resource_register_page_url_name = 'register:instrument'
    resource_xml_download_page_url_name = 'utils:view_instrument_as_xml'

class AcquisitionCapabilitiesManagementListView(ResourceManagementListView):
    model = models.AcquisitionCapabilities

    resource_delete_page_url_name = 'delete:acquisition_capability_set'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    resource_register_page_url_name = 'register:acquisition_capability_set'
    resource_xml_download_page_url_name = 'utils:view_acquisition_capability_set_as_xml'

class AcquisitionManagementListView(ResourceManagementListView):
    model = models.Acquisition

    resource_delete_page_url_name = 'delete:acquisition'
    resource_update_page_url_name = 'update:acquisition'
    resource_register_page_url_name = 'register:acquisition'
    resource_xml_download_page_url_name = 'utils:view_acquisition_as_xml'

class ComputationCapabilitiesManagementListView(ResourceManagementListView):
    model = models.ComputationCapabilities

    resource_delete_page_url_name = 'delete:computation_capability_set'
    resource_update_page_url_name = 'update:computation_capability_set'
    resource_register_page_url_name = 'register:computation_capability_set'
    resource_xml_download_page_url_name = 'utils:view_computation_capability_set_as_xml'

class ComputationManagementListView(ResourceManagementListView):
    model = models.Computation

    resource_delete_page_url_name = 'delete:computation'
    resource_update_page_url_name = 'update:computation'
    resource_register_page_url_name = 'register:computation'
    resource_xml_download_page_url_name = 'utils:view_computation_as_xml'

class ProcessManagementListView(ResourceManagementListView):
    model = models.Process

    resource_delete_page_url_name = 'delete:process'
    resource_update_page_url_name = 'update:process'
    resource_register_page_url_name = 'register:process'
    resource_xml_download_page_url_name = 'utils:view_process_as_xml'

class DataCollectionManagementListView(ResourceManagementListView):
    model = models.DataCollection

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

    resource_delete_page_url_name = 'delete:catalogue'
    resource_update_page_url_name = 'update:catalogue'
    resource_register_page_url_name = 'register:catalogue'
    resource_xml_download_page_url_name = 'utils:view_catalogue_as_xml'
    resource_management_category_list_page_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'

class CatalogueEntryManagementListView(ResourceManagementListView):
    model = models.CatalogueEntry

    resource_delete_page_url_name = 'delete:catalogue_entry'
    resource_update_page_url_name = 'update:catalogue_entry'
    resource_register_page_url_name = 'register:catalogue_entry'
    resource_xml_download_page_url_name = 'utils:view_catalogue_entry_as_xml'
    resource_management_category_list_page_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'

class CatalogueDataSubsetManagementListView(ResourceManagementListView):
    model = models.CatalogueDataSubset

    resource_delete_page_url_name = 'delete:catalogue_data_subset'
    resource_update_page_url_name = 'update:catalogue_data_subset'
    resource_register_page_url_name = 'register:catalogue_data_subset'
    resource_xml_download_page_url_name = 'utils:view_catalogue_data_subset_as_xml'
    resource_management_category_list_page_breadcrumb_text = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:catalogue_related_metadata_index'
