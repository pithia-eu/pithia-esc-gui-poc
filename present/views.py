from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from common.models import (
    APIInteractionMethod,
    DataCollection,
    Workflow,
    WorkflowAPIInteractionMethod,
)
from browse.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
)

# Create your views here.

def interact_with_data_collection_through_api(request, data_collection_id):
    try:
        data_collection = DataCollection.objects.get(pk=data_collection_id)
    except DataCollection.DoesNotExist:
        messages.error(request, 'A data collection matching the specified ID was not found.')
        return HttpResponseRedirect(reverse('browse:list_data_collections'))

    try:
        api_interaction_method = APIInteractionMethod.objects.get(scientific_metadata=data_collection)
    except APIInteractionMethod.DoesNotExist:
        messages.error(request, 'No API interaction method was found for this data collection.')
        return HttpResponseRedirect(reverse('browse:data_collection_detail', kwargs={'data_collection_id': data_collection_id}))

    return render(request, 'present/index.html', {
        'title': f'Interact with {data_collection.name} via API',
        'scientific_metadata': data_collection,
        'api_specification_url': api_interaction_method.specification_url,
        'browse_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
        'resource_type_list_page_breadcrumb_text': _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
        'resource_list_page_breadcrumb_text': DataCollection.type_plural_readable.title(),
    })

def interact_with_workflow_through_api(request, workflow_id):
    try:
        workflow = Workflow.objects.get(pk=workflow_id)
    except Workflow.DoesNotExist:
        messages.error(request, 'A workflow matching the specified ID was not found.')
        return HttpResponseRedirect(reverse('browse:list_workflows'))
    
    try:
        workflow_api_interaction_method = WorkflowAPIInteractionMethod.objects.get(scientific_metadata=workflow)
    except WorkflowAPIInteractionMethod.DoesNotExist:
        messages.error(request, 'No API interaction method was found for this workflow.')
        return HttpResponseRedirect(reverse('browse:workflow_details', kwargs={'workflow_id': workflow_id}))
    
    return render(request, 'present/index_workflow.html', {
        'title': f'Interact with {workflow.name} via API',
        'scientific_metadata': workflow,
        'api_specification_url': workflow_api_interaction_method.specification_url,
        'browse_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
        'resource_list_page_breadcrumb_text': Workflow.type_plural_readable.title(),
    })