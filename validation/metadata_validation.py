import xmlschema
from requests import get
from lxml import etree
from common.helpers import get_acquisition_capability_sets_referencing_instrument_operational_ids
from validation.errors import (
    InvalidRootElementName,
    FileNameNotMatchingWithLocalID,
    FileRegisteredBefore,
)
from common.mongodb_models import (
    CurrentCatalogueDataSubset,
    CurrentInstrument,
)
from .url_validation import (
    get_invalid_ontology_urls_from_parsed_xml,
    get_invalid_resource_urls_from_parsed_xml,
    get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml
)
from pathlib import Path
from bson import ObjectId
from .helpers import (
    create_validation_details_error,
    _map_string_to_li_element,
    _create_li_element_with_register_link_from_resource_type_from_resource_url,
    _map_etree_element_to_text,
    _map_acquisition_capability_to_update_link,
    _map_operational_mode_object_to_id_string,
)
from xmlschema.exceptions import XMLSchemaException

import logging

logger = logging.getLogger(__name__)

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
CATALOGUE_XML_ROOT_TAG_NAME = 'Catalogue'
CATALOGUE_ENTRY_XML_ROOT_TAG_NAME = 'CatalogueEntry'
CATALOGUE_DATA_SUBSET_XML_ROOT_TAG_NAME = 'DataSubset'

# Syntax validation
def validate_and_parse_xml_file(xml_file):
    """
    Parses an XML file, which also verifies whether the file's syntax is valid or not.
    """
    xml_file.seek(0)
    return etree.parse(xml_file)

# Root element name validation
def validate_xml_root_element_name_equals_expected_name(xml_file, expected_root_localname):
    """
    Compares an XML file's root element name against a given expected root element name.
    """
    xml_file_parsed = validate_and_parse_xml_file(xml_file)
    root = xml_file_parsed.getroot()
    root_localname = etree.QName(root).localname # Get the root tag text without the namespace
    if root_localname != expected_root_localname:
        raise InvalidRootElementName(
            'The metadata file submitted is for the wrong resource type.',
            f'Expected the metadata file to have a root element name of "{expected_root_localname}", but got "{root_localname}".'
        )

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

def validate_xml_against_schema_at_url(xml_file, schema_url):
    """
    Validates the XML file against a schema hosted at a URL.
    """
    xml_file.seek(0)
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    xml_schema.validate(xml_file.read())

def validate_xml_with_doi_against_schema_at_url(xml_file, schema_url):
    """
    Validates the XML file with a DOI element against a schema hosted at a URL.
    """
    valid_doi_name = '10.000/000'
    xml_file.seek(0)
    xml_file_string = xml_file.read()
    xml_file_string_parsed = etree.fromstring(xml_file_string)
    doi_name_element = xml_file_string_parsed.find('.//{http://www.doi.org/2010/DOISchema}referentDoiName')
    doi_registration_agency_name_element = xml_file_string_parsed.find('.//{http://www.doi.org/2010/DOISchema}registrationAgencyDoiName')
    if doi_name_element is not None:
        doi_name_element.text = valid_doi_name
    if doi_registration_agency_name_element is not None:
        doi_registration_agency_name_element.text = valid_doi_name
    schema_response = get(schema_url)
    xml_schema = xmlschema.XMLSchema(schema_response.text.encode())
    xml_schema.validate(etree.tostring(xml_file_string_parsed))

def validate_xml_against_own_schema(xml_file):
    """
    Validates the XML file against its own schema by
    fetching the schema from the URL specified at the
    xsi:schemaLocation attribute within the XML file.
    """
    xml_file_parsed = validate_and_parse_xml_file(xml_file)
    schema_url = get_schema_location_url_from_parsed_xml_file(xml_file_parsed)
    validate_xml_against_schema_at_url(xml_file, schema_url)

# Matching file name and localID tag text validation
def validate_xml_file_name(xml_file):
    """
    Returns whether the name for an XML file matches
    with the innerText of its <localID> element.
    """
    xml_file_parsed = validate_and_parse_xml_file(xml_file)
    # There should be only one <localID> tag in the tree
    localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text
    xml_file_name_with_no_extension = Path(xml_file.name).stem
    if localid_tag_text != xml_file_name_with_no_extension:
        raise FileNameNotMatchingWithLocalID(
            'File name not matching with localID',
            f'The file name \"{xml_file_name_with_no_extension}\" must match the localID of the metadata \"{localid_tag_text}\".'
        )

