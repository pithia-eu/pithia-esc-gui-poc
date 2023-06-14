from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from common.models import (
    DataCollection,
    APIInteractionMethod
)

# Create your views here.

def interact_with_data_collection_through_api(request, data_collection_id):
    try:
        data_collection = DataCollection.objects.get(pk=data_collection_id)
    except DataCollection.DoesNotExist:
        messages.error(request, 'A data collection matching the specified ID was not found.')
        return HttpResponseRedirect(reverse('browse:list_data_collections'))

    try:
        api_interaction_method = APIInteractionMethod.objects.get(data_collection=data_collection)
    except APIInteractionMethod.DoesNotExist:
        messages.error(request, 'No API interaction method was found for this data collection.')
        return HttpResponseRedirect(reverse('browse:data_collection_detail', kwargs={ 'data_collection_id': data_collection_id }))

    return render(request, 'present/index.html', {
        'title': f'Interact with {data_collection["name"]}',
        'data_collection': data_collection,
        'api_specification_url': api_interaction_method.specification_url,
    })