from django.urls import reverse
from utils.ontology_helpers import get_graph_of_pithia_ontology_component
from common.helpers import get_mongodb_model_by_resource_type_from_resource_url
from validation.url_validation import validate_ontology_term_url, is_resource_url_structure_valid
from .html_helpers import create_anchor_tag_html_from_ontology_term_details
from .ontology_helpers import get_pref_label_from_ontology_node_iri

def create_ontology_term_detail_url_from_ontology_term_server_url(ontology_term_server_url):
    ontology_term_server_url_split = ontology_term_server_url.split('/')
    ontology_category = ontology_term_server_url_split[-2]
    ontology_term_id = ontology_term_server_url_split[-1]
    return reverse('browse:ontology_term_detail', args=[ontology_category, ontology_term_id])

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
        referenced_resource_server_url_split = resource_server_url.split('/')
        referenced_resource_type = referenced_resource_server_url_split[-3]
        referenced_resource_namespace = referenced_resource_server_url_split[-2]
        referenced_resource_localid = referenced_resource_server_url_split[-1]
        referenced_op_mode_id = ''
        if '#' in referenced_resource_localid:
            referenced_resource_localid_split = referenced_resource_localid.split('#')
            referenced_resource_localid = referenced_resource_localid_split[0]
            referenced_op_mode_id = referenced_resource_localid_split[1]
            print('referenced_resource_localid', referenced_resource_localid)
            print('referenced_op_mode_id', referenced_op_mode_id)
        referenced_resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(referenced_resource_type)
        if referenced_resource_mongodb_model == 'unknown':
            converted_resource_server_urls.append({
                'original_server_url': resource_server_url,
                'converted_url': resource_server_url,
                'converted_url_text': referenced_resource_localid,
            })
            continue
        referenced_resource = None
        if len(referenced_op_mode_id) > 0:
            referenced_resource = referenced_resource_mongodb_model.find_one({
                'identifier.PITHIA_Identifier.namespace': referenced_resource_namespace,
                'identifier.PITHIA_Identifier.localID': referenced_resource_localid,
                'operationalMode.InstrumentOperationalMode.id': referenced_op_mode_id
            }, {
                '_id': 1,
                'name': 1
            })
        else:
            referenced_resource = referenced_resource_mongodb_model.find_one({
                'identifier.PITHIA_Identifier.namespace': referenced_resource_namespace,
                'identifier.PITHIA_Identifier.localID': referenced_resource_localid,
            }, {
                '_id': 1,
                'name': 1
            })
        if referenced_resource is None:
            converted_resource_server_urls.append({
                'original_server_url': resource_server_url,
                'converted_url': resource_server_url,
                'converted_url_text': referenced_resource_localid,
            })
            continue
        resource_objectid_str = str(referenced_resource['_id'])
        if referenced_resource_type.lower() == 'computationcapabilities':
            referenced_resource_type = 'computation_capability_set'
        elif referenced_resource_type.lower() == 'acquisitioncapabilities':
            referenced_resource_type = 'acquisition_capability_set'
        referenced_resource_detail_url = reverse(f'browse:{referenced_resource_type}_detail', args=[resource_objectid_str])
        url_mapping = {
            'original_server_url': resource_server_url,
            'converted_url': referenced_resource_detail_url,
            'converted_url_text': referenced_resource["name"],
        }
        if len(referenced_op_mode_id) > 0:
            url_mapping['converted_url'] = f'{url_mapping["converted_url"]}#{referenced_op_mode_id}'
            url_mapping['converted_url_text'] = f'{url_mapping["converted_url_text"]}, {referenced_op_mode_id}'
        converted_resource_server_urls.append(url_mapping)
    return converted_resource_server_urls