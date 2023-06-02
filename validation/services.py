import logging
import xmlschema
from django.core.exceptions import ObjectDoesNotExist
from lxml import etree
from pathlib import Path
from requests import get
from xmlschema.exceptions import XMLSchemaException

from .errors_new import (
    InvalidRootElementName,
    FileNameNotMatchingWithLocalID,
    FileRegisteredBefore,
    UpdateFileNotMatching,
)
from .helpers import (
    create_validation_summary_error,
    _map_string_to_li_element,
    _create_li_element_with_register_link_from_resource_type_from_resource_url,
    _map_acquisition_capability_to_update_link,
)
from .url_validation import (
    get_invalid_ontology_urls_from_parsed_xml,
    get_invalid_resource_urls_from_parsed_xml,
    get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml
)

from common.helpers import get_acquisition_capability_sets_referencing_instrument_operational_ids
from common.models import (
    Instrument,
    ScientificMetadata,
)

logger = logging.getLogger(__name__)

class XMLMetadataFile:
    """
    A wrapper class around an XML Metadata File
    being submitted for validation. Facilitates
    accessing certain properties and hides
    complexity behind functions.
    """
    def __init__(self, xml_file_string, xml_file_name) -> None:
        self._xml_file_name = xml_file_name
        self._xml_file_contents = xml_file_string
        self._parsed_xml = self._parse_xml_string(self._xml_file_contents)

    @classmethod
    def from_file(cls, xml_file):
        xml_file.seek(0)
        return cls(xml_file.read(), xml_file.name)

    def _parse_xml_file(self, xml_file):
        return etree.parse(xml_file)

    def _parse_xml_string(self, xml_string: str):
        try:
            return etree.fromstring(xml_string)
        except ValueError:
            return etree.fromstring(xml_string.encode('utf-8'))

    @property
    def contents(self):
        return self._xml_file_contents

    # Scientific Metadata properties
    @property
    def localid(self):
        # There should be only one <localID> tag in the tree
        return self._parse_xml_file.find('.//{https://metadata.pithia.eu/schemas/2.2}localID').text

    @property
    def namespace(self):
        return self._parse_xml_file.find('.//{https://metadata.pithia.eu/schemas/2.2}namespace').text

    # Helper properties
    @property
    def file_name_no_extension(self):
        return Path(self._xml_file_name).stem
    
    @property
    def schema_url(self):
        urls_with_xsi_ns = self._parsed_xml.xpath("//@*[local-name()='schemaLocation' and namespace-uri()='http://www.w3.org/2001/XMLSchema-instance']")
        urls_with_xsi_ns = urls_with_xsi_ns[0].split()
        schema_url = urls_with_xsi_ns[0]
        if len(urls_with_xsi_ns) > 1:
            schema_url = urls_with_xsi_ns[1]
        return schema_url

    @property
    def root_element_name(self):
        # Get the root tag text without the namespace
        root_localname = etree.QName(self._parsed_xml).localname
        return root_localname

class DataSubsetXMLMetadataFile(XMLMetadataFile):
    def __init__(self, xml_file_string, xml_file_name) -> None:
        xml_file_string = self._xml_string_with_spoofed_doi(xml_file_string)
        super().__init__(xml_file_string, xml_file_name)

    def _xml_string_with_spoofed_doi(self, xml_string):
        parsed_xml_string = self._parse_xml_string(xml_string)
        valid_doi_name = '10.000/000'
        doi_name_element = parsed_xml_string.find('.//{http://www.doi.org/2010/DOISchema}referentDoiName')
        doi_registration_agency_name_element = parsed_xml_string.find('.//{http://www.doi.org/2010/DOISchema}registrationAgencyDoiName')
        if doi_name_element is not None:
            doi_name_element.text = valid_doi_name
        if doi_registration_agency_name_element is not None:
            doi_registration_agency_name_element.text = valid_doi_name
        contents_with_spoofed_doi = etree.tostring(parsed_xml_string).decode()
        try:
            contents_with_spoofed_doi = contents_with_spoofed_doi.decode()
        except (UnicodeDecodeError, AttributeError):
            pass
        return contents_with_spoofed_doi

class InstrumentXMLMetadataFile(XMLMetadataFile):
    @property
    def operational_mode_ids(self):
        # Operational mode IDs are the only values enclosed in <id></id> tags
        return [om_element.text for om_element in self._parse_xml_file.findall('.//{https://metadata.pithia.eu/schemas/2.2}id')]


class MetadataRootElementNameValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile, expected_root_localname):
        """
        Validates the root element name of an XML metadata file
        by confirming the XML metadata file's root element
        matches with an expected root element name.
        """
        root_localname = xml_file.root_element_name
        if root_localname != expected_root_localname:
            raise InvalidRootElementName(
                f'Expected the metadata file to have a root element name of "{expected_root_localname}", but got "{root_localname}".'
            )


class MetadataFileXSDValidator:
    @classmethod
    def _validate_xml_file_string_against_schema(cls, xml_file_string: str, schema):
        xml_schema = xmlschema.XMLSchema(schema)
        xml_schema.validate(xml_file_string)

    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        """
        Validates an XML metadata file against the schema it
        specifies at its schemaLocation URL.
        """
        xml_file_schema_url = xml_file.schema_url
        schema_response = get(xml_file_schema_url)
        schema = schema_response.text.encode()
        return cls._validate_xml_file_string_against_schema(xml_file.contents, schema)


class MetadataFileNameValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        """
        Validates the name of an XML metadata file matches
        with the innerText of its <localID> element.
        """
        localid_tag_text = xml_file.localid
        xml_file_name_with_no_extension = xml_file.file_name_no_extension
        if localid_tag_text != xml_file_name_with_no_extension:
            raise FileNameNotMatchingWithLocalID(
                f'The file name \"{xml_file_name_with_no_extension}\" must match the localID of the metadata \"{localid_tag_text}\".'
            )

class MetadataFileRegistrationValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile, model: ScientificMetadata):
        """
        Validates whether an XML metadata file has been
        registered before or not.
        """
        xml_file_localid = xml_file.localid
        xml_file_namespace = xml_file.namespace
        try:
            model.objects.get_by_namespace_and_localid(
                namespace=xml_file_namespace,
                localid=xml_file_localid
            )
        except ObjectDoesNotExist:
            return
        
        raise FileRegisteredBefore(
            f'Metadata sharing the same localID of "{xml_file_localid}" has already been registered with the e-Science Centre.',
        )

class MetadataFileUpdateValidator:
    @classmethod
    def is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
        self,
        xml_file: InstrumentXMLMetadataFile,
        current_instrument_id,
        model: Instrument
    ):
        operational_mode_ids_of_updated_xml = xml_file.operational_mode_ids
        instrument_to_update = model.objects.get(pk=current_instrument_id)
        operational_mode_ids_of_current_xml = instrument_to_update.operational_mode_ids
        operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
        return len(operational_mode_ids_intersection) == len(operational_mode_ids_of_current_xml)

    @classmethod
    def validate(cls, xml_file: XMLMetadataFile, model: ScientificMetadata, metadata_registration_id):
        """
        Validates whether the localID and namespace of
        an updated XML metadata file matches the localID
        and namespace of its current corresponding
        e-Science Centre registration.
        """
        xml_file_localid = xml_file.localid
        xml_file_namespace = xml_file.namespace
        existing_registration = model.objects.get(pk=metadata_registration_id)
        if (not all([
            xml_file_localid == existing_registration.localid,
            xml_file_namespace == existing_registration.namespace
        ])):
            raise UpdateFileNotMatching('The localID and namespace must be matching with the current version of the metadata.')

class MetadataFileMetadataURLReferencesValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        pass

class MetadataFileOntologyURLReferencesValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        pass

# XSD Schema validation
# def validate_xml_against_own_schema(xml_file):
#     """
#     Validates the XML file against its own schema by
#     fetching the schema from the URL specified at the
#     xsi:schemaLocation attribute within the XML file.
#     """
#     xml_file_parsed = validate_and_parse_xml_file(xml_file)
#     schema_url = get_schema_location_url_from_parsed_xml_file(xml_file_parsed)
#     validate_xml_against_schema_at_url(xml_file, schema_url)

