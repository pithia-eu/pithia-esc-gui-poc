import re
from django.urls import reverse

from common.helpers import (
    get_mongodb_model_from_catalogue_related_resource_url,
    get_mongodb_model_by_resource_type_from_resource_url,
)
from ontology.utils import (
    get_graph_of_pithia_ontology_component,
    get_pref_label_from_ontology_node_iri,
)
from utils.mapping_functions import prepare_resource_for_template
from utils.string_helpers import _split_camel_case
from utils.url_helpers import (
    create_ontology_term_detail_url_from_ontology_term_server_url,
    divide_catalogue_related_resource_url_into_main_components,
    divide_resource_url_into_main_components,
    divide_resource_url_from_op_mode_id,
)
from validation.url_validation import (
    PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
    SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE,
    validate_ontology_term_url
)


# Server URL mapping
def map_ontology_server_urls_to_browse_urls(ontology_server_urls: list) -> list:
    """
    Maps ontology server URLs to e-Science Centre ontology browse page URLs
    based on the ontology term that each ontology server URL is for.
    """
    converted_ontology_server_urls = []
    ontology_term_category_graphs = {}
    for ontology_server_url in ontology_server_urls:
        is_ontology_server_url_valid = validate_ontology_term_url(ontology_server_url)
        if is_ontology_server_url_valid == False:
            converted_ontology_server_urls.append({
                'original_server_url': ontology_server_url,
                'converted_url': ontology_server_url,
                'converted_url_text': ontology_server_url,
            })
            continue
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

def map_metadata_server_urls_to_browse_urls(resource_server_urls: list) -> list:
    """
    Maps metadata server URLs to e-Science Centre browse page URLs
    based on the metadata term that each metadata server URL is for.
    """
    converted_resource_server_urls = []
    for resource_server_url in resource_server_urls:
        referenced_resource_type = ''
        referenced_resource_namespace = ''
        referenced_resource_localid = ''
        referenced_op_mode_id = ''
        referenced_resource_mongodb_model = None
        
        url_mapping = {
            'original_server_url': resource_server_url,
            'converted_url': resource_server_url,
            'converted_url_text': resource_server_url.split('/')[-1],
        }

        if '/catalogue/' in resource_server_url:
            resource_server_url_components = divide_catalogue_related_resource_url_into_main_components(resource_server_url)
            referenced_resource_type = resource_server_url_components['resource_type']
            referenced_resource_namespace = resource_server_url_components['namespace']
            referenced_resource_localid = resource_server_url_components['localid']
            referenced_resource_mongodb_model = get_mongodb_model_from_catalogue_related_resource_url(resource_server_url)
        else:
            resource_server_url_copy = resource_server_url
            if '#' in resource_server_url_copy:
                components_of_resource_server_url_with_op_mode_id = divide_resource_url_from_op_mode_id(resource_server_url_copy)
                resource_server_url_copy = components_of_resource_server_url_with_op_mode_id['resource_url']
                referenced_op_mode_id = components_of_resource_server_url_with_op_mode_id['op_mode_id']
            resource_server_url_components = divide_resource_url_into_main_components(resource_server_url_copy)
            referenced_resource_type = resource_server_url_components['resource_type']
            referenced_resource_namespace = resource_server_url_components['namespace']
            referenced_resource_localid = resource_server_url_components['localid']
            referenced_resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(referenced_resource_type)
        
        if referenced_resource_mongodb_model == 'unknown':
            converted_resource_server_urls.append(url_mapping)
            continue
        referenced_resource = None
        find_params = {
            'identifier.PITHIA_Identifier.namespace': referenced_resource_namespace,
            'identifier.PITHIA_Identifier.localID': referenced_resource_localid,
        }
        if len(referenced_op_mode_id) > 0:
            find_params['operationalMode.InstrumentOperationalMode.id'] = referenced_op_mode_id
        referenced_resource = referenced_resource_mongodb_model.find_one(find_params, {
            '_id': 1,
            'name': 1,
            'entryName': 1,
            'dataSubsetName': 1,
        })
        if referenced_resource is None:
            converted_resource_server_urls.append(url_mapping)
            continue
        referenced_resource = prepare_resource_for_template(referenced_resource)
        resource_objectid_str = str(referenced_resource['_id'])
        url_name = referenced_resource_type.lower()
        if referenced_resource_type.lower() == 'computationcapabilities':
            url_name = 'computation_capability_set'
        elif referenced_resource_type.lower() == 'acquisitioncapabilities':
            url_name = 'acquisition_capability_set'
        elif referenced_resource_type.lower() == 'collection':
            url_name = 'data_collection'
        elif referenced_resource_type.lower() == 'catalogue' and referenced_resource_localid.startswith('Catalogue_'):
            url_name = 'catalogue'
        elif referenced_resource_type.lower() == 'catalogue' and referenced_resource_localid.startswith('CatalogueEntry_'):
            url_name = 'catalogue_entry'
        elif referenced_resource_type.lower() == 'catalogue' and referenced_resource_localid.startswith('DataSubset_'):
            url_name = 'catalogue_data_subset'
        referenced_resource_detail_url = reverse(f'browse:{url_name}_detail', args=[resource_objectid_str])
        url_mapping = {
            'original_server_url': resource_server_url,
            'converted_url': referenced_resource_detail_url,
            'converted_url_text': referenced_resource['name'],
        }
        if len(referenced_op_mode_id) > 0:
            url_mapping['converted_url'] = f'{url_mapping["converted_url"]}#{referenced_op_mode_id}'
            url_mapping['converted_url_text'] = f'{url_mapping["converted_url_text"]}#{referenced_op_mode_id}'
        converted_resource_server_urls.append(url_mapping)
    return converted_resource_server_urls


