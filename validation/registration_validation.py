from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary


def validate_xml_file_is_unique(mongodb_model, xml_file=None, converted_xml_file=None):
    if converted_xml_file is None:
        converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
        # Remove the top-level tag - this will be just <Organisation>, for example
        converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
    xml_file_pithia_identifier = converted_xml_file['identifier']['PITHIA_Identifier']
    num_times_uploaded_before = mongodb_model.count_documents({
        'identifier.PITHIA_Identifier.localID': xml_file_pithia_identifier['localID'],
        'identifier.PITHIA_Identifier.namespace': xml_file_pithia_identifier['namespace'],
    })
    return num_times_uploaded_before == 0