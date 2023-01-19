import os
import environ
import mongomock
from lxml import etree
from lxml.etree import XMLSyntaxError
from genericpath import isfile
from pathlib import Path
from django.test import SimpleTestCase, tag
from register.register import register_metadata_xml_file
from validation.metadata_validation import (
    ORGANISATION_XML_ROOT_TAG_NAME,
    INDIVIDUAL_XML_ROOT_TAG_NAME,
    PROJECT_XML_ROOT_TAG_NAME,
    PLATFORM_XML_ROOT_TAG_NAME,
    OPERATION_XML_ROOT_TAG_NAME,
    INSTRUMENT_XML_ROOT_TAG_NAME,
    ACQUISITION_CAPABILITY_XML_ROOT_TAG_NAME,
    ACQUISITION_XML_ROOT_TAG_NAME,
    COMPUTATION_CAPABILITY_XML_ROOT_TAG_NAME,
    COMPUTATION_XML_ROOT_TAG_NAME,
    PROCESS_XML_ROOT_TAG_NAME,
    DATA_COLLECTION_XML_ROOT_TAG_NAME,
    validate_xml_against_own_schema,
    parse_xml_file,
    validate_and_get_validation_details_of_xml_file,
    validate_xml_root_element_name_equals_expected_name,
    validate_xml_file_name,
    validate_xml_file_is_unregistered,
    is_updated_xml_file_localid_matching_with_current_resource_localid,
)
from validation.url_validation import (
    get_invalid_ontology_urls_from_parsed_xml,
    get_invalid_resource_urls_from_parsed_xml,
    divide_resource_url_into_main_components,
    is_resource_url_structure_valid,
    divide_resource_url_from_op_mode_id,
    get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml,
    validate_ontology_term_url,
)
from validation.errors import FileRegisteredBefore
from bson.errors import InvalidId
from pithiaesc.settings import BASE_DIR

_TEST_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files')
_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

env = environ.Env()

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.

class FileTestCase:
    xml_file_name = ''

    def setUp(self) -> None:
        self.xml_file_path = os.path.join(_XML_METADATA_FILE_DIR, self.xml_file_name)
        return super().setUp()

@tag('organisation')
class OrganisationFileTestCase(FileTestCase):
    xml_file_name = 'Organisation_Test.xml'

@tag('individual')
class IndividualFileTestCase(FileTestCase):
    xml_file_name = 'Individual_Test.xml'

@tag('project')
class ProjectFileTestCase(FileTestCase):
    xml_file_name = 'Project_Test.xml'

@tag('platform')
class PlatformFileTestCase(FileTestCase):
    xml_file_name = 'Platform_Test.xml'

@tag('operation')
class OperationFileTestCase(FileTestCase):
    xml_file_name = 'Operation_Test.xml'

@tag('instrument')
class InstrumentFileTestCase(FileTestCase):
    xml_file_name = 'Instrument_Test.xml'

@tag('acquisition_capabilities')
class AcquisitionCapabilitiesFileTestCase(FileTestCase):
    xml_file_name = 'AcquisitionCapabilities_Test.xml'

@tag('acquisition')
class AcquisitionFileTestCase(FileTestCase):
    xml_file_name = 'Acquisition_Test.xml'

@tag('computation_capabilities')
class ComputationCapabilitiesFileTestCase(FileTestCase):
    xml_file_name = 'ComputationCapabilities_Test.xml'

@tag('computation')
class ComputationFileTestCase(FileTestCase):
    xml_file_name = 'Computation_Test.xml'

@tag('process')
class ProcessFileTestCase(FileTestCase):
    xml_file_name = 'Composite_Test.xml'

@tag('data_collection')
class DataCollectionFileTestCase(FileTestCase):
    xml_file_name = 'DataCollection_Test.xml'

