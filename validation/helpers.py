def _create_validation_error_details_dict(err_type, err_message, extra_details):
    return {
        'type': str(err_type),
        'message': err_message,
        'extra_details': extra_details
    }

def _map_string_to_li_element(string):
    return f'<li>{string}</li>'

def _map_string_to_li_element_with_register_link(string):
    if string == 'collection':
        string == 'data_collection'
    elif string == 'acquisitionCapabilities':
        string = 'acquisition_capability_set'
    elif string == 'computationCapabilities':
        string = 'computation_capability_set'
    return f'<li><a href="{reverse_lazy(f"register:{string}")}" target="_blank" class="alert-link">{string.capitalize()} Metadata Registration</a></li>'

def _map_acquisition_capability_to_update_link(resource):
    return f'<li><a href="{reverse_lazy("update:acquisition_capability_set", args=[resource["_id"]])}" target="_blank" class="alert-link">Update {resource["name"]}</a></li>'

def _map_etree_element_to_text(element):
    return element.text

def _map_operational_mode_object_to_id_string(om):
    return om['InstrumentOperationalMode']['id']