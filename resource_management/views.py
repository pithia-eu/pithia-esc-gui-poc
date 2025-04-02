from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from common import models
from common.decorators import login_session_institution_required
from user_management.services import (
    get_institution_id_for_login_session,
    get_members_by_institution_id,
)

_INDEX_PAGE_TITLE = 'Manage Registrations'
_DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE = 'Data Collection-related Metadata'
_STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE = 'Static Dataset-related Metadata'

def _create_manage_resource_page_title(resource_type_plural_readable):
    return resource_type_plural_readable.title()

# Create your views here.
@login_session_institution_required
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'data_collection_related_index_page_title': _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    })

@login_session_institution_required
def data_collection_related_metadata_index(request):
    institution_id = get_institution_id_for_login_session(request.session)

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

@login_session_institution_required
def static_dataset_related_metadata_index(request):
    institution_id = get_institution_id_for_login_session(request.session)
    
    num_current_static_datasets = models.StaticDataset.objects.owned_by_institution(institution_id).count()
    num_current_static_dataset_entries = models.StaticDatasetEntry.objects.owned_by_institution(institution_id).count()
    num_current_data_subsets = models.DataSubset.objects.owned_by_institution(institution_id).count()
    return render(request, 'resource_management/static_dataset_index.html', {
        'num_current_static_datasets': num_current_static_datasets,
        'num_current_static_dataset_entries': num_current_static_dataset_entries,
        'num_current_data_subsets': num_current_data_subsets,
        'title': _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE,
        'index_page_url_name_breadcrumb': 'resource_management:index',
        'index_page_title_breadcrumb': _INDEX_PAGE_TITLE,
    })

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceManagementListView(ListView):
    template_name = 'resource_management/resource_management_list_by_type_outer.html'
    context_object_name = 'resources'
    
    resource_delete_page_url_name = ''
    resource_update_page_url_name = ''
    resource_update_with_wizard_page_url_name = ''
    resource_register_page_url_name = ''
    resource_register_with_editor_name = ''
    resource_xml_download_page_url_name = ''
    resource_management_category_list_page_breadcrumb_text = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:data_collection_related_metadata_index'

    def get(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.owned_by_institution(self.institution_id).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _create_manage_resource_page_title(self.model.type_plural_readable)
        context['description'] = self.model.type_description_readable
        context['resource_type_plural'] = self.model.type_plural_readable
        context['empty_resource_list_text'] = f'No {self.model.type_plural_readable.lower()} have been registered by your institution.'
        context['institution_members_by_id'] = {im['edu_person_unique_id']: im['name'] for im in get_members_by_institution_id(self.institution_id)}
        context['resource_delete_page_url_name'] = self.resource_delete_page_url_name
        context['resource_update_page_url_name'] = self.resource_update_page_url_name
        context['resource_update_with_wizard_page_url_name'] = self.resource_update_with_wizard_page_url_name
        context['resource_register_page_url_name'] = self.resource_register_page_url_name
        context['resource_register_with_editor_name'] = self.resource_register_with_editor_name
        context['resource_xml_download_page_url_name'] = self.resource_xml_download_page_url_name
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = self.resource_management_category_list_page_breadcrumb_text
        context['resource_management_category_list_page_breadcrumb_url_name'] = self.resource_management_category_list_page_breadcrumb_url_name
        return context

class OrganisationManagementListView(ResourceManagementListView):
    model = models.Organisation

    resource_delete_page_url_name = 'delete:organisation'
    resource_update_page_url_name = 'update:organisation'
    resource_update_with_wizard_page_url_name = 'update:organisation_with_editor'
    resource_register_page_url_name = 'register:organisation'
    resource_register_with_editor_name = 'register:organisation_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_organisation_as_xml_with_editing'

class IndividualManagementListView(ResourceManagementListView):
    model = models.Individual

    resource_delete_page_url_name = 'delete:individual'
    resource_update_page_url_name = 'update:individual'
    resource_update_with_wizard_page_url_name = 'update:individual_with_editor'
    resource_register_page_url_name = 'register:individual'
    resource_register_with_editor_name = 'register:individual_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_individual_as_xml_with_editing'

class ProjectManagementListView(ResourceManagementListView):
    model = models.Project

    resource_delete_page_url_name = 'delete:project'
    resource_update_page_url_name = 'update:project'
    resource_update_with_wizard_page_url_name = 'update:project_with_editor'
    resource_register_page_url_name = 'register:project'
    resource_register_with_editor_name = 'register:project_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_project_as_xml_with_editing'

class PlatformManagementListView(ResourceManagementListView):
    model = models.Platform
    template_name = 'resource_management/platform_management_list_outer.html'

    resource_delete_page_url_name = 'delete:platform'
    resource_update_page_url_name = 'update:platform'
    resource_update_with_wizard_page_url_name = 'update:platform_with_editor'
    resource_register_page_url_name = 'register:platform'
    resource_register_with_editor_name = 'register:platform_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_platform_as_xml_with_editing'

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
        context['no_platform_networks_message'] = 'No platform networks have been registered by your institution.'
        context['no_platforms_message'] = 'No individual platforms have been registered by your institution.'
        return context

class OperationManagementListView(ResourceManagementListView):
    model = models.Operation

    resource_delete_page_url_name = 'delete:operation'
    resource_update_page_url_name = 'update:operation'
    resource_update_with_wizard_page_url_name = 'update:operation_with_editor'
    resource_register_page_url_name = 'register:operation'
    resource_register_with_editor_name = 'register:operation_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_operation_as_xml_with_editing'

class InstrumentManagementListView(ResourceManagementListView):
    model = models.Instrument

    resource_delete_page_url_name = 'delete:instrument'
    resource_update_page_url_name = 'update:instrument'
    resource_update_with_wizard_page_url_name = 'update:instrument_with_editor'
    resource_register_page_url_name = 'register:instrument'
    resource_register_with_editor_name = 'register:instrument_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_instrument_as_xml_with_editing'

class AcquisitionCapabilitiesManagementListView(ResourceManagementListView):
    model = models.AcquisitionCapabilities

    resource_delete_page_url_name = 'delete:acquisition_capability_set'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    resource_update_with_wizard_page_url_name = 'update:acquisition_capability_set_with_editor'
    resource_register_page_url_name = 'register:acquisition_capability_set'
    resource_register_with_editor_name = 'register:acquisition_capability_set_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_acquisition_capability_set_as_xml_with_editing'

class AcquisitionManagementListView(ResourceManagementListView):
    model = models.Acquisition

    resource_delete_page_url_name = 'delete:acquisition'
    resource_update_page_url_name = 'update:acquisition'
    resource_update_with_wizard_page_url_name = 'update:acquisition_with_editor'
    resource_register_page_url_name = 'register:acquisition'
    resource_register_with_editor_name = 'register:acquisition_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_acquisition_as_xml_with_editing'

class ComputationCapabilitiesManagementListView(ResourceManagementListView):
    model = models.ComputationCapabilities

    resource_delete_page_url_name = 'delete:computation_capability_set'
    resource_update_page_url_name = 'update:computation_capability_set'
    resource_update_with_wizard_page_url_name = 'update:computation_capability_set_with_editor'
    resource_register_page_url_name = 'register:computation_capability_set'
    resource_register_with_editor_name = 'register:computation_capability_set_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_computation_capability_set_as_xml_with_editing'

class ComputationManagementListView(ResourceManagementListView):
    model = models.Computation

    resource_delete_page_url_name = 'delete:computation'
    resource_update_page_url_name = 'update:computation'
    resource_update_with_wizard_page_url_name = 'update:computation_with_editor'
    resource_register_page_url_name = 'register:computation'
    resource_register_with_editor_name = 'register:computation_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_computation_as_xml_with_editing'

class ProcessManagementListView(ResourceManagementListView):
    model = models.Process

    resource_delete_page_url_name = 'delete:process'
    resource_update_page_url_name = 'update:process'
    resource_update_with_wizard_page_url_name = 'update:process_with_editor'
    resource_register_page_url_name = 'register:process'
    resource_register_with_editor_name = 'register:process_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_process_as_xml_with_editing'

class DataCollectionManagementListView(ResourceManagementListView):
    template_name = 'resource_management/data_collection_management_list_outer.html'
    model = models.DataCollection

    resource_delete_page_url_name = 'delete:data_collection'
    resource_update_page_url_name = 'update:data_collection'
    resource_update_with_wizard_page_url_name = 'update:data_collection_with_editor'
    resource_register_page_url_name = 'register:data_collection'
    resource_register_with_editor_name = 'register:data_collection_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_data_collection_as_xml_with_editing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_method_update_page_url_name'] = 'update:data_collection_interaction_methods'
        return context

