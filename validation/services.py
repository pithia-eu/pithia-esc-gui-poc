import logging
import os
import xmlschema
from datetime import (
    datetime,
    timezone,
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import escape
from typing import Union
from xmlschema.exceptions import XMLSchemaException

from .errors import (
    FileNameNotMatchingWithLocalID,
    FileRegisteredBefore,
    InvalidNamespaceValue,
    InvalidRootElementName,
    UpdateFileNotMatching,
)
from .file_wrappers import (
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .helpers import (
    create_li_element_with_register_link_from_resource_type_from_resource_url,
    create_validation_summary_error,
    map_acquisition_capability_to_update_link,
    map_string_to_li_element,
)
from .url_validation_services import (
    MetadataFileMetadataURLReferencesValidator,
    MetadataFileOntologyURLReferencesValidator,
)

from common.models import (
    Instrument,
    AcquisitionCapabilities,
    ScientificMetadata,
)
from pithiaesc.settings import BASE_DIR

logger = logging.getLogger(__name__)


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
    def _instantiate_pithia_schema(cls):
        try:
            cwd_before_validation = os.getcwd()
            # Temporarily change the cwd to so the XSD
            # validator can see the schema files.
            os.chdir(os.path.join(BASE_DIR, 'validation', 'local_schema_files'))
            with open(os.path.join('pithia.xsd')) as schema_file:
                schema = xmlschema.XMLSchema(schema_file)
        finally:
            # Change the cwd back as XSD validation is
            # finished.
            os.chdir(cwd_before_validation)
        
        return schema

    @classmethod
    def _validate_xml_file_string_against_schema(cls, xml_file_string: str, schema: xmlschema.XMLSchema):
        schema.validate(xml_file_string)

    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        """
        Validates an XML metadata file against the schema it
        specifies at its schemaLocation URL.
        """
        schema = cls._instantiate_pithia_schema()
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


class MetadataNamespaceValidator:
    @classmethod
    def validate(cls, xml_file: XMLMetadataFile):
        """
        Validates the <namespace> value of an
        XML metadata file.
        """
        namespace_tag_text = xml_file.namespace
        if len(namespace_tag_text.split()) > 1:
            raise InvalidNamespaceValue(
                f'The namespace should not contain any whitespace.'
            )


class MetadataFileRegistrationValidator:
    @classmethod
    def _is_localid_already_in_use(cls, localid: str, model: ScientificMetadata = ScientificMetadata):
        try:
            model.objects.get(pk=localid)
        except ObjectDoesNotExist:
            return False
        return True

    @classmethod
    def validate(cls, xml_file: XMLMetadataFile, model: ScientificMetadata):
        """
        Validates whether an XML metadata file has been
        registered before or not.
        """
        xml_file_localid = xml_file.localid
        if not cls._is_localid_already_in_use(xml_file_localid, model):
            return False
        
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
    ) -> Union[bool, list]:
        """
        Checks whether each Operational Mode ID present in
        the Instrument that is currently registered is also
        within the updated XML metadata file for that
        Instrument.
        """
        operational_mode_ids_of_updated_xml = xml_file.operational_mode_ids
        instrument_to_update = model.objects.get(pk=current_instrument_id)
        operational_mode_ids_of_current_xml = instrument_to_update.operational_mode_ids
        operational_mode_ids_intersection = set(operational_mode_ids_of_updated_xml).intersection(set(operational_mode_ids_of_current_xml))
        result = len(operational_mode_ids_intersection) == len(operational_mode_ids_of_current_xml)
        missing_ids = [id for id in list(operational_mode_ids_of_current_xml) if id not in list(operational_mode_ids_intersection)]
        missing_operational_mode_urls = [f'{instrument_to_update.metadata_server_url}#{id}' for id in missing_ids]
        return result, missing_operational_mode_urls

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
        # Namespace validation
        MetadataNamespaceValidator.validate(xml_metadata_file)
    except InvalidNamespaceValue as err:
        logger.exception('Error occurred whilst validating XML. Please see error message for details.')
        validation_summary['error'] = create_validation_summary_error(
            message='Invalid namespace.',
            details=str(err),
        )
        return validation_summary

    try:
        # Registration validation
        if validate_for_registration is True:
            MetadataFileRegistrationValidator.validate(xml_metadata_file, model)
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
            is_each_op_mode_in_update_valid, missing_operational_mode_urls = MetadataFileUpdateValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
                xml_metadata_file,
                metadata_id_to_validate_for_update,
                Instrument
            )
            if not is_each_op_mode_in_update_valid:
                acquisition_capability_sets = AcquisitionCapabilities.objects.referencing_operational_mode_urls(missing_operational_mode_urls)
                validation_summary['warnings'].append(create_validation_summary_error(
                    message='Any references to this instrument\'s operational mode IDs will be invalidated after this update.',
                    details='After updating this instrument, please update any references to this instrument\'s operational mode IDs in the acquisition capabilities listed below: <ul>%s</ul>' % ''.join(list(map(map_acquisition_capability_to_update_link, acquisition_capability_sets)))
                ))
        except AttributeError:
            pass

    # Resource URL validation
    # Check which resource URLs are valid and return
    # the invalid ones.
    invalid_resource_urls = MetadataFileMetadataURLReferencesValidator.is_each_potential_resource_url_valid(xml_metadata_file)
    invalid_operational_mode_urls = MetadataFileMetadataURLReferencesValidator.is_each_potential_operational_mode_url_valid(xml_metadata_file)

    # Keys to access invalid URL categories
    INCORRECTLY_STRUCTURED_URLS = 'urls_with_incorrect_structure'
    UNREGISTERED_RESOURCE_URLS = 'urls_pointing_to_unregistered_resources'
    UNREGISTERED_RESOURCE_URL_TYPES = 'types_of_missing_resources'
    UNREGISTERED_OPERATIONAL_MODE_URLS = 'urls_pointing_to_registered_resources_with_missing_op_modes'

    # Process the returned invalid resource URLs.
    incorrectly_structured_urls = invalid_resource_urls.get(INCORRECTLY_STRUCTURED_URLS, []) + invalid_operational_mode_urls.get(INCORRECTLY_STRUCTURED_URLS, [])
    unregistered_resource_urls = invalid_resource_urls.get(UNREGISTERED_RESOURCE_URLS, []) + invalid_operational_mode_urls.get(UNREGISTERED_RESOURCE_URLS, [])
    unregistered_resource_url_types = invalid_resource_urls.get(UNREGISTERED_RESOURCE_URL_TYPES, []) + invalid_operational_mode_urls.get(UNREGISTERED_RESOURCE_URL_TYPES, [])
    unregistered_operational_mode_urls = invalid_operational_mode_urls.get(UNREGISTERED_OPERATIONAL_MODE_URLS, [])
    
    if len(incorrectly_structured_urls) > 0:
        error_msg = 'Invalid document URLs: <ul>%s</ul><div class="mt-2">Your resource URL may reference an unsupported resource type, or may not follow the correct structure.</div>' % ''.join(list(map(map_string_to_li_element, incorrectly_structured_urls)))
        error_msg = error_msg + '<div class="mt-2">Expected resource URL structure: <i>https://metadata.pithia.eu/resources/2.2/<b>resource type</b>/<b>namespace</b>/<b>localID</b></i></div>'
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple resource URLs specified via the xlink:href attribute are invalid.',
            details=error_msg
        )
        return validation_summary

    if len(unregistered_resource_urls) > 0:
        error_msg = 'Unregistered document URLs: <ul>%s</ul><b>Note:</b> If your URLs start with "<i>http://</i>" please change this to "<i>https://</i>".' % ''.join(list(map(map_string_to_li_element, unregistered_resource_urls)))
        error_msg = error_msg + '<div class="mt-2">Please use the following links to register the resources referenced in the submitted metadata file:</div>'
        error_msg = error_msg + '<ul class="mt-2">%s</ul>' % ''.join(list(map(create_li_element_with_register_link_from_resource_type_from_resource_url, unregistered_resource_url_types)))
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple resources referenced by the xlink:href attribute have not been registered with the e-Science Centre.',
            details=error_msg
        )
        return validation_summary

    if len(unregistered_operational_mode_urls) > 0:
        error_msg = 'Invalid operational mode references: <ul>%s</ul>' % ''.join(list(map(map_string_to_li_element, unregistered_operational_mode_urls)))
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple referenced operational modes are invalid.',
            details=error_msg
        )
        return validation_summary

    # Ontology URL validation
    invalid_ontology_urls = MetadataFileOntologyURLReferencesValidator.is_each_potential_ontology_url_in_xml_file_valid(xml_metadata_file)
    if len(invalid_ontology_urls) > 0:
        error_msg = 'Invalid ontology term URLs: <ul>%s</ul><div class="mt-2">These ontology URLs may reference terms which have not yet been added to the PITHIA ontology, or no longer exist in the PITHIA ontology. Please also ensure URLs start with "<i>https://</i>" and not "<i>http://</i>".</div>' % ''.join(list(map(map_string_to_li_element, invalid_ontology_urls)))
        validation_summary['error'] = create_validation_summary_error(
            message='One or multiple ontology terms referenced by the xlink:href attribute are not valid PITHIA ontology terms.',
            details=error_msg
        )

    return validation_summary

