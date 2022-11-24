from bson import ObjectId
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from common.mongodb_models import OriginalMetadataXml
from validation.registration_validation import validate_xml_file_is_unique


def register_metadata_xml_file(xml_file, mongodb_model, xml_conversion_check_and_fix):
    converted_metadata_file_dictionary = convert_xml_metadata_file_to_dictionary(xml_file)
    # Remove the top-level tag - this will be just <Organisation>, for example
    converted_metadata_file_dictionary = converted_metadata_file_dictionary[(list(converted_metadata_file_dictionary)[0])]
    if not validate_xml_file_is_unique(mongodb_model, converted_xml_file=converted_metadata_file_dictionary):
        return 'This XML metadata file has been registered before.'
    if xml_conversion_check_and_fix:
        xml_conversion_check_and_fix(converted_metadata_file_dictionary)
    metadata_registration_result = mongodb_model.insert_one(converted_metadata_file_dictionary)
    xml_file.seek(0)
    xml_file_string = xml_file.read()
    if isinstance(xml_file_string, bytes):
        xml_file_string = xml_file_string.decode()
    original_metadata_xml = {
        'resourceId': metadata_registration_result.inserted_id,
        'value': xml_file_string
    }
    OriginalMetadataXml.insert_one(original_metadata_xml)
    return converted_metadata_file_dictionary