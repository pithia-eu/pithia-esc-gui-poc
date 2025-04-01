from django.urls import reverse_lazy

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

def create_li_element_with_register_link_from_resource_type_from_resource_url(resource_type_from_resource_url):
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
    elif resource_type_from_resource_url.startswith('catalogue_Catalogue_'):
        url_name = 'catalogue'
        url_base_text = 'Catalogue'
    elif resource_type_from_resource_url.startswith('catalogue_CatalogueEntry_'):
        url_name = 'static_dataset_entry'
        url_base_text = 'Catalogue Entry'
    elif resource_type_from_resource_url.startswith('catalogue_DataSubset_'):
        url_name = 'data_subset'
        url_base_text = 'Catalogue Data Subset'
    return f'<li><a href="{reverse_lazy(f"register:{url_name}")}" target="_blank" class="alert-link">{url_base_text} Metadata Registration</a></li>'

def map_acquisition_capability_to_update_link(resource):
    return f'<li><a href="{reverse_lazy("update:acquisition_capability_set", args=[resource.id])}" target="_blank" class="alert-link">Update {resource.name}</a></li>'