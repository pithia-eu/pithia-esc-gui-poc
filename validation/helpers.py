from django.urls import reverse_lazy

def create_validation_details_error(message='An error occurred during validation', details=''):
    return {
        'message': message,
        'details': details
    }

def _map_string_to_li_element(string):
    return f'<li>{string}</li>'

def _create_li_element_with_register_link_from_resource_type_from_resource_url(resource_type_from_resource_url):
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
        url_name = 'catalogue_entry'
        url_base_text = 'Catalogue Entry'
    elif resource_type_from_resource_url.startswith('catalogue_DataSubset_'):
        url_name = 'catalogue_data_subset'
        url_base_text = 'Catalogue Data Subset'
    return f'<li><a href="{reverse_lazy(f"register:{url_name}")}" target="_blank" class="alert-link">{url_base_text} Metadata Registration</a></li>'

def _map_acquisition_capability_to_update_link(resource):
    return f'<li><a href="{reverse_lazy("update:acquisition_capability_set", args=[resource["_id"]])}" target="_blank" class="alert-link">Update {resource["name"]}</a></li>'

def _map_etree_element_to_text(element):
    return element.text

def _map_operational_mode_object_to_id_string(om):
    return om['InstrumentOperationalMode']['id']