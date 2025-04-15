import copy
import itertools
import json
import logging
import re
from dateutil.parser import isoparse
from django.http import JsonResponse
from django.utils.http import urlencode
from django.views.decorators.http import require_POST
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.urls import reverse
from django.views.generic import (
    ListView,
    TemplateView,
)
from lxml import etree
from openapi_spec_validator import validate_spec_url

from .services import (
    get_properties_for_ontology_server_urls,
    map_metadata_server_urls_to_browse_urls,
    map_ontology_server_urls_to_browse_urls,
)
from .utils import (
    reformat_and_clean_resource_copy_for_property_table,
    remove_common_disallowed_properties_from_property_table_dict,
    remove_disallowed_properties_from_property_table_dict,
)

from common import models
from common.constants import (
    STATIC_DATASET_TYPE_DESCRIPTION,
    STATIC_DATASET_TYPE_PLURAL_READABLE,
    STATIC_DATASET_TYPE_READABLE,
)
from common.xml_metadata_mapping_shortcuts import DoiKernelMetadataMappingShortcuts
from handle_management.services import HandleClient
from ontology.services import (
    get_ontology_category_terms_in_xml_format,
    OntologyCategoryMetadataService,
)


logger = logging.getLogger(__name__)

_INDEX_PAGE_TITLE = 'All Scientific Metadata'
_DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE = 'Data Collection-related Metadata'
_XML_SCHEMAS_PAGE_TITLE = 'Metadata Models'


# Create your views here.
def index(request):
    return render(request, 'browse/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'data_collection_related_resource_types_page_title': _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
    })


