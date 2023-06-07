# TODO: remove old code
from bson.objectid import ObjectId
# End of TODO: remove old code
from dateutil.parser import parse
from django.http import (
    JsonResponse,
    # TODO: remove old code
    # HttpResponseNotFound,
)
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.urls import reverse
from django.views.generic import (
    ListView,
    # TODO: remove old code
    TemplateView,
)

from .services import (
    create_readable_scientific_metadata_flattened,
    get_server_urls_from_scientific_metadata_flattened,
    map_metadata_server_urls_to_browse_urls,
    map_ontology_server_urls_to_browse_urls,
)

from common import (
    models,
    mongodb_models,
)
from handle_management.handle_api import (
    get_handle_record,
    instantiate_client_and_load_credentials,
)
from utils.dict_helpers import flatten
from utils.mapping_functions import prepare_resource_for_template

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
    # num_current_organsations = mongodb_models.CurrentOrganisation.estimated_document_count()
    # num_current_individuals = mongodb_models.CurrentIndividual.estimated_document_count()
    # num_current_projects = mongodb_models.CurrentProject.estimated_document_count()
    # num_current_platforms = mongodb_models.CurrentPlatform.estimated_document_count()
    # num_current_instruments = mongodb_models.CurrentInstrument.estimated_document_count()
    # num_current_operations = mongodb_models.CurrentOperation.estimated_document_count()
    # num_current_acquisition_capability_sets = mongodb_models.CurrentAcquisitionCapability.estimated_document_count()
    # num_current_acquisitions = mongodb_models.CurrentAcquisition.estimated_document_count()
    # num_current_computation_capability_sets = mongodb_models.CurrentComputationCapability.estimated_document_count()
    # num_current_computations = mongodb_models.CurrentComputation.estimated_document_count()
    # num_current_processes = mongodb_models.CurrentProcess.estimated_document_count()
    # num_current_data_collections = mongodb_models.CurrentDataCollection.estimated_document_count()
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
    return render(request, 'browse/schemas.html', {
        'title': _XML_SCHEMAS_PAGE_TITLE
    })

class ResourceListView(ListView):
    template_name = 'browse/resource_list_by_type.html'
    context_object_name = 'resources'

    description = ''
    resource_mongodb_model = None
    resource_type_plural = ''
    resource_detail_page_url_name = ''
    resource_list = []

    def get_resource_list(self):
        resource_list = list(self.resource_mongodb_model.find({}))
        return list(map(prepare_resource_for_template, resource_list))
    
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model.type_plural_readable.title()
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
    model = models.Organisation
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    resource_detail_page_url_name = 'browse:organisation_detail'
    description = 'Data Provider/Owner organisation'

class IndividualListView(ResourceListView):
    model = models.Individual
    resource_mongodb_model = mongodb_models.CurrentIndividual
    resource_detail_page_url_name = 'browse:individual_detail'
    description = 'An individual, acting in a particular role and associated with an Organisation'

class ProjectListView(ResourceListView):
    model = models.Project
    resource_mongodb_model = mongodb_models.CurrentProject
    resource_detail_page_url_name = 'browse:project_detail'
    description = 'An identifiable activity designed to accomplish a set of objectives'

class PlatformListView(ResourceListView):
    model = models.Platform
    resource_mongodb_model = mongodb_models.CurrentPlatform
    resource_detail_page_url_name = 'browse:platform_detail'
    description = 'An identifiable object that brings the acquisition instrument(s) to the appropriate environment (e.g., satellite, ground observatory)'

class InstrumentListView(ResourceListView):
    model = models.Instrument
    resource_mongodb_model = mongodb_models.CurrentInstrument
    resource_detail_page_url_name = 'browse:instrument_detail'
    description = 'An object responsible for interacting with the Feature of Interest in order to acquire Observed Property values'