# Registration validation
def validate_xml_file_is_unregistered(mongodb_model, xml_file):
    """
    Returns whether there is pre-registered metadata with the same localID and namespace
    as the metadata that the user would like to register.
    """
    xml_file_parsed = validate_and_parse_xml_file(xml_file)
    localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text
    namespace_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}namespace').text
    num_times_uploaded_before = mongodb_model.count_documents({
        'identifier.PITHIA_Identifier.localID': localid_tag_text,
        'identifier.PITHIA_Identifier.namespace': namespace_tag_text,
    })
    if num_times_uploaded_before > 0:
        raise FileRegisteredBefore(
            'This XML metadata file has been registered before.',
            f'Metadata sharing the same localID of "{localid_tag_text}" has already been registered with the e-Science Centre.',
        )

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
    xml_file_parsed = validate_and_parse_xml_file(xml_file)
    localid_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text
    namespace_tag_text = xml_file_parsed.find('.//{https://metadata.pithia.eu/schemas/2.2}namespace').text
    resource_to_update = mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_to_update_pithia_identifier = resource_to_update['identifier']['PITHIA_Identifier']
    return all([
        localid_tag_text == resource_to_update_pithia_identifier['localID'],
        namespace_tag_text == resource_to_update_pithia_identifier['namespace']
    ])

# Operational mode ID modification check
def is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(xml_file, current_instrument_id, mongodb_model=CurrentInstrument):
    xml_file_parsed = validate_and_parse_xml_file(xml_file)
    # Operational mode IDs are the only values enclosed in <id></id> tags
    operational_mode_ids_of_updated_xml = list(
        map(
            _map_etree_element_to_text,
            xml_file_parsed.findall('.//{https://metadata.pithia.eu/schemas/2.2}id')
        )
    )
    instrument_to_update = mongodb_model.find_one(
        {
            '_id': ObjectId(current_instrument_id)
        },
        {
            'operationalMode': True
        }
    )
    operational_mode_ids_of_current_xml = []
    if 'operationalMode' in instrument_to_update:
        operational_mode_ids_of_current_xml = list(
            map(_map_operational_mode_object_to_id_string, instrument_to_update['operationalMode'])
        )
    operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
    return len(operational_mode_ids_intersection) == len(operational_mode_ids_of_current_xml)

