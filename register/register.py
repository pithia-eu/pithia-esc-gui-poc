from bson import ObjectId
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from common.mongodb_models import OriginalMetadataXml
from validation.registration_validation import validate_xml_file_is_unique


def move_current_version_of_resource_to_revisions(resource_pithia_identifier, current_resource_mongodb_model, resource_revision_mongodb_model, session=None):
    current_version_of_resource = current_resource_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.localID': resource_pithia_identifier['localID'],
        'identifier.PITHIA_Identifier.namespace': resource_pithia_identifier['namespace'],
    }, session=session)
    if not current_version_of_resource:
        print('Resource not found.')
        return 'Resource not found.'
    # It's "moving" the resource, so first copy the resource to the revisions
    # collection, and then delete from the current version collection.
    current_resource_mongodb_model.delete_one({
        '_id': ObjectId(current_version_of_resource['_id'])
    }, session=session)
    resource_revision_mongodb_model.insert_one(current_version_of_resource, session=session)

def register_metadata_xml_file(xml_file, mongodb_model, xml_conversion_check_and_fix, session=None):
    metadata_file_dict = convert_xml_metadata_file_to_dictionary(xml_file)
    # Remove the top-level tag - this will be just <Organisation>, for example
    metadata_file_dict = metadata_file_dict[(list(metadata_file_dict)[0])]
    if not validate_xml_file_is_unique(mongodb_model, converted_xml_file=metadata_file_dict):
        return 'This XML metadata file has been registered before.'
    if xml_conversion_check_and_fix:
        xml_conversion_check_and_fix(metadata_file_dict)
    metadata_registration_result = mongodb_model.insert_one(metadata_file_dict, session=session)
    xml_file.seek(0)
    xml_file_string = xml_file.read()
    if isinstance(xml_file_string, bytes):
        xml_file_string = xml_file_string.decode()
    original_metadata_xml = {
        'resourceId': metadata_registration_result.inserted_id,
        'value': xml_file_string
    }
    OriginalMetadataXml.insert_one(original_metadata_xml, session=session)
    return metadata_registration_result