def validate_xml_file_references_and_return_errors(xml_metadata_file: XMLMetadataFile):
    incorrectly_structured_url_errors = []
    unregistered_resource_url_errors = []
    unregistered_operational_mode_url_errors = []

    # Resource URL validation
    # Check which resource URLs are valid and return
    # the invalid ones.
    invalid_resource_urls = MetadataFileMetadataURLReferencesValidator.is_each_potential_resource_url_valid(xml_metadata_file)
    invalid_operational_mode_urls = MetadataFileMetadataURLReferencesValidator.is_each_potential_operational_mode_url_valid(xml_metadata_file)

    # Keys to access invalid URL categories
    INCORRECTLY_STRUCTURED_URLS = 'urls_with_incorrect_structure'
    UNREGISTERED_RESOURCE_URLS = 'urls_pointing_to_unregistered_resources'
    UNREGISTERED_RESOURCE_URL_TYPES = 'types_of_missing_resources'
    UNREGISTERED_OPERATIONAL_MODE_URLS = 'urls_pointing_to_registered_resources_with_missing_op_modes'

    # Process the returned invalid resource URLs.
    incorrectly_structured_urls = invalid_resource_urls.get(INCORRECTLY_STRUCTURED_URLS, []) + invalid_operational_mode_urls.get(INCORRECTLY_STRUCTURED_URLS, [])
    unregistered_resource_urls = invalid_resource_urls.get(UNREGISTERED_RESOURCE_URLS, []) + invalid_operational_mode_urls.get(UNREGISTERED_RESOURCE_URLS, [])
    unregistered_resource_url_types = invalid_resource_urls.get(UNREGISTERED_RESOURCE_URL_TYPES, []) + invalid_operational_mode_urls.get(UNREGISTERED_RESOURCE_URL_TYPES, [])
    unregistered_operational_mode_urls = invalid_operational_mode_urls.get(UNREGISTERED_OPERATIONAL_MODE_URLS, [])
    
    if len(incorrectly_structured_urls) > 0:
        error_msg = 'One or multiple resource URLs specified via the xlink:href attribute are invalid.'
        error_msg = error_msg + '<br>'
        error_msg = error_msg + 'Invalid document URLs: <ul>%s</ul><div class="mt-2">Your resource URL may reference an unsupported resource type, or may not follow the correct structure.</div>' % ''.join(list(map(map_string_to_li_element, incorrectly_structured_urls)))
        error_msg = error_msg + '<div class="mt-2">Expected resource URL structure: <i>https://metadata.pithia.eu/resources/2.2/<b>resource type</b>/<b>namespace</b>/<b>localID</b></i></div>'
        incorrectly_structured_url_errors.append(error_msg)

    if len(unregistered_resource_urls) > 0:
        error_msg = 'One or multiple resources referenced by the xlink:href attribute have not been registered with the e-Science Centre.'
        error_msg = error_msg + '<br>'
        error_msg = error_msg + 'Unregistered document URLs: <ul>%s</ul><b>Note:</b> If your URLs start with "<i>http://</i>" please change this to "<i>https://</i>".' % ''.join(list(map(map_string_to_li_element, unregistered_resource_urls)))
        error_msg = error_msg + '<div class="mt-2">Please use the following links to register the resources referenced in the submitted metadata file:</div>'
        error_msg = error_msg + '<ul class="mt-2">%s</ul>' % ''.join(list(map(create_li_element_with_register_link_from_resource_type_from_resource_url, unregistered_resource_url_types)))
        unregistered_resource_url_errors.append(error_msg)

    if len(unregistered_operational_mode_urls) > 0:
        error_msg = 'One or multiple referenced operational modes are invalid.'
        error_msg = error_msg + '<br>'
        error_msg = error_msg + 'Invalid operational mode references: <ul>%s</ul>' % ''.join(list(map(map_string_to_li_element, unregistered_operational_mode_urls)))
        unregistered_operational_mode_url_errors.append(error_msg)

    # Ontology URL validation
    invalid_ontology_urls = MetadataFileOntologyURLReferencesValidator.is_each_potential_ontology_url_in_xml_file_valid(xml_metadata_file)
    invalid_ontology_url_errors = []
    if len(invalid_ontology_urls) > 0:
        error_msg = 'One or multiple ontology terms referenced by the xlink:href attribute are not valid PITHIA ontology terms.'
        error_msg = error_msg + '<br>'
        error_msg = error_msg + 'Invalid ontology term URLs: <ul>%s</ul><div class="mt-2">These ontology URLs may reference terms which have not yet been added to the PITHIA ontology, or no longer exist in the PITHIA ontology. Please also ensure URLs start with "<i>https://</i>" and not "<i>http://</i>".</div>' % ''.join(list(map(map_string_to_li_element, invalid_ontology_urls)))
        invalid_ontology_url_errors.append(error_msg)

    return {
        'incorrectly_structured_url_errors': incorrectly_structured_url_errors,
        'unregistered_resource_url_errors': unregistered_resource_url_errors,
        'unregistered_operational_mode_url_errors': unregistered_operational_mode_url_errors,
        'invalid_ontology_url_errors': invalid_ontology_url_errors,
    }