def validate_and_get_validation_details_of_xml_file(
    xml_file,
    expected_root_localname,
    mongodb_model,
    check_file_is_unregistered=False,
    check_xml_file_localid_matches_existing_resource_localid=False,
    existing_resource_id='',
    spoof_doi=False
):
    """
    Validates an XML metadata file for:
    * Syntax-correctness
    * Root element name-correctness
    * XSD-compliance
    * Matching file name (without the extension)
      with the metadata's localID
    * Situational checks
    * Corresponding e-Science Centre registrations
      to the metadata server URLs that the submitted
      file uses.
    * Corresponding ontology terms to the ontology
      server URLs that the file uses.
    
    Situational checks:
    * If registering the file, a check is done on
      whether the file has been registered before.

    * If submitting the file for an update, a check
      is done that the submitted file's namespace
      and localID is the same as the file registered
      with the e-Science Centre.
    """
    validation_details = {
        'error': None,
        'warnings': [],
    }

    try:
        # Syntax validation
        xml_file_parsed = validate_and_parse_xml_file(xml_file)

        # Root element name validation
        validate_xml_root_element_name_equals_expected_name(xml_file, expected_root_localname)

        # XSD Schema validation
        schema_url = get_schema_location_url_from_parsed_xml_file(xml_file_parsed)
        if mongodb_model == CurrentCatalogueDataSubset:
            validate_xml_with_doi_against_schema_at_url(xml_file, schema_url)
        else:
            validate_xml_against_schema_at_url(xml_file, schema_url)

        # Matching file name and localID tag text validation
        validate_xml_file_name(xml_file)

        # New registration validation
        if (check_file_is_unregistered is True):
            validate_xml_file_is_unregistered(mongodb_model, xml_file)

        # localID and namespace of file is the same as the resource to update's validation
        if (check_xml_file_localid_matches_existing_resource_localid == True and
            existing_resource_id != ''):
            if is_updated_xml_file_localid_matching_with_current_resource_localid(xml_file, existing_resource_id, mongodb_model) == False:
                validation_details['error'] = create_validation_details_error(
                    message='Invalid localID and namespace',
                    details='The localID and namespace must be matching with the current version of the metadata.',
                )
                return validation_details

        # Operational mode IDs are changed and pre-existing IDs are referenced by any Acquisition Capabilities validation
        if (check_xml_file_localid_matches_existing_resource_localid == True and
            existing_resource_id != '' and
            mongodb_model == CurrentInstrument):
            if not is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
                xml_file,
                existing_resource_id,
            ):
                acquisition_capability_sets = get_acquisition_capability_sets_referencing_instrument_operational_ids(existing_resource_id)
                validation_details['warnings'].append(create_validation_details_error(
                    message='Any references to this instrument\'s operational mode IDs must will be invalidated after this update.',
                    details='After updating this instrument, please update any references to this instrument\'s operational mode IDs in the acquisition capabilities listed below: <ul>%s</ul>' % ''.join(list(map(_map_acquisition_capability_to_update_link, acquisition_capability_sets)))
                ))

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
            validation_details['error'] = create_validation_details_error(
                message='One or multiple resource URLs specified via the xlink:href attribute are invalid.',
                details=error_msg
            )
            return validation_details

        if len(resource_urls_pointing_to_unregistered_resources) > 0:
            error_msg = 'Unregistered document URLs: <ul>%s</ul><b>Note:</b> If your URLs start with "<i>http://</i>" please change this to "<i>https://</i>".' % ''.join(list(map(_map_string_to_li_element, resource_urls_pointing_to_unregistered_resources)))
            error_msg = error_msg + '<div class="mt-2">Please use the following links to register the resources referenced in the submitted metadata file:</div>'
            error_msg = error_msg + '<ul class="mt-2">%s</ul>' % ''.join(list(map(_create_li_element_with_register_link_from_resource_type_from_resource_url, types_of_missing_resources)))
            validation_details['error'] = create_validation_details_error(
                message='One or multiple resources referenced by the xlink:href attribute have not been registered with the e-Science Centre.',
                details=error_msg
            )
            return validation_details

        if len(resource_urls_pointing_to_registered_resources_with_missing_op_modes) > 0:
            error_msg = 'Invalid operational mode references: <ul>%s</ul>' % ''.join(list(map(_map_string_to_li_element, resource_urls_pointing_to_registered_resources_with_missing_op_modes)))
            validation_details['error'] = create_validation_details_error(
                message='One or multiple referenced operational modes are invalid.',
                details=error_msg
            )
            return validation_details

        # Ontology URL validation
        invalid_ontology_urls = get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed)
        if len(invalid_ontology_urls) > 0:
            error_msg = 'Invalid ontology term URLs: <ul>%s</ul><div class="mt-2">These ontology URLs may reference terms which have not yet been added to the PITHIA ontology, or no longer exist in the PITHIA ontology. Please also ensure URLs start with "<i>https://</i>" and not "<i>http://</i>".</div>' % ''.join(list(map(_map_string_to_li_element, invalid_ontology_urls)))
            validation_details['error'] = create_validation_details_error(
                message='One or multiple ontology terms referenced by the xlink:href attribute are not valid PITHIA ontology terms.',
                details=error_msg
            )

    except etree.XMLSyntaxError as err:
        logger.exception('Error occurred whilst validating XML syntax.')
        validation_details['error'] = create_validation_details_error(
            message='Syntax is invalid.',
            details=str(err),
        )
    except XMLSchemaException as err:
        logger.exception('Error occurred whilst validating XML for schema correctness.')
        validation_details['error'] = create_validation_details_error(
            message='XML does not conform to the corresponding schema.',
            details=str(err),
        )
    except (InvalidRootElementName, FileRegisteredBefore, FileNameNotMatchingWithLocalID) as err:
        logger.exception('Error occurred whilst validating XML. Please see error message for details.')
        validation_details['error'] = create_validation_details_error(
            err.message,
            err.details
        )
    except BaseException as err:
        logger.exception('An unexpected error occurred whilst validating the XML.')
        validation_details['error'] = create_validation_details_error(
            details=str(err)
        )

    return validation_details