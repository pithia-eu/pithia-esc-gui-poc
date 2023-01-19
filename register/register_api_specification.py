from common.mongodb_models import CurrentDataCollectionInteractionMethod

def register_api_specification(api_specification_url, data_collection_localid, api_description='', session=None):
    return CurrentDataCollectionInteractionMethod.insert_one({
        'interaction_method': 'api',
        'interaction_url': api_specification_url,
        'interaction_method_description': api_description, 
        'data_collection_localid': data_collection_localid
    }, session=session)