from lxml import etree

from common import models

def find_metadata_registrations_matching_query(query, model):
    query_sections = query.split()
    print('query_sections', query_sections)
    registrations_with_match = []
    if len(query_sections) == 0:
        return registrations_with_match
    xpath_match_query = ''
    for counter, qs in enumerate(query_sections):
        xpath_match_query += f'contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), translate("{qs}", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))'
        if counter != len(query_sections) - 1:
            xpath_match_query += ' and '
    registrations = model.objects.all()
    for r in registrations:
        parsed_xml = etree.fromstring(r.xml.encode())
        text_nodes_in_parsed_xml = parsed_xml.xpath('.//*/text()')
        text_nodes_in_parsed_xml = [' '.join(str(tn).strip().replace('\n', '').split()) for tn in text_nodes_in_parsed_xml if str(tn).strip() != '']
        for tn in text_nodes_in_parsed_xml:
            if all(qs.lower() in tn.lower() for qs in query_sections):
                registrations_with_match.append(r)

    # Ensure there are no duplicate data collections
    registrations_with_match = {r.id: r for r in registrations_with_match}.values()
    return registrations_with_match

def find_metadata_registrations_matching_query_exactly(query, model):
    registrations = model.objects.all()
    registrations_with_match = []
    for r in registrations:
        parsed_xml = etree.fromstring(r.xml.encode())
        if parsed_xml.xpath(f'.//*/text()[contains(., "{query}")]'):
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
    