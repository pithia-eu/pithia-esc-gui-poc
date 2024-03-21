"""Prepares cleaned form data for XML conversion.
"""
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

def process_documentation(form_cleaned_data):
    return {
        'citation_title': form_cleaned_data.get('citation_title'),
        'citation_date': form_cleaned_data.get('citation_publication_date'),
        # CI_DateTypeCode values are normally the values
        # used below.
        'ci_date_type_code': 'Publication Date',
        'ci_date_type_code_code_list': '',
        'ci_date_type_code_code_list_value': '',
        'ci_linkage_url': form_cleaned_data.get('citation_linkage_url'),
        'other_citation_details': form_cleaned_data.get('other_citation_details'),
        'doi': form_cleaned_data.get('citation_doi'),
    }

def process_project_keywords(form_cleaned_data):
    keyword_dict_from_form = form_cleaned_data.get('keywords_json')
    keyword_dict_list = []
    for key, value in keyword_dict_from_form.items():
        keyword_dict_list.append({
            'keywords': value.get('keywords', []),
            'type': {
                'code_list': value.get('code', ''),
                'code_list_value': key,
            }
        })
    return keyword_dict_list

def process_related_parties(form_cleaned_data):
    related_parties_dict_from_form = form_cleaned_data.get('related_parties_json')
    related_parties_dict_list = []
    for key, value in related_parties_dict_from_form.items():
        related_parties_dict_list.append({
            'role': key,
            'parties': value,
        })
    return related_parties_dict_list