class StaticDatasetManagementListView(ResourceManagementListView):
    model = models.StaticDataset

    resource_delete_page_url_name = 'delete:static_dataset'
    resource_update_page_url_name = 'update:static_dataset'
    resource_update_with_wizard_page_url_name = 'update:static_dataset_with_editor'
    resource_register_page_url_name = 'register:static_dataset'
    resource_register_with_editor_name = 'register:static_dataset_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_static_dataset_as_xml_with_editing'
    resource_management_category_list_page_breadcrumb_text = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:static_dataset_related_metadata_index'

class StaticDatasetEntryManagementListView(ResourceManagementListView):
    model = models.StaticDatasetEntry

    resource_delete_page_url_name = 'delete:static_dataset_entry'
    resource_update_page_url_name = 'update:static_dataset_entry'
    resource_update_with_wizard_page_url_name = 'update:static_dataset_entry_with_editor'
    resource_register_page_url_name = 'register:static_dataset_entry'
    resource_register_with_editor_name = 'register:static_dataset_entry_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_static_dataset_entry_as_xml_with_editing'
    resource_management_category_list_page_breadcrumb_text = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:static_dataset_related_metadata_index'

class DataSubsetManagementListView(ResourceManagementListView):
    model = models.DataSubset

    resource_delete_page_url_name = 'delete:data_subset'
    resource_update_page_url_name = 'update:data_subset'
    resource_update_with_wizard_page_url_name = 'update:data_subset_with_editor'
    resource_register_page_url_name = 'register:data_subset'
    resource_register_with_editor_name = 'register:data_subset_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_data_subset_as_xml_with_editing'
    resource_management_category_list_page_breadcrumb_text = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:static_dataset_related_metadata_index'

class WorkflowManagementListView(ResourceManagementListView):
    template_name = 'resource_management/workflow_management_list_outer.html'
    model = models.Workflow

    resource_delete_page_url_name = 'delete:workflow'
    resource_update_page_url_name = 'update:workflow'
    resource_update_with_wizard_page_url_name = 'update:workflow_with_editor'
    resource_register_page_url_name = 'register:workflow'
    resource_register_with_editor_name = 'register:workflow_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_workflow_as_xml_with_editing'