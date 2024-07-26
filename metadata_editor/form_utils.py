from .editor_dataclasses import ProcessCapabilityMetadataUpdate


# Contact info fields
def _format_time_to_12_hour_format(time_unformatted):
    return time_unformatted.strftime('%I:%M%p').lstrip('0').lower()

def get_hours_of_service_from_form(form_cleaned_data):
    try:
        time_start_parsed = form_cleaned_data.get('hours_of_service_start')
        time_end_parsed = form_cleaned_data.get('hours_of_service_end')

        time_start_formatted = _format_time_to_12_hour_format(time_start_parsed)
        time_end_formatted = _format_time_to_12_hour_format(time_end_parsed)
        return f'{time_start_formatted}-{time_end_formatted}'
    except BaseException:
        print('An error occurred when trying to process hours of service.')
        return ''

def get_phone_field_string_value(form_cleaned_data):
    phone = form_cleaned_data.get('phone', '')
    if phone:
        phone = phone.as_international
    return phone

# Capabilities field
def map_process_capabilities_to_dataclasses(form_cleaned_data):
    return [
        ProcessCapabilityMetadataUpdate(
            name=pc.get('name'),
            observed_property=pc.get('observedProperty'),
            dimensionality_instance=pc.get('dimensionalityInstance'),
            dimensionality_timeline=pc.get('dimensionalityTimeline'),
            cadence=pc.get('cadence'),
            cadence_unit=pc.get('cadenceUnits'),
            vector_representation=pc.get('vectorRepresentation'),
            coordinate_system=pc.get('coordinateSystem'),
            units=pc.get('units'),
            qualifier=pc.get('qualifier'),
        )
    for pc in form_cleaned_data.get('capabilities_json')]