import re
from dateutil.parser import parse
from django.urls import reverse
from common import mongodb_models
from django.shortcuts import render
from bson.objectid import ObjectId
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView

from utils.mapping_functions import prepare_resource_for_template
from validation.url_validation import (
    PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
    SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
)
from utils.string_helpers import _split_camel_case

_INDEX_PAGE_TITLE = 'Browse Metadata'
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
    num_current_organsations = mongodb_models.CurrentOrganisation.count_documents({})
    num_current_individuals = mongodb_models.CurrentIndividual.count_documents({})
    num_current_projects = mongodb_models.CurrentProject.count_documents({})
    num_current_platforms = mongodb_models.CurrentPlatform.count_documents({})
    num_current_instruments = mongodb_models.CurrentInstrument.count_documents({})
    num_current_operations = mongodb_models.CurrentOperation.count_documents({})
    num_current_acquisition_capability_sets = mongodb_models.CurrentAcquisitionCapability.count_documents({})
    num_current_acquisitions = mongodb_models.CurrentAcquisition.count_documents({})
    num_current_computation_capability_sets = mongodb_models.CurrentComputationCapability.count_documents({})
    num_current_computations = mongodb_models.CurrentComputation.count_documents({})
    num_current_processes = mongodb_models.CurrentProcess.count_documents({})
    num_current_data_collections = mongodb_models.CurrentDataCollection.count_documents({})
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
    num_current_catalogues = mongodb_models.CurrentCatalogue.count_documents({})
    num_current_catalogue_entries = mongodb_models.CurrentCatalogueEntry.count_documents({})
    num_current_catalogue_data_subsets = mongodb_models.CurrentCatalogueDataSubset.count_documents({})
    return render(request, 'browse/catalogue_related_resource_types.html', {
        'title': _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE,
        'num_current_catalogues': num_current_catalogues,
        'num_current_catalogue_entries': num_current_catalogue_entries,
        'num_current_catalogue_data_subsets': num_current_catalogue_data_subsets,
        'browse_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
    })

def schemas(request):
    return render(request, 'browse/schemas.html', {
        'title': _XML_SCHEMAS_PAGE_TITLE
    })