def data_collection_related_resource_types(request):
    """Acts as a centre point to all registration list pages
    for each Data Collection-related registration (i.e.,
    all scientific metadata types up to Data Collections).
    Lists the links to these pages and the total number of
    registrations for each scientific metadata type.
    """
    num_current_organsations = models.Organisation.objects.count()
    num_current_individuals = models.Individual.objects.count()
    num_current_projects = models.Project.objects.count()
    num_current_platforms = models.Platform.objects.count()
    num_current_instruments = models.Instrument.objects.count()
    num_current_operations = models.Operation.objects.count()
    num_current_acquisition_capability_sets = models.AcquisitionCapabilities.objects.count()
    num_current_acquisitions = models.Acquisition.objects.count()
    num_current_computation_capability_sets = models.ComputationCapabilities.objects.count()
    num_current_computations = models.Computation.objects.count()
    num_current_processes = models.Process.objects.count()
    num_current_data_collections = models.DataCollection.objects.count()
    return render(request, 'browse/data_collection_related_resource_types.html', {
        'title': _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
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
        'browse_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })


def static_dataset_tree(request):
    """Lists all static dataset entries and data subsets
    in a categorised tree view.
    """
    xml_of_static_dataset_categories = get_ontology_category_terms_in_xml_format('staticDatasetCategory')
    static_dataset_categories = OntologyCategoryMetadataService(xml_of_static_dataset_categories)
    static_dataset_category_properties_by_iri = static_dataset_categories.get_name_and_definition_of_ontology_terms_by_iri()
    static_dataset_entries = set(models.StaticDatasetEntry.objects.all())
    for key, value in static_dataset_category_properties_by_iri.items():
        if 'entries' not in value:
            value.update({
                'entries': [],
            })
        entries_for_category = [entry for entry in static_dataset_entries if entry.static_dataset_category == key]
        value.update({
            'entries': entries_for_category,
        })
    static_dataset_category_properties_by_iri.update({
        'other': {
            'name': 'Other',
            'definition': '',
            'entries': [
                entry
                for entry in static_dataset_entries
                if entry.static_dataset_category not in static_dataset_category_properties_by_iri
            ],
        },
    })
    return render(request, 'browse/static_dataset_tree.html', {
        'title': STATIC_DATASET_TYPE_PLURAL_READABLE.title(),
        'description': STATIC_DATASET_TYPE_DESCRIPTION,
        'browse_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
        'resources': static_dataset_entries,
        'static_dataset_category_properties_by_iri': static_dataset_category_properties_by_iri,
        'type_readable': STATIC_DATASET_TYPE_READABLE,
        'type_plural_readable': STATIC_DATASET_TYPE_PLURAL_READABLE,
    })


def schemas(request):
    """A list of links to the XML metadata schemas.
    """
    return render(request, 'browse/schemas.html', {
        'title': _XML_SCHEMAS_PAGE_TITLE
    })


class ResourceListView(ListView):
    """A list of detail page links of scientific metadata
    registrations for one given type. E.g., a list of
    all registered Data Collections.

    This view is intended to be subclassed and to not
    be called directly.
    """
    template_name = 'browse/resource_list_by_type.html'
    context_object_name = 'resources'

    resource_detail_page_url_name = ''
    
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model.type_plural_readable.title()
        context['description'] = self.model.type_description_readable
        context['type_readable'] = self.model.type_readable
        context['type_plural_readable'] = self.model.type_plural_readable
        context['empty_resource_list_text'] = f'No {self.model.type_plural_readable.lower()} were found.'
        context['resource_detail_page_url_name'] = self.resource_detail_page_url_name
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrganisationListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Organisation
    registration.
    """
    model = models.Organisation
    resource_detail_page_url_name = 'browse:organisation_detail'


class IndividualListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Individual
    registration.
    """
    model = models.Individual
    resource_detail_page_url_name = 'browse:individual_detail'


class ProjectListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Project
    registration.
    """
    model = models.Project
    resource_detail_page_url_name = 'browse:project_detail'


class PlatformListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Platform
    registration.
    """
    model = models.Platform
    resource_detail_page_url_name = 'browse:platform_detail'


class InstrumentListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Instrument
    registration.
    """
    model = models.Instrument
    resource_detail_page_url_name = 'browse:instrument_detail'


class OperationListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Operation
    registration.
    """
    model = models.Operation
    resource_detail_page_url_name = 'browse:operation_detail'


class AcquisitionCapabilitiesListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Acquisition
    Capabilities registration.
    """
    model = models.AcquisitionCapabilities
    resource_detail_page_url_name = 'browse:acquisition_capability_set_detail'


class AcquisitionListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Acquisition
    registration.
    """
    model = models.Acquisition
    resource_detail_page_url_name = 'browse:acquisition_detail'


class ComputationCapabilitiesListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Computation
    Capabilities registration.
    """
    model = models.ComputationCapabilities
    resource_detail_page_url_name = 'browse:computation_capability_set_detail'


class ComputationListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Computation
    registration.
    """
    model = models.Computation
    resource_detail_page_url_name = 'browse:computation_detail'


class ProcessListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Process
    registration.
    """
    model = models.Process
    resource_detail_page_url_name = 'browse:process_detail'


class DataCollectionListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Data
    Collection registration.
    """
    template_name = 'browse/data_collection_list.html'
    model = models.DataCollection
    resource_detail_page_url_name = 'browse:data_collection_detail'

    def get_queryset(self):
        data_collections = super().get_queryset()
        # Get URLs of activity indicators early to help
        # mitigate against possible ontology server loading
        # times.
        xml_of_computation_types_ontology_category = get_ontology_category_terms_in_xml_format('computationType')
        computation_types_ontology_category = OntologyCategoryMetadataService(xml_of_computation_types_ontology_category)
        urls_of_activity_indicators = computation_types_ontology_category.get_all_descendents_of_ontology_term('https://metadata.pithia.eu/ontology/2.2/computationType/ActivityIndicator')

        ACTIVITY_INDICATORS_KEY = 'Activity Indicators'
        SENSOR_MEASUREMENTS_KEY = 'Sensor Measurements'
        COMPUTATIONAL_MODELS_KEY = 'Computational Models'
        ANNOTATIONS_KEY = 'Annotations'
        MIXED_KEY = 'Mixed'
        OTHER_KEY = 'Other'

        data_collections_by_type = {
            ACTIVITY_INDICATORS_KEY: [],
            SENSOR_MEASUREMENTS_KEY: [],
            COMPUTATIONAL_MODELS_KEY: [],
            ANNOTATIONS_KEY: [],
            MIXED_KEY: [],
            OTHER_KEY: [],
        }
        # https://metadata.pithia.eu/ontology/2.2/computationType/GeomagneticActivityIndicator
        # https://metadata.pithia.eu/ontology/2.2/computationType/AssimilativeModel
        # https://metadata.pithia.eu/ontology/2.2/instrumentType/Imager

        for dc in data_collections:
            if not dc.type_urls:
                data_collections_by_type[OTHER_KEY].append(dc)
                continue
            type_urls = dc.type_urls
            is_activity_indicator = any([url in urls_of_activity_indicators for url in type_urls])
            is_sensor_measurement = any([re.search('\/instrumentType/(.*)$', url) for url in type_urls])
            is_computational_model = any([re.search('\/computationType/(.*)$', url) for url in type_urls])
            is_annotation = any([re.search('\/annotationType/(.*)$', url) for url in type_urls])

            if sum([is_sensor_measurement, is_computational_model]) > 1:
                data_collections_by_type[MIXED_KEY].append(dc)
            elif is_activity_indicator:
                data_collections_by_type[ACTIVITY_INDICATORS_KEY].append(dc)
            elif is_sensor_measurement:
                data_collections_by_type[SENSOR_MEASUREMENTS_KEY].append(dc)
            elif is_computational_model:
                data_collections_by_type[COMPUTATIONAL_MODELS_KEY].append(dc)
            elif is_annotation:
                data_collections_by_type[ANNOTATIONS_KEY].append(dc)
            else:
                data_collections_by_type[OTHER_KEY].append(dc)

        return data_collections_by_type
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_count'] = len(self.model.objects.all())
        return context


class WorkflowListView(ResourceListView):
    """A subclass of ResourceListView.

    Lists the detail page links for each Workflow
    registration.
    """
    template_name = 'browse/workflow_list.html'
    model = models.Workflow
    resource_detail_page_url_name = 'browse:workflow_detail'


class ResourceDetailView(TemplateView):
    """The detail page for a scientific metadata
    registration. The properties of a scientific
    metadata registration are displayed here.

    This view is intended to be subclassed and to not
    be called directly.
    """
    title = 'Resource Detail'
    resource = None
    resource_id = ''
    resource_human_readable = {}
    resource_description_split = []
    ontology_server_urls = []
    resource_server_urls = []
    resource_list_by_type_url_name = ''
    resource_download_url_name = ''
    template_name = 'browse/detail/bases/base.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        property_table_dict = remove_common_disallowed_properties_from_property_table_dict(property_table_dict)
        return property_table_dict

    def get_description_from_xml(self, resource):
        return etree.fromstring(resource.xml.encode('utf-8')).find('{https://metadata.pithia.eu/schemas/2.2}description').text

    def get_related_registrations(self):
        return {
            'Organisations': self.resource.properties.organisation_urls,
            'Individuals': self.resource.properties.individual_urls,
            'Projects': self.resource.properties.project_urls,
            'Platforms': self.resource.properties.platform_urls,
            'Operations': self.resource.properties.operation_urls,
            'Instruments': self.resource.properties.instrument_urls,
            'Acquisition Capabilities': self.resource.properties.acquisition_capabilities_urls,
            'Acquisitions': self.resource.properties.acquisition_urls,
            'Computation Capabilities': self.resource.properties.computation_capabilities_urls,
            'Computations': self.resource.properties.computation_urls,
            'Processes': self.resource.properties.process_urls,
            'Data Collections': self.resource.properties.data_collection_urls,
            'Static Dataset Entries': self.resource.properties.static_dataset_entry_urls,
        }

    def clean_related_registrations_dict(self, related_registrations_dict):
        cleaned_related_registrations_dict = {}
        for key, value in related_registrations_dict.items():
            if not value:
                continue
            elif isinstance(value, dict) and not value.get('@xlink:href'):
                continue
            cleaned_related_registrations_dict.update({
                key: value
            })
        return cleaned_related_registrations_dict
        
    
    def format_and_split_string_by_multi_newlines(self, description):
        try:
            description_formatted = description.replace('\t', '')
            description_formatted = re.sub('\n\s+\n', '\n\n', description_formatted)
            description_formatted_split = description_formatted.split('\n\n')
            for counter, s in enumerate(description_formatted_split):
                description_formatted_split[counter] = s.replace('\n', ' ')
            return description_formatted_split
        except AttributeError as err:
            logger.exception(err)
        return []

    def map_server_urls_to_ids(self, server_urls):
        return {
            url: url.split('/')[-1]
            for url in server_urls
        }

    def get(self, request, *args, **kwargs):
        self.resource = get_object_or_404(self.model, pk=self.resource_id)
        self.ontology_server_urls = self.resource.properties.ontology_urls
        self.resource_server_urls = self.resource.properties.resource_urls
        self.property_table_dict = self.configure_resource_copy_for_property_table(copy.deepcopy(self.resource.json))
        self.property_table_dict = reformat_and_clean_resource_copy_for_property_table(self.property_table_dict)
        self.title = self.resource.name
        if self.resource.description and self.resource.description.strip() != '':
            description_from_xml = self.get_description_from_xml(self.resource)
            self.resource_description_split = self.format_and_split_string_by_multi_newlines(description_from_xml)
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['resource_description_split'] = self.resource_description_split
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        context['resource_list_page_breadcrumb_text'] = self.model.type_plural_readable.title()
        context['resource_list_page_breadcrumb_url_name'] = self.resource_list_by_type_url_name
        context['resource_download_url_name'] = self.resource_download_url_name
        context['resource'] = self.resource
        context['ontology_server_urls'] = self.ontology_server_urls
        context['resource_server_urls'] = self.resource_server_urls
        context['server_url_to_id_mappings'] = {
            **self.map_server_urls_to_ids(self.ontology_server_urls),
            **self.map_server_urls_to_ids(self.resource_server_urls),
        }
        context['related_registrations'] = self.clean_related_registrations_dict(self.get_related_registrations())
        context['property_table_dict'] = self.property_table_dict
        context['scientific_metadata_creation_date_parsed'] = isoparse(self.resource.creation_date_json)
        context['scientific_metadata_last_modification_date_parsed'] = isoparse(self.resource.last_modification_date_json)
        context['server_url_conversion_url'] = reverse('browse:convert_server_urls')
        context['ontology_node_properties_mapping_url'] = reverse('browse:ontology_node_properties_mapping_url')
        return context


class OnlineResourcesViewMixin:
    def categorise_online_resources_from_resource(self, resource: models.DataCollection | models.DataSubset):
        interaction_methods_by_type = {
            'api': [],
            'online_resource': [],
        }
        for online_resource in resource.properties.online_resources:
            service_functions = online_resource.get('service_functions')
            is_openapi_a_service_function = 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/OpenAPI' in service_functions

            if is_openapi_a_service_function:
                try:
                    validate_spec_url(online_resource.get('linkage'))
                    online_resource.update({
                        'linkage': f"{reverse('present:interact_with_data_collection_through_api', kwargs={'data_collection_id': self.resource_id})}?{urlencode({'name': online_resource.get('name', '')})}"
                    })
                except Exception:
                    pass

                interaction_methods_by_type['api'].append(online_resource)
                continue
            interaction_methods_by_type['online_resource'].append(online_resource)

        # Remove empty categories
        interaction_methods_by_type = {key: value for key, value in interaction_methods_by_type.items() if value}
            
        return interaction_methods_by_type

    def get_online_resources_from_resource_by_type(self, resource: models.DataCollection | models.DataSubset):
        interaction_methods_by_type = {}
        # Link interaction methods
        for online_resource in resource.properties.online_resources:
            service_function = online_resource.get('service_function')
            if not service_function:
                service_function = 'unknown'
            if service_function not in interaction_methods_by_type:
                interaction_methods_by_type[service_function] = []
            interaction_methods_by_type[service_function].append(online_resource)
        return interaction_methods_by_type


class OrganisationDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Organisation registration.
    """
    model = models.Organisation
    resource_list_by_type_url_name = 'browse:list_organisations'
    resource_download_url_name = 'utils:view_organisation_as_xml'
    template_name = 'browse/detail/bases/organisation.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'contactInfo',
                'positionName',
                'shortName',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().get(request, *args, **kwargs)


class IndividualDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Individual registration.
    """
    model = models.Individual
    resource_list_by_type_url_name = 'browse:list_individuals'
    resource_download_url_name = 'utils:view_individual_as_xml'
    template_name = 'browse/detail/bases/individual.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'contactInfo',
                'organisation',
                'positionName',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().get(request, *args, **kwargs)


class ProjectDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Project registration.
    """
    project_abstract_split = []

    model = models.Project
    template_name = 'browse/detail/bases/project.html'
    resource_list_by_type_url_name = 'browse:list_projects'
    resource_download_url_name = 'utils:view_project_as_xml'

    def get_abstract_from_xml(self, resource):
        return etree.fromstring(resource.xml.encode('utf-8')).find('{https://metadata.pithia.eu/schemas/2.2}abstract').text

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'abstract',
                'documentation',
                'keywords',
                'status',
                'URL',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_abstract_split'] = self.format_and_split_string_by_multi_newlines(self.get_abstract_from_xml(self.resource))
        return context


class PlatformDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Platform registration.
    """
    model = models.Platform
    resource_list_by_type_url_name = 'browse:list_platforms'
    resource_download_url_name = 'utils:view_platform_as_xml'
    template_name = 'browse/detail/bases/platform.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'childPlatform',
                'documentation',
                'location',
                'shortName',
                'standardIdentifier',
                'type',
                'URL',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().get(request, *args, **kwargs)


class InstrumentDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Instrument registration.
    """
    model = models.Instrument
    resource_list_by_type_url_name = 'browse:list_instruments'
    resource_download_url_name = 'utils:view_instrument_as_xml'
    template_name = 'browse/detail/bases/instrument.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'documentation',
                'member',
                'operationalMode',
                'type',
                'URL',
                'version',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().get(request, *args, **kwargs)


class OperationDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Operation registration.
    """
    model = models.Operation
    resource_list_by_type_url_name = 'browse:list_operations'
    resource_download_url_name = 'utils:view_operation_as_xml'
    template_name = 'browse/detail/bases/operation.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'documentation',
                'operationTime',
                'platform',
                'status',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().get(request, *args, **kwargs)


class AcquisitionCapabilitiesDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Acquisition Capabilities registration.
    """
    model = models.AcquisitionCapabilities
    resource_list_by_type_url_name = 'browse:list_acquisition_capability_sets'
    resource_download_url_name = 'utils:view_acquisition_capability_set_as_xml'
    template_name = 'browse/detail/bases/acquisition_capabilities.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'capabilities',
                'dataLevel',
                'documentation',
                'inputDescription',
                'instrumentModePair',
                'outputDescription',
                'qualityAssessment',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().get(request, *args, **kwargs)


class AcquisitionDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Acquisition registration.
    """
    model = models.Acquisition
    resource_list_by_type_url_name = 'browse:list_acquisitions'
    resource_download_url_name = 'utils:view_acquisition_as_xml'
    template_name = 'browse/detail/bases/acquisition.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'capabilityLinks',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().get(request, *args, **kwargs)


class ComputationCapabilitiesDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Computation Capabilities registration.
    """
    model = models.ComputationCapabilities
    resource_list_by_type_url_name = 'browse:list_computation_capability_sets'
    resource_download_url_name = 'utils:view_computation_capability_set_as_xml'
    template_name = 'browse/detail/bases/computation_capabilities.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'capabilities',
                'childComputation',
                'dataLevel',
                'documentation',
                'processingInput',
                'processingOutput',
                'qualityAssessment',
                'type',
                'version',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().get(request, *args, **kwargs)


class ComputationDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Computation registration.
    """
    model = models.Computation
    resource_list_by_type_url_name = 'browse:list_computations'
    resource_download_url_name = 'utils:view_computation_as_xml'
    template_name = 'browse/detail/bases/computation.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'capabilityLinks',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().get(request, *args, **kwargs)


class ProcessDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Process registration.
    """
    model = models.Process
    resource_list_by_type_url_name = 'browse:list_processes'
    resource_download_url_name = 'utils:view_process_as_xml'
    template_name = 'browse/detail/bases/process.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'acquisitionComponent',
                'computationComponent',
                'dataLevel',
                'documentation',
                'qualityAssessment',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().get(request, *args, **kwargs)


class DataCollectionDetailView(ResourceDetailView, OnlineResourcesViewMixin):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Data Collection registration.
    """
    model = models.DataCollection
    resource_list_by_type_url_name = 'browse:list_data_collections'
    resource_download_url_name = 'utils:view_data_collection_as_xml'
    template_name = 'browse/detail/bases/data_collection.html'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'collectionResults',
                'dataLevel',
                'om:featureOfInterest',
                'om:procedure',
                'permission',
                'project',
                'qualityAssessment',
                'relatedParty',
                'subCollection',
                'type',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        self.resource = get_object_or_404(self.model, pk=self.resource_id)
        self.interaction_methods_by_type = self.categorise_online_resources_from_resource(self.resource)
        # Legacy API Interaction methods
        api_interaction_methods = list(models.APIInteractionMethod.objects.filter(scientific_metadata=self.resource))
        if api_interaction_methods:
            self.interaction_methods_by_type['api'] = self.interaction_methods_by_type.get('api', []) + [{
                'service_functions': ['https://metadata.pithia.eu/ontology/2.2/serviceFunction/OpenAPI'],
                'linkage': reverse('present:interact_with_data_collection_through_api', kwargs={'data_collection_id': self.resource_id}),
                'name': 'Access with the PITHIA e-Science Centre',
                'protocol': '',
                'description': api_int_method.config.get('description', ''),
                'data_format': '',
            } for api_int_method in api_interaction_methods]

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_methods_by_type'] = dict(sorted(self.interaction_methods_by_type.items()))
        context['num_interaction_methods'] = len(list(itertools.chain(*self.interaction_methods_by_type.values())))
        context['data_collection_id'] = self.resource_id
        
        return context


class StaticDatasetEntryDetailView(ResourceDetailView):
    """A subclass of StaticDatasetRelatedResourceDetailView.

    A detail page displaying the properties of
    a Static Dataset Entry registration.
    """
    model = models.StaticDatasetEntry
    resource_list_by_type_url_name = 'browse:list_static_dataset_entries'
    resource_download_url_name = 'utils:view_static_dataset_entry_as_xml'
    template_name = 'browse/detail/bases/static_dataset_entry.html'

    def get_description_from_xml(self, resource):
        return etree.fromstring(resource.xml.encode('utf-8')).find('{https://metadata.pithia.eu/schemas/2.2}entryDescription').text

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'staticDatasetIdentifier',
                'entryName',
                'entryDescription',
                'phenomenonTime',
            ]
        )
        return cleaned_property_table_dict

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['static_dataset_entry_id']
        return super().get(request, *args, **kwargs)


