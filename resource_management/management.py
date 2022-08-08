from bson.objectid import ObjectId

from register.register import register_metadata_xml_file

def replace_resource_with_newer_version(current_resource_id, new_resource_file, resource_mongodb_model, xml_conversion_check_and_fix):
    resource_mongodb_model.delete_one({
        '_id': ObjectId(current_resource_id)
    })
    return register_metadata_xml_file(new_resource_file, resource_mongodb_model, xml_conversion_check_and_fix)

def delete_resource(resource_id, resource_mongodb_model):
    return resource_mongodb_model.delete_one({
        '_id': ObjectId(resource_id)
    })