def get_server_urls_from_scientific_metadata_flattened(scientific_metadata_flattened: dict) -> tuple[list, list]:
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

def create_readable_scientific_metadata_flattened(scientific_metadata_flattened: dict) -> dict:
    """
    Creates human readable versions of the provided scientific metadata
    dict's keys.
    """
    hidden_keys = [
        '_id',
        'description',
    ]
    hidden_key_regex = [
        re.compile(r'^name'),
        re.compile(r'^contactinfo'),
        re.compile(r'^identifier'),
        re.compile(r'.*onlineresource <b>(1/1)</b>\.description'),
        re.compile(r'.*onlineresource <b>(1/1)</b>\.linkage'),
        # re.compile(r'.*onlineresource <b>1</b>\.name'),
    ]
    scientific_metadata_readable = {}
    for key in scientific_metadata_flattened:
        if key.startswith('@') or any(x == key.lower() for x in hidden_keys) or any(regex for regex in hidden_key_regex if re.match(regex, key.lower())):
            continue
        key_split_by_dot = key.split('.')
        human_readable_key_strings = []
        for string in key_split_by_dot:
            # If there is only one occurrence of a property
            # doesn't make sense to keep the number suffix
            is_only_numbered_key = True
            if string.endswith('<b>(1/1)</b>'):
                for key2 in scientific_metadata_flattened:
                    if string.replace('<b>(1/', '<b>(2/') in key2:
                        is_only_numbered_key = False
            if is_only_numbered_key:
                string = string.replace('<b>(1/1)</b>', '')

            # Skip these strings
            if  string.startswith('#') or string == '@xlink:href':
                continue

            # Only keep the part of the key after the ':'
            if ':' in string:
                index_of_colon = string.index(':')
                string = string[index_of_colon + 1:]
            # Only keep the part of the key after the '@'
            if '@' in string:
                index_of_at_symbol = string.index('@')
                string = string[index_of_at_symbol + 1:]

            # Append the string that the be part of the 
            # human-readable key
            if string == '_id' or string.isupper():
                human_readable_key_strings.append(string)
            elif '_' in string:
                human_readable_string = ' '.join(string.split('_'))
                human_readable_string = ' '.join(_split_camel_case(human_readable_string))
                human_readable_key_strings.append(human_readable_string)
            else:
                human_readable_string = ' '.join(_split_camel_case(string))
                if not human_readable_string[0].isupper():
                    human_readable_string = human_readable_string.title()
                human_readable_key_strings.append(human_readable_string)
        human_readable_key_strings[-1] = f'<b>{human_readable_key_strings[-1]}</b>'
        human_readable_key_last_string = human_readable_key_strings[-1]
        human_readable_key_strings.pop()

        human_readable_key = ' > '.join(human_readable_key_strings).strip()
        if human_readable_key.startswith('Om:'):
            human_readable_key = human_readable_key.replace('Om:', '')
        if len(human_readable_key_strings):
            human_readable_key = f'{human_readable_key_last_string} <small class="text-muted fst-italic">(from {human_readable_key})</small>'
        else:
            human_readable_key = human_readable_key_last_string
        if human_readable_key != '':
            scientific_metadata_readable[human_readable_key] = scientific_metadata_flattened[key]
    return scientific_metadata_readable