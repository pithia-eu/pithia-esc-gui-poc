from lxml import etree

from common import models
from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from ontology.utils import (
    get_xml_of_ontology_category_terms_locally,
)

# Utilities
def parse_registration_xml(r):
    """Parses the XML of a metadata registration.
    """
    return etree.fromstring(r.xml.encode())

def parse_rdf_text(rdf_text):
    """Parses the RDF of an ontology component.
    """
    return etree.fromstring(rdf_text.encode())

def remove_whitespace_only_strings_from_text_list(text_list):
    return [ss for ss in text_list if ss.strip() != '']

def remove_newlines_and_normalise_whitespace_in_text_list(text_list):
    return [' '.join(pt.replace('\n', '').split()) for pt in text_list]

def is_query_in_string(query, string):
    return query in string

def is_each_query_section_in_string(query_sections, string):
    return all(qs.lower() in string.lower() for qs in query_sections)


# Text node filtering
def get_and_process_text_nodes_from_registration(r):
    """Finds and returns a list of strings retrieved
    from text nodes of a metadata registration.
    """
    parsed_xml = parse_registration_xml(r)
    if (etree.QName(parsed_xml).localname == models.Organisation.root_element_name
       or etree.QName(parsed_xml).localname == models.Individual.root_element_name):
        text_nodes_in_parsed_xml = parsed_xml.xpath('//*[not(descendant::gco:CharacterString) and not(ancestor-or-self::gco:CharacterString)]/text()', namespaces={
            'gco': 'http://www.isotc211.org/2005/gco'
        })
    else:
        text_nodes_in_parsed_xml = parsed_xml.xpath('//*/text()')
    # Convert all text nodes to strings to make
    # further processing easier.
    return [str(tn) for tn in text_nodes_in_parsed_xml]

def filter_metadata_registrations_by_text_nodes(query_or_query_sections, registrations, query_matching_fn, text_formatting_fns=[]):
    registrations_with_match = []
    for r in registrations:
        # Extract text nodes and ontology URLs from all registrations
        r_text_node_strings = get_and_process_text_nodes_from_registration(r)
        for fn in text_formatting_fns:
            r_text_node_strings = fn(r_text_node_strings)
        for tns in r_text_node_strings:
            if query_matching_fn(query_or_query_sections, tns):
                registrations_with_match.append(r)

    return list({r.id: r for r in registrations_with_match}.values())

def filter_metadata_registrations_by_text_nodes_default(query_sections, registrations):
    return filter_metadata_registrations_by_text_nodes(query_sections, registrations, is_each_query_section_in_string, [
        remove_whitespace_only_strings_from_text_list,
        remove_newlines_and_normalise_whitespace_in_text_list,
    ])

def filter_metadata_registrations_by_text_nodes_exact(query, registrations):
    return filter_metadata_registrations_by_text_nodes(query, registrations, is_query_in_string, [
        remove_whitespace_only_strings_from_text_list
    ])

# Custom simple search - Organisations and Projects
def filter_metadata_registrations_by_name_exact(query, registrations):
    registrations_with_match = []
    for r in registrations:
        if query not in r.name:
            continue
        registrations_with_match.append(r)

    return list({r.id: r for r in registrations_with_match}.values())


# Ontology URL filtering
def get_ontology_urls_from_registration(r):
    """Finds and returns a list of ontology term
    URLs found within a metadata registration.
    """
    parsed_xml = parse_registration_xml(r)
    return list(set(parsed_xml.xpath(f'.//*[contains(@xlink:href, "{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}")]/@xlink:href', namespaces={
        'xlink': 'http://www.w3.org/1999/xlink'
    })))

def get_and_map_ontology_urls_to_registrations(registrations):
    """Creates a dict of ontology URLs and the registrations
    that they were found in.
    """
    ontology_urls_to_registrations = {}
    for r in registrations:
        # Ontology URLs are mapped to the registrations they came from
        r_ontology_urls = get_ontology_urls_from_registration(r)
        for o_url in r_ontology_urls:
            if o_url not in ontology_urls_to_registrations:
                ontology_urls_to_registrations[o_url] = []
            ontology_urls_to_registrations[o_url].append(r)
    return ontology_urls_to_registrations