def validate_new_xml_file_registration_and_return_errors(xml_metadata_file: XMLMetadataFile, model: ScientificMetadata):
    errors = []
    try:
        MetadataFileRegistrationValidator.validate(xml_metadata_file, model)
    except FileRegisteredBefore as err:
        logger.exception('Error occurred during metadata validation.')
        error_msg = str(err)
        errors.append(error_msg)
    return errors

def validate_xml_file_update_and_return_errors(xml_metadata_file: XMLMetadataFile, model: ScientificMetadata, existing_metadata_id):
    errors = []
    try:
        MetadataFileUpdateValidator.validate(xml_metadata_file, model, existing_metadata_id)
    except UpdateFileNotMatching as err:
        logger.exception('Error occurred during metadata validation.')
        error_msg = str(err)
        errors.append(error_msg)
    except ObjectDoesNotExist:
        logger.exception('Error occurred during metadata validation.')
        error_msg = 'The metadata registration being updated could not be found.'
        errors.append(error_msg)
    return errors

def validate_instrument_xml_file_update_and_return_errors(xml_metadata_file: InstrumentXMLMetadataFile, existing_metadata_id):
    errors = []
    try:
        # Operational mode IDs are changed and pre-existing IDs are referenced by any Acquisition Capabilities validation
        is_each_op_mode_in_update_valid, missing_operational_mode_urls = MetadataFileUpdateValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
            xml_metadata_file,
            existing_metadata_id,
            Instrument
        )
        if not is_each_op_mode_in_update_valid:
            acquisition_capability_sets = AcquisitionCapabilities.objects.referencing_operational_mode_urls(missing_operational_mode_urls)
            if len(acquisition_capability_sets) > 0:
                error_msg = '<div class="mt-2">Any references to the following operational modes will be invalidated after this update:<div>'
                error_msg = error_msg + '<ul class="mt-3">%s</ul>' % ''.join(list(map(map_string_to_li_element, missing_operational_mode_urls)))
                error_msg = error_msg + '<div class="mt-3">To fix this, please also update any references to this instrument\'s operational mode IDs in the acquisition capabilities listed below, after updating this instrument:</div><ul class="mt-3">%s</ul>' % ''.join(list(map(map_acquisition_capability_to_update_link, acquisition_capability_sets)))
                errors.append(error_msg)
    except AttributeError:
        logger.exception('This metadata file doesn\'t have operational modes')
    return errors

def validate_xml_file_with_xsd_and_return_errors(xml_metadata_file: XMLMetadataFile):
    errors = []
    try:
        MetadataFileXSDValidator.validate(xml_metadata_file)
    except XMLSchemaException as err:
        logger.exception('Error occurred during metadata validation.')
        error_msg = f'<span style="white-space: pre-wrap;">{escape(str(err).strip())}</span>'
        errors.append(error_msg)
    return errors

def is_localid_taken(localid: str):
    result = MetadataFileRegistrationValidator._is_localid_already_in_use(localid)
    result_dict = {
        'result': result,
    }
    if result is True:
        result_dict['suggestion'] = f'{localid}{int(datetime.now(timezone.utc).timestamp())}'
    return result_dict