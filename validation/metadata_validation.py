import re
import traceback
import xmlschema
from requests import get
from lxml import etree
from rdflib import Graph, URIRef, RDF, SKOS
from validation.exceptions import InvalidRootElementNameForMetadataFileException, MetadataFileNameAndLocalIDNotMatchingException, UnregisteredOntologyTermException, UnregisteredMetadataDocumentException
from common.mongodb_models import CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject
from validation.registration_validation import validate_xml_file_is_unique
from validation.update_validation import validate_xml_file_localid_matches_existing_resource_localid
ORGANISATION_XML_ROOT_TAG_NAME = 'Organisation'
INDIVIDUAL_XML_ROOT_TAG_NAME = 'Individual'
PROJECT_XML_ROOT_TAG_NAME = 'Project'
PLATFORM_XML_ROOT_TAG_NAME = 'Platform'
INSTRUMENT_XML_ROOT_TAG_NAME = 'Instrument'
OPERATION_XML_ROOT_TAG_NAME = 'Operation'
ACQUISITION_XML_ROOT_TAG_NAME = 'Acquisition'
COMPUTATION_XML_ROOT_TAG_NAME = 'Computation'
PROCESS_XML_ROOT_TAG_NAME = 'CompositeProcess'
DATA_COLLECTION_XML_ROOT_TAG_NAME = 'DataCollection'

def parse_xml_file(xml_file):
    # Returns an ElementTree
    return etree.parse(xml_file)

def _create_validation_error_details_dict(err_type, err_message, extra_details):
    return {
        'type': str(err_type),
        'message': err_message,
        'extra_details': extra_details
    }

def _map_string_to_li_element(string):
    return f'<li>{string}</li>'

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
        root = xml_file_parsed.getroot()
        urls_with_xsi_ns = root.xpath("//@*[local-name()='schemaLocation' and namespace-uri()='http://www.w3.org/2001/XMLSchema-instance']")
        urls_with_xsi_ns = urls_with_xsi_ns[0].split()
        schema_url = urls_with_xsi_ns[0]
        if len(urls_with_xsi_ns) > 1:
            schema_url = urls_with_xsi_ns[1]
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

        # Matching file name and localID tag text validation
        localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text # There should be only one <localID> tag in the tree
        xml_file_name_with_no_extension = re.sub('.xml$' , '', xml_file.name)
        if localid_tag_text != xml_file_name_with_no_extension:
            validation_checklist['error'] = _create_validation_error_details_dict(MetadataFileNameAndLocalIDNotMatchingException, f"The file name \"{xml_file_name_with_no_extension}\" must match the localID of the metadata \"{localid_tag_text}\".", None)
            return validation_checklist

        # Relation validaiton (whether a resource the metadata file
        # is referencing exists in the database or not).
        unregistered_references = get_unregistered_references_from_xml(xml_file_parsed)
        unregistered_document_hrefs = unregistered_references['document_hrefs']
        unregistered_document_types = unregistered_references['document_types']
        unregistered_ontology_term_hrefs = unregistered_references['ontology_term_hrefs']
        if len(unregistered_document_hrefs) > 0:
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredMetadataDocumentException()), 'Invalid document URLs: %s.' % ', '.join(unregistered_document_hrefs), {
                'unregistered_document_types': unregistered_document_types
            })
            return validation_checklist
        validation_checklist['is_each_document_reference_valid'] = True
        if len(unregistered_ontology_term_hrefs) > 0:
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredOntologyTermException()), 'Invalid ontology term URLs: <ul>%s</ul><b>Note:</b> Please ensure all URLs work before uploading and start with "<i>https://</i>" instead of "<i>http://</i>".' % ''.join(list(map(_map_string_to_li_element, unregistered_ontology_term_hrefs))), None)
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

def get_mongodb_model_for_resource_type(resource_type):
    if resource_type == 'organisation':
        return CurrentOrganisation
    elif resource_type == 'individual':
        return CurrentIndividual
    elif resource_type == 'project':
        return CurrentProject
    elif resource_type == 'platform':
        return CurrentPlatform
    elif resource_type == 'operation':
        return CurrentOperation
    elif resource_type == 'instrument':
        return CurrentInstrument
    elif resource_type == 'acquisition':
        return CurrentAcquisition
    elif resource_type == 'computation':
        return CurrentComputation
    elif resource_type == 'process':
        return CurrentProcess
    elif resource_type == 'data-collection':
        return CurrentDataCollection
    return 'unknown'

def get_resource_from_xlink_href_components(resource_mongodb_model, localID, namespace, version):
    find_dictionary = {
        'identifier.PITHIA_Identifier.localID': localID,
        'identifier.PITHIA_Identifier.namespace': namespace,
    }
    if version:
        find_dictionary['identifier.PITHIA_Identifier.version'] = version
    return resource_mongodb_model.find_one(find_dictionary)

def split_xlink_href(href):
    return href.split('/')

def get_unregistered_references_from_xml(xml_file_parsed):
    unregistered_references = {
        'document_hrefs': set(),
        'document_types': set(),
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
            href_components  = split_xlink_href(href)
            ontology_component = href_components[-2]
            ontology_term_id = href_components[-1]
            is_valid_ontology_term = validate_ontology_term_url(href)
            if is_valid_ontology_term == False:
                unregistered_references['ontology_term_hrefs'].add(href)

        if 'resources' in href:
            resource_type = href_components[-3]
            namespace = href_components[-2]
            localID = href_components[-1]
            version = None
            if len(href_components) > 3:
                version = href_components[3]
            resource_mongodb_model = get_mongodb_model_for_resource_type(resource_type)
            if resource_mongodb_model == 'unknown':
                continue
            referenced_resource = get_resource_from_xlink_href_components(resource_mongodb_model, localID, namespace, version)
            if referenced_resource == None:
                unregistered_references['document_hrefs'].add(href)
                unregistered_references['document_types'].add(resource_type)
    
    for key in unregistered_references:
        unregistered_references[key] = list(unregistered_references[key])
    return unregistered_references