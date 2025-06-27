from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from common import models
from common.decorators import login_session_institution_required
from ontology.services import get_ontology_category_terms_in_xml_format
from ontology.utils import (
    OntologyCategoryMetadata,
    OntologyTermMetadata,
    get_ontology_term_category_from_url
)
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


class OrganisationManagementListViewMixin:
    model = models.Organisation

    resource_delete_page_url_name = 'delete:organisation'
    resource_update_page_url_name = 'update:organisation'
    resource_update_with_wizard_page_url_name = 'update:organisation_with_editor'
    resource_register_page_url_name = 'register:organisation'
    resource_register_with_editor_name = 'register:organisation_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_organisation_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:organisations_check')


class IndividualManagementListViewMixin:
    model = models.Individual

    resource_delete_page_url_name = 'delete:individual'
    resource_update_page_url_name = 'update:individual'
    resource_update_with_wizard_page_url_name = 'update:individual_with_editor'
    resource_register_page_url_name = 'register:individual'
    resource_register_with_editor_name = 'register:individual_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_individual_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:individuals_check')


class ProjectManagementListViewMixin:
    model = models.Project

    resource_delete_page_url_name = 'delete:project'
    resource_update_page_url_name = 'update:project'
    resource_update_with_wizard_page_url_name = 'update:project_with_editor'
    resource_register_page_url_name = 'register:project'
    resource_register_with_editor_name = 'register:project_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_project_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:projects_check')


class PlatformManagementListViewMixin:
    model = models.Platform

    resource_delete_page_url_name = 'delete:platform'
    resource_update_page_url_name = 'update:platform'
    resource_update_with_wizard_page_url_name = 'update:platform_with_editor'
    resource_register_page_url_name = 'register:platform'
    resource_register_with_editor_name = 'register:platform_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_platform_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:platforms_check')


class OperationManagementListViewMixin:
    model = models.Operation

    resource_delete_page_url_name = 'delete:operation'
    resource_update_page_url_name = 'update:operation'
    resource_update_with_wizard_page_url_name = 'update:operation_with_editor'
    resource_register_page_url_name = 'register:operation'
    resource_register_with_editor_name = 'register:operation_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_operation_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:operations_check')


class InstrumentManagementListViewMixin:
    model = models.Instrument

    resource_delete_page_url_name = 'delete:instrument'
    resource_update_page_url_name = 'update:instrument'
    resource_update_with_wizard_page_url_name = 'update:instrument_with_editor'
    resource_register_page_url_name = 'register:instrument'
    resource_register_with_editor_name = 'register:instrument_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_instrument_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:instruments_check')


class AcquisitionCapabilitiesManagementListViewMixin:
    model = models.AcquisitionCapabilities

    resource_delete_page_url_name = 'delete:acquisition_capability_set'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    resource_update_with_wizard_page_url_name = 'update:acquisition_capability_set_with_editor'
    resource_register_page_url_name = 'register:acquisition_capability_set'
    resource_register_with_editor_name = 'register:acquisition_capability_set_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_acquisition_capability_set_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:acquisition_capability_sets_check')


class AcquisitionManagementListViewMixin:
    model = models.Acquisition

    resource_delete_page_url_name = 'delete:acquisition'
    resource_update_page_url_name = 'update:acquisition'
    resource_update_with_wizard_page_url_name = 'update:acquisition_with_editor'
    resource_register_page_url_name = 'register:acquisition'
    resource_register_with_editor_name = 'register:acquisition_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_acquisition_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:acquisitions_check')


class ComputationCapabilitiesManagementListViewMixin:
    model = models.ComputationCapabilities

    resource_delete_page_url_name = 'delete:computation_capability_set'
    resource_update_page_url_name = 'update:computation_capability_set'
    resource_update_with_wizard_page_url_name = 'update:computation_capability_set_with_editor'
    resource_register_page_url_name = 'register:computation_capability_set'
    resource_register_with_editor_name = 'register:computation_capability_set_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_computation_capability_set_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:computation_capability_sets_check')


class ComputationManagementListViewMixin:
    model = models.Computation

    resource_delete_page_url_name = 'delete:computation'
    resource_update_page_url_name = 'update:computation'
    resource_update_with_wizard_page_url_name = 'update:computation_with_editor'
    resource_register_page_url_name = 'register:computation'
    resource_register_with_editor_name = 'register:computation_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_computation_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:computations_check')


class ProcessManagementListViewMixin:
    model = models.Process

    resource_delete_page_url_name = 'delete:process'
    resource_update_page_url_name = 'update:process'
    resource_update_with_wizard_page_url_name = 'update:process_with_editor'
    resource_register_page_url_name = 'register:process'
    resource_register_with_editor_name = 'register:process_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_process_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:processes_check')


class DataCollectionManagementListViewMixin:
    model = models.DataCollection

    resource_delete_page_url_name = 'delete:data_collection'
    resource_update_page_url_name = 'update:data_collection'
    resource_update_with_wizard_page_url_name = 'update:data_collection_with_editor'
    resource_register_page_url_name = 'register:data_collection'
    resource_register_with_editor_name = 'register:data_collection_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_data_collection_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:data_collections_check')


class StaticDatasetEntryManagementListViewMixin:
    model = models.StaticDatasetEntry

    resource_delete_page_url_name = 'delete:static_dataset_entry'
    resource_update_page_url_name = 'update:static_dataset_entry'
    resource_update_with_wizard_page_url_name = 'update:static_dataset_entry_with_editor'
    resource_register_page_url_name = 'register:static_dataset_entry'
    resource_register_with_editor_name = 'register:static_dataset_entry_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_static_dataset_entry_as_xml_with_editing'
    resource_management_category_list_page_breadcrumb_text = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:static_dataset_related_metadata_index'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:static_dataset_entries_check')


