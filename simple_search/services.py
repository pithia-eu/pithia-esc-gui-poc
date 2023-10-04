from lxml import etree

from common import models

def find_metadata_registrations_matching_query(query, model):
    registrations = model.objects.all()
    registrations_with_match = []
    for r in registrations:
        parsed_xml = etree.fromstring(r.xml.encode())
        if parsed_xml.xpath(f'.//*[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), translate("{query}", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]'):
            # If partial case-insensitive text match found.
            # Credit: https://stackoverflow.com/a/36427554
            registrations_with_match.append(r)
    
    return registrations_with_match

def find_metadata_registrations_matching_query_exactly(query, model):
    registrations = model.objects.all()
    registrations_with_match = []
    for r in registrations:
        parsed_xml = etree.fromstring(r.xml.encode())
        if parsed_xml.xpath(f'.//*[text()[contains(., "{query}")]]'):
            registrations_with_match.append(r)

    return registrations_with_match

def get_data_collections_from_metadata_dependents(metadata_dependents):
    return [md for md in metadata_dependents if md.type_in_metadata_server_url == models.DataCollection.type_in_metadata_server_url]

def get_data_collections_from_other_metadata(registrations):
    data_collections_found = []
    for r in registrations:
        data_collections_from_metadata_dependents = get_data_collections_from_metadata_dependents(r.metadata_dependents)
        data_collections_found += data_collections_from_metadata_dependents
    return data_collections_found

def find_data_collections_for_simple_search(query):
    data_collections_matching_query = []

    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Organisation))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Individual))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Project))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Platform))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Operation))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Instrument))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.AcquisitionCapabilities))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Acquisition))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.ComputationCapabilities))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Computation))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Process))

    data_collections = find_metadata_registrations_matching_query(query, models.DataCollection)
    data_collections_matching_query += data_collections

    # Ensure there are no duplicate data collections
    data_collections_matching_query = {dc.id: dc for dc in data_collections_matching_query}.values()

    print('query', query)
    print('data_collections_matching_query', data_collections_matching_query)
    print('')
    
    return data_collections_matching_query

def find_data_collections_for_case_sensitive_simple_search(query):
    # https://stackoverflow.com/a/14300008
    pass
    