import os
from django.urls import reverse


# Resource URL identification functions
def is_operational_mode_url(url):
    return '#' in url

# Resource URL component extraction functions
def divide_data_collection_related_resource_url_into_main_components(resource_url):
    resource_url_split = resource_url.split('/')
    return {
        'url_base': '/'.join(resource_url_split[:5]),
        'resource_type': resource_url_split[5],
        'namespace': resource_url_split[6],
        'localid': resource_url_split[7],
    }

def divide_catalogue_related_resource_url_into_main_components(resource_url):
    resource_url_split = resource_url.split('/')
    return {
        'url_base': '/'.join(resource_url_split[:5]),
        'resource_type': resource_url_split[5],
        'namespace': resource_url_split[6],
        'event': resource_url_split[7],
        'localid': resource_url_split[8],
    }

def divide_resource_url_into_main_components(resource_url):
    try:
        return divide_catalogue_related_resource_url_into_main_components(resource_url)
    except IndexError:
        pass
    
    try:
        return divide_data_collection_related_resource_url_into_main_components(resource_url)
    except IndexError:
        pass

    return {
        'url_base': None,
        'resource_type': None,
        'namespace': None,
        'localid': None,
    }

def divide_resource_url_from_op_mode_id(resource_url_with_op_mode_id):
    resource_url_with_op_mode_id_split = resource_url_with_op_mode_id.split('#')
    return {
        'resource_url': '#'.join(resource_url_with_op_mode_id_split[:-1]),
        'op_mode_id': resource_url_with_op_mode_id_split[-1],
    }

def get_namespace_and_localid_from_resource_url(resource_url: str) -> tuple[str, str]:
    resource_server_url_components = divide_resource_url_into_main_components(resource_url)
    return resource_server_url_components['namespace'], resource_server_url_components['localid']

def create_ontology_term_detail_url_from_ontology_term_server_url(ontology_term_server_url):
    ontology_term_server_url_split = ontology_term_server_url.split('/')
    ontology_category = ontology_term_server_url_split[-2]
    ontology_term_id = ontology_term_server_url_split[-1]
    return reverse('ontology:ontology_term_detail', args=[ontology_category, ontology_term_id])

def create_data_subset_detail_page_url(data_subset_id: str) -> str:
    data_subset_detail_page_url = reverse('browse:catalogue_data_subset_detail', kwargs={ 'catalogue_data_subset_id': data_subset_id })
    return f'{os.environ["HANDLE_URL_PREFIX"]}{str(data_subset_detail_page_url)}'
