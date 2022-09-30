from common.mongodb_models import CurrentDataCollectionInteractionMethod

def register_api_specification(api_specification_url, data_collection_id):
    return CurrentDataCollectionInteractionMethod.insert_one({
        'interaction_method': 'api',
        'api_specification_url': api_specification_url,
        'data_collection_id': data_collection_id
    })