from bson import ObjectId
from common.mongodb_models import OriginalMetadataXml


def copy_current_version_of_resource_to_revisions(resource_pithia_identifier, current_resource_mongodb_model, resource_revision_mongodb_model):
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

def assign_original_xml_file_entry_to_new_resource_id(old_resource_id, new_resource_id):
    current_orginal_xml_file = OriginalMetadataXml.find_one({
        'resourceId': ObjectId(str(old_resource_id))
    })
    if current_orginal_xml_file is None:
        print('The original XML metadata string for this resource was not found.')
        return 'The original XML metadata string for this resource was not found.'
    return OriginalMetadataXml.update_one({
        'resourceId': ObjectId(str(old_resource_id))
    }, { '$set': {
        'resourceId': ObjectId(str(new_resource_id))
    }})