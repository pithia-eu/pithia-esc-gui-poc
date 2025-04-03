import logging
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import urlize
from operator import itemgetter
from typing import Union

from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE
from common.models import (
    Instrument,
    ScientificMetadata,
)
from ontology.services import (
    get_graph_of_pithia_ontology_component,
    get_skos_properties_from_ontology_node,
    get_pref_label_from_ontology_node_iri,
)
from utils.url_helpers import (
    create_ontology_term_detail_url_from_ontology_term_server_url,
    divide_resource_url_from_op_mode_id,
    divide_resource_url_into_main_components,
    is_operational_mode_url,
)


logger = logging.getLogger(__name__)


# Server URL mapping
def get_properties_for_ontology_server_urls(ontology_server_urls: list, skos_properties: list = ['prefLabel']) -> list:
    """Gets the ontology properties and corresponding ontology browser URL
    for each ontology server URL passed in a given list.
    """
    properties_by_ontology_url = {}
    for url in ontology_server_urls:
        if url in properties_by_ontology_url:
            continue
        corresponding_ontology_browser_url = None
        try:
            corresponding_ontology_browser_url = create_ontology_term_detail_url_from_ontology_term_server_url(url)
        except Exception as err:
            logger.exception(err)
        
        # SKOS properties
        corresponding_properties = {}
        try:
            category_from_url = url.split('/')[-2]
            ontology_graphs_by_category = {}
            if category_from_url not in ontology_graphs_by_category:
                ontology_graphs_by_category[category_from_url] = get_graph_of_pithia_ontology_component(category_from_url)
            corresponding_graph = ontology_graphs_by_category[category_from_url]
            corresponding_properties = get_skos_properties_from_ontology_node(
                url,
                skos_properties,
                corresponding_graph
            )
            for key, value in corresponding_properties.items():
                corresponding_properties.update({key: urlize(value)})
        except Exception as err:
            logger.exception(err)

        properties_by_ontology_url[url] = {
            'ontology_browser_url': corresponding_ontology_browser_url,
            'skos_properties': corresponding_properties
        }
    return properties_by_ontology_url

def map_ontology_server_urls_to_browse_urls(ontology_server_urls: list) -> list:
    """Maps ontology server URLs to e-Science Centre ontology browse page URLs
    based on the ontology term that each ontology server URL is for.
    """
    converted_ontology_server_urls = []
    ontology_term_category_graphs = {}

    for ontology_server_url in ontology_server_urls:
        converted_url = ontology_server_url
        converted_url_text = ontology_server_url
        if SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE not in ontology_server_url:
            converted_ontology_server_urls.append({
                'original_server_url': ontology_server_url,
                'converted_url': converted_url,
                'converted_url_text': 'Unknown',
            })
            continue
        try:
            ontology_term_id = ontology_server_url.split('/')[-1]
            converted_url_text = ontology_term_id
            ontology_term_category = ontology_server_url.split('/')[-2]
            converted_url = create_ontology_term_detail_url_from_ontology_term_server_url(ontology_server_url)
            # If the graph for the ontology term has already been fetched,
            # get the stored version of it to improve page loading times
            graph_for_ontology_term = None
            if ontology_term_category in ontology_term_category_graphs:
                graph_for_ontology_term = ontology_term_category_graphs[ontology_term_category]
            else:
                graph_for_ontology_term = get_graph_of_pithia_ontology_component(ontology_term_category)
                ontology_term_category_graphs[ontology_term_category] = graph_for_ontology_term
            pref_label = get_pref_label_from_ontology_node_iri(ontology_server_url, g=graph_for_ontology_term)
            if pref_label:
                converted_url_text = pref_label
        except Exception as err:
            logger.exception(err)
        converted_ontology_server_urls.append({
            'original_server_url': ontology_server_url,
            'converted_url': converted_url,
            'converted_url_text': converted_url_text,
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
    """Maps metadata server URLs to e-Science Centre browse page URLs
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
        url_mapping['converted_url'] = f'{instrument.get_absolute_url()}?operational_mode_id={operational_mode_id}#{operational_mode_id}'
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
            if (not subclass.type_in_metadata_server_url == type_in_metadata_server_url
                or not localid.startswith(subclass.localid_base)):
                continue
            model = subclass
        
        try:
            referenced_resource = model.objects.get_by_metadata_server_url(url)
        except (AttributeError, ObjectDoesNotExist):
            logger.exception(f'Could not find detail page URL mapping for metadata server URL: {url}')
            mapped_resource_server_urls.append(url_mapping)
            continue
        url_mapping['converted_url'] = referenced_resource.get_absolute_url()
        url_mapping['converted_url_text'] = referenced_resource.name
        mapped_resource_server_urls.append(url_mapping)
    return mapped_resource_server_urls