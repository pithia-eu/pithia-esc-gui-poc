import traceback
import xmlschema
from django.urls import reverse_lazy
from requests import get
from lxml import etree
from common.helpers import get_acquisition_capability_sets_referencing_instrument_operational_ids
from validation.errors import (
    InvalidResourceURL,
    InvalidRootElementName,
    FileNameNotMatchingWithLocalID,
    UnregisteredOntologyTermReferenced,
    UnregisteredResourceReferenced
)
from common.mongodb_models import CurrentInstrument
from .url_validation import get_invalid_ontology_urls_from_parsed_xml, get_invalid_resource_urls_from_parsed_xml, get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml
from pathlib import Path
from bson import ObjectId
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from .helpers import (
    _create_validation_error_details_dict,
    _map_string_to_li_element,
    _map_string_to_li_element_with_register_link,
    _map_etree_element_to_text,
    _map_acquisition_capability_to_update_link,
    _map_operational_mode_object_to_id_string,
)

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

# Syntax validation
def parse_xml_file(xml_file):
    """
    Parses an XML file, which also verifies whether the file's syntax is valid or not.
    """
    return etree.parse(xml_file)

# Root element name validation
def validate_xml_root_element_name_equals_expected_name(xml_file, expected_root_localname):
    """
    Compares an XML file's root element name against a given expected root element name,
    then returns a dict containing these details along with whether the actual root
    element name and the expected root element name were matching.
    """
    xml_file_parsed = parse_xml_file(xml_file)
    root = xml_file_parsed.getroot()
    root_localname = etree.QName(root).localname # Get the root tag text without the namespace
    return {
        'root_element_name': f'{root_localname}',
        'expected_root_element_name': f'{expected_root_localname}',
        'is_root_element_name_valid': root_localname == expected_root_localname
    }

# XSD Schema validation
def get_schema_location_url_from_parsed_xml_file(xml_file_parsed):
    """
    Fetches the schema at the URL specified within the parsed xml file
    under the xsi:schemaLocation attribute.
    """
    root = xml_file_parsed.getroot()
    urls_with_xsi_ns = root.xpath("//@*[local-name()='schemaLocation' and namespace-uri()='http://www.w3.org/2001/XMLSchema-instance']")
    urls_with_xsi_ns = urls_with_xsi_ns[0].split()
    schema_url = urls_with_xsi_ns[0]
    if len(urls_with_xsi_ns) > 1:
        schema_url = urls_with_xsi_ns[1]
    return schema_url

def is_xml_valid_against_schema_at_url(xml_file, schema_url):
    """
    Returns whether an XML file is valid against a schema
    at a URL.
    """
    xml_file.seek(0)
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    return xml_schema.is_valid(xml_file.read())

def validate_xml_against_schema_at_url(xml_file, schema_url):
    """
    Validates the XML file against a schema hosted at a URL.
    """
    xml_file.seek(0)
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    xml_schema.validate(xml_file.read())

# Matching file name and localID tag text validation
def is_xml_file_name_matching_with_localid(xml_file):
    """
    Returns whether the name for an XML file matches
    with the innerText of its <localID> element.
    """
    xml_file_parsed = parse_xml_file(xml_file)
    localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text # There should be only one <localID> tag in the tree
    xml_file_name_with_no_extension = Path(xml_file.name).stem
    return localid_tag_text == xml_file_name_with_no_extension

# Registration validation
def is_xml_file_already_registered(mongodb_model, xml_file=None, converted_xml_file=None):
    """
    Returns whether there is pre-registered metadata with the same localID and namespace
    as the metadata that the user would like to register.
    """
    if converted_xml_file is None:
        converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
        # Remove the top-level tag - this will be just <Organisation>, for example
        converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
    xml_file_pithia_identifier = converted_xml_file['identifier']['PITHIA_Identifier']
    num_times_uploaded_before = mongodb_model.count_documents({
        'identifier.PITHIA_Identifier.localID': xml_file_pithia_identifier['localID'],
        'identifier.PITHIA_Identifier.namespace': xml_file_pithia_identifier['namespace'],
    })
    return num_times_uploaded_before == 0

