def validate_xml_file_is_unique(converted_xml_file, mongodb_model):
    xml_file_pithia_identifier = converted_xml_file['identifier']['PITHIA_Identifier']
    num_times_uploaded_before = mongodb_model.count_documents({
        'identifier.PITHIA_Identifier.localID': xml_file_pithia_identifier['localID'],
        'identifier.PITHIA_Identifier.namespace': xml_file_pithia_identifier['namespace'],
    })
    return num_times_uploaded_before == 0