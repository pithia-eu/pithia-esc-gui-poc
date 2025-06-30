from django.urls import reverse_lazy
from django.utils.text import slugify

from .constants import (
    _STATIC_DATASET_MANAGEMENT_INDEX_PAGE_TITLE,
)

from common import models
from common.xml_metadata_mapping_shortcuts import DataSubsetXmlMappingShortcuts
from ontology.services import get_ontology_category_terms_in_xml_format
from ontology.utils import (
    OntologyCategoryMetadata,
    OntologyTermMetadata,
    get_ontology_term_category_from_url
)


# Management list view mixins
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


# View mixins for outdated registrations checks
class BaseOutdatedRegistrationsCheckViewMixin:
    def __init__(self) -> None:
        self.outdated_registrations = dict()
        return super().__init__()

    def _get_template_for_outdated_registration_entry(self, registration):
        return {
            'registration': registration,
        }

    def _get_entry_for_outdated_registration(self, registration):
        if registration.pk not in self.outdated_registrations:
            self.outdated_registrations.update({
                registration.pk: self._get_template_for_outdated_registration_entry(registration),
            })
        return self.outdated_registrations[registration.pk]

    def validate_registration(self, registration: models.ScientificMetadata):
        # Implemented in subclasses
        pass

    def _get_outdated_registrations(self):
        for registration in self.registrations_owned_by_logged_in_institution:
            self.validate_registration(registration)
        return self.outdated_registrations


class OutdatedMetadataReferencesCheckViewMixin(BaseOutdatedRegistrationsCheckViewMixin):
    def __init__(self) -> None:
        super().__init__()
        self.deprecated_metadata_urls = set()
        self.not_found_metadata_urls = set()

    def _get_template_for_outdated_registration_entry(self, registration):
        template = super()._get_template_for_outdated_registration_entry(registration)
        template.update({
            'deprecated_metadata_urls': dict(),
            'not_found_metadata_urls': dict(),
        })
        return template

    def _is_metadata_registration_deprecated(self, registration: models.ScientificMetadata):
        return 'deprecate' in registration.name.lower()

    def _update_deprecated_metadata_urls_for_outdated_registration(
            self,
            registration,
            deprecated_metadata_url: str):
        entry = self._get_entry_for_outdated_registration(registration)
        deprecated_metadata_urls_for_entry = entry.get('deprecated_metadata_urls')
        if deprecated_metadata_url not in deprecated_metadata_urls_for_entry:
            deprecated_metadata_urls_for_entry.update({
                deprecated_metadata_url: {
                    'number_of_occurrences': 0,
                }
            })
        deprecated_metadata_urls_for_entry[deprecated_metadata_url]['number_of_occurrences'] += 1

    def _update_not_found_metadata_urls_for_outdated_registration(
            self,
            registration,
            not_found_metadata_url: str):
        entry = self._get_entry_for_outdated_registration(registration)
        not_found_metadata_urls_for_entry = entry.get('not_found_metadata_urls')
        if not_found_metadata_url not in not_found_metadata_urls_for_entry:
            not_found_metadata_urls_for_entry.update({
                not_found_metadata_url: {
                    'number_of_occurrences': 0,
                }
            })
        not_found_metadata_urls_for_entry[not_found_metadata_url]['number_of_occurrences'] += 1

    def _check_for_outdated_metadata_urls_in_registration(self, registration: models.ScientificMetadata):
        for metadata_url in registration.properties.resource_urls:
            if metadata_url in self.not_found_metadata_urls:
                self._update_not_found_metadata_urls_for_outdated_registration(
                    registration,
                    metadata_url
                )
                continue
            if metadata_url in self.deprecated_metadata_urls:
                self._update_deprecated_metadata_urls_for_outdated_registration(
                    registration,
                    metadata_url
                )
                continue
            try:
                referenced_registration = models.ScientificMetadata.objects.get_by_metadata_server_url(metadata_url)
            except models.ScientificMetadata.DoesNotExist:
                self._update_not_found_metadata_urls_for_outdated_registration(
                    registration,
                    metadata_url
                )
                self.not_found_metadata_urls.add(metadata_url)
                continue
            if not self._is_metadata_registration_deprecated(referenced_registration):
                continue
            self._update_deprecated_metadata_urls_for_outdated_registration(
                registration,
                metadata_url
            )
            self.deprecated_metadata_urls.add(metadata_url)

    def validate_registration(self, registration: models.ScientificMetadata):
        super().validate_registration(registration)
        self._check_for_outdated_metadata_urls_in_registration(registration)


