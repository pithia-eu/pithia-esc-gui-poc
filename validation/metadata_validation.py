import traceback
import xmlschema
from django.urls import reverse_lazy
from requests import get
from lxml import etree
from rdflib import Graph, URIRef, RDF, SKOS
from common.helpers import get_acquisition_capabilities_referencing_instrument_operational_ids, get_mongodb_model_for_resource_type
from validation.exceptions import InvalidMetadataDocumentUrlException, InvalidRootElementNameForMetadataFileException, MetadataFileNameAndLocalIDNotMatchingException, UnregisteredOntologyTermException, UnregisteredMetadataDocumentException
from common.mongodb_models import CurrentInstrument
from validation.registration_validation import validate_xml_file_is_unique
from validation.update_validation import validate_xml_file_localid_matches_existing_resource_localid
from pathlib import Path
from bson import ObjectId

ORGANISATION_XML_ROOT_TAG_NAME = 'Organisation'
INDIVIDUAL_XML_ROOT_TAG_NAME = 'Individual'
PROJECT_XML_ROOT_TAG_NAME = 'Project'
PLATFORM_XML_ROOT_TAG_NAME = 'Platform'
INSTRUMENT_XML_ROOT_TAG_NAME = 'Instrument'
OPERATION_XML_ROOT_TAG_NAME = 'Operation'
ACQUISITION_CAPABILITY_XML_ROOT_TAG_NAME = 'AcquisitionCapabilities'
ACQUISITION_XML_ROOT_TAG_NAME = 'Acquisition'
COMPUTATION_CAPABILITY_XML_ROOT_TAG_NAME = 'ComputationCapabilities'
COMPUTATION_XML_ROOT_TAG_NAME = 'Computation'
PROCESS_XML_ROOT_TAG_NAME = 'CompositeProcess'
DATA_COLLECTION_XML_ROOT_TAG_NAME = 'DataCollection'

PITHIA_METADATA_SERVER_URL_BASE='https://metadata.pithia.eu/resources/2.2'
SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE='https://metadata.pithia.eu/ontology/2.2'

def parse_xml_file(xml_file):
    # Returns an ElementTree
    return etree.parse(xml_file)

def _create_validation_error_details_dict(err_type, err_message, extra_details):
    return {
        'type': str(err_type),
        'message': err_message,
        'extra_details': extra_details
    }

def get_schema_location_url_from_parsed_xml_file(xml_file_parsed):
    root = xml_file_parsed.getroot()
    urls_with_xsi_ns = root.xpath("//@*[local-name()='schemaLocation' and namespace-uri()='http://www.w3.org/2001/XMLSchema-instance']")
    urls_with_xsi_ns = urls_with_xsi_ns[0].split()
    schema_url = urls_with_xsi_ns[0]
    if len(urls_with_xsi_ns) > 1:
        schema_url = urls_with_xsi_ns[1]
    return schema_url

def _map_string_to_li_element(string):
    return f'<li>{string}</li>'

def _map_string_to_li_element_with_register_link(string):
    if string == 'collection':
        string == 'data_collection'
    elif string == 'acquisitionCapabilities':
        string = 'acquisition_capability'
    elif string == 'computationCapabilities':
        string = 'computation_capability'
    return f'<li><a href="{reverse_lazy(f"register:{string}")}" target="_blank" class="alert-link">{string.capitalize()} Metadata Registration</a></li>'

def _map_acquisition_capability_to_update_link(resource):
    return f'<li><a href="{reverse_lazy("update:acquisition_capability", args=[resource["_id"]])}" target="_blank" class="alert-link">Update {resource["name"]}</a></li>'

def _map_etree_element_to_text(element):
    return element.text

def _map_operational_mode_object_to_id_string(om):
    return om['InstrumentOperationalMode']['id']

