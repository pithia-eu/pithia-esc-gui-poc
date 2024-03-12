from unidecode import unidecode

# Contact info
def process_contact_info_in_form(form_cleaned_data):
    return {
        'phone': form_cleaned_data.get('phone'),
        'address': {
            'delivery_point': form_cleaned_data.get('delivery_point'),
            'city': form_cleaned_data.get('city'),
            'administrative_area': form_cleaned_data.get('administrative_area'),
            'postal_code': form_cleaned_data.get('postal_code'),
            'country': unidecode(form_cleaned_data.get('country')),
            'electronic_mail_address': form_cleaned_data.get('email_address'),
        },
        'online_resource': form_cleaned_data.get('online_resource'),
        'hours_of_service': form_cleaned_data.get('hours_of_service'),
        'contact_instructions': form_cleaned_data.get('contact_instructions'),
    }

# Hours of service
def _format_time_to_12_hour_format(time_unformatted):
    return time_unformatted.strftime('%I:%M%p').lstrip('0').lower()

def process_hours_of_service_in_form(form_cleaned_data):
    try:
        time_start_parsed = form_cleaned_data.get('hours_of_service_start')
        time_end_parsed = form_cleaned_data.get('hours_of_service_end')

        time_start_formatted = _format_time_to_12_hour_format(time_start_parsed)
        time_end_formatted = _format_time_to_12_hour_format(time_end_parsed)
        return f'{time_start_formatted}-{time_end_formatted}'
    except BaseException:
        print('An error occurred when trying to process hours of service.')
        return ''