class DataSubsetDetailView(ResourceDetailView, OnlineResourcesViewMixin):
    """A subclass of StaticDatasetRelatedResourceDetailView.

    A detail page displaying the properties of
    a Data Subset registration.
    """
    model = models.DataSubset
    resource_list_by_type_url_name = 'browse:list_data_subsets'
    resource_download_url_name = 'utils:view_data_subset_as_xml'
    template_name = 'browse/detail/bases/data_subset.html'
    interaction_methods_by_type = {}

    def get_description_from_xml(self, resource):
        return etree.fromstring(resource.xml.encode('utf-8')).find('{https://metadata.pithia.eu/schemas/2.2}dataSubsetDescription').text

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'dataCollection',
                'dataLevel',
                'dataSubsetName',
                'dataSubsetDescription',
                'doi',
                'entryIdentifier',
                'qualityAssessment',
                'resultTime',
                'source',
            ]
        )
        return cleaned_property_table_dict

    def get_context_handle_variables(self):
        handle_context = {
            'data_for_handles': [],
        }
        # Prepare to get handle data from the handle API.
        try:
            handle_client = HandleClient()
        except BaseException as e:
            logger.exception('An unexpected error occurred whilst instantiating the PyHandle client.')
            # No point doing any further operations
            # if cannot get data from API.
            return handle_context
        
        # Get the handle name-URL mappings for the page URL.
        handle_url_mappings = models.HandleURLMapping.objects.for_url(self.url_for_handle_url_mappings)
        handle_names = [
            handle_url_mapping.handle_name
            for handle_url_mapping in handle_url_mappings
        ]
        # Get handle data from the handle API.
        data_for_handles_unformatted = [
            handle_client.get_handle_record(handle_name)
            for handle_name in handle_names
        ]
        handle_context.update({
            'data_for_handles': [
                {
                    'url': data.get('URL'),
                    'doi_kernel_metadata': DoiKernelMetadataMappingShortcuts(
                        data.get('DOI_KERNEL_METADATA')
                    ).properties
                }
                for data in data_for_handles_unformatted
                if data is not None
            ],
        })
        return handle_context

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_subset_id']
        self.url_for_handle_url_mappings = request.build_absolute_uri()

        # Custom handling 404 handling - shows DOI information
        # on missing resource.
        try:
            self.resource = self.model.objects.get(pk=self.resource_id)
        except models.DataSubset.DoesNotExist:
            context = {'title': 'Not Found'}
            context.update(self.get_context_handle_variables())
            return render(request, 'browse/detail_404.html', context)
        
        self.interaction_methods_by_type = self.categorise_online_resources_from_resource(self.resource)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_methods_by_type'] = dict(sorted(self.interaction_methods_by_type.items()))
        context['num_interaction_methods'] = len(list(itertools.chain(*self.interaction_methods_by_type.values())))
        return context