def validate_xml_metadata_file(xml_file, expected_root_localname, mongodb_model=None, check_file_is_unregistered=False, check_xml_file_localid_matches_existing_resource_localid=False, existing_resource_id=''):
    validation_checklist = {
        'is_root_element_name_valid': False,
        'is_syntax_valid': False,
        'is_valid_against_schema': False,
        'is_file_name_matching_with_localid': False,
        'is_each_document_reference_valid': False,
        'is_each_ontology_reference_valid': False,
    }

    try:
        # Syntax validation
        xml_file_parsed = etree.parse(xml_file)
        validation_checklist['is_syntax_valid'] = True

        # Root element name validation
        root_element_name_validation_details = validate_xml_root_element_name_equals_expected_name(xml_file_parsed, expected_root_localname)
        validation_checklist['is_root_element_name_valid'] = root_element_name_validation_details['is_root_element_name_valid']
        if not validation_checklist['is_root_element_name_valid']:
            validation_checklist['error'] = _create_validation_error_details_dict(InvalidRootElementNameForMetadataFileException, f"Expected the metadata file to have a root element name of \"{root_element_name_validation_details['expected_root_element_name']}\", but got \"{root_element_name_validation_details['root_element_name']}\".", None)
            return validation_checklist

        # XSD Schema validation
        schema_url = get_schema_location_url_from_parsed_xml_file(xml_file_parsed)
        validate_xml_against_schema_at_url(xml_file, schema_url)
        validation_checklist['is_valid_against_schema'] = True

        # New registration validation
        if check_file_is_unregistered is True and mongodb_model is not None:
            validation_checklist['is_new_registration'] = False
            if not validate_xml_file_is_unique(mongodb_model, xml_file=xml_file):
                validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), 'This XML metadata file has been registered before.', None)
                return validation_checklist
            validation_checklist['is_new_registration'] = True

        # localID and namespace of file is the same as the resource to update's validation
        if check_xml_file_localid_matches_existing_resource_localid == True and mongodb_model is not None and existing_resource_id != '':
            validation_checklist['is_xml_file_localid_matching_with_existing_resource_localid'] = False
            if validate_xml_file_localid_matches_existing_resource_localid(mongodb_model, existing_resource_id, xml_file=xml_file) == False:
                validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), 'The localID and namespace must be matching with the resource being updated.', None)
                return validation_checklist
            validation_checklist['is_xml_file_localid_matching_with_existing_resource_localid'] = True

        # Operational mode IDs are changed and pre-existing IDs are referenced by any Acquisition Capabilities validation
        if check_xml_file_localid_matches_existing_resource_localid == True and existing_resource_id != '' and mongodb_model is not None and mongodb_model == CurrentInstrument:
            operational_mode_ids_of_updated_xml = list(map(_map_etree_element_to_text, xml_file_parsed.findall('.//{https://metadata.pithia.eu/schemas/2.2}id')))
            instrument_to_update = CurrentInstrument.find_one({
                                        '_id': ObjectId(existing_resource_id)
                                    }, {
                                        'operationalMode': True
                                    })
            operational_mode_ids_of_current_xml = list(map(_map_operational_mode_object_to_id_string, instrument_to_update['operationalMode']))
            operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
            if len(operational_mode_ids_intersection) < len(operational_mode_ids_of_current_xml):
                acquisition_capabilities = get_acquisition_capabilities_referencing_instrument_operational_ids(existing_resource_id)
                validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), 'Please remove references to this instrument\'s operational mode IDs from the acquisition capabilities listed below, before updating this instrument: <ul>%s</ul>' % ''.join(list(map(_map_acquisition_capability_to_update_link, acquisition_capabilities))), None)
                return validation_checklist

        # Matching file name and localID tag text validation
        localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text # There should be only one <localID> tag in the tree
        xml_file_name_with_no_extension = Path(xml_file.name).stem
        if localid_tag_text != xml_file_name_with_no_extension:
            validation_checklist['error'] = _create_validation_error_details_dict(MetadataFileNameAndLocalIDNotMatchingException, f"The file name \"{xml_file_name_with_no_extension}\" must match the localID of the metadata \"{localid_tag_text}\".", None)
            return validation_checklist
        validation_checklist['is_file_name_matching_with_localid'] = True

        # Relation validation (whether a resource the metadata file
        # is referencing exists in the database or not).
        unregistered_references = get_unregistered_references_from_xml(xml_file_parsed)
        unregistered_document_hrefs = unregistered_references['document_hrefs']
        unregistered_document_types = list(set(unregistered_references['document_types']))
        invalid_document_hrefs = list(set(unregistered_references['invalid_document_hrefs']))
        document_hrefs_with_invalid_op_mode_ids = list(set(unregistered_references['document_hrefs_with_invalid_op_mode_ids']))
        unregistered_ontology_term_hrefs = unregistered_references['ontology_term_hrefs']
        if len(invalid_document_hrefs) > 0:
            error_msg = 'Invalid document URLs: <ul>%s</ul><div class="mt-2">Your resource URL may reference an unsupported resource type, or may not follow the correct structure.</div>' % ''.join(list(map(_map_string_to_li_element, unregistered_document_hrefs)))
            error_msg = error_msg + '<div class="mt-2">Expected resource URL structure: <i>https://metadata.pithia.eu/resources/2.2/<b>resource type</b>/<b>namespace</b>/<b>localID</b></i></div>'
            validation_checklist['error'] = _create_validation_error_details_dict(type(InvalidMetadataDocumentUrlException()), error_msg, None)
            return validation_checklist
        if len(unregistered_document_hrefs) > 0:
            error_msg = 'Unregistered document URLs: <ul>%s</ul><b>Note:</b> If your URLs start with "<i>http://</i>" please change this to "<i>https://</i>".' % ''.join(list(map(_map_string_to_li_element, unregistered_document_hrefs)))
            error_msg = error_msg + '<div class="mt-2">Please use the following links to register the resources referenced in the submitted metadata file:</div>'
            error_msg = error_msg + '<ul class="mt-2">%s</ul>' % ''.join(list(map(_map_string_to_li_element_with_register_link, unregistered_document_types)))
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredMetadataDocumentException()), error_msg, None)
            return validation_checklist
        if len(document_hrefs_with_invalid_op_mode_ids) > 0:
            error_msg = 'The operational mode IDs in these document URLs are invalid: <ul>%s</ul>' % ''.join(list(map(_map_string_to_li_element, document_hrefs_with_invalid_op_mode_ids)))
            validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), error_msg, None)
            return validation_checklist
        validation_checklist['is_each_document_reference_valid'] = True
        if len(unregistered_ontology_term_hrefs) > 0:
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredOntologyTermException()), 'Invalid ontology term URLs: <ul>%s</ul><div class="mt-2">These ontology URLs may reference terms which have not yet been added to the PITHIA ontology, or no longer exist in the PITHIA ontology. Please also ensure URLs start with "<i>https://</i>" and not "<i>http://</i>".</div>' % ''.join(list(map(_map_string_to_li_element, unregistered_ontology_term_hrefs))), None)
            return validation_checklist
        validation_checklist['is_each_ontology_reference_valid'] = True
    except etree.XMLSyntaxError as err:
        print(traceback.format_exc())
        validation_checklist['error'] = _create_validation_error_details_dict(type(err), str(err), None)
    except etree.DocumentInvalid as err:
        print(traceback.format_exc())
        validation_checklist['error'] = _create_validation_error_details_dict(type(err), str(err), None)
    except BaseException as err:
        print(traceback.format_exc())
        validation_checklist['error'] = _create_validation_error_details_dict(type(err), str(err), None)
    

    return validation_checklist

def validate_xml_root_element_name_equals_expected_name(xml_file_parsed, expected_root_localname):
    root = xml_file_parsed.getroot()
    root_localname = etree.QName(root).localname # Get the root tag text without the namespace
    return {
        'root_element_name': f'{root_localname}',
        'expected_root_element_name': f'{expected_root_localname}',
        'is_root_element_name_valid': root_localname == expected_root_localname
    }

def is_xml_valid_against_schema_at_url(xml_file, schema_url):
    xml_file.seek(0)
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    return xml_schema.is_valid(xml_file.read())

def validate_xml_against_schema_at_url(xml_file, schema_url):
    xml_file.seek(0)
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    xml_schema.validate(xml_file.read())

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
    resource_urls = root.xpath(f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}')]/@*[local-name()='href' and namespace-uri()='http://www.w3.org/1999/xlink']", namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
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
        resource_mongodb_model = get_mongodb_model_for_resource_type(resource_type)
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
            resource_mongodb_model = get_mongodb_model_for_resource_type(resource_type)
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