class ResourceListView(TemplateView):
    template_name = 'browse/resource_list_by_type.html'
    description = ''
    resource_mongodb_model = None
    resource_type_plural = ''
    resource_detail_page_url_name = ''
    resource_list = []

    def get_resource_list(self):
        resource_list = list(self.resource_mongodb_model.find({}))
        return list(map(prepare_resource_for_template, resource_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.resource_type_plural
        context['description'] = self.description
        context['resource_list'] = self.get_resource_list()
        context['empty_resource_list_text'] = f'No {self.resource_type_plural.lower()} have been registered with the e-Science Centre.'
        context['resource_detail_page_url_name'] = self.resource_detail_page_url_name
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrganisationListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    resource_type_plural = 'Organisations'
    resource_detail_page_url_name = 'browse:organisation_detail'
    description = 'Data Provider/Owner organisation'

class IndividualListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    resource_type_plural = 'Individuals'
    resource_detail_page_url_name = 'browse:individual_detail'
    description = 'An individual, acting in a particular role and associated with an Organisation'

class ProjectListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentProject
    resource_type_plural = 'Projects'
    resource_detail_page_url_name = 'browse:project_detail'
    description = 'An identifiable activity designed to accomplish a set of objectives'

class PlatformListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    resource_type_plural = 'Platforms'
    resource_detail_page_url_name = 'browse:platform_detail'
    description = 'An identifiable object that brings the acquisition instrument(s) to the appropriate environment (e.g., satellite, ground observatory)'

class InstrumentListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    resource_type_plural = 'Instruments'
    resource_detail_page_url_name = 'browse:instrument_detail'
    description = 'An object responsible for interacting with the Feature of Interest in order to acquire Observed Property values'

class OperationListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    resource_type_plural = 'Operations'
    resource_detail_page_url_name = 'browse:operation_detail'
    description = 'Description of how a platform operates in order to support data acquisition by the instrument'

class AcquisitionCapabilitiesListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    resource_detail_page_url_name = 'browse:acquisition_capability_set_detail'
    description = ''

class AcquisitionListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    resource_detail_page_url_name = 'browse:acquisition_detail'
    description = 'Interaction of the Instrument with the Feature of Interest to obtain its Observed Properties'

class ComputationCapabilitiesListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    resource_detail_page_url_name = 'browse:computation_capability_set_detail'
    description = ''

class ComputationListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_type_plural = 'Computations'
    resource_detail_page_url_name = 'browse:computation_detail'
    description = 'Numerical calculation without interacting with the Feature of Interest; characterised by its numerical input and output'

class ProcessListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_type_plural = 'Processes'
    resource_detail_page_url_name = 'browse:process_detail'
    description = 'A designated procedure used to assign a number, term, or other symbols to a Phenomenon generating the Result; consists of Acquisitions and Computations'

class DataCollectionListView(ResourceListView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_type_plural = 'Data Collections'
    resource_detail_page_url_name = 'browse:data_collection_detail'
    description = 'Top-level definition of a collection of the model or measurement data, with CollectionResults pointing to its URL(s) for accessing the data. Note: data collections do not include begin and end times, please see Catalogue'

class CatalogueRelatedResourceListView(ResourceListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:catalogue_related_resource_types'
        return context

class CatalogueListView(CatalogueRelatedResourceListView):
    resource_mongodb_model = mongodb_models.CurrentCatalogue
    resource_type_plural = 'Catalogues'
    resource_detail_page_url_name = 'browse:catalogue_detail'
    description = ''

class CatalogueEntryListView(CatalogueRelatedResourceListView):
    resource_mongodb_model = mongodb_models.CurrentCatalogueEntry
    resource_type_plural = 'Catalogue Entries'
    resource_detail_page_url_name = 'browse:catalogue_entry_detail'
    description = ''

class CatalogueDataSubsetListView(CatalogueRelatedResourceListView):
    resource_mongodb_model = mongodb_models.CurrentCatalogueDataSubset
    resource_type_plural = 'Catalogue Data Subsets'
    resource_detail_page_url_name = 'browse:catalogue_data_subset_detail'
    description = ''

def flatten(d):
    out = {}
    if d is None:
        return out
    for key, value in d.items():
        if isinstance(value, dict):
            value = [value]
        if isinstance(value, list):
            index = 0
            for subdict in value:
                index = int(index) + 1
                deeper = flatten(subdict).items()
                out.update({
                    key + ' <b>(' + str(index) + '/' + str(len(value)) + ')</b>.' + key2: value2 for key2, value2 in deeper
                })
        else:
            out[key] = value
    return out

def _get_ontology_server_urls_from_flattened_resource(resource_flattened):
    ontology_server_urls = set()
    resource_server_urls = set()
    for key, value in resource_flattened.items():
        if key.endswith('@xlink:href') and value.startswith(SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE):
            ontology_server_urls.add(value)
        if key.endswith('@xlink:href') and value.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE):
            resource_server_urls.add(value)

    return list(ontology_server_urls), list(resource_server_urls)

def _update_flattened_resource_keys_to_human_readable_html(resource_flattened):
    hidden_keys = [
        '_id',
        'description',
    ]
    hidden_key_regex = [
        re.compile(r'^name'),
        re.compile(r'^contactinfo'),
        re.compile(r'^identifier'),
        re.compile(r'.*onlineresource <b>(1/1)</b>\.description'),
        re.compile(r'.*onlineresource <b>(1/1)</b>\.linkage'),
        # re.compile(r'.*onlineresource <b>1</b>\.name'),
    ]
    resource_human_readable = {}
    for key in resource_flattened:
        if key.startswith('@') or any(x == key.lower() for x in hidden_keys) or any(regex for regex in hidden_key_regex if re.match(regex, key.lower())):
            continue
        key_split_by_dot = key.split('.')
        human_readable_key_strings = []
        for string in key_split_by_dot:
            # If there is only one occurrence of a property
            # doesn't make sense to keep the number suffix
            is_only_numbered_key = True
            if string.endswith('<b>(1/1)</b>'):
                for key2 in resource_flattened:
                    if string.replace('<b>(1/', '<b>(2/') in key2:
                        is_only_numbered_key = False
            if is_only_numbered_key:
                string = string.replace('<b>(1/1)</b>', '')

            # Skip these strings
            if  string.startswith('#') or string == '@xlink:href':
                continue

            # Only keep the part of the key after the ':'
            if ':' in string:
                index_of_colon = string.index(':')
                string = string[index_of_colon + 1:]
            # Only keep the part of the key after the '@'
            if '@' in string:
                index_of_at_symbol = string.index('@')
                string = string[index_of_at_symbol + 1:]

            # Append the string that the be part of the 
            # human-readable key
            if string == '_id' or string.isupper():
                human_readable_key_strings.append(string)
            elif '_' in string:
                human_readable_string = ' '.join(string.split('_'))
                human_readable_string = ' '.join(_split_camel_case(human_readable_string))
                human_readable_key_strings.append(human_readable_string)
            else:
                human_readable_string = ' '.join(_split_camel_case(string))
                if not human_readable_string[0].isupper():
                    human_readable_string = human_readable_string.title()
                human_readable_key_strings.append(human_readable_string)
        human_readable_key_strings[-1] = f'<b>{human_readable_key_strings[-1]}</b>'
        human_readable_key_last_string = human_readable_key_strings[-1]
        human_readable_key_strings.pop()

        human_readable_key = ' > '.join(human_readable_key_strings).strip()
        if human_readable_key.startswith('Om:'):
            human_readable_key = human_readable_key.replace('Om:', '')
        if len(human_readable_key_strings):
            human_readable_key = f'{human_readable_key_last_string} <small class="text-muted fst-italic">(from {human_readable_key})</small>'
        else:
            human_readable_key = human_readable_key_last_string
        if human_readable_key != '':
            resource_human_readable[human_readable_key] = resource_flattened[key]
    return resource_human_readable

class ResourceDetailView(TemplateView):
    title = 'Resource Detail'
    resource = None
    resource_id = ''
    resource_mongodb_model = None
    resource_type_plural = ''
    resource_flattened = None
    resource_human_readable = {}
    ontology_server_urls = []
    resource_server_urls = []
    resource_list_by_type_url_name = ''
    template_name = 'browse/detail.html'

    def get(self, request, *args, **kwargs):
        self.resource_human_readable = {}
        if self.resource is None:
            # Extra check done for data_collection() view
            self.resource = self.resource_mongodb_model.find_one({
                '_id': ObjectId(self.resource_id)
            })
        if self.resource is None:
            return HttpResponseNotFound('Resource not found.')
        self.resource = prepare_resource_for_template(self.resource)
        self.resource_flattened = flatten(self.resource)
        self.ontology_server_urls, self.resource_server_urls = _get_ontology_server_urls_from_flattened_resource(self.resource_flattened)
        self.resource_human_readable = _update_flattened_resource_keys_to_human_readable_html(self.resource_flattened)
        self.title = self.resource['identifier']['PITHIA_Identifier']['localID']
        if 'name' in self.resource:
            self.title = self.resource['name']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['resource'] = self.resource
        context['resource_flattened'] = self.resource_flattened
        context['ontology_server_urls'] = self.ontology_server_urls
        context['resource_server_urls'] = self.resource_server_urls
        context['resource_human_readable'] = self.resource_human_readable
        context['resource_creation_date'] = parse(self.resource['identifier']['PITHIA_Identifier']['creationDate'])
        context['resource_last_modification_date'] = parse(self.resource['identifier']['PITHIA_Identifier']['lastModificationDate'])
        context['server_url_conversion_url'] = reverse('utils:convert_server_urls')
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        context['resource_list_page_breadcrumb_text'] = self.resource_type_plural
        context['resource_list_page_breadcrumb_url_name'] = self.resource_list_by_type_url_name
        return context

class OrganisationDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    resource_type_plural = 'Organisations'
    resource_list_by_type_url_name = 'browse:list_organisations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().get(request, *args, **kwargs)

class IndividualDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    resource_type_plural = 'Individuals'
    resource_list_by_type_url_name = 'browse:list_individuals'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().get(request, *args, **kwargs)

class ProjectDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentProject
    resource_type_plural = 'Projects'
    resource_list_by_type_url_name = 'browse:list_projects'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().get(request, *args, **kwargs)

class PlatformDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    resource_type_plural = 'Platforms'
    resource_list_by_type_url_name = 'browse:list_platforms'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().get(request, *args, **kwargs)

class InstrumentDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    resource_type_plural = 'Instruments'
    resource_list_by_type_url_name = 'browse:list_instruments'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().get(request, *args, **kwargs)

class OperationDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    resource_type_plural = 'Operations'
    resource_list_by_type_url_name = 'browse:list_operations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().get(request, *args, **kwargs)

class AcquisitionCapabilitiesDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    resource_list_by_type_url_name = 'browse:list_acquisition_capability_sets'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().get(request, *args, **kwargs)

class AcquisitionDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    resource_list_by_type_url_name = 'browse:list_acquisitions'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().get(request, *args, **kwargs)

class ComputationCapabilitiesDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    resource_list_by_type_url_name = 'browse:list_computation_capability_sets'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().get(request, *args, **kwargs)

class ComputationDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_type_plural = 'Computations'
    resource_list_by_type_url_name = 'browse:list_computations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().get(request, *args, **kwargs)

class ProcessDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_type_plural = 'Processes'
    resource_list_by_type_url_name = 'browse:list_processes'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().get(request, *args, **kwargs)

class DataCollectionDetailView(ResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_type_plural = 'Data Collections'
    resource_list_by_type_url_name = 'browse:list_data_collections'
    template_name = 'browse/detail_interaction_methods.html'
    interaction_methods = []
    link_interaction_methods = []

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        self.resource = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        if self.resource is None:
            return HttpResponseNotFound('Resource not found.')
        self.interaction_methods = mongodb_models.CurrentDataCollectionInteractionMethod.find({
            'data_collection_localid': self.resource['identifier']['PITHIA_Identifier']['localID']
        })
        if 'collectionResults' in self.resource:
            if 'source' in self.resource['collectionResults']:
                self.link_interaction_methods = self.resource['collectionResults']['source']

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction_methods'] = list(self.interaction_methods)
        context['link_interaction_methods'] = list(self.link_interaction_methods)
        context['data_collection_id'] = self.resource_id
        
        return context

class CatalogueRelatedResourceDetailView(ResourceDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:catalogue_related_resource_types'
        return context

class CatalogueDetailView(CatalogueRelatedResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentCatalogue
    resource_type_plural = 'Catalogues'
    resource_list_by_type_url_name = 'browse:list_catalogues'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().get(request, *args, **kwargs)

class CatalogueEntryDetailView(CatalogueRelatedResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentCatalogueEntry
    resource_type_plural = 'Catalogue Entries'
    resource_list_by_type_url_name = 'browse:list_catalogue_entries'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().get(request, *args, **kwargs)

class CatalogueDataSubsetDetailView(CatalogueRelatedResourceDetailView):
    resource_mongodb_model = mongodb_models.CurrentCatalogueDataSubset
    resource_type_plural = 'Catalogue Data Subsets'
    resource_list_by_type_url_name = 'browse:list_catalogue_data_subsets'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        return super().get(request, *args, **kwargs)
