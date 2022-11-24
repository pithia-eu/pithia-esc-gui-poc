from .url_helpers import convert_ontology_server_urls_to_browse_urls, convert_resource_server_urls_to_browse_urls
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http import HttpResponseNotFound
from bson import ObjectId
from common.mongodb_models import OriginalMetadataXml

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

class ViewResourceAsXmlView(TemplateView):
    resource_id = ''
    template_name = 'utils/resource_as_xml.html'
    xml = ''

    def get(self, request, *args, **kwargs):
        original_metadata_xml = OriginalMetadataXml.find_one({
            'resourceId': ObjectId(self.resource_id)
        })
        if original_metadata_xml is None:
            return HttpResponseNotFound('The XML for this resource was not found.')
        self.xml = original_metadata_xml['value']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['xml'] = self.xml
        return context

class view_organisation_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)

class view_individual_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class view_project_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class view_platform_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class view_operation_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class view_instrument_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class view_acquisition_capability_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_id']
        return super().dispatch(request, *args, **kwargs)

class view_acquisition_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class view_computation_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class view_computation_capability_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_id']
        return super().dispatch(request, *args, **kwargs)

class view_process_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class view_data_collection_as_xml(ViewResourceAsXmlView):
    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)