# Update validation
def is_updated_xml_file_localid_matching_with_current_resource_localid(
    xml_file,
    resource_id,
    mongodb_model,
):
    """
    Returns whether the localID and namespace of the updated metadata
    is the same as the current version of the metadata.
    """
    if converted_xml_file is None:
        converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
        # Remove the top-level tag - this will be just <Organisation>, for example
        converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
    xml_file_pithia_identifier = converted_xml_file['identifier']['PITHIA_Identifier']
    resource_to_update = mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_to_update_pithia_identifier = resource_to_update['identifier']['PITHIA_Identifier']
    return xml_file_pithia_identifier['localID'] == resource_to_update_pithia_identifier['localID'] and xml_file_pithia_identifier['namespace'] == resource_to_update_pithia_identifier['namespace']

# Operational mode ID modification check
def is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(xml_file, current_instrument_id):
    xml_file_parsed = parse_xml_file(xml_file)
    operational_mode_ids_of_updated_xml = list(
        map(
            _map_etree_element_to_text,
            xml_file_parsed.findall('.//{https://metadata.pithia.eu/schemas/2.2}id')
        )
    )
    instrument_to_update = CurrentInstrument.find_one(
        {
            '_id': ObjectId(current_instrument_id)
        },
        {
            'operationalMode': True
        }
    )
    operational_mode_ids_of_current_xml = list(
        map(_map_operational_mode_object_to_id_string, instrument_to_update['operationalMode'])
    )
    operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
    return len(operational_mode_ids_intersection) == len(operational_mode_ids_of_current_xml)

