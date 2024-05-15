"""Prepares cleaned form data for XML conversion.
"""
import json
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
    keywords_from_form = form_cleaned_data.get('keywords_json', [])
    keyword_dict_list = []
    for keyword_dict in keywords_from_form:
        keywords = keyword_dict.get('keywords')
        code_list = keyword_dict.get('type', {}).get('codeList')
        code_list_value = keyword_dict.get('type', {}).get('codeListValue')
        if any(not x for x in (keywords, code_list, code_list_value)):
            continue
        keyword_dict_list.append({
            'keywords': keywords,
            'type': {
                'code_list': code_list,
                'code_list_value': code_list_value,
            }
        })
    return keyword_dict_list

def process_related_parties(form_cleaned_data):
    related_parties_from_form = form_cleaned_data.get('related_parties_json', [])
    related_party_dict_list = []
    for related_party_dict in related_parties_from_form:
        role = related_party_dict.get('role')
        party = related_party_dict.get('parties')
        if any(not x for x in (role, party)):
            continue
        related_party_dict_list.append({
            'role': role,
            'parties': party,
        })
    return related_party_dict_list

def process_geometry_location_point_pos(form_cleaned_data):
    pos_point_1_from_form = form_cleaned_data.get('geometry_location_point_pos_1')
    pos_point_2_from_form = form_cleaned_data.get('geometry_location_point_pos_2')
    if (not pos_point_1_from_form
        or not pos_point_2_from_form):
        return ''
    return f'{pos_point_1_from_form} {pos_point_2_from_form}'

def process_location(form_cleaned_data):
    return {
        'geometry_location': {
            'point': {
                'id': form_cleaned_data.get('geometry_location_point_id'),
                'srs_name': form_cleaned_data.get('geometry_location_point_srs_name'),
                'pos': process_geometry_location_point_pos(form_cleaned_data),
            },
        },
        'name_location': {
            'code': form_cleaned_data.get('location_name')
        },
    }

def _process_time_position(time_position):
    if not time_position:
        return ''
    return time_position.isoformat()

def process_operation_time(form_cleaned_data):
    return {
        'time_period': {
            'id': form_cleaned_data.get('time_period_id'),
            'begin': {
                'time_instant': {
                    'id': form_cleaned_data.get('time_instant_begin_id'),
                    'time_position': _process_time_position(form_cleaned_data.get('time_instant_begin_position')),
                }
            },
            'end': {
                'time_instant': {
                    'id': form_cleaned_data.get('time_instant_end_id'),
                    'time_position': _process_time_position(form_cleaned_data.get('time_instant_end_position')),
                }
            },
        },
    }

def process_workflow_data_collections(form_cleaned_data):
    return [
        form_cleaned_data['data_collection_1'],
        *form_cleaned_data['data_collection_2_and_others'],
    ]

def process_capabilities(form_cleaned_data):
    capabilities_from_form = form_cleaned_data.get('capabilities_json', [])
    capabilities_dict_list = []
    for capability in capabilities_from_form:
        if '' in capability.get('vectorRepresentation'):
            capability.get('vectorRepresentation').remove('')
        if '' in capability.get('qualifier'):
            capability.get('qualifier').remove('')
        if all(not c for c in list(capability.values())):
            continue
        capabilities_dict_list.append({
            'name': capability.get('name'),
            'observed_property': capability.get('observedProperty'),
            'dimensionality_instance': capability.get('dimensionalityInstance'),
            'dimensionality_timeline': capability.get('dimensionalityTimeline'),
            'cadence': capability.get('cadence'),
            'cadence_units': capability.get('cadenceUnits'),
            'vector_representation': capability.get('vectorRepresentation'),
            'coordinate_system': capability.get('coordinateSystem'),
            'units': capability.get('units'),
            'qualifier': capability.get('qualifier'),
        })
    return capabilities_dict_list

def process_instrument_mode_pair(form_cleaned_data):
    instrument = form_cleaned_data.get('instrument_mode_pair_instrument')
    mode = form_cleaned_data.get('instrument_mode_pair_mode')
    return {
        'instrument': instrument,
        'mode': mode,
    }

def process_quality_assessment(form_cleaned_data):
    return {
        'data_quality_flags': form_cleaned_data.get('data_quality_flags'),
        'metadata_quality_flags': form_cleaned_data.get('metadata_quality_flags'),
    }

def process_operational_modes(form_cleaned_data):
    operational_modes_from_form = form_cleaned_data.get('operational_modes_json')
    operational_mode_dict_list = []
    for om in operational_modes_from_form:
        id = om.get('id')
        name = om.get('name')
        description = om.get('description')
        if any(not value for value in (id, name, description)):
            continue
        operational_mode_dict_list.append(om)
    return operational_mode_dict_list

def _process_time_spans(time_spans):
    return [
        {
            'begin_position': ts.get('beginPosition'),
            'end_position': ts.get('endPosition'),
        } for ts in time_spans
    ]

def remove_blank_dicts_from_dict_list(dict_list):
    return [d for d in dict_list if any(value for value in list(d.values()))]

def process_acquisition_capability_links(form_cleaned_data):
    capability_links_from_form = form_cleaned_data.get('capability_links_json')
    capability_link_dict_list = []
    for cl in capability_links_from_form:
        if '' in cl.get('platforms'):
            cl.get('platforms').remove('')
        cl['standardIdentifiers'] = remove_blank_dicts_from_dict_list(json.loads(cl.get('standardIdentifiers')))
        cl['timeSpans'] = remove_blank_dicts_from_dict_list(json.loads(cl.get('timeSpans')))
        if all(not value for value in list(cl.values())):
            continue
        capability_link_dict_list.append({
            'platforms': cl.get('platforms'),
            'acquisition_capabilities': cl.get('acquisitionCapabilities'),
            'standard_identifiers': cl.get('standardIdentifiers'),
            'time_spans': _process_time_spans(cl.get('timeSpans')),
        })
    return capability_link_dict_list