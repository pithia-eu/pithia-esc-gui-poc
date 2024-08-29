import copy
import json
import logging
import re
from dateutil.parser import parse
from django.http import JsonResponse
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
from handle_management.handle_api import (
    get_handle_record,
    instantiate_client_and_load_credentials,
)

logger = logging.getLogger(__name__)

_INDEX_PAGE_TITLE = 'All Scientific Metadata'
_DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE = 'Data Collection-related Metadata'
_CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE = 'Catalogue-related Metadata'
_XML_SCHEMAS_PAGE_TITLE = 'Metadata Models'

# Create your views here.
def index(request):
    return render(request, 'browse/index.html', {
        'title': _INDEX_PAGE_TITLE,
        'data_collection_related_resource_types_page_title': _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
        'catalogue_related_resource_types_page_title': _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE,
    })

def data_collection_related_resource_types(request):
    """
    Acts as a centre point to all registration list pages
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

def catalogue_related_resource_types(request):
    """
    Acts as a centre point to all registration list pages
    for each Catalogue-related registration (i.e., all
    scientific metadata types from Catalogues to Catalogue
    Data Subsets). Lists the links to these pages and the
    total number of registrations for each scientific
    metadata type.
    """
    num_current_catalogues = models.Catalogue.objects.count()
    num_current_catalogue_entries = models.CatalogueEntry.objects.count()
    num_current_catalogue_data_subsets = models.CatalogueDataSubset.objects.count()
    return render(request, 'browse/catalogue_related_resource_types.html', {
        'title': _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE,
        'num_current_catalogues': num_current_catalogues,
        'num_current_catalogue_entries': num_current_catalogue_entries,
        'num_current_catalogue_data_subsets': num_current_catalogue_data_subsets,
        'browse_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })

def schemas(request):
    """
    A list of links to the XML metadata schemas.
    """
    return render(request, 'browse/schemas.html', {
        'title': _XML_SCHEMAS_PAGE_TITLE
    })

class ResourceListView(ListView):
    """
    A list of detail page links of scientific metadata
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
        context['empty_resource_list_text'] = f'No {self.model.type_plural_readable.lower()} were found.'
        context['resource_detail_page_url_name'] = self.resource_detail_page_url_name
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrganisationListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Organisation
    registration.
    """
    model = models.Organisation
    resource_detail_page_url_name = 'browse:organisation_detail'

class IndividualListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Individual
    registration.
    """
    model = models.Individual
    resource_detail_page_url_name = 'browse:individual_detail'

class ProjectListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Project
    registration.
    """
    model = models.Project
    resource_detail_page_url_name = 'browse:project_detail'

class PlatformListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Platform
    registration.
    """
    model = models.Platform
    resource_detail_page_url_name = 'browse:platform_detail'

class InstrumentListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Instrument
    registration.
    """
    model = models.Instrument
    resource_detail_page_url_name = 'browse:instrument_detail'

class OperationListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Operation
    registration.
    """
    model = models.Operation
    resource_detail_page_url_name = 'browse:operation_detail'

class AcquisitionCapabilitiesListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Acquisition
    Capabilities registration.
    """
    model = models.AcquisitionCapabilities
    resource_detail_page_url_name = 'browse:acquisition_capability_set_detail'

class AcquisitionListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Acquisition
    registration.
    """
    model = models.Acquisition
    resource_detail_page_url_name = 'browse:acquisition_detail'

class ComputationCapabilitiesListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Computation
    Capabilities registration.
    """
    model = models.ComputationCapabilities
    resource_detail_page_url_name = 'browse:computation_capability_set_detail'

class ComputationListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Computation
    registration.
    """
    model = models.Computation
    resource_detail_page_url_name = 'browse:computation_detail'

class ProcessListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Process
    registration.
    """
    model = models.Process
    resource_detail_page_url_name = 'browse:process_detail'

class DataCollectionListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Data
    Collection registration.
    """
    template_name = 'browse/data_collection_list.html'
    model = models.DataCollection
    resource_detail_page_url_name = 'browse:data_collection_detail'

    def get_queryset(self):
        data_collections = super().get_queryset()

        ACTIVITY_INDICATORS_KEY = 'Activity Indicators'
        SENSOR_MEASUREMENTS_KEY = 'Sensor Measurements'
        COMPUTATIONAL_MODELS_KEY = 'Computational Models'
        MIXED_KEY = 'Mixed'
        OTHER_KEY = 'Other'

        data_collections_by_type = {
            ACTIVITY_INDICATORS_KEY: [],
            SENSOR_MEASUREMENTS_KEY: [],
            COMPUTATIONAL_MODELS_KEY: [],
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
            is_activity_indicator = any([re.search('\/computationType/(.*)ActivityIndicator$', url) for url in type_urls])
            is_sensor_measurement = any([re.search('\/instrumentType/(.*)$', url) for url in type_urls])
            is_computational_model = any([re.search('\/computationType/(.*)$', url) for url in type_urls])

            if sum([is_sensor_measurement, is_computational_model]) > 1:
                data_collections_by_type[MIXED_KEY].append(dc)
            elif is_activity_indicator:
                data_collections_by_type[ACTIVITY_INDICATORS_KEY].append(dc)
            elif is_sensor_measurement:
                data_collections_by_type[SENSOR_MEASUREMENTS_KEY].append(dc)
            elif is_computational_model:
                data_collections_by_type[COMPUTATIONAL_MODELS_KEY].append(dc)
            else:
                data_collections_by_type[OTHER_KEY].append(dc)

        return data_collections_by_type

class CatalogueRelatedResourceListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Maps Data Collection-related features (e.g., breadcrumbs)
    to Catalogue-related features.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:catalogue_related_resource_types'
        return context

class CatalogueListView(CatalogueRelatedResourceListView):
    """
    A subclass of CatalogueRelatedResourceListView.

    Lists the detail page links for each Catalogue
    registration.
    """
    model = models.Catalogue
    resource_detail_page_url_name = 'browse:catalogue_detail'

class CatalogueEntryListView(CatalogueRelatedResourceListView):
    """
    A subclass of CatalogueRelatedResourceListView.

    Lists the detail page links for each Catalogue
    Entry registration.
    """
    model = models.CatalogueEntry
    resource_detail_page_url_name = 'browse:catalogue_entry_detail'

class CatalogueDataSubsetListView(CatalogueRelatedResourceListView):
    """
    A subclass of CatalogueRelatedResourceListView.

    Lists the detail page links for each Catalogue
    Data Subset registration.
    """
    model = models.CatalogueDataSubset
    resource_detail_page_url_name = 'browse:catalogue_data_subset_detail'

class WorkflowListView(ResourceListView):
    """
    A subclass of ResourceListView.

    Lists the detail page links for each Workflow
    registration.
    """
    template_name = 'browse/workflow_list.html'
    model = models.Workflow
    resource_detail_page_url_name = 'browse:workflow_detail'


class ResourceDetailView(TemplateView):
    """
    The detail page for a scientific metadata
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
            'Catalogues': self.resource.properties.catalogue_urls,
            'Catalogue Entries': self.resource.properties.catalogue_entry_urls,
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
        self.ontology_server_urls = self.resource.ontology_urls
        self.resource_server_urls = self.resource.metadata_urls
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
        context['scientific_metadata_creation_date_parsed'] = parse(self.resource.creation_date_json)
        context['scientific_metadata_last_modification_date_parsed'] = parse(self.resource.last_modification_date_json)
        context['server_url_conversion_url'] = reverse('browse:convert_server_urls')
        context['ontology_node_properties_mapping_url'] = reverse('browse:ontology_node_properties_mapping_url')
        return context

class OrganisationDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

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
    """
    A subclass of ResourceDetailView.

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

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Organisation': related_registrations.pop('Organisations'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().get(request, *args, **kwargs)

class ProjectDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

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
            disallowed_property_keys=['abstract']
        )
        return cleaned_property_table_dict

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Sub-projects': related_registrations.pop('Projects'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_abstract_split'] = self.format_and_split_string_by_multi_newlines(self.get_abstract_from_xml(self.resource))
        return context

class PlatformDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Platform registration.
    """
    model = models.Platform
    resource_list_by_type_url_name = 'browse:list_platforms'
    resource_download_url_name = 'utils:view_platform_as_xml'

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Child Platforms': related_registrations.pop('Platforms'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().get(request, *args, **kwargs)

class InstrumentDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Instrument registration.
    """
    model = models.Instrument
    resource_list_by_type_url_name = 'browse:list_instruments'
    resource_download_url_name = 'utils:view_instrument_as_xml'

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Members': related_registrations.pop('Instruments'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().get(request, *args, **kwargs)

class OperationDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Operation registration.
    """
    model = models.Operation
    resource_list_by_type_url_name = 'browse:list_operations'
    resource_download_url_name = 'utils:view_operation_as_xml'

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Platforms': related_registrations.pop('Platforms'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().get(request, *args, **kwargs)

class AcquisitionCapabilitiesDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Acquisition Capabilities registration.
    """
    model = models.AcquisitionCapabilities
    resource_list_by_type_url_name = 'browse:list_acquisition_capability_sets'
    resource_download_url_name = 'utils:view_acquisition_capability_set_as_xml'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().get(request, *args, **kwargs)

class AcquisitionDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    an Acquisition registration.
    """
    model = models.Acquisition
    resource_list_by_type_url_name = 'browse:list_acquisitions'
    resource_download_url_name = 'utils:view_acquisition_as_xml'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().get(request, *args, **kwargs)

class ComputationCapabilitiesDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Computation Capabilities registration.
    """
    model = models.ComputationCapabilities
    resource_list_by_type_url_name = 'browse:list_computation_capability_sets'
    resource_download_url_name = 'utils:view_computation_capability_set_as_xml'

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Child Computations': related_registrations.pop('Computation Capabilities'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().get(request, *args, **kwargs)

class ComputationDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Computation registration.
    """
    model = models.Computation
    resource_list_by_type_url_name = 'browse:list_computations'
    resource_download_url_name = 'utils:view_computation_as_xml'
    template_name = 'browse/detail/bases/computation.html'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().get(request, *args, **kwargs)

class ProcessDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

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
                'qualityAssessment',
            ]
        )
        return cleaned_property_table_dict

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Acquisitions': related_registrations.pop('Acquisitions'),
            'Computations': related_registrations.pop('Computations'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().get(request, *args, **kwargs)

class DataCollectionDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    A detail page displaying the properties of
    a Data Collection registration.
    """
    model = models.DataCollection
    resource_list_by_type_url_name = 'browse:list_data_collections'
    resource_download_url_name = 'utils:view_data_collection_as_xml'
    template_name = 'browse/detail/bases/data_collection.html'
    interaction_methods = []
    link_interaction_methods = []

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
                'type',
            ]
        )
        return cleaned_property_table_dict

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Projects': related_registrations.pop('Projects'),
            'Procedure': related_registrations.pop('Processes'),
            'Sub-collections': related_registrations.pop('Data Collections'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        self.resource = get_object_or_404(self.model, pk=self.resource_id)
        # API Interaction methods
        self.api_interaction_methods = models.APIInteractionMethod.objects.filter(scientific_metadata=self.resource)
        # Link interaction methods
        self.link_interaction_methods = self.resource.link_interaction_methods

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_interaction_methods'] = list(self.api_interaction_methods)
        context['link_interaction_methods'] = list(self.link_interaction_methods)
        context['data_collection_id'] = self.resource_id
        
        return context

class CatalogueRelatedResourceDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

    Maps Data Collection-related features (e.g., breadcrumbs)
    to Catalogue-related features.

    This view is intended to be subclassed and to not
    be called directly.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:catalogue_related_resource_types'
        return context

class CatalogueDetailView(CatalogueRelatedResourceDetailView):
    """
    A subclass of CatalogueRelatedResourceDetailView.

    A detail page displaying the properties of
    a Catalogue registration.
    """
    model = models.Catalogue
    resource_list_by_type_url_name = 'browse:list_catalogues'
    resource_download_url_name = 'utils:view_catalogue_as_xml'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().get(request, *args, **kwargs)

class CatalogueEntryDetailView(CatalogueRelatedResourceDetailView):
    """
    A subclass of CatalogueRelatedResourceDetailView.

    A detail page displaying the properties of
    a Catalogue Entry registration.
    """
    model = models.CatalogueEntry
    resource_list_by_type_url_name = 'browse:list_catalogue_entries'
    resource_download_url_name = 'utils:view_catalogue_entry_as_xml'

    def get_description_from_xml(self, resource):
        return etree.fromstring(resource.xml.encode('utf-8')).find('{https://metadata.pithia.eu/schemas/2.2}entryDescription').text

    def configure_resource_copy_for_property_table(self, property_table_dict: dict) -> dict:
        cleaned_property_table_dict = super().configure_resource_copy_for_property_table(property_table_dict)
        cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
            cleaned_property_table_dict,
            disallowed_property_keys=[
                'entryName',
                'entryDescription',
            ]
        )
        return cleaned_property_table_dict

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'From Catalogue': related_registrations.pop('Catalogues'),
        })
        return related_registrations

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().get(request, *args, **kwargs)

