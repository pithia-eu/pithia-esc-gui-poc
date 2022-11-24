from .url_helpers import convert_ontology_server_urls_to_browse_urls, convert_resource_server_urls_to_browse_urls
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.http import HttpResponseNotFound
from bson import ObjectId
from common.mongodb_models import OriginalMetadataXml, CurrentOrganisation, CurrentIndividual, CurrentProject, CurrentPlatform, CurrentOperation, CurrentInstrument, CurrentAcquisitionCapability, CurrentAcquisition, CurrentComputationCapability, CurrentComputation, CurrentProcess, CurrentDataCollection

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
    resource_mongodb_model = None
    resource_name = ''
    resource_localid = ''
    template_name = 'utils/resource_as_xml.html'
    xml = ''

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
        return context

class view_organisation_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentOrganisation

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)

class view_individual_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentIndividual

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class view_project_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentProject

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class view_platform_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentPlatform

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class view_operation_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentOperation

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class view_instrument_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentInstrument

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class view_acquisition_capability_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentAcquisitionCapability

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_id']
        return super().dispatch(request, *args, **kwargs)

class view_acquisition_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentAcquisition

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class view_computation_capability_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentComputationCapability

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_id']
        return super().dispatch(request, *args, **kwargs)

class view_computation_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentComputation

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class view_process_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentProcess

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class view_data_collection_as_xml(ViewResourceAsXmlView):
    resource_mongodb_model = CurrentDataCollection

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)