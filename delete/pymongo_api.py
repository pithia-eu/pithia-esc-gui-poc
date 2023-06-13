from .utils import (
    get_data_collection_related_resources_linked_through_resource_id,
    delete_current_version_and_revisions_and_xmls_of_resource_id,
    delete_current_versions_and_revisions_of_data_collection_interaction_methods,
    get_catalogue_related_resources_linked_through_resource_id,
)

from common.mongodb_models import CurrentDataCollection
from mongodb import client

def delete_data_collection_related_resource(resource_localid, resource_mongodb_model, resource_revision_mongodb_model, resource_type_in_resource_url):
    resource_to_delete = resource_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.localID': resource_localid
    })
    resource_id = str(resource_to_delete['_id'])
    with client.start_session() as s:
        def cb(s):
            # Delete the resource and resources that are referencing the resource to be deleted. These should not
            # be able to exist without the resource being deleted.
            linked_resources = get_data_collection_related_resources_linked_through_resource_id(resource_id, resource_type_in_resource_url, resource_mongodb_model)
            if resource_mongodb_model == CurrentDataCollection:
                catalogue_related_resources = get_catalogue_related_resources_linked_through_resource_id(resource_id, resource_mongodb_model)
                linked_resources.extend(catalogue_related_resources)
            delete_current_version_and_revisions_and_xmls_of_resource_id(resource_id, resource_mongodb_model, resource_revision_mongodb_model, session=s)
            for r in linked_resources:
                delete_current_version_and_revisions_and_xmls_of_resource_id(r[0]['_id'], r[2], r[3], session=s)
            if resource_mongodb_model == CurrentDataCollection:
                delete_current_versions_and_revisions_of_data_collection_interaction_methods(resource_id, session=s)
        s.with_transaction(cb)

def delete_catalogue_related_resource(resource_localid, resource_mongodb_model, resource_revision_mongodb_model):
    resource_to_delete = resource_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.localID': resource_localid
    })
    resource_id = str(resource_to_delete['_id'])
    with client.start_session() as s:
        def cb(s):
            # Delete the resource and resources that are referencing the resource to be deleted. These should not
            # be able to exist without the resource being deleted.
            linked_resources = get_catalogue_related_resources_linked_through_resource_id(resource_id, resource_mongodb_model)
            delete_current_version_and_revisions_and_xmls_of_resource_id(resource_id, resource_mongodb_model, resource_revision_mongodb_model, session=s)
            for r in linked_resources:
                delete_current_version_and_revisions_and_xmls_of_resource_id(r[0]['_id'], r[2], r[3], session=s)
        s.with_transaction(cb)