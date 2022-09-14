from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from bson.objectid import ObjectId


def validate_xml_file_localid_matches_existing_resource_localid(mongodb_model, resource_id, xml_file=None, converted_xml_file=None):
    if converted_xml_file is None:
        converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
        # Remove the top-level tag - this will be just <Organisation>, for example
        converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
    xml_file_pithia_identifier = converted_xml_file['identifier']['PITHIA_Identifier']
    resource_to_update = mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_to_update_pithia_identifier = resource_to_update['identifier']['PITHIA_Identifier']
    return xml_file_pithia_identifier['localID'] == resource_to_update_pithia_identifier['localID'] and xml_file_pithia_identifier['namespace'] == resource_to_update_pithia_identifier['namespace']