class CatalogueDataSubsetDetailView(CatalogueRelatedResourceDetailView):
    """
    A subclass of CatalogueRelatedResourceDetailView.

    A detail page displaying the properties of
    a Catalogue Data Subset registration.
    """
    model = models.CatalogueDataSubset
    resource_list_by_type_url_name = 'browse:list_catalogue_data_subsets'
    resource_download_url_name = 'utils:view_catalogue_data_subset_as_xml'
    template_name = 'browse/detail/bases/catalogue_data_subset.html'

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
                'entryIdentifier',
                'qualityAssessment',
                'source',
            ]
        )
        return cleaned_property_table_dict

    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'From Data Collection': related_registrations.pop('Data Collections'),
            'Catalogue Entry': related_registrations.pop('Catalogue Entries'),
        })
        return related_registrations

    def add_handle_data_to_context(self, context):
        context['handles'] = self.handles
        context['data_for_handles'] = []
        if self.data_for_handles:
            context['data_for_handles'] = [reformat_and_clean_resource_copy_for_property_table(data) for data in self.data_for_handles if data is not None]
        return context

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        self.handle = None
        self.handle_data = None
        self.handles = []
        self.data_for_handles = []

        try:
            self.client, self.credentials = instantiate_client_and_load_credentials()
        except BaseException as e:
            logger.exception('An unexpected error occurred whilst instantiating the PyHandle client.')
            return super().get(request, *args, **kwargs)

        handle_url_mappings = models.HandleURLMapping.objects.for_url(request.get_full_path())
        self.handles = [hum.handle_name for hum in handle_url_mappings]
        self.data_for_handles = [get_handle_record(handle, self.client) for handle in self.handles]

        try:
            self.resource = self.model.objects.get(pk=self.resource_id)
        except models.CatalogueDataSubset.DoesNotExist:
            context = {}
            context = self.add_handle_data_to_context(context)
            return render(request, 'browse/detail_404.html', context)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.add_handle_data_to_context(context)
        return context

class WorkflowDetailView(ResourceDetailView):
    """
    A subclass of ResourceDetailView.

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
    
    def get_related_registrations(self):
        related_registrations = super().get_related_registrations()
        related_registrations.update({
            'Involved Data Collections': related_registrations.pop('Data Collections'),
        })
        return related_registrations

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
