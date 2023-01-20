import os
import environ
from lxml.etree import XMLSyntaxError
from pathlib import Path
from django.test import tag
from register.register import register_metadata_xml_file
from validation.metadata_validation import (
    validate_xml_against_own_schema,
    parse_xml_file,
    validate_and_get_validation_details_of_xml_file,
    validate_xml_root_element_name_equals_expected_name,
    validate_xml_file_name,
    validate_xml_file_is_unregistered,
    is_updated_xml_file_localid_matching_with_current_resource_localid,
    is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument,
)
from validation.errors import FileRegisteredBefore
from bson.errors import InvalidId
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

env = environ.Env()

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

class OperationalModesValidationTestCase:
    @tag('fast')
    def test_is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(self):
        """
        is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument() returns True.
        """
        with open(self.xml_file_path) as xml_file:
            registered_instrument = register_metadata_xml_file(
                xml_file,
                self.mongodb_model,
                self.fix_conversion_errors_if_any,
            )
            result = is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
                xml_file,
                registered_instrument['_id'],
                mongodb_model=self.mongodb_model
            )
            self.assertEqual(result, True)
            print(f'Passed operational modes test for {Path(xml_file.name).name}.')

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