class OutdatedOntologyTermReferencesCheckViewMixin(BaseOutdatedRegistrationsCheckViewMixin):
    def __init__(self) -> None:
        super().__init__()
        self.ontology_categories_loaded = dict()
        self.deprecated_ontology_term_urls = set()
        self.not_found_ontology_term_urls = set()

    def _get_template_for_outdated_registration_entry(self, registration):
        template = super()._get_template_for_outdated_registration_entry(registration)
        template.update({
            'deprecated_ontology_urls': dict(),
            'not_found_ontology_urls': dict(),
        })
        return template

    def _load_in_ontology_category(self, ontology_category):
        try:
            self.ontology_categories_loaded.update({
                ontology_category: OntologyCategoryMetadata(get_ontology_category_terms_in_xml_format(ontology_category))
            })
        except Exception:
            self.ontology_categories_loaded.update({
                ontology_category: None,
            })

    def _get_ontology_category_metadata(self, ontology_category):
        if ontology_category not in self.ontology_categories_loaded:
            self._load_in_ontology_category(ontology_category)
        return self.ontology_categories_loaded.get(ontology_category)

    def _get_ontology_term_metadata_or_none(self, ontology_category_metadata, ontology_term_url: str):
        xml_of_ontology_term = ontology_category_metadata.get_term_with_iri(ontology_term_url)
        try:
            ontology_term_metadata = OntologyTermMetadata(xml_of_ontology_term)
            return ontology_term_metadata
        except Exception:
            pass
        return None

    def _is_ontology_term_deprecated(self, ontology_term_metadata):
        return 'deprecate' in ontology_term_metadata.pref_label.lower()

    def _update_deprecated_ontology_terms_for_outdated_registration(
            self,
            registration,
            deprecated_ontology_term_url: str):
        entry = self._get_entry_for_outdated_registration(registration)
        deprecated_ontology_term_urls_for_entry = entry.get('deprecated_ontology_urls')
        if deprecated_ontology_term_url not in deprecated_ontology_term_urls_for_entry:
            deprecated_ontology_term_urls_for_entry.update({
                deprecated_ontology_term_url: {
                    'number_of_occurrences': 0,
                }
            })
        deprecated_ontology_term_urls_for_entry[deprecated_ontology_term_url]['number_of_occurrences'] += 1

    def _update_not_found_ontology_terms_for_outdated_registration(
            self,
            registration,
            not_found_ontology_term_url: str):
        entry = self._get_entry_for_outdated_registration(registration)
        not_found_ontology_term_urls_for_entry = entry.get('not_found_ontology_urls')
        if not_found_ontology_term_url not in not_found_ontology_term_urls_for_entry:
            not_found_ontology_term_urls_for_entry.update({
                not_found_ontology_term_url: {
                    'number_of_occurrences': 0,
                }
            })
        not_found_ontology_term_urls_for_entry[not_found_ontology_term_url]['number_of_occurrences'] += 1

    def _check_for_outdated_ontology_terms_in_registration(self, registration):
        for ontology_term_url in registration.properties.ontology_urls:
            if ontology_term_url in self.not_found_ontology_term_urls:
                self._update_not_found_ontology_terms_for_outdated_registration(
                    registration,
                    ontology_term_url
                )
                continue
            if ontology_term_url in self.deprecated_ontology_term_urls:
                self._update_deprecated_ontology_terms_for_outdated_registration(
                    registration,
                    ontology_term_url
                )
                continue
            category = get_ontology_term_category_from_url(ontology_term_url)
            ontology_category_metadata = self._get_ontology_category_metadata(category)
            ontology_term_metadata = self._get_ontology_term_metadata_or_none(
                ontology_category_metadata,
                ontology_term_url
            )
            if not ontology_term_metadata:
                self._update_not_found_ontology_terms_for_outdated_registration(
                    registration,
                    ontology_term_url
                )
                self.not_found_ontology_term_urls.add(ontology_term_url)
                continue
            if not self._is_ontology_term_deprecated(ontology_term_metadata):
                continue
            self._update_deprecated_ontology_terms_for_outdated_registration(
                registration,
                ontology_term_url
            )
            self.deprecated_ontology_term_urls.add(ontology_term_url)

    def validate_registration(self, registration: models.ScientificMetadata):
        super().validate_registration(registration)
        self._check_for_outdated_ontology_terms_in_registration(registration)


# Data subset validation view mixin
class DataSubsetResourceManagementViewMixin:
    SIMILAR_SOURCE_NAMES_ERROR = 'Some online resource names in the metadata file are too similar to one another. Please update the metadata file to resolve these issues, then re-upload it.'
    
    def check_source_names(self, form):
        self.temp_xml_file = self.request.FILES.getlist('files')[0]
        data_subset_shortcutted = DataSubsetXmlMappingShortcuts(self.temp_xml_file.read().decode())
        source_names = [
            source.get('name', '')
            for source in data_subset_shortcutted.online_resources
            if source.get('name', '')
        ]
        source_names_normalised = set(
            slugify(source_name)
            for source_name in source_names
        )
        return len(source_names) == len(source_names_normalised)