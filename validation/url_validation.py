from requests import get
from rdflib import Graph, URIRef, RDF, SKOS
from common.helpers import get_mongodb_model_by_resource_type_from_resource_url
from common.mongodb_models import CurrentInstrument


PITHIA_METADATA_SERVER_URL_BASE='https://metadata.pithia.eu/resources/2.2'
SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE='https://metadata.pithia.eu/ontology/2.2'

def validate_ontology_term_url(ontology_term_url):
    response = get(ontology_term_url) # e.g. http://ontology.espas-fp7.eu/relatedPartyRole/Operator
    if response.status_code == 404:
        return False
    if response.ok:
        response_text = response.text
        g = Graph()
        g.parse(data=response_text, format='application/rdf+xml')
        ontology_term = URIRef(ontology_term_url)
        return (ontology_term, RDF['type'], SKOS['Concept']) in g
    response.raise_for_status()
    return False

def get_resource_from_xlink_href_value_components(resource_mongodb_model, localID, namespace):
    find_dictionary = {
        'identifier.PITHIA_Identifier.localID': localID,
        'identifier.PITHIA_Identifier.namespace': namespace,
    }
    return resource_mongodb_model.find_one(find_dictionary)

def get_instrument_by_operational_mode_id(operational_mode_id):
    return CurrentInstrument.find_one({
        'operationalMode.InstrumentOperationalMode.id': operational_mode_id
    })

def check_resource_url_is_valid_and_get_resource_url_identifying_components(resource_url):
    resource_url_split = resource_url.split('/')
    resource_type = resource_url_split[-3]
    namespace = resource_url_split[-2]
    localID = resource_url_split[-1]
    


def split_xlink_href_value_by_hashtag(href):
    return href.split('#')

def split_xlink_href_value_by_forward_slash(href):
    return href.split('/')

def get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed):
    invalid_urls = []
    root = xml_file_parsed.getroot()
    ontology_urls = root.xpath(f"//*[contains(@xlink:href, '{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE}')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for url in ontology_urls:
        is_valid_ontology_term = validate_ontology_term_url(url)
        if is_valid_ontology_term == False:
            invalid_urls.append(url)
    return invalid_urls

def get_invalid_resource_urls_from_parsed_xml(xml_file_parsed):
    invalid_urls = []
    root = xml_file_parsed.getroot()
    resource_urls = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and not(contains(@xlink:href, '#'))]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for url in resource_urls:
        url_components  = split_xlink_href_value_by_forward_slash(url)
        resource_type = url_components[-3]
        namespace = url_components[-2]
        localID = url_components[-1]

        # If resource_mongodb_model is unknown, the resource type is not yet supported
        # or some parts of the URL path are in the wrong order:
        # e.g. https://metadata.pithia.eu/resources/2.2/pithia/organisation/Organisation_LGDC (wrong)
        # instead of https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_LGDC (correct)
        resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type)
        if resource_mongodb_model == 'unknown':
            invalid_urls.append((url, 'The URL was formatted incorrectly.'))

        referenced_resource = None
        referenced_resource = get_resource_from_xlink_href_value_components(resource_mongodb_model, localID, namespace)
        if referenced_resource == None:
            invalid_urls.append((url, 'The resource this URL is referencing was not found.', resource_type))
    return invalid_urls

