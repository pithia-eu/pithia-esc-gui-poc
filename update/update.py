from bson import ObjectId
from common.mongodb_models import OriginalMetadataXml, CurrentDataCollectionInteractionMethod
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary


def update_current_version_of_resource(
    resource_id,
    xml_file,
    current_resource_mongodb_model,
    xml_conversion_check_and_fix,
    session=None
):
    metadata_file_dictionary = convert_xml_metadata_file_to_dictionary(xml_file)
    # Remove the top-level tag - this will be just <Organisation>, for example
    metadata_file_dictionary = metadata_file_dictionary[(list(metadata_file_dictionary)[0])]
    if xml_conversion_check_and_fix:
        xml_conversion_check_and_fix(metadata_file_dictionary)
    current_resource_mongodb_model.update_one({
        '_id': ObjectId(str(resource_id))
    }, { '$set': metadata_file_dictionary }, session=session)
    return metadata_file_dictionary

def update_data_collection_api_interaction_method_specification_url(
    data_collection_localid,
    api_specification_url,
    session=None
):
    return CurrentDataCollectionInteractionMethod.update_one(
        {
            'data_collection_localid': data_collection_localid,
            'interaction_method': 'api',
        },
        {
            '$set': {
                'interaction_url': api_specification_url
            }
        },
        session=session
    )

def update_data_collection_api_interaction_method_description(
    data_collection_localid,
    api_description,
    session=None
):
    return CurrentDataCollectionInteractionMethod.update_one(
        {
            'data_collection_localid': data_collection_localid,
            'interaction_method': 'api',
        },
        {
            '$set': {
                'interaction_method_description': api_description
            }
        },
        session=session
    )