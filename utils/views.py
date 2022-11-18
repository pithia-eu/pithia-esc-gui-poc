from django.shortcuts import render
from .url_helpers import convert_ontology_server_urls_to_browse_urls, convert_resource_server_urls_to_browse_urls
from django.http import JsonResponse

# Create your views here.

def get_esc_url_templates_for_ontology_server_urls_and_resource_server_urls(request):
    ontology_server_urls = request.GET['ontology_server_urls']
    resource_server_urls = request.GET['resource_server_urls']
    esc_ontology_urls = convert_ontology_server_urls_to_browse_urls(ontology_server_urls)
    esc_resource_urls = convert_resource_server_urls_to_browse_urls(resource_server_urls)
    
    return JsonResponse({
        'ontology_urls': esc_ontology_urls,
        'resource_urls': esc_resource_urls,
    })