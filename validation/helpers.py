import logging
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)


def create_validation_summary_error(
    message='An unexpected error occurred whilst validating the XML.',
    details=''
):
    return {
        'message': message,
        'details': details
    }

def map_string_to_li_element(string):
    return f'<li>{string}</li>'

def create_register_url_from_resource_type_from_resource_url(resource_type_from_resource_url):
    try:
        # Data collection-related URLs
        url_name = resource_type_from_resource_url
        url_base_text = resource_type_from_resource_url.title()
        if resource_type_from_resource_url == 'acquisitionCapabilities':
            url_name = 'acquisition_capability_set'
            url_base_text = 'Acquisition Capabilities'
        elif resource_type_from_resource_url == 'computationCapabilities':
            url_name = 'computation_capability_set'
            url_base_text = 'Computation Capabilities'
        elif resource_type_from_resource_url == 'collection':
            url_name = 'data_collection'
            url_base_text = 'Data Collection'
    except AttributeError:
        pass
    
    # Static dataset-related URLs are sets
    type, localid = resource_type_from_resource_url[0], resource_type_from_resource_url[1]
    if localid.startswith('StaticDatasetEntry_'):
        url_name = 'static_dataset_entry'
        url_base_text = 'Static Dataset Entry'
    elif localid.startswith('DataSubset_'):
        url_name = 'data_subset'
        url_base_text = 'Data Subset'
    return (
        reverse_lazy(f"register:{url_name}"),
        f'{url_base_text} Registration'
    )

def map_acquisition_capability_to_update_link(resource):
    return f'<li><a href="{reverse_lazy("update:acquisition_capability_set", args=[resource.id])}" target="_blank" class="alert-link">Update {resource.name}</a></li>'