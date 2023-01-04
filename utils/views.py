from .url_helpers import convert_ontology_server_urls_to_browse_urls, convert_resource_server_urls_to_browse_urls
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http import HttpResponseNotFound
from bson import ObjectId
from common.mongodb_models import (
    CurrentOrganisation,
    CurrentIndividual,
    CurrentProject,
    CurrentPlatform,
    CurrentOperation,
    CurrentInstrument,
    CurrentAcquisitionCapability,
    CurrentAcquisition,
    CurrentComputationCapability,
    CurrentComputation,
    CurrentProcess,
    CurrentDataCollection,
    CurrentCatalogue,
    CurrentCatalogueEntry,
    CurrentCatalogueDataSubset,
    OriginalMetadataXml,
)
from resource_management.views import _INDEX_PAGE_TITLE


# Create your views here.

def get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls(request):
    ontology_server_urls = []
    resource_server_urls = []
    if 'ontology-server-urls' in request.GET:
        ontology_server_urls = request.GET['ontology-server-urls'].split(',')
    if 'resource-server-urls' in request.GET:
        resource_server_urls = request.GET['resource-server-urls'].split(',')
    esc_ontology_urls = convert_ontology_server_urls_to_browse_urls(ontology_server_urls)
    esc_resource_urls = convert_resource_server_urls_to_browse_urls(resource_server_urls)
    
    return JsonResponse({
        'ontology_urls': esc_ontology_urls,
        'resource_urls': esc_resource_urls,
    })

class ResourceXmlDownloadView(TemplateView):
    resource_id = ''
    resource_mongodb_model = None
    resource_name = ''
    resource_localid = ''
    template_name = 'utils/resource_as_xml.html'
    xml = ''
    resource_management_list_page_breadcrumb_text = ''
    resource_management_list_page_breadcrumb_url_name = ''

    def get(self, request, *args, **kwargs):
        original_metadata_xml = OriginalMetadataXml.find_one({
            'resourceId': ObjectId(self.resource_id)
        })
        if original_metadata_xml is None:
            return HttpResponseNotFound('The XML for this resource was not found.')
        self.xml = original_metadata_xml['value']
        resource = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        }, projection={
            'identifier': 1,
            'name': 1,
        })
        self.resource_localid = resource['identifier']['PITHIA_Identifier']['localID']
        self.resource_name = resource['name']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_name'] = self.resource_name
        context['resource_localid'] = self.resource_localid
        context['xml'] = self.xml
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

class view_organisation_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentOrganisation
    resource_management_list_page_breadcrumb_text = 'Register & Manage Organisations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)

class view_individual_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentIndividual
    resource_management_list_page_breadcrumb_text = 'Register & Manage Individuals'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class view_project_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentProject
    resource_management_list_page_breadcrumb_text = 'Register & Manage Projects'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class view_platform_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentPlatform
    resource_management_list_page_breadcrumb_text = 'Register & Manage Platforms'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class view_operation_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentOperation
    resource_management_list_page_breadcrumb_text = 'Register & Manage Operations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class view_instrument_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentInstrument
    resource_management_list_page_breadcrumb_text = 'Register & Manage Instruments'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class view_acquisition_capability_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_management_list_page_breadcrumb_text = 'Register & Manage Acquisition Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capabilities'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_id']
        return super().dispatch(request, *args, **kwargs)

class view_acquisition_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentAcquisition
    resource_management_list_page_breadcrumb_text = 'Register & Manage Acquisitions'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class view_computation_capability_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentComputationCapability
    resource_management_list_page_breadcrumb_text = 'Register & Manage Computation Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capabilities'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_id']
        return super().dispatch(request, *args, **kwargs)

class view_computation_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentComputation
    resource_management_list_page_breadcrumb_text = 'Register & Manage Computations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class view_process_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentProcess
    resource_management_list_page_breadcrumb_text = 'Register & Manage Processes'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class view_data_collection_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentDataCollection
    resource_management_list_page_breadcrumb_text = 'Register & Manage Data Collections'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)

class view_catalogue_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentCatalogue
    resource_management_list_page_breadcrumb_text = 'Register & Manage Catalogues'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().dispatch(request, *args, **kwargs)

class view_catalogue_entry_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentCatalogueEntry
    resource_management_list_page_breadcrumb_text = 'Register & Manage Catalogue Entries'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().dispatch(request, *args, **kwargs)

class view_catalogue_data_subset_as_xml(ResourceXmlDownloadView):
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_management_list_page_breadcrumb_text = 'Register & Manage Catalogue Data Subsets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        return super().dispatch(request, *args, **kwargs)