def validate_xml_file_and_return_summary(
    xml_metadata_file: XMLMetadataFile,
    model: ScientificMetadata,
    validate_for_registration=False,
    metadata_id_to_validate_for_update=None
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
    validation_summary = {
        'error': None,
        'warnings': [],
    }

    try:
        # Root element name validation
        MetadataRootElementNameValidator.validate(xml_metadata_file, model.root_element_name)
    except InvalidRootElementName as err:
        logger.exception('Error occurred whilst validating XML. Please see error message for details.')
        validation_summary['error'] = create_validation_summary_error(
            'The metadata file submitted is for the wrong resource type.',
            str(err)
        )
        return validation_summary

    try:
        # XSD Schema validation
        MetadataFileXSDValidator.validate(xml_metadata_file)
    except XMLSchemaException as err:
        logger.exception('Error occurred whilst validating XML for schema correctness.')
        validation_summary['error'] = create_validation_summary_error(
            message='XML does not conform to the corresponding schema.',
            details=str(err),
        )
        return validation_summary

    try:
        # Matching file name and localID tag text validation
        MetadataFileNameValidator.validate(xml_metadata_file)
    except FileNameNotMatchingWithLocalID as err:
        logger.exception('Error occurred whilst validating XML. Please see error message for details.')
        validation_summary['error'] = create_validation_summary_error(
            message='File name not matching with localID',
            details=str(err),
        )
        return validation_summary

    try:
        # Registration validation
        if validate_for_registration is True:
            MetadataFileRegistrationValidator.validate(xml_metadata_file)
    except FileRegisteredBefore as err:
        logger.exception('Error occurred whilst validating XML. Please see error message for details.')
        validation_summary['error'] = create_validation_summary_error(
            message='This XML metadata file has been registered before.',
            details=str(err),
        )
        return validation_summary

    
    if metadata_id_to_validate_for_update is not None:
        # Update validation
        try:
            MetadataFileUpdateValidator.validate(xml_metadata_file, model, metadata_id_to_validate_for_update)
        except UpdateFileNotMatching as err:
            validation_summary['error'] = create_validation_summary_error(
                message='Invalid localID and namespace',
                details=str(err),
            )
            return validation_summary
        except ObjectDoesNotExist:
            validation_summary['error'] = create_validation_summary_error(
                message='Registration not found.',
                details='The metadata registration being updated could not be found.'
            )
            return validation_summary

        try:
            # Operational mode IDs are changed and pre-existing IDs are referenced by any Acquisition Capabilities validation
            is_each_op_mode_in_update_valid = MetadataFileUpdateValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument()
            if not is_each_op_mode_in_update_valid:
                acquisition_capability_sets = get_acquisition_capability_sets_referencing_instrument_operational_ids(existing_resource_id)
                validation_summary['warnings'].append(create_validation_summary_error(
                    message='Any references to this instrument\'s operational mode IDs must will be invalidated after this update.',
                    details='After updating this instrument, please update any references to this instrument\'s operational mode IDs in the acquisition capabilities listed below: <ul>%s</ul>' % ''.join(list(map(_map_acquisition_capability_to_update_link, acquisition_capability_sets)))
                ))
        except AttributeError:
            pass

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
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple resource URLs specified via the xlink:href attribute are invalid.',
            details=error_msg
        )
        return validation_summary

    if len(resource_urls_pointing_to_unregistered_resources) > 0:
        error_msg = 'Unregistered document URLs: <ul>%s</ul><b>Note:</b> If your URLs start with "<i>http://</i>" please change this to "<i>https://</i>".' % ''.join(list(map(_map_string_to_li_element, resource_urls_pointing_to_unregistered_resources)))
        error_msg = error_msg + '<div class="mt-2">Please use the following links to register the resources referenced in the submitted metadata file:</div>'
        error_msg = error_msg + '<ul class="mt-2">%s</ul>' % ''.join(list(map(_create_li_element_with_register_link_from_resource_type_from_resource_url, types_of_missing_resources)))
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple resources referenced by the xlink:href attribute have not been registered with the e-Science Centre.',
            details=error_msg
        )
        return validation_summary

    if len(resource_urls_pointing_to_registered_resources_with_missing_op_modes) > 0:
        error_msg = 'Invalid operational mode references: <ul>%s</ul>' % ''.join(list(map(_map_string_to_li_element, resource_urls_pointing_to_registered_resources_with_missing_op_modes)))
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple referenced operational modes are invalid.',
            details=error_msg
        )
        return validation_summary

    # Ontology URL validation
    invalid_ontology_urls = get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed)
    if len(invalid_ontology_urls) > 0:
        error_msg = 'Invalid ontology term URLs: <ul>%s</ul><div class="mt-2">These ontology URLs may reference terms which have not yet been added to the PITHIA ontology, or no longer exist in the PITHIA ontology. Please also ensure URLs start with "<i>https://</i>" and not "<i>http://</i>".</div>' % ''.join(list(map(_map_string_to_li_element, invalid_ontology_urls)))
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple ontology terms referenced by the xlink:href attribute are not valid PITHIA ontology terms.',
            details=error_msg
        )

    return validation_summary