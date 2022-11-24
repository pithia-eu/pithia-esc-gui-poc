from bson import ObjectId
from common.mongodb_models import OriginalMetadataXml, CurrentDataCollectionInteractionMethod, DataCollectionInteractionMethodRevision


def create_revision_of_current_resource_version(resource_pithia_identifier, current_resource_mongodb_model, resource_revision_mongodb_model):
    current_version_of_resource = current_resource_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.localID': resource_pithia_identifier['localID'],
        'identifier.PITHIA_Identifier.namespace': resource_pithia_identifier['namespace'],
    })
    if not current_version_of_resource:
        print('Resource not found.')
        return 'Resource not found.'
    current_version_of_resource.pop('_id', None)
    resource_revision_mongodb_model.insert_one(current_version_of_resource)
    return current_version_of_resource

def assign_original_xml_file_entry_to_revision_id(old_resource_id, revision_id):
    current_orginal_xml_file = OriginalMetadataXml.find_one({
        'resourceId': ObjectId(str(old_resource_id))
    })
    if current_orginal_xml_file is None:
        print('The original XML metadata string for this resource was not found.')
        return 'The original XML metadata string for this resource was not found.'
    return OriginalMetadataXml.update_one({
        'resourceId': ObjectId(str(old_resource_id))
    }, { '$set': {
        'resourceId': ObjectId(str(revision_id))
    }})

def create_revision_of_data_collection_api_interaction_method(data_collection_localid):
    current_version_of_api_interaction_method = CurrentDataCollectionInteractionMethod.find_one({
        'data_collection_localid': data_collection_localid,
        'interaction_method': 'api',
    })
    if current_version_of_api_interaction_method == None:
        print('No API interaction method for this data collection was found.')
        return 'No API interaction method for this data collection was found.'
    current_version_of_api_interaction_method.pop('_id', None)
    DataCollectionInteractionMethodRevision.insert_one(current_version_of_api_interaction_method)
    return current_version_of_api_interaction_method