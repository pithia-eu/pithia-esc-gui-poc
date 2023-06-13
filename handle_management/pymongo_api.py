
from bson import ObjectId
from operator import itemgetter
from pymongo import collection

from .xml_utils import (
    get_doi_xml_string_from_metadata_xml_string,
)

from common.helpers import get_mongodb_model_by_resource_type_from_resource_url
from common.mongodb_models import (
    CurrentCatalogueDataSubset,
    CurrentDataCollection,
    CurrentIndividual,
    CurrentOrganisation,
    HandleUrlMapping,
    OriginalMetadataXml,
)
from utils.url_helpers import (
    divide_resource_url_into_main_components,
    get_namespace_and_localid_from_resource_url,
)

# From xml_utils.py
def get_first_related_party_name_from_data_collection_old(data_collection: dict):
    if not isinstance(data_collection, dict) or (isinstance(data_collection, dict) and 'relatedParty' not in data_collection):
        return None
    related_party_url = data_collection['relatedParty'][0]['ResponsiblePartyInfo']['party']['@xlink:href']
    resource_type_in_resource_url, namespace, localid = itemgetter('resource_type', 'namespace', 'localid')(divide_resource_url_into_main_components(related_party_url))
    related_party_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type_in_resource_url)
    related_party = related_party_mongodb_model.find_one({
        'identifier.PITHIA_Identifier.namespace': namespace,
        'identifier.PITHIA_Identifier.localID': localid,
    })
    if related_party is None:
        return None
    if related_party_mongodb_model == CurrentIndividual:
        organisation_url = related_party['organisation']['@xlink:href']
        organisation_namespace, organisation_localid = itemgetter('namespace', 'localid')(divide_resource_url_into_main_components(organisation_url))
        organisation = CurrentOrganisation.find_one({
            'identifier.PITHIA_Identifier.namespace': organisation_namespace,
            'identifier.PITHIA_Identifier.localID': organisation_localid,
        })
        if organisation is not None:
            related_party = organisation
    return related_party['name']

def add_data_subset_data_to_doi_metadata_kernel_dict_old(
    data_subset_id: str,
    doi_dict: dict,
    data_collection_model: collection = CurrentDataCollection,
    catalogue_data_subset_model: collection = CurrentCatalogueDataSubset
):
    data_subset = catalogue_data_subset_model.find_one({
        '_id': ObjectId(data_subset_id)
    })
    if data_subset is None:
        return doi_dict
    if 'dataCollection' not in data_subset:
        return doi_dict
    referenced_data_collection_url = data_subset['dataCollection']['@xlink:href']
    namespace, localid = get_namespace_and_localid_from_resource_url(referenced_data_collection_url)
    referenced_data_collection = data_collection_model.find_one({
        'identifier.PITHIA_Identifier.namespace': namespace,
        'identifier.PITHIA_Identifier.localID': localid,
    })
    if referenced_data_collection is None:
        return doi_dict
    referenced_data_collection_name = referenced_data_collection['name']
    doi_dict['referentCreation']['name']['value'] = referenced_data_collection_name
    principal_agent_name_value = get_first_related_party_name_from_data_collection_old(referenced_data_collection)
    if principal_agent_name_value is not None:
        doi_dict['referentCreation']['principalAgent']['name']['value'] = principal_agent_name_value
    return doi_dict

def get_doi_xml_string_for_resource_id(resource_id):
    original_metadata_xml = OriginalMetadataXml.find_one({
        'resourceId': ObjectId(resource_id),
    }, { 'value': 1 })
    xml_string = original_metadata_xml['value']
    return get_doi_xml_string_from_metadata_xml_string(xml_string)

# From utils.py
def add_handle_to_url_mapping_old(handle: str, url: str, session=None):
    HandleUrlMapping.insert_one({
        'handle_name': handle,
        'url': url,
    }, session=session)