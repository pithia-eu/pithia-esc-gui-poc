import re
from django.core.exceptions import ObjectDoesNotExist
from operator import itemgetter
from typing import (
    Tuple,
    Union,
)

from common.constants import (
    PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
    SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE,
)
from common.models import (
    Instrument,
    ScientificMetadata,
)
from ontology.utils import (
    get_graph_of_pithia_ontology_component,
    get_pref_label_from_ontology_node_iri,
)
from utils.url_helpers import (
    create_ontology_term_detail_url_from_ontology_term_server_url,
    divide_resource_url_from_op_mode_id,
    divide_resource_url_into_main_components,
    is_operational_mode_url,
)
from validation.url_validation_services import MetadataFileOntologyURLReferencesValidator


# Server URL mapping
def map_ontology_server_urls_to_browse_urls(ontology_server_urls: list) -> list:
    """
    Maps ontology server URLs to e-Science Centre ontology browse page URLs
    based on the ontology term that each ontology server URL is for.
    """
    converted_ontology_server_urls = []
    ontology_term_category_graphs = {}

    invalid_ontology_server_urls = MetadataFileOntologyURLReferencesValidator._is_each_ontology_url_valid(ontology_server_urls)
    for url in invalid_ontology_server_urls:
        converted_ontology_server_urls.append({
            'original_server_url': url,
            'converted_url': url,
            'converted_url_text': url,
        })
    
    valid_ontology_server_urls = [url for url in ontology_server_urls if url not in invalid_ontology_server_urls]
    for ontology_server_url in valid_ontology_server_urls:
        ontology_term_detail_url = create_ontology_term_detail_url_from_ontology_term_server_url(ontology_server_url)
        ontology_term_id = ontology_server_url.split('/')[-1]
        ontology_term_category = ontology_server_url.split('/')[-2]
        # If the graph for the ontology term has already been fetched,
        # get the stored version of it to improve page loading times
        graph_for_ontology_term = None
        if ontology_term_category in ontology_term_category_graphs:
            graph_for_ontology_term = ontology_term_category_graphs[ontology_term_category]
        else:
            graph_for_ontology_term = get_graph_of_pithia_ontology_component(ontology_term_category)
            ontology_term_category_graphs[ontology_term_category] = graph_for_ontology_term
        ontology_term_pref_label = get_pref_label_from_ontology_node_iri(ontology_server_url, g=graph_for_ontology_term)
        if ontology_term_pref_label is None:
            ontology_term_pref_label = ontology_term_id
        converted_ontology_server_urls.append({
            'original_server_url': ontology_server_url,
            'converted_url': ontology_term_detail_url,
            'converted_url_text': ontology_term_pref_label,
        })
    return converted_ontology_server_urls

# Credit: https://stackoverflow.com/a/4578605
def _sort_resource_server_urls_from_operational_mode_urls(pred, resource_server_urls: list) -> Union[list, list]:
    operational_mode_urls = []
    non_operational_mode_urls = []
    for url in resource_server_urls:
        if pred(url):
            operational_mode_urls.append(url)
        else:
            non_operational_mode_urls.append(url)
    return operational_mode_urls, non_operational_mode_urls


def map_metadata_server_urls_to_browse_urls(resource_server_urls: list) -> list:
    """
    Maps metadata server URLs to e-Science Centre browse page URLs
    based on the metadata term that each metadata server URL is for.
    """
    mapped_resource_server_urls = []
    operational_mode_urls, non_operational_mode_urls = _sort_resource_server_urls_from_operational_mode_urls(
        lambda url: is_operational_mode_url(url),
        resource_server_urls
    )

    for url in operational_mode_urls:
        url_without_op_mode_id, operational_mode_id = itemgetter('resource_url', 'op_mode_id')(divide_resource_url_from_op_mode_id(url))
        url_mapping = {
            'original_server_url': url,
            'converted_url': url,
            # Use the localID in the resource URL as a default in
            # case a corresponding registration cannot be found.
            'converted_url_text': url_without_op_mode_id.split('/')[-1],
        }
        instrument = None

        try:
            instrument = Instrument.objects.get_by_operational_mode_url(url)
        except (AttributeError, Instrument.DoesNotExist):
            mapped_resource_server_urls.append(url_mapping)
            continue
        operational_mode_name = operational_mode_id
        try:
            operational_mode_name = instrument.get_operational_mode_by_id(operational_mode_id).get('name')
        except AttributeError:
            pass
        url_mapping['converted_url'] = f'{instrument.get_absolute_url()}#{operational_mode_id}'
        url_mapping['converted_url_text'] = f'{instrument.name}#{operational_mode_name}'
        mapped_resource_server_urls.append(url_mapping)

    for url in non_operational_mode_urls:
        url_mapping = {
            'original_server_url': url,
            'converted_url': url,
            # Use the localID in the resource URL as a default in
            # case a corresponding registration cannot be found.
            'converted_url_text': url.split('/')[-1],
        }

        referenced_resource = None
        scientific_metadata_subclasses = ScientificMetadata.__subclasses__()
        type_in_metadata_server_url, localid = itemgetter('resource_type', 'localid')(divide_resource_url_into_main_components(url))
        model = None
        for subclass in scientific_metadata_subclasses:
            if (subclass.type_in_metadata_server_url == type_in_metadata_server_url
                and localid.startswith(subclass.localid_base)):
                model = subclass
        
        try:
            referenced_resource = model.objects.get_by_metadata_server_url(url)
        except (AttributeError, ObjectDoesNotExist):
            mapped_resource_server_urls.append(url_mapping)
            continue
        url_mapping['converted_url'] = referenced_resource.get_absolute_url()
        url_mapping['converted_url_text'] = referenced_resource.name
        mapped_resource_server_urls.append(url_mapping)
    return mapped_resource_server_urls


def get_server_urls_from_scientific_metadata_flattened(scientific_metadata_flattened: dict) -> Tuple[list, list]:
    """
    Finds server URLs (ontology, metadata) in a scientific metadata dict
    that has been flattened.
    """
    ontology_server_urls = set()
    resource_server_urls = set()
    for key, value in scientific_metadata_flattened.items():
        if key.endswith('@xlink:href') and value.startswith(SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE):
            ontology_server_urls.add(value)
        if key.endswith('@xlink:href') and value.startswith(PITHIA_METADATA_SERVER_HTTPS_URL_BASE):
            resource_server_urls.add(value)

    return list(ontology_server_urls), list(resource_server_urls)