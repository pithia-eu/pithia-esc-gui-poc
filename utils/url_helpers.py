from django.urls import reverse
from ontology.utils import (
    get_graph_of_pithia_ontology_component,
    get_pref_label_from_ontology_node_iri,
)
from common.helpers import (
    get_mongodb_model_by_resource_type_from_resource_url,
    get_mongodb_model_from_catalogue_related_resource_url,
)
from utils.mapping_functions import prepare_resource_for_template
from validation.url_validation import validate_ontology_term_url
from validation.url_validation_utils import (
    divide_resource_url_into_main_components,
    divide_resource_url_from_op_mode_id,
    divide_catalogue_related_resource_url_into_main_components,
)

def create_ontology_term_detail_url_from_ontology_term_server_url(ontology_term_server_url):
    ontology_term_server_url_split = ontology_term_server_url.split('/')
    ontology_category = ontology_term_server_url_split[-2]
    ontology_term_id = ontology_term_server_url_split[-1]
    return reverse('ontology:ontology_term_detail', args=[ontology_category, ontology_term_id])

def convert_ontology_server_urls_to_browse_urls(ontology_server_urls):
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

def convert_resource_server_urls_to_browse_urls(resource_server_urls):
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
            'converted_url_text': referenced_resource_localid,
        }
        if '/catalogue/' in resource_server_url:
            resource_server_url_components = divide_catalogue_related_resource_url_into_main_components(resource_server_url)
            referenced_resource_type = resource_server_url_components['resource_type']
            referenced_resource_namespace = resource_server_url_components['namespace']
            referenced_resource_localid = resource_server_url_components['localid']
            referenced_resource_mongodb_model = get_mongodb_model_from_catalogue_related_resource_url(resource_server_url)
        else:
            if '#' in referenced_resource_localid:
                components_of_resource_server_url_with_op_mode_id = divide_resource_url_from_op_mode_id(resource_server_url)
                resource_server_url = components_of_resource_server_url_with_op_mode_id['resource_url']
                referenced_op_mode_id = components_of_resource_server_url_with_op_mode_id['op_mode_id']
            resource_server_url_components = divide_resource_url_into_main_components(resource_server_url)
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
            'converted_url_text': referenced_resource["name"],
        }
        if len(referenced_op_mode_id) > 0:
            url_mapping['converted_url'] = f'{url_mapping["converted_url"]}#{referenced_op_mode_id}'
            url_mapping['converted_url_text'] = f'{url_mapping["converted_url_text"]}#{referenced_op_mode_id}'
        converted_resource_server_urls.append(url_mapping)
    return converted_resource_server_urls