from lxml import etree
from rdflib import URIRef
from rdflib.resource import Resource

from common import models
from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from ontology.utils import (
    get_rdf_text_for_ontology_component,
    get_rdf_text_locally,
)


def parse_registration_xml(r):
    """
    Parses the XML of a metadata registration.
    """
    return etree.fromstring(r.xml.encode())

def parse_rdf_text(rdf_text):
    """
    Parses the RDF of an ontology component.
    """
    return etree.fromstring(rdf_text.encode())

def get_and_process_text_nodes_from_registration(r):
    """
    Finds and returns a list of strings retrieved
    from text nodes of a metadata registration.
    """
    parsed_xml = parse_registration_xml(r)
    text_nodes_in_parsed_xml = parsed_xml.xpath('.//*/text()')
    # Convert all text nodes to strings to make
    # further processing easier.
    return [str(tn) for tn in text_nodes_in_parsed_xml]

def get_ontology_urls_from_registration(r):
    """
    Finds and returns a list of ontology term
    URLs found within a metadata registration.
    """
    parsed_xml = parse_registration_xml(r)
    return parsed_xml.xpath(f'.//*[contains(@xlink:href, "{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}")]/@xlink:href', namespaces={
        'xlink': 'http://www.w3.org/1999/xlink'
    })

def get_and_process_text_nodes_of_ontology_url(ontology_url, ontology_component_rdf):
    """
    Gets the text properties of the ontology term
    node corresponding with a given ontology term
    URL.
    """
    searchable_text = []
    parsed_rdf = parse_rdf_text(ontology_component_rdf)
    ontology_url_element = parsed_rdf.xpath(f'.//skos:Concept[@rdf:about="{ontology_url}"]', namespaces={
        'skos': 'http://www.w3.org/2004/02/skos/core#',
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    })
    for el in ontology_url_element:
        searchable_text += el.xpath('.//*/text()')
    
    return searchable_text

def get_searchable_text_list_from_ontology_urls(ontology_urls):
    """
    Gets and combines each list of text properties for
    each ontology URL, into one combined list.
    """
    ontology_urls = list(set(ontology_urls))
    searchable_ontology_text = []
    processed_ontology_component_rdfs = {}
    for o_url in ontology_urls:
        o_url_shortened = o_url.replace(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/', '')
        ontology_component_name, term_id = o_url_shortened.split('/')

        if ontology_component_name not in processed_ontology_component_rdfs:
            processed_ontology_component_rdfs[ontology_component_name] = get_rdf_text_locally(ontology_component_name)
        ontology_component_rdf = processed_ontology_component_rdfs[ontology_component_name]
        searchable_text_for_ontology_url = get_and_process_text_nodes_of_ontology_url(o_url, ontology_component_rdf)
        searchable_ontology_text += searchable_text_for_ontology_url
    
    return list(set(searchable_ontology_text))


# TODO: not needed, remove in future commit.
def get_metadata_urls_from_registration(r):
    parsed_xml = parse_registration_xml(r)
    return parsed_xml.xpath('.//*[contains(@xlink:href, "https://metadata.pithia.eu/resources/2.2/")]/@xlink:href', namespaces={
        'xlink': 'http://www.w3.org/1999/xlink'
    })

def find_metadata_registrations_matching_query(query, model, exact=False):
    """
    Finds and returns metadata registrations according to
    the simple search matching criteria.
    """
    query_sections = query.split()
    registrations_with_match = []
    if len(query_sections) == 0:
        return registrations_with_match

    registrations = model.objects.all()
    for r in registrations:
        r_text_node_strings = get_and_process_text_nodes_from_registration(r)
        r_ontology_urls = get_ontology_urls_from_registration(r)
        r_ontology_url_searchable_strings = get_searchable_text_list_from_ontology_urls(r_ontology_urls)
        r_searchable_strings = r_text_node_strings + r_ontology_url_searchable_strings
        r_searchable_strings = [ss for ss in r_searchable_strings if ss.strip() != '']
        if not exact:
            r_searchable_strings = [' '.join(ss.replace('\n', '').split()) for ss in r_searchable_strings]
        for ss in r_searchable_strings:
            match_criteria = all(qs.lower() in ss.lower() for qs in query_sections)
            if exact:
                match_criteria = query in ss
            if match_criteria:
                registrations_with_match.append(r)

    # Ensure there are no duplicate data collections
    registrations_with_match = {r.id: r for r in registrations_with_match}.values()
    return registrations_with_match

def get_data_collections_from_metadata_dependents(metadata_dependents):
    """
    Utility function - gets and returns the metadata dependents
    which are Data Collections from a list of given metadata
    dependents.
    """
    return [md for md in metadata_dependents if md.type_in_metadata_server_url == models.DataCollection.type_in_metadata_server_url]

def get_data_collections_from_other_metadata(registrations):
    """
    Gets and returns dependent Data Collections from a list
    of given pre-Data Collection step registrations.
    """
    data_collections_found = []
    for r in registrations:
        data_collections_from_metadata_dependents = get_data_collections_from_metadata_dependents(r.metadata_dependents)
        data_collections_found += data_collections_from_metadata_dependents
    return data_collections_found

def find_data_collections_for_simple_search(query, exact=False):
    """
    Does a simple search based on the given query.
    """

    data_collections_matching_query = []

    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Organisation, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Individual, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Project, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Platform, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Operation, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Instrument, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.AcquisitionCapabilities, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Acquisition, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.ComputationCapabilities, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Computation, exact=exact))
    data_collections_matching_query += get_data_collections_from_other_metadata(find_metadata_registrations_matching_query(query, models.Process, exact=exact))

    data_collections = find_metadata_registrations_matching_query(query, models.DataCollection, exact=exact)
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
    