class WorkflowDetailView(ResourceDetailView):
    """A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Workflow registration.
    """
    template_name = 'browse/detail/bases/workflow.html'
    model = models.Workflow
    resource_list_by_type_url_name = 'browse:list_workflows'
    resource_download_url_name = 'utils:view_workflow_as_xml'

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'workflowDetails',
                'dataCollection',
            ]
        )
        return cleaned_property_table_dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workflow_interaction_method'] = self.resource.interactionmethod_set.first()
        return context

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['workflow_id']
        return super().get(request, *args, **kwargs)


@require_POST
def get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls(request):
    """Used for mapping ontology server URLs and
    metadata server URLs to their corresponding
    detail pages. Mappings are displayed in 
    scientific metadata detail pages.
    """
    ontology_server_urls = json.loads(request.POST.get('ontology-server-urls', '[]'))
    resource_server_urls = json.loads(request.POST.get('resource-server-urls', '[]'))
    esc_ontology_urls = map_ontology_server_urls_to_browse_urls(ontology_server_urls)
    esc_resource_urls = map_metadata_server_urls_to_browse_urls(resource_server_urls)
    
    return JsonResponse({
        'ontology_urls': esc_ontology_urls,
        'resource_urls': esc_resource_urls,
    })


@require_POST
def map_ontology_server_urls_to_corresponding_properties(request):
    """Maps ontology server URLs to corresponding
    ontology properties and ontology browser URL.
    """
    ontology_server_urls = json.loads(request.POST.get('urls', []))
    properties_to_get = json.loads(request.POST.get('properties', []))
    properties_for_ontology_server_urls = get_properties_for_ontology_server_urls(
        ontology_server_urls,
        properties_to_get
    )
    return JsonResponse(properties_for_ontology_server_urls)