class DataSubsetManagementListViewMixin:
    model = models.DataSubset

    resource_delete_page_url_name = 'delete:data_subset'
    resource_update_page_url_name = 'update:data_subset'
    resource_update_with_wizard_page_url_name = 'update:data_subset_with_editor'
    resource_register_page_url_name = 'register:data_subset'
    resource_register_with_editor_name = 'register:data_subset_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_data_subset_as_xml_with_editing'
    resource_management_category_list_page_breadcrumb_text = _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE
    resource_management_category_list_page_breadcrumb_url_name = 'resource_management:static_dataset_related_metadata_index'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:data_subsets_check')


class WorkflowManagementListViewMixin:
    model = models.Workflow

    resource_delete_page_url_name = 'delete:workflow'
    resource_update_page_url_name = 'update:workflow'
    resource_update_with_wizard_page_url_name = 'update:workflow_with_editor'
    resource_register_page_url_name = 'register:workflow'
    resource_register_with_editor_name = 'register:workflow_with_editor'
    resource_xml_download_page_url_name = 'utils_secure:view_workflow_as_xml_with_editing'
    outdated_resource_check_url_name = reverse_lazy('resource_management:checks:workflows_check')


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


# Outdated registrations checks
class OutdatedRegistrationsCheckViewMixin:
    def _add_registration_to_registrations_by_ontology_url(self, registration, registrations_by_ontology_url: dict):
        for ontology_url in registration.properties.ontology_urls:
            if ontology_url not in registrations_by_ontology_url:
                registrations_by_ontology_url.update({
                    ontology_url: {
                        'category': '',
                        'registrations': [],
                    },
                })
            registrations_by_ontology_url[ontology_url]['registrations'].append(registration)
        return registrations_by_ontology_url

    def _add_registrations_referencing_not_found_ontology_url(
            self,
            registrations,
            not_found_ontology_url: str,
            outdated_registrations: dict):
        for r in registrations:
            if r.pk not in outdated_registrations:
                outdated_registrations[r.pk] = {
                    'registration': r,
                    'not_found_ontology_urls': dict(),
                }
            if not_found_ontology_url not in outdated_registrations[r.pk]['not_found_ontology_urls']:
                outdated_registrations[r.pk]['not_found_ontology_urls'].update({
                    not_found_ontology_url: {
                        'number_of_occurrences': 1,
                    }
                })
                continue
            outdated_registrations[r.pk]['not_found_ontology_urls'][not_found_ontology_url]['number_of_occurrences'] += 1
        return outdated_registrations

    def _add_registrations_referencing_deprecated_ontology_url(
            self,
            registrations,
            deprecated_ontology_url: str,
            outdated_registrations: dict):
        for r in registrations:
            if r.pk not in outdated_registrations:
                outdated_registrations[r.pk] = {
                    'registration': r,
                    'deprecated_ontology_urls': dict(),
                }
            if deprecated_ontology_url not in outdated_registrations[r.pk]['deprecated_ontology_urls']:
                outdated_registrations[r.pk]['deprecated_ontology_urls'].update({
                    deprecated_ontology_url: {
                        'number_of_occurrences': 1,
                    }
                })
                continue
            outdated_registrations[r.pk]['deprecated_ontology_urls'][deprecated_ontology_url]['number_of_occurrences'] += 1
        return outdated_registrations

    def get_outdated_registrations(self):
        registrations = self.model.objects.owned_by_institution(
            get_institution_id_for_login_session(self.request.session)
        )
        registrations_by_ontology_url = {}
        for r in registrations:
            registrations_by_ontology_url = self._add_registration_to_registrations_by_ontology_url(
                r,
                registrations_by_ontology_url
            )

        ontology_category_names = set()
        for ontology_url, ontology_url_data in registrations_by_ontology_url.items():
            category = get_ontology_term_category_from_url(ontology_url)
            ontology_url_data.update({
                'category': category
            })
            ontology_category_names.add(category)
        ontology_categories = {
            category: OntologyCategoryMetadata(get_ontology_category_terms_in_xml_format(category))
            for category in ontology_category_names
        }
        outdated_registrations = dict()
        for ontology_url, ontology_url_data in registrations_by_ontology_url.items():
            category_name = ontology_url_data.get('category', '')
            category_metadata = ontology_categories.get(category_name)
            if not category_metadata:
                continue
            xml_of_ontology_term = category_metadata.get_term_with_iri(ontology_url)
            if not xml_of_ontology_term:
                self._add_registrations_referencing_not_found_ontology_url(
                    registrations_by_ontology_url.get(ontology_url).get('registrations', []),
                    ontology_url,
                    outdated_registrations
                )
                continue
            ontology_term_metadata = OntologyTermMetadata(xml_of_ontology_term)
            if 'deprecate' not in ontology_term_metadata.pref_label.lower():
                continue
            self._add_registrations_referencing_deprecated_ontology_url(
                registrations_by_ontology_url.get(ontology_url).get('registrations', []),
                ontology_url,
                outdated_registrations
            )
        return outdated_registrations


class OutdatedResourcesCheckTemplateView(TemplateView, OutdatedRegistrationsCheckViewMixin):
    template_name = 'resource_management/outdated_registrations_list.html'
    
    outdated_registrations = dict()

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