from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView

from .constants import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE,
)
from .utils import _create_manage_resource_page_title
from .view_mixins import (
    AcquisitionCapabilitiesManagementListViewMixin,
    AcquisitionManagementListViewMixin,
    ComputationCapabilitiesManagementListViewMixin,
    ComputationManagementListViewMixin,
    DataCollectionManagementListViewMixin,
    DataSubsetManagementListViewMixin,
    IndividualManagementListViewMixin,
    InstrumentManagementListViewMixin,
    OperationManagementListViewMixin,
    OrganisationManagementListViewMixin,
    OutdatedMetadataReferencesCheckViewMixin,
    OutdatedOntologyTermReferencesCheckViewMixin,
    PlatformManagementListViewMixin,
    ProcessManagementListViewMixin,
    ProjectManagementListViewMixin,
    StaticDatasetEntryManagementListViewMixin,
    WorkflowManagementListViewMixin,
)

from common import models
from common.decorators import login_session_institution_required
from user_management.services import (
    get_institution_id_for_login_session,
    get_members_by_institution_id,
)


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

    num_current_static_dataset_entries = models.StaticDatasetEntry.objects.owned_by_institution(institution_id).count()
    num_current_data_subsets = models.DataSubset.objects.owned_by_institution(institution_id).count()
    return render(request, 'resource_management/static_dataset_index.html', {
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
        context['outdated_resource_check_url_name'] = self.outdated_resource_check_url_name

        return context


class OrganisationManagementListView(OrganisationManagementListViewMixin, ResourceManagementListView):
    pass


class IndividualManagementListView(IndividualManagementListViewMixin, ResourceManagementListView):
    pass


class ProjectManagementListView(ProjectManagementListViewMixin, ResourceManagementListView):
    pass


class PlatformManagementListView(PlatformManagementListViewMixin, ResourceManagementListView):
    template_name = 'resource_management/platform_management_list_outer.html'

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


class OperationManagementListView(OperationManagementListViewMixin, ResourceManagementListView):
    pass


class InstrumentManagementListView(InstrumentManagementListViewMixin, ResourceManagementListView):
    pass


class AcquisitionCapabilitiesManagementListView(AcquisitionCapabilitiesManagementListViewMixin, ResourceManagementListView):
    pass


class AcquisitionManagementListView(AcquisitionManagementListViewMixin, ResourceManagementListView):
    pass


class ComputationCapabilitiesManagementListView(ComputationCapabilitiesManagementListViewMixin, ResourceManagementListView):
    pass


class ComputationManagementListView(ComputationManagementListViewMixin, ResourceManagementListView):
    pass


class ProcessManagementListView(ProcessManagementListViewMixin, ResourceManagementListView):
    pass


class DataCollectionManagementListView(DataCollectionManagementListViewMixin, ResourceManagementListView):
    template_name = 'resource_management/data_collection_management_list_outer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_method_update_page_url_name'] = 'update:data_collection_interaction_methods'
        return context


class StaticDatasetEntryManagementListView(StaticDatasetEntryManagementListViewMixin, ResourceManagementListView):
    pass


class DataSubsetManagementListView(DataSubsetManagementListViewMixin, ResourceManagementListView):
    pass


class WorkflowManagementListView(WorkflowManagementListViewMixin, ResourceManagementListView):
    template_name = 'resource_management/workflow_management_list_outer.html'


class OutdatedResourcesCheckTemplateView(
        OutdatedMetadataReferencesCheckViewMixin,
        OutdatedOntologyTermReferencesCheckViewMixin,
        TemplateView):
    template_name = 'resource_management/outdated_registrations_list.html'

    def get_outdated_registrations(self):
        return super()._get_outdated_registrations()

    def dispatch(self, request, *args, **kwargs):
        self.registrations_owned_by_logged_in_institution = self.model.objects.owned_by_institution(
            get_institution_id_for_login_session(self.request.session)
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'outdated_registrations': self.get_outdated_registrations(),
            'resource_delete_page_url_name': self.resource_delete_page_url_name,
            'resource_update_page_url_name': self.resource_update_page_url_name,
            'resource_update_with_wizard_page_url_name': self.resource_update_with_wizard_page_url_name,
            'resource_register_page_url_name': self.resource_register_page_url_name,
            'resource_register_with_editor_name': self.resource_register_with_editor_name,
            'resource_xml_download_page_url_name': self.resource_xml_download_page_url_name,
        })
        return context



class OutdatedOrganisationsCheckTemplateView(OrganisationManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedIndividualsCheckTemplateView(IndividualManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedProjectsCheckTemplateView(ProjectManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedPlatformsCheckTemplateView(PlatformManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedOperationsCheckTemplateView(OperationManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedInstrumentsCheckTemplateView(InstrumentManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedAcquisitionCapabilitiesCheckTemplateView(AcquisitionCapabilitiesManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedAcquisitionsCheckTemplateView(AcquisitionManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedComputationCapabilitiesCheckTemplateView(ComputationCapabilitiesManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedComputationsCheckTemplateView(ComputationManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedProcessesCheckTemplateView(ProcessManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedDataCollectionsCheckTemplateView(DataCollectionManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedStaticDatasetEntriesCheckTemplateView(StaticDatasetEntryManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedDataSubsetsCheckTemplateView(DataSubsetManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass


class OutdatedWorkflowsCheckTemplateView(WorkflowManagementListViewMixin, OutdatedResourcesCheckTemplateView):
    pass