def validate_and_get_validation_details_of_xml_file(
    xml_file,
    expected_root_localname,
    mongodb_model=None,
    check_file_is_unregistered=False,
    check_xml_file_localid_matches_existing_resource_localid=False,
    existing_resource_id=''
):
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
        xml_file_parsed = parse_xml_file(xml_file)

        # Root element name validation
        root_element_name_validation_details = validate_xml_root_element_name_equals_expected_name(xml_file_parsed, expected_root_localname)
        if not validation_checklist['is_root_element_name_valid']:
            validation_checklist['error'] = _create_validation_error_details_dict(InvalidRootElementName, f"Expected the metadata file to have a root element name of \"{root_element_name_validation_details['expected_root_element_name']}\", but got \"{root_element_name_validation_details['root_element_name']}\".", None)
            return validation_checklist

        # XSD Schema validation
        schema_url = get_schema_location_url_from_parsed_xml_file(xml_file_parsed)
        validate_xml_against_schema_at_url(xml_file, schema_url)
        validation_checklist['is_valid_against_schema'] = True

        # New registration validation
        if (check_file_is_unregistered is True and
            mongodb_model is not None):
            validation_checklist['is_new_registration'] = False
            if not is_xml_file_already_registered(mongodb_model, xml_file=xml_file):
                validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), 'This XML metadata file has been registered before.', None)
                return validation_checklist
            validation_checklist['is_new_registration'] = True

        # localID and namespace of file is the same as the resource to update's validation
        if check_xml_file_localid_matches_existing_resource_localid == True and mongodb_model is not None and existing_resource_id != '':
            validation_checklist['is_xml_file_localid_matching_with_existing_resource_localid'] = False
            if is_updated_xml_file_localid_matching_with_current_resource_localid(xml_file, existing_resource_id, mongodb_model) == False:
                validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), 'The localID and namespace must be matching with the resource being updated.', None)
                return validation_checklist
            validation_checklist['is_xml_file_localid_matching_with_existing_resource_localid'] = True

        # Operational mode IDs are changed and pre-existing IDs are referenced by any Acquisition Capabilities validation
        if (check_xml_file_localid_matches_existing_resource_localid == True and
            existing_resource_id != '' and
            mongodb_model is not None and
            mongodb_model == CurrentInstrument):
            operational_mode_ids_of_updated_xml = list(map(_map_etree_element_to_text, xml_file_parsed.findall('.//{https://metadata.pithia.eu/schemas/2.2}id')))
            instrument_to_update = CurrentInstrument.find_one({
                                        '_id': ObjectId(existing_resource_id)
                                    }, {
                                        'operationalMode': True
                                    })
            operational_mode_ids_of_current_xml = list(map(_map_operational_mode_object_to_id_string, instrument_to_update['operationalMode']))
            operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
            if len(operational_mode_ids_intersection) < len(operational_mode_ids_of_current_xml):
                acquisition_capability_sets = get_acquisition_capability_sets_referencing_instrument_operational_ids(existing_resource_id)
                validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), 'Please remove references to this instrument\'s operational mode IDs from the acquisition capabilities listed below, before updating this instrument: <ul>%s</ul>' % ''.join(list(map(_map_acquisition_capability_to_update_link, acquisition_capability_sets))), None)
                return validation_checklist

        # Matching file name and localID tag text validation
        localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text # There should be only one <localID> tag in the tree
        xml_file_name_with_no_extension = Path(xml_file.name).stem
        if localid_tag_text != xml_file_name_with_no_extension:
            validation_checklist['error'] = _create_validation_error_details_dict(FileNameNotMatchingWithLocalID, f"The file name \"{xml_file_name_with_no_extension}\" must match the localID of the metadata \"{localid_tag_text}\".", None)
            return validation_checklist
        validation_checklist['is_file_name_matching_with_localid'] = True

        # Relation validation (whether a resource the metadata file
        # is referencing exists in the database or not).
        
        # Resource URL validation
        invalid_resource_urls = get_invalid_resource_urls_from_parsed_xml(xml_file_parsed)
        invalid_resource_urls_with_op_mode_ids = get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml(xml_file_parsed)
        resource_urls_with_incorrect_structure = [*invalid_resource_urls['urls_with_incorrect_structure'], *invalid_resource_urls_with_op_mode_ids['urls_with_incorrect_structure']]
        resource_urls_pointing_to_unregistered_resources = [*invalid_resource_urls['urls_pointing_to_unregistered_resources'], *invalid_resource_urls_with_op_mode_ids['urls_pointing_to_unregistered_resources']]
        types_of_missing_resources = [*invalid_resource_urls['types_of_missing_resources'], *invalid_resource_urls_with_op_mode_ids['types_of_missing_resources']]
        resource_urls_pointing_to_registered_resources_with_missing_op_modes = invalid_resource_urls_with_op_mode_ids['urls_pointing_to_registered_resources_with_missing_op_modes']
        
        if len(resource_urls_with_incorrect_structure) > 0:
            error_msg = 'Invalid document URLs: <ul>%s</ul><div class="mt-2">Your resource URL may reference an unsupported resource type, or may not follow the correct structure.</div>' % ''.join(list(map(_map_string_to_li_element, resource_urls_with_incorrect_structure)))
            error_msg = error_msg + '<div class="mt-2">Expected resource URL structure: <i>https://metadata.pithia.eu/resources/2.2/<b>resource type</b>/<b>namespace</b>/<b>localID</b></i></div>'
            validation_checklist['error'] = _create_validation_error_details_dict(type(InvalidResourceURL()), error_msg, None)
            return validation_checklist

        if len(resource_urls_pointing_to_unregistered_resources) > 0:
            error_msg = 'Unregistered document URLs: <ul>%s</ul><b>Note:</b> If your URLs start with "<i>http://</i>" please change this to "<i>https://</i>".' % ''.join(list(map(_map_string_to_li_element, resource_urls_pointing_to_unregistered_resources)))
            error_msg = error_msg + '<div class="mt-2">Please use the following links to register the resources referenced in the submitted metadata file:</div>'
            error_msg = error_msg + '<ul class="mt-2">%s</ul>' % ''.join(list(map(_map_string_to_li_element_with_register_link, types_of_missing_resources)))
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredResourceReferenced()), error_msg, None)
            return validation_checklist

        if len(resource_urls_pointing_to_registered_resources_with_missing_op_modes) > 0:
            error_msg = 'The operational mode IDs in these document URLs are invalid: <ul>%s</ul>' % ''.join(list(map(_map_string_to_li_element, resource_urls_pointing_to_registered_resources_with_missing_op_modes)))
            validation_checklist['error'] = _create_validation_error_details_dict(type(BaseException()), error_msg, None)
            return validation_checklist
        validation_checklist['is_each_document_reference_valid'] = True

        # Ontology URL validation
        invalid_ontology_urls = get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed)
        if len(invalid_ontology_urls) > 0:
            validation_checklist['error'] = _create_validation_error_details_dict(type(UnregisteredOntologyTermReferenced()), 'Invalid ontology term URLs: <ul>%s</ul><div class="mt-2">These ontology URLs may reference terms which have not yet been added to the PITHIA ontology, or no longer exist in the PITHIA ontology. Please also ensure URLs start with "<i>https://</i>" and not "<i>http://</i>".</div>' % ''.join(list(map(_map_string_to_li_element, invalid_ontology_urls))), None)
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