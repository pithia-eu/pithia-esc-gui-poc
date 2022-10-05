from bson import ObjectId

from common.mongodb_models import CurrentDataCollectionInteractionMethod

def _map_id_property(resource):
    return resource['_id']

def get_revision_ids_for_resource_id(resource_id, resource_mongodb_model, resource_revision_mongodb_model):
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    }, projection={ 'identifier': 1 })
    return list(map(_map_id_property, list(resource_revision_mongodb_model.find({
        'identifier.PITHIA_Identifier.localID': resource['identifier']['PITHIA_Identifier']['localID'],
        'identifier.PITHIA_Identifier.namespace': resource['identifier']['PITHIA_Identifier']['namespace'],
    }, projection={ '_id': 1 }))))

def get_interaction_methods_linked_to_data_collection_id(data_collection_id):
    linked_interaction_methods = []
    linked_interaction_methods.extend(list(CurrentDataCollectionInteractionMethod.find({
        'data_collection_id': ObjectId(data_collection_id)
    })))
    return linked_interaction_methods