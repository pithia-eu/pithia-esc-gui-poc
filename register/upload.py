# TODO: Replace ESPAS_Identifier with pithia:Identifier
def find_and_copy_current_version_of_resource_to_revisions_collection(resource_pithia_identifier, current_resource_mongodb_model, resource_revision_mongodb_model):
    current_version_of_resource = current_resource_mongodb_model.find_one({
        'identifier.ESPAS_Identifier.localID': resource_pithia_identifier['localID'],
        'identifier.ESPAS_Identifier.namespace': resource_pithia_identifier['namespace'],
    })
    if not current_version_of_resource:
        return
    return resource_revision_mongodb_model.insert_one(current_version_of_resource)

def replace_current_version_of_resource_with_newer_version(newer_resource_version, current_resource_mongodb_model):
    # The resource version is expected to be added
    # by data owners, but if not, may need to add
    # it here.
    current_resource_mongodb_model.delete_many({})
    return current_resource_mongodb_model.insert_one(newer_resource_version)