def get_unregistered_resources_and_unregistered_op_mode_urls(xml_file_parsed):
    invalid_urls = []
    root = xml_file_parsed.getroot()
    resource_urls = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and contains(@xlink:href, '#')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
    for url in resource_urls:
        # Storing url in a variable as it may get changed when checking for
        # hashtags.
        url_copy = url
        operational_mode_id = None
        url_split_by_hashtag = split_xlink_href_value_by_hashtag(url_copy)
        if len(url_split_by_hashtag) > 1:
            operational_mode_id = url_split_by_hashtag[-1]
            url_copy = url_split_by_hashtag[0]
        url_components  = split_xlink_href_value_by_forward_slash(url_copy)
        resource_type = url_components[-3]
        namespace = url_components[-2]
        localID = url_components[-1]

        # If resource_mongodb_model is unknown, the resource type is not yet supported
        # or some parts of the URL path are in the wrong order:
        # e.g. https://metadata.pithia.eu/resources/2.2/pithia/organisation/Organisation_LGDC (wrong)
        # instead of https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_LGDC (correct)
        resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type)
        if resource_mongodb_model == 'unknown':
            invalid_urls.append((url, 'The URL was formatted incorrectly.'))

        referenced_resource = None
        referenced_resource = get_resource_from_xlink_href_value_components(resource_mongodb_model, localID, namespace)
        if referenced_resource == None:
            invalid_urls.append((url, 'The resource this URL is referencing was not found.', resource_type))
            continue
        
        if operational_mode_id != None:
            # The '#' at the end of some resource URLs should only link to Instruments
            instrument_retrieved_by_operational_mode_id = get_instrument_by_operational_mode_id(operational_mode_id)
            if instrument_retrieved_by_operational_mode_id == None:
                hashtag_index = url.index('#')
                invalid_url = url[:hashtag_index] + '<b>' + url[hashtag_index:] + '</b>'
                invalid_urls.append((invalid_url, 'The operational mode this URL is referencing was not found.'))
    return invalid_urls

def get_unregistered_references_from_xml(xml_file_parsed):
    unregistered_references = {
        'document_hrefs': set(),
        'document_types': set(),
        'invalid_document_hrefs': set(),
        'document_hrefs_with_invalid_op_mode_ids': set(),
        'ontology_term_hrefs': set(),
    }
    parent = xml_file_parsed.getroot()
    hrefs = parent.xpath("//@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']")
    if not len(hrefs) > 0:
        for key in unregistered_references:
            unregistered_references[key] = list(unregistered_references[key])
        return unregistered_references
    for href in hrefs:
        if 'ontology' in href:
            href_components  = split_xlink_href_value_by_forward_slash(href)
            ontology_component = href_components[-2]
            ontology_term_id = href_components[-1]
            is_valid_ontology_term = validate_ontology_term_url(href)
            if is_valid_ontology_term == False:
                unregistered_references['ontology_term_hrefs'].add(href)

        if 'resources' in href:
            # Storing href in a variable as it may get changed when checking for
            # hashtags.
            href_to_check = href
            href_split_by_hashtag = split_xlink_href_value_by_hashtag(href_to_check)
            operational_mode_id = None
            if len(href_split_by_hashtag) > 1:
                operational_mode_id = href_split_by_hashtag[-1]
                href_to_check = href_split_by_hashtag[0]
            href_components  = split_xlink_href_value_by_forward_slash(href_to_check)
            resource_type = href_components[-3]
            namespace = href_components[-2]
            localID = href_components[-1]
            resource_mongodb_model = get_mongodb_model_by_resource_type_from_resource_url(resource_type)
            referenced_resource = None
            # If resource_mongodb_model is unknown, the resource type is not yet supported
            # or some parts of the URL path are in the wrong order:
            # e.g. https://metadata.pithia.eu/resources/2.2/pithia/organisation/Organisation_LGDC (wrong)
            # instead of https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_LGDC (correct)
            if resource_mongodb_model != 'unknown':
                referenced_resource = get_resource_from_xlink_href_value_components(resource_mongodb_model, localID, namespace)
            else:
                unregistered_references['invalid_document_hrefs'].add(href)

            if referenced_resource == None:
                unregistered_references['document_hrefs'].add(href)
                unregistered_references['document_types'].add(resource_type)
            else:
                if operational_mode_id != None:
                    # The '#' at the end of some resource URLs should only link to Instruments
                    instrument_retrieved_by_operational_mode_id = get_instrument_by_operational_mode_id(operational_mode_id)
                    if instrument_retrieved_by_operational_mode_id == None:
                        hashtag_index = href.index('#')
                        invalid_href = href[:hashtag_index] + '<b>' + href[hashtag_index:] + '</b>'
                        unregistered_references['document_hrefs_with_invalid_op_mode_ids'].add(invalid_href)
    
    for key in unregistered_references:
        unregistered_references[key] = list(unregistered_references[key])
    return unregistered_references