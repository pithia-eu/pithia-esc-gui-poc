from bson import ObjectId
from common.mongodb_models import CurrentDataCollectionInteractionMethod


def move_current_existing_version_of_api_interaction_method_to_revisions(data_collection_localid, current_interaction_method_mongodb_model, interaction_method_revision_mongodb_model):
    current_version_of_api_interaction_method = current_interaction_method_mongodb_model.find_one({
        'data_collection_localid': data_collection_localid,
    })
    if current_version_of_api_interaction_method == None:
        return 'No API interaction method for this data collection were found.'
    # It's "moving" the interaction method, so first copy the interaction method
    # to the revisions collection, and then delete from the current version collection.
    current_interaction_method_mongodb_model.delete_one({
        '_id': ObjectId(current_version_of_api_interaction_method['_id'])
    })
    interaction_method_revision_mongodb_model.insert_one(current_version_of_api_interaction_method)

def register_api_specification(api_specification_url, data_collection_localid, api_description=''):
    return CurrentDataCollectionInteractionMethod.insert_one({
        'interaction_method': 'api',
        'interaction_url': api_specification_url,
        'interaction_method_description': api_description, 
        'data_collection_localid': data_collection_localid
    })