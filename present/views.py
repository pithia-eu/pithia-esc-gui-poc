from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from bson import ObjectId

from common.mongodb_models import CurrentDataCollection, CurrentDataCollectionInteractionMethod

# Create your views here.

def interact_with_data_collection_through_api(request, data_collection_id):
    data_collection = CurrentDataCollection.find_one({
        '_id': ObjectId(data_collection_id)
    })
    if data_collection == None:
        messages.error(request, 'A data collection matching the specified ID was not found.')
        return HttpResponseRedirect(reverse('browse:list_data_collections'))
    print(data_collection['identifier']['PITHIA_Identifier']['localID'])
    api_interaction_method = CurrentDataCollectionInteractionMethod.find_one({
        'interaction_method': 'api',
        'data_collection_localid': data_collection['identifier']['PITHIA_Identifier']['localID']
    })
    if api_interaction_method == None:
        messages.error(request, 'No API interaction method was found for this data collection.')
        return HttpResponseRedirect(reverse('browse:data_collection_detail', kwargs={ 'data_collection_id': data_collection_id }))

    return render(request, 'present/index.html', {
        'title': f'Interact with {data_collection["name"]}',
        'data_collection': data_collection,
        'api_specification_url': api_interaction_method['interaction_url'],
    })