class InvalidSyntaxValidationTestCase:
    @tag('fast')
    def test_file_with_invalid_syntax(self):
        """
        The file causes parse_xml_file() to raise an exception
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test_InvalidSyntax.xml')) as invalid_xml_file:
            try:
                parse_xml_file(invalid_xml_file)
            except:
                print('Exception raised, as expected!')
            self.assertRaises(XMLSyntaxError, parse_xml_file, invalid_xml_file)

class SyntaxValidationTestCase:
    @tag('fast')
    def test_file_with_valid_syntax(self):
        """
        The file does not cause parse_xml_file() to raise an exception
        """
        try:
            with open(self.xml_file_path) as xml_file:
                parse_xml_file(xml_file)
                print(f'Passed syntax validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('parse_xml_file() raised an exception unexpectedly!')

class RootElementValidationTestCase:
    root_element_name = ''
    @tag('fast')
    def test_file_with_valid_root_element_name(self):
        """
        The organisation metadata file does not cause validate_xml_root_element_name_equals_expected_name() to raise an exception.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                validate_xml_root_element_name_equals_expected_name(xml_file, self.root_element_name)
                print(f'Passed root element validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('validate_xml_root_element_name_equals_expected_name raised an exception unexpectedly!')

class XSDValidationTestCase:
    @tag('slow')
    def test_validate_against_own_schema(self):
        """
        validate_xml_against_own_schema() does not raise an exception when passed a valid xml file.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                validate_xml_against_own_schema(xml_file)
                print(f'Passed XSD validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('validate_xml_against_own_schema() raised an exception unexpectedly!')

class FileNameValidationTestCase:
    @tag('fast')
    def test_validate_xml_file_name(self):
        """
        validate_xml_file_name() does not raise an exception when passed a valid xml file.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                validate_xml_file_name(xml_file)
                print(f'Passed file name validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('validate_xml_file_name() raised an exception unexpectedly!')

class NewRegistrationValidationTestCase:
    @tag('fast')
    def test_validate_xml_file_is_unregistered(self):
        """
        validate_xml_file_is_unregistered() does not raise an exception when passed a valid xml file.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                validate_xml_file_is_unregistered(
                    self.mongodb_model,
                    xml_file
                )
                print(f'Passed new registration validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('validate_xml_file_name() raised an exception unexpectedly!')

    @tag('fast')
    def test_validate_xml_file_is_unregistered_fails(self):
        """
        validate_xml_file_is_unregistered() raises an exception when passed an xml file that has already been registered.
        """
        with open(self.xml_file_path) as xml_file:
            register_metadata_xml_file(
                xml_file,
                self.mongodb_model,
                None
            )
            self.assertRaises(
                FileRegisteredBefore,
                validate_xml_file_is_unregistered,
                self.mongodb_model,
                xml_file
            )
            print(f'Passed registration validation failure for {Path(xml_file.name).name}.')

class UpdateValidationTestCase:
    @tag('fast')
    def test_is_updated_xml_file_localid_matching_with_current_resource_localid(self):
        """
        is_updated_xml_file_localid_matching_with_current_resource_localid() does not raise an exception when passed a valid xml_file
        """
        try:
            with open(self.xml_file_path) as xml_file:
                registered_resource = register_metadata_xml_file(
                    xml_file,
                    self.mongodb_model,
                    None,
                )
                is_updated_xml_file_localid_matching_with_current_resource_localid(
                    xml_file,
                    registered_resource['_id'],
                    self.mongodb_model,
                )
                print(f'Passed update validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('is_updated_xml_file_localid_matching_with_current_resource_localid() raised an exception unexpectedly!')

    @tag('fast')
    def test_is_updated_xml_file_localid_matching_with_current_resource_localid(self):
        """
        is_updated_xml_file_localid_matching_with_current_resource_localid() does not raise an exception when passed a valid xml_file
        """
        with open(self.xml_file_path) as xml_file:
            self.assertRaises(
                InvalidId,
                is_updated_xml_file_localid_matching_with_current_resource_localid,
                xml_file,
                '',
                self.mongodb_model,
            )
            print(f'Passed update validation failure for {Path(xml_file.name).name}.')

class ValidationChecklistTestCase:
    @tag('slow')
    def test_validate_and_get_validation_details_of_xml_file(self):
        """
        The validation results does not contain an error.
        """
        with open(self.xml_file_path) as xml_file:
            try:
                validation_results = validate_and_get_validation_details_of_xml_file(
                    xml_file,
                    self.root_element_name,
                    self.mongodb_model,
                    check_file_is_unregistered=True
                )
                if validation_results['error'] is not None:
                    print('error', validation_results['error'])
                    print(f'Failed validation checklist test for {Path(xml_file.name).name}.')
                    self.fail('validate_and_get_validation_details_of_xml_file() returned an error.')
                self.assertEqual(validation_results['error'], None)
                print(f'Passed validation checklist test for {Path(xml_file.name).name}.')
            except:
                self.fail('validate_and_get_validation_details_of_xml_file() raised an exception unexpectedly!')

class OrganisationSyntaxValidationTestCase(OrganisationFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class OrganisationRootElementValidationTestCase(OrganisationFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    root_element_name = ORGANISATION_XML_ROOT_TAG_NAME
class OrganisationXSDValidationTestCase(OrganisationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class OrganisationFileNameValidationTestCase(OrganisationFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class OrganisationNewRegistrationValidationTestCase(OrganisationFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    def setUp(self) -> None:
        client = mongomock.MongoClient()
        self.mongodb_model = client[env('DB_NAME')]['current-organisations']
        return super().setUp()
class OrganisationUpdateValidationTestCase(OrganisationFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    def setUp(self) -> None:
        client = mongomock.MongoClient()
        self.mongodb_model = client[env('DB_NAME')]['current-organisations']
        return super().setUp()
class OrganisationValidationChecklistTestCase(OrganisationFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    def setUp(self) -> None:
        self.root_element_name = ORGANISATION_XML_ROOT_TAG_NAME
        client = mongomock.MongoClient()
        self.mongodb_model = client[env('DB_NAME')]['current-organisations']
        return super().setUp()


class IndividualSyntaxValidationTestCase(IndividualFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass


class UrlsFromFilesValidationTestCase(SimpleTestCase):
    def test_invalid_ontology_urls_are_detected(self):
        """
        get_invalid_ontology_urls() returns a list of invalid ontology urls.
        """
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_parsed = etree.parse(xml_file)
            invalid_ontology_urls = get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed)
            self.assertEquals(len(invalid_ontology_urls), 1)

    def test_invalid_resource_urls_are_detected(self):
        """
        get_invalid_resource_urls() returns a dict of invalid resource urls.
        """
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_parsed = etree.parse(xml_file)
            invalid_resource_urls = get_invalid_resource_urls_from_parsed_xml(xml_file_parsed)
            self.assertEquals(len(invalid_resource_urls['urls_pointing_to_unregistered_resources']), 2)

    def test_invalid_resource_urls_with_op_mode_ids_are_detected(self):
        """
        get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml()
        returns a dict of invalid resource urls.
        """
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_parsed = etree.parse(xml_file)
            invalid_resource_urls_with_op_mode_ids = get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml(xml_file_parsed)
            print('invalid_resource_urls_with_op_mode_ids', invalid_resource_urls_with_op_mode_ids)
            self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_with_incorrect_structure']), 1)
            self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_pointing_to_unregistered_resources']), 1)
            self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_pointing_to_registered_resources_with_missing_op_modes']), 0)


class UrlValidationTestCase(SimpleTestCase):
    def test_ontology_url_validation(self):
        """
        validate_ontology_term_url() returns an ontology node if valid, False, if not.
        """
        valid_ontology_url_1 = 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider'
        valid_ontology_url_2 = 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/ViewOnly'
        invalid_ontology_url_1 = 'https://metadata.pithia.eu/ontology/2.2/invalid/test'
        invalid_ontology_url_2 = 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/DataProvider'

        print(validate_ontology_term_url(valid_ontology_url_1))
        self.assertEquals(validate_ontology_term_url(valid_ontology_url_1), True)
        self.assertEquals(validate_ontology_term_url(valid_ontology_url_2), True)
        self.assertEquals(validate_ontology_term_url(invalid_ontology_url_1), False)
        self.assertEquals(validate_ontology_term_url(invalid_ontology_url_2), False)

    def test_resource_urls_are_divided_correctly(self):
        """
        divide_resource_url_into_main_components() divides resource URLs
        into their main components:
        - url_base: e.g., https://metadata.pithia.eu/resources/2.2
        - resource_type: e.g., organisation
        - namespace: e.g., pithia
        - localid: e.g., Organisation_PITHIA
        """
        resource_url_division_1 = divide_resource_url_into_main_components('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        resource_url_division_2 = divide_resource_url_into_main_components('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        resource_url_division_3 = divide_resource_url_into_main_components('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST')
        
        self.assertEquals(resource_url_division_1['url_base'], 'https://metadata.pithia.eu/resources/2.2')
        self.assertEquals(resource_url_division_1['resource_type'], 'pithia')
        self.assertEquals(resource_url_division_1['namespace'], 'project')
        self.assertEquals(resource_url_division_1['localID'], 'Project_TEST')
        self.assertEquals(resource_url_division_2['url_base'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2')
        self.assertEquals(resource_url_division_3['url_base'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST')
        self.assertEquals(resource_url_division_3['resource_type'], 'organisation')
        self.assertEquals(resource_url_division_3['namespace'], 'pithia')

    def test_resource_urls_with_op_mode_ids_are_divided_correctly(self):
        """
        divide_resource_url_from_op_mode_id() divides resource URLs into
        two components:
        - resource_url: e.g., https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_PITHIA#ionogram
        - op_mode_id: e.g., https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_PITHIA#ionogram
        """
        resource_url_division_1 = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST#ionogram')
        resource_url_division_2 = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST#sweep')
        resource_url_division_3 = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST#test')
        resource_url_division_4 = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST#ionogram#ionogram#ionogram#ionogram')

        self.assertEquals(resource_url_division_1['resource_url'], 'https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        self.assertEquals(resource_url_division_1['op_mode_id'], 'ionogram')
        self.assertEquals(resource_url_division_2['resource_url'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        self.assertEquals(resource_url_division_2['op_mode_id'], 'sweep')
        self.assertEquals(resource_url_division_3['resource_url'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST')
        self.assertEquals(resource_url_division_3['op_mode_id'], 'test')
        self.assertEquals(resource_url_division_4['resource_url'], 'https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST#ionogram#ionogram#ionogram')
        self.assertEquals(resource_url_division_4['op_mode_id'], 'ionogram')

    def test_invalid_resource_url_structures_are_detected(self):
        """
        is_resource_url_structure_valid() returns False
        for all URLs provided for this test.
        """

        blank_string_result = is_resource_url_structure_valid('')
        swapped_namespace_and_resource_type_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        random_string_result_1 = is_resource_url_structure_valid('////')
        random_string_result_2 = is_resource_url_structure_valid('///')
        random_string_result_3 = is_resource_url_structure_valid('//')
        random_string_result_4 = is_resource_url_structure_valid('/')
        non_resource_url_result = is_resource_url_structure_valid('http://www.google')
        http_resource_url_result = is_resource_url_structure_valid('http://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        no_url_protocol_result = is_resource_url_structure_valid('metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        domain_name_duplication_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        acquisition_capability_sets_incorrect_casing_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/AcquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        computation_capability_sets_incorrect_casing_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/ComputationCapabilities/pithia/AcquisitionCapabilities_TEST')

        self.assertEquals(blank_string_result, False)
        self.assertEquals(swapped_namespace_and_resource_type_result, False)
        self.assertEquals(random_string_result_1, False)
        self.assertEquals(random_string_result_2, False)
        self.assertEquals(random_string_result_3, False)
        self.assertEquals(random_string_result_4, False)
        self.assertEquals(non_resource_url_result, False)
        self.assertEquals(http_resource_url_result, False)
        self.assertEquals(no_url_protocol_result, False)
        self.assertEquals(domain_name_duplication_result, False)
        self.assertEquals(acquisition_capability_sets_incorrect_casing_result, False)
        self.assertEquals(computation_capability_sets_incorrect_casing_result, False)

    def test_valid_resource_urls_pass_validation(self):
        """
        is_resource_url_structure_valid() returns True for
        all URLs provided for this test.
        """

        valid_organisation_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        valid_individual_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/individual/pithia/Individual_TEST')
        valid_project_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        valid_platform_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/platform/pithia/Platform_TEST')
        valid_operation_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/operation/pithia/Operation_TEST')
        valid_instrument_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_TEST')
        valid_aqcuisition_capabilities_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        valid_acquisition_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisition/pithia/Acquisition_TEST')
        valid_computation_capability_sets_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_TEST')
        valid_computation_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computation/pithia/Computation_TEST')
        valid_process_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/process/pithia/CompositeProcess_TEST')
        valid_data_collection_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/collection/pithia/DataCollection_TEST')

        self.assertEquals(valid_organisation_url_result, True)
        self.assertEquals(valid_individual_url_result, True)
        self.assertEquals(valid_project_url_result, True)
        self.assertEquals(valid_platform_url_result, True)
        self.assertEquals(valid_operation_url_result, True)
        self.assertEquals(valid_instrument_url_result, True)
        self.assertEquals(valid_aqcuisition_capabilities_url_result, True)
        self.assertEquals(valid_acquisition_url_result, True)
        self.assertEquals(valid_computation_capability_sets_url_result, True)
        self.assertEquals(valid_computation_url_result, True)
        self.assertEquals(valid_process_url_result, True)
        self.assertEquals(valid_data_collection_url_result, True)