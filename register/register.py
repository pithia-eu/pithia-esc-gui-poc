# TODO: Replace ESPAS_Identifier with pithia:Identifier
from bson import ObjectId
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from register.mongodb_models import OriginalMetadataXml


def move_current_version_of_resource_to_revisions(resource_pithia_identifier, current_resource_mongodb_model, resource_revision_mongodb_model):
    current_version_of_resource = current_resource_mongodb_model.find_one({
        'identifier.pithia:Identifier.localID': resource_pithia_identifier['localID'],
        'identifier.pithia:Identifier.namespace': resource_pithia_identifier['namespace'],
    })
    if not current_version_of_resource:
        print('Resource not found.')
        return 'Resource not found.'
    # It's "moving" the resource, so first copy the resource to the revisions
    # collection, and then delete from the current version collection.
    current_resource_mongodb_model.delete_one({
        '_id': ObjectId(current_version_of_resource['_id'])
    })
    resource_revision_mongodb_model.insert_one(current_version_of_resource)

def register_metadata_xml_file(xml_file, mongodb_model, xml_conversion_check_and_fix):
    metadata_file_dict = convert_xml_metadata_file_to_dictionary(xml_file)
    # Remove the top-level tag - this will be just <Organisation>, for example
    metadata_file_dict = metadata_file_dict[(list(metadata_file_dict)[0])]
    # The XML-to-Python dictionary conversion may not convert correctly
    # according to the blue PowerPoint diagram, so checks and fixes should be
    # applied.
    if xml_conversion_check_and_fix:
        xml_conversion_check_and_fix(metadata_file_dict)
    metadata_registration_result = mongodb_model.insert_one(metadata_file_dict)
    xml_file.seek(0)
    original_metadata_xml = {
        'resourceId': metadata_registration_result.inserted_id,
        'value': xml_file.read().decode()
    }
    OriginalMetadataXml.insert_one(original_metadata_xml)