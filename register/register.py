from bson import ObjectId
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from common.mongodb_models import OriginalMetadataXml
from validation.metadata_validation import validate_xml_file_is_unregistered


def register_metadata_xml_file(xml_file, mongodb_model, xml_conversion_check_and_fix, session=None):
    converted_metadata_file_dictionary = convert_xml_metadata_file_to_dictionary(xml_file)
    # Remove the top-level tag - this will be just <Organisation>, for example
    converted_metadata_file_dictionary = converted_metadata_file_dictionary[(list(converted_metadata_file_dictionary)[0])]
    validate_xml_file_is_unregistered(mongodb_model, xml_file)
    if xml_conversion_check_and_fix:
        xml_conversion_check_and_fix(converted_metadata_file_dictionary)
    mongodb_model.insert_one(converted_metadata_file_dictionary, session=session)
    return converted_metadata_file_dictionary

def store_xml_file_as_string_and_map_to_resource_id(xml_file, resource_id, session=None):
    xml_file.seek(0)
    xml_file_string = xml_file.read()
    if isinstance(xml_file_string, bytes):
        xml_file_string = xml_file_string.decode()
    original_metadata_xml = {
        'resourceId': ObjectId(resource_id),
        'value': xml_file_string
    }
    OriginalMetadataXml.insert_one(original_metadata_xml, session=session)

def update_original_metadata_xml_string(updated_xml_string, resource_id, session=None):
    return OriginalMetadataXml.update_one(
        {
            'resourceId': ObjectId(resource_id),
        },
        {
            '$set': {
                'value': updated_xml_string
            }
        },
        session=session
    )