class OperationListView(ResourceListView):
    model = models.Operation
    resource_mongodb_model = mongodb_models.CurrentOperation
    resource_detail_page_url_name = 'browse:operation_detail'
    description = 'Description of how a platform operates in order to support data acquisition by the instrument'

class AcquisitionCapabilitiesListView(ResourceListView):
    model = models.AcquisitionCapabilities
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    resource_detail_page_url_name = 'browse:acquisition_capability_set_detail'
    description = ''

class AcquisitionListView(ResourceListView):
    model = models.Acquisition
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_detail_page_url_name = 'browse:acquisition_detail'
    description = 'Interaction of the Instrument with the Feature of Interest to obtain its Observed Properties'

class ComputationCapabilitiesListView(ResourceListView):
    model = models.ComputationCapabilities
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    resource_detail_page_url_name = 'browse:computation_capability_set_detail'
    description = ''

class ComputationListView(ResourceListView):
    model = models.Computation
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_detail_page_url_name = 'browse:computation_detail'
    description = 'Numerical calculation without interacting with the Feature of Interest; characterised by its numerical input and output'

class ProcessListView(ResourceListView):
    model = models.Process
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_detail_page_url_name = 'browse:process_detail'
    description = 'A designated procedure used to assign a number, term, or other symbols to a Phenomenon generating the Result; consists of Acquisitions and Computations'

class DataCollectionListView(ResourceListView):
    model = models.DataCollection
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_detail_page_url_name = 'browse:data_collection_detail'
    description = 'Top-level definition of a collection of the model or measurement data, with CollectionResults pointing to its URL(s) for accessing the data. Note: data collections do not include begin and end times, please see Catalogue'

