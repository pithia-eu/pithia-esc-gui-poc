# TODO: Replace ESPAS_Identifier with pithia:Identifier
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary


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

def register_metadata_xml_file(xml_file, mongodb_model, xml_conversion_check_and_fix):
    xml_file.seek(0)
    metadata_file_dict = convert_xml_metadata_file_to_dictionary(xml_file)
    # Remove the top-level tag
    metadata_file_dict = metadata_file_dict[(list(metadata_file_dict)[0])]
    if xml_conversion_check_and_fix:
        xml_conversion_check_and_fix(metadata_file_dict)
    xml_file.seek(0)
    metadata_file_dict['original_xml_as_string'] = xml_file.read().decode()
    
    return mongodb_model.insert_one(metadata_file_dict)