def get_and_process_text_nodes_of_ontology_url(ontology_url, ontology_component_rdf):
    """Gets the text properties of the ontology term
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
    
    return list(set([str(tn) for tn in searchable_text]))

def get_ontology_component_name_from_ontology_url(ontology_url):
    o_url_shortened = ontology_url.replace(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/', '')
    ontology_component_name, term_id = o_url_shortened.split('/')
    return ontology_component_name

def get_and_map_searchable_text_to_ontology_urls(ontology_urls, ontology_rdfs):
    """Creates a dict mapping each ontology URL to its
    corresponding text properties, fetched from the
    Space Physics Ontology.
    """
    ontology_urls = list(set(ontology_urls))
    ontology_urls_to_text_nodes = {}
    for o_url in ontology_urls:
        ontology_component_name = get_ontology_component_name_from_ontology_url(o_url)
        ontology_component_rdf = ontology_rdfs[ontology_component_name]
        searchable_text_for_ontology_url = get_and_process_text_nodes_of_ontology_url(o_url, ontology_component_rdf)
        if o_url not in ontology_urls_to_text_nodes:
            ontology_urls_to_text_nodes[o_url] = []
        ontology_urls_to_text_nodes[o_url] += searchable_text_for_ontology_url
        ontology_urls_to_text_nodes[o_url] = list(set(ontology_urls_to_text_nodes[o_url]))
    
    return ontology_urls_to_text_nodes

def get_rdfs_from_ontology_urls(ontology_urls):
    """Creates a dict of ontology component
    RDFs that the ontology URLs are from.
    """
    ontology_rdfs = {}
    for o_url in ontology_urls:
        o_url_shortened = o_url.replace(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/', '')
        ontology_component_name, term_id = o_url_shortened.split('/')
        if ontology_component_name not in ontology_rdfs:
            ontology_rdfs[ontology_component_name] = ''
    
    for key in ontology_rdfs.keys():
        ontology_rdfs[key] = get_xml_of_ontology_category_terms_locally(key)

    return ontology_rdfs

def filter_metadata_registrations_by_ontology_urls(query_or_query_sections, ontology_urls_to_registrations, ontology_rdfs, query_matching_fn, text_formatting_fns=[]):
    registrations_with_match = []
    # Pass the ontology URLs and RDFs to map each URL to its text properties
    ontology_urls_to_ontology_text_node_strings = get_and_map_searchable_text_to_ontology_urls(ontology_urls_to_registrations.keys(), ontology_rdfs)

    # Go through the ontology URL to text properties
    # mappings and find matches.
    for key, value in ontology_urls_to_ontology_text_node_strings.items():
        for fn in text_formatting_fns:
            value = fn(value)
        for tns in value:
            if query_matching_fn(query_or_query_sections, tns):
                registrations_with_match += ontology_urls_to_registrations[key]
                break
    return list({r.id: r for r in registrations_with_match}.values())

def filter_metadata_registrations_by_ontology_urls_default(query_sections, ontology_urls_to_registrations, ontology_rdfs):
    return filter_metadata_registrations_by_ontology_urls(
        query_sections,
        ontology_urls_to_registrations,
        ontology_rdfs,
        is_each_query_section_in_string,
        [remove_whitespace_only_strings_from_text_list, remove_newlines_and_normalise_whitespace_in_text_list],
    )

def filter_metadata_registrations_by_ontology_urls_exact(query, ontology_urls_to_registrations, ontology_rdfs):
    return filter_metadata_registrations_by_ontology_urls(
        query,
        ontology_urls_to_registrations,
        ontology_rdfs,
        is_query_in_string,
        [remove_whitespace_only_strings_from_text_list],
    )

# Find Data Collections referring to pre-Data Collection step registrations.
def get_data_collections_from_metadata_dependents(metadata_dependents):
    """Utility function - gets and returns the metadata dependents
    which are Data Collections from a list of given metadata
    dependents.
    """
    return [md for md in metadata_dependents if md.type_in_metadata_server_url == models.DataCollection.type_in_metadata_server_url]

def get_data_collections_from_other_metadata(registrations, checked_metadata: set = set()):
    """Gets and returns dependent Data Collections from a list
    of given pre-Data Collection step registrations.
    """
    data_collections_found = []
    for r in registrations:
        if str(r.pk) in checked_metadata:
            continue
        metadata_dependents, new_checked_metadata = r.get_metadata_dependents_and_checked_metadata(
            checked_metadata=checked_metadata,
            up_to_weight=models.DataCollection.weight
        )
        checked_metadata.union(new_checked_metadata)
        data_collections_from_metadata_dependents = get_data_collections_from_metadata_dependents(metadata_dependents)
        data_collections_found += data_collections_from_metadata_dependents
    return data_collections_found, checked_metadata


def get_registrations_for_simple_search(model):
    return model.objects.all()

def find_data_collections_for_simple_search(query, exact=False):
    """Does a simple search based on the given query.
    """

    data_collections_matching_query = []
    if len(query.split()) == 0:
        return data_collections_matching_query
    
    query_or_query_sections = query.split()
    text_node_filtering_fn = filter_metadata_registrations_by_text_nodes_default
    ontology_url_filtering_fn = filter_metadata_registrations_by_ontology_urls_default
    if exact:
        text_node_filtering_fn = filter_metadata_registrations_by_text_nodes_exact
        ontology_url_filtering_fn = filter_metadata_registrations_by_ontology_urls_exact
        query_or_query_sections = query

    individuals = get_registrations_for_simple_search(models.Individual)
    platforms = get_registrations_for_simple_search(models.Platform)
    operations = get_registrations_for_simple_search(models.Operation)
    instruments = get_registrations_for_simple_search(models.Instrument)
    acquisition_capabilities = get_registrations_for_simple_search(models.AcquisitionCapabilities)
    acquisitions = get_registrations_for_simple_search(models.Acquisition)
    computation_capabilities = get_registrations_for_simple_search(models.ComputationCapabilities)
    computations = get_registrations_for_simple_search(models.Computation)
    processes = get_registrations_for_simple_search(models.Process)
    data_collections = get_registrations_for_simple_search(models.DataCollection)

    # Text node filtering
    individuals_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, individuals)
    platforms_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, platforms)
    operations_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, operations)
    instruments_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, instruments)
    acquisition_capabilities_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, acquisition_capabilities)
    acquisitions_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, acquisitions)
    computation_capabilities_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, computation_capabilities)
    computations_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, computations)
    processes_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, processes)
    data_collections_filtered_by_text_nodes = text_node_filtering_fn(query_or_query_sections, data_collections)

    # Ontology URL filtering
    ontology_urls_mapped_to_individuals = get_and_map_ontology_urls_to_registrations(individuals)
    ontology_urls_mapped_to_platforms = get_and_map_ontology_urls_to_registrations(platforms)
    ontology_urls_mapped_to_operations = get_and_map_ontology_urls_to_registrations(operations)
    ontology_urls_mapped_to_instruments = get_and_map_ontology_urls_to_registrations(instruments)
    ontology_urls_mapped_to_acquisition_capabilities = get_and_map_ontology_urls_to_registrations(acquisition_capabilities)
    ontology_urls_mapped_to_acquisitions = get_and_map_ontology_urls_to_registrations(acquisitions)
    ontology_urls_mapped_to_computation_capabilities = get_and_map_ontology_urls_to_registrations(computation_capabilities)
    ontology_urls_mapped_to_computations = get_and_map_ontology_urls_to_registrations(computations)
    ontology_urls_mapped_to_processes = get_and_map_ontology_urls_to_registrations(processes)
    ontology_urls_mapped_to_data_collections = get_and_map_ontology_urls_to_registrations(data_collections)

    ontology_rdfs = get_rdfs_from_ontology_urls(list(set(
        list(ontology_urls_mapped_to_individuals.keys())
        + list(ontology_urls_mapped_to_platforms.keys())
        + list(ontology_urls_mapped_to_operations.keys())
        + list(ontology_urls_mapped_to_instruments.keys())
        + list(ontology_urls_mapped_to_acquisition_capabilities.keys())
        + list(ontology_urls_mapped_to_acquisitions.keys())
        + list(ontology_urls_mapped_to_computation_capabilities.keys())
        + list(ontology_urls_mapped_to_computations.keys())
        + list(ontology_urls_mapped_to_processes.keys())
        + list(ontology_urls_mapped_to_data_collections.keys())
    )))
    
    individuals_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_individuals, ontology_rdfs)
    platforms_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_platforms, ontology_rdfs)
    operations_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_operations, ontology_rdfs)
    instruments_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_instruments, ontology_rdfs)
    acquisition_capabilities_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_acquisition_capabilities, ontology_rdfs)
    acquisitions_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_acquisitions, ontology_rdfs)
    computation_capabilities_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_computation_capabilities, ontology_rdfs)
    computations_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_computations, ontology_rdfs)
    processes_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_processes, ontology_rdfs)
    data_collections_filtered_by_ontology_urls = ontology_url_filtering_fn(query_or_query_sections, ontology_urls_mapped_to_data_collections, ontology_rdfs)

    organisations_filtered_by_name = list(models.Organisation.objects.for_simple_search(query_or_query_sections))
    projects_filtered_by_name = list(models.Project.objects.for_simple_search(query_or_query_sections))
    if exact:
        organisations_filtered_by_name = filter_metadata_registrations_by_name_exact(query_or_query_sections, list(models.Organisation.objects.all()))
        projects_filtered_by_name = filter_metadata_registrations_by_name_exact(query_or_query_sections, list(models.Project.objects.all()))

    checked_metadata = set()
    # Organisations
    data_collections_from_organisations, updated_checked_metadata_from_organisations = get_data_collections_from_other_metadata(organisations_filtered_by_name, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_organisations
    checked_metadata.union(updated_checked_metadata_from_organisations)
    # Individuals
    data_collections_from_individuals, updated_checked_metadata_from_individuals = get_data_collections_from_other_metadata(individuals_filtered_by_text_nodes + individuals_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_individuals
    checked_metadata.union(updated_checked_metadata_from_individuals)
    # Projects
    data_collections_from_projects, updated_checked_metadata_from_projects = get_data_collections_from_other_metadata(projects_filtered_by_name, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_projects
    checked_metadata.union(updated_checked_metadata_from_projects)
    # Platforms
    data_collections_from_platforms, updated_checked_metadata_from_platforms = get_data_collections_from_other_metadata(platforms_filtered_by_text_nodes + platforms_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_platforms
    checked_metadata.union(updated_checked_metadata_from_platforms)
    # Operations
    data_collections_from_operations, updated_checked_metadata_from_operations = get_data_collections_from_other_metadata(operations_filtered_by_text_nodes + operations_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_operations
    checked_metadata.union(updated_checked_metadata_from_operations)
    # Instruments
    data_collections_from_instruments, updated_checked_metadata_from_instruments = get_data_collections_from_other_metadata(instruments_filtered_by_text_nodes + instruments_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_instruments
    checked_metadata.union(updated_checked_metadata_from_instruments)
    # Acquisition Capabilities
    data_collections_from_acquisition_capabilities, updated_checked_metadata_from_acquisition_capabilities = get_data_collections_from_other_metadata(acquisition_capabilities_filtered_by_text_nodes + acquisition_capabilities_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_acquisition_capabilities
    checked_metadata.union(updated_checked_metadata_from_acquisition_capabilities)
    # Acquisitions
    data_collections_from_acquisitions, updated_checked_metadata_from_acquisitions = get_data_collections_from_other_metadata(acquisitions_filtered_by_text_nodes + acquisitions_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_acquisitions
    checked_metadata.union(updated_checked_metadata_from_acquisitions)
    # Computation Capabilities
    data_collections_from_computation_capabilities, updated_checked_metadata_from_computation_capabilities = get_data_collections_from_other_metadata(computation_capabilities_filtered_by_text_nodes + computation_capabilities_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_computation_capabilities
    checked_metadata.union(updated_checked_metadata_from_computation_capabilities)
    # Computations
    data_collections_from_computations, updated_checked_metadata_from_computations = get_data_collections_from_other_metadata(computations_filtered_by_text_nodes + computations_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_computations
    checked_metadata.union(updated_checked_metadata_from_computations)
    # Processes
    data_collections_from_processes, updated_checked_metadata_from_processes = get_data_collections_from_other_metadata(processes_filtered_by_text_nodes + processes_filtered_by_ontology_urls, checked_metadata=checked_metadata)
    data_collections_matching_query += data_collections_from_processes
    data_collections_matching_query += data_collections_filtered_by_text_nodes + data_collections_filtered_by_ontology_urls

    # Ensure there are no duplicate data collections
    data_collections_matching_query = {dc.id: dc for dc in data_collections_matching_query}.values()
    
    return data_collections_matching_query