class CatalogueRelatedResourceListView(ResourceListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:catalogue_related_resource_types'
        return context

class CatalogueListView(CatalogueRelatedResourceListView):
    model = models.Catalogue
    resource_mongodb_model = mongodb_models.CurrentCatalogue
    resource_detail_page_url_name = 'browse:catalogue_detail'
    description = ''

class CatalogueEntryListView(CatalogueRelatedResourceListView):
    model = models.CatalogueEntry
    resource_mongodb_model = mongodb_models.CurrentCatalogueEntry
    resource_detail_page_url_name = 'browse:catalogue_entry_detail'
    description = ''

class CatalogueDataSubsetListView(CatalogueRelatedResourceListView):
    model = models.CatalogueDataSubset
    resource_mongodb_model = mongodb_models.CurrentCatalogueDataSubset
    resource_detail_page_url_name = 'browse:catalogue_data_subset_detail'
    description = ''

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
        self.resource = get_object_or_404(self.model, pk=self.resource_id)
        self.scientific_metadata = prepare_resource_for_template(self.resource.json)
        self.scientific_metadata_flattened = flatten(self.scientific_metadata)
        self.ontology_server_urls, self.resource_server_urls = get_server_urls_from_scientific_metadata_flattened(self.scientific_metadata_flattened)
        self.scientific_metadata_readable = create_readable_scientific_metadata_flattened(self.scientific_metadata_flattened)
        self.title = self.resource.name
        # TODO: remove old code
        # self.resource_human_readable = {}
        # if self.resource is None:
        #     # Extra check done for data_collection() view
        #     self.resource = self.resource_mongodb_model.find_one({
        #         '_id': ObjectId(self.resource_id)
        #     })
        # if self.resource is None:
        #     self.title = 'Not found'
        #     self.template_name = 'browse/detail_404.html'
        #     return super().get(request, *args, **kwargs)
        #     # return HttpResponseNotFound('Resource not found.')
        # self.resource = prepare_resource_for_template(self.resource)
        # self.resource_flattened = flatten(self.resource)
        # self.ontology_server_urls, self.resource_server_urls = get_server_urls_from_scientific_metadata_flattened(self.resource_flattened)
        # self.resource_human_readable = create_readable_scientific_metadata_flattened(self.resource_flattened)
        # self.title = self.resource['identifier']['PITHIA_Identifier']['localID']
        # if 'name' in self.resource:
        #     self.title = self.resource['name']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:data_collection_related_resource_types'
        context['resource_list_page_breadcrumb_text'] = self.model.type_plural_readable.title()
        context['resource_list_page_breadcrumb_url_name'] = self.resource_list_by_type_url_name
        if self.resource is None:
            return context
        context['resource'] = self.resource
        context['scientific_metadata_flattened'] = self.scientific_metadata_flattened
        context['ontology_server_urls'] = self.ontology_server_urls
        context['resource_server_urls'] = self.resource_server_urls
        context['scientific_metadata_readable'] = self.scientific_metadata_readable
        context['scientific_metadata_creation_date_parsed'] = parse(self.resource.creation_date_json)
        context['scientific_metadata_last_modification_date_parsed'] = parse(self.resource.last_modification_date_json)
        context['server_url_conversion_url'] = reverse('browse:convert_server_urls')
        return context

class OrganisationDetailView(ResourceDetailView):
    model = models.Organisation
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    resource_type_plural = 'Organisations'
    resource_list_by_type_url_name = 'browse:list_organisations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().get(request, *args, **kwargs)

class IndividualDetailView(ResourceDetailView):
    model = models.Individual
    resource_mongodb_model = mongodb_models.CurrentIndividual
    resource_type_plural = 'Individuals'
    resource_list_by_type_url_name = 'browse:list_individuals'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().get(request, *args, **kwargs)

class ProjectDetailView(ResourceDetailView):
    model = models.Project
    resource_mongodb_model = mongodb_models.CurrentProject
    resource_type_plural = 'Projects'
    resource_list_by_type_url_name = 'browse:list_projects'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().get(request, *args, **kwargs)

class PlatformDetailView(ResourceDetailView):
    model = models.Platform
    resource_mongodb_model = mongodb_models.CurrentPlatform
    resource_type_plural = 'Platforms'
    resource_list_by_type_url_name = 'browse:list_platforms'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().get(request, *args, **kwargs)

class InstrumentDetailView(ResourceDetailView):
    model = models.Instrument
    resource_mongodb_model = mongodb_models.CurrentInstrument
    resource_type_plural = 'Instruments'
    resource_list_by_type_url_name = 'browse:list_instruments'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().get(request, *args, **kwargs)

class OperationDetailView(ResourceDetailView):
    model = models.Operation
    resource_mongodb_model = mongodb_models.CurrentOperation
    resource_type_plural = 'Operations'
    resource_list_by_type_url_name = 'browse:list_operations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().get(request, *args, **kwargs)

class AcquisitionCapabilitiesDetailView(ResourceDetailView):
    model = models.AcquisitionCapabilities
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    resource_type_plural = 'Acquisition Capabilities'
    resource_list_by_type_url_name = 'browse:list_acquisition_capability_sets'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().get(request, *args, **kwargs)

class AcquisitionDetailView(ResourceDetailView):
    model = models.Acquisition
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    resource_list_by_type_url_name = 'browse:list_acquisitions'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().get(request, *args, **kwargs)

class ComputationCapabilitiesDetailView(ResourceDetailView):
    model = models.ComputationCapabilities
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    resource_type_plural = 'Computation Capabilities'
    resource_list_by_type_url_name = 'browse:list_computation_capability_sets'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().get(request, *args, **kwargs)

class ComputationDetailView(ResourceDetailView):
    model = models.Computation
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_type_plural = 'Computations'
    resource_list_by_type_url_name = 'browse:list_computations'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().get(request, *args, **kwargs)

class ProcessDetailView(ResourceDetailView):
    model = models.Process
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_type_plural = 'Processes'
    resource_list_by_type_url_name = 'browse:list_processes'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().get(request, *args, **kwargs)

class DataCollectionDetailView(ResourceDetailView):
    model = models.DataCollection
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_type_plural = 'Data Collections'
    resource_list_by_type_url_name = 'browse:list_data_collections'
    template_name = 'browse/detail_interaction_methods.html'
    interaction_methods = []
    link_interaction_methods = []

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        # TODO: remove old code
        # self.resource_id = self.kwargs['data_collection_id']
        # self.resource = self.resource_mongodb_model.find_one({
        #     '_id': ObjectId(self.resource_id)
        # })
        # if self.resource is None:
        #     return HttpResponseNotFound('Resource not found.')
        # self.interaction_methods = mongodb_models.CurrentDataCollectionInteractionMethod.find({
        #     'data_collection_localid': self.resource['identifier']['PITHIA_Identifier']['localID']
        # })
        # if 'collectionResults' in self.resource:
        #     if 'source' in self.resource['collectionResults']:
        #         self.link_interaction_methods = self.resource['collectionResults']['source']

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: temp whilst TechnicalMetadata model is not implemented
        context['interaction_methods'] = []
        # context['interaction_methods'] = list(models.TechnicalMetadata.objects.interaction_methods_for_data_collection(self.resource.pk))
        # try:
        #     context['link_interaction_methods'] = self.resource.url_interaction_methods
        # except KeyError:
        #     context['link_interaction_methods'] = []
        context['data_collection_id'] = self.resource_id
        # TODO: remove old code
        # context = super().get_context_data(**kwargs)
        # context['interaction_methods'] = list(self.interaction_methods)
        # context['link_interaction_methods'] = list(self.link_interaction_methods)
        # context['data_collection_id'] = self.resource_id
        
        return context

class CatalogueRelatedResourceDetailView(ResourceDetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _CATALOGUE_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_type_list_page_breadcrumb_url_name'] = 'browse:catalogue_related_resource_types'
        return context

class CatalogueDetailView(CatalogueRelatedResourceDetailView):
    model = models.Catalogue
    resource_mongodb_model = mongodb_models.CurrentCatalogue
    resource_list_by_type_url_name = 'browse:list_catalogues'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().get(request, *args, **kwargs)

class CatalogueEntryDetailView(CatalogueRelatedResourceDetailView):
    model = models.CatalogueEntry
    resource_mongodb_model = mongodb_models.CurrentCatalogueEntry
    resource_list_by_type_url_name = 'browse:list_catalogue_entries'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().get(request, *args, **kwargs)

class CatalogueDataSubsetDetailView(CatalogueRelatedResourceDetailView):
    model = models.CatalogueDataSubset
    resource_mongodb_model = mongodb_models.CurrentCatalogueDataSubset
    resource_list_by_type_url_name = 'browse:list_catalogue_data_subsets'

    def get(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        self.client, self.credentials = instantiate_client_and_load_credentials()
        handle_url_mapping = mongodb_models.HandleUrlMapping.find_one({
            'url': {'$regex': f'{request.get_full_path()}$'}
        })
        self.handle = None
        self.handle_data = None
        if handle_url_mapping is not None:
            self.handle = handle_url_mapping['handle_name']
            self.handle_data = get_handle_record(self.handle, self.client)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['handle'] = self.handle
        context['handle_data'] = None
        if self.handle_data is not None:
            context['handle_data'] = create_readable_scientific_metadata_flattened(self.handle_data)
        return context

def get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls(request):
    ontology_server_urls = []
    resource_server_urls = []
    if 'ontology-server-urls' in request.GET:
        ontology_server_urls = request.GET['ontology-server-urls'].split(',')
    if 'resource-server-urls' in request.GET:
        resource_server_urls = request.GET['resource-server-urls'].split(',')
    esc_ontology_urls = map_ontology_server_urls_to_browse_urls(ontology_server_urls)
    esc_resource_urls = map_metadata_server_urls_to_browse_urls(resource_server_urls)
    
    return JsonResponse({
        'ontology_urls': esc_ontology_urls,
        'resource_urls': esc_resource_urls,
    })
