import os
from django.test import tag
from lxml.etree import XMLSyntaxError
from pathlib import Path

from .errors import (
    FileRegisteredBefore,
    UpdateFileNotMatching,
)
from .file_wrappers import (
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .services import (
    InstrumentMetadataFileValidator,
    MetadataFileRegistrationValidator,
    MetadataFileXSDValidator,
    MetadataFileUpdateValidator,
)

from common import models
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'


class FileTestCase:
    xml_file_name = ''

    def setUp(self) -> None:
        self.xml_file_path = os.path.join(_XML_METADATA_FILE_DIR, self.xml_file_name)
        return super().setUp()


@tag('organisation')
class OrganisationFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Organisation_Test.xml'
        self.model = models.Organisation
        self.root_element_name = models.Organisation.root_element_name
        return super().setUp()


@tag('individual')
class IndividualFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Individual_Test.xml'
        self.model = models.Individual
        self.root_element_name = models.Individual.root_element_name
        return super().setUp()


@tag('project')
class ProjectFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Project_Test.xml'
        self.model = models.Project
        self.root_element_name = models.Project.root_element_name
        return super().setUp()


@tag('platform')
class PlatformFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Platform_Test.xml'
        self.model = models.Platform
        self.root_element_name = models.Platform.root_element_name
        return super().setUp()


@tag('operation')
class OperationFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Operation_Test.xml'
        self.model = models.Operation
        self.root_element_name = models.Operation.root_element_name
        return super().setUp()


@tag('instrument')
class InstrumentFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Instrument_Test.xml'
        self.model = models.Instrument
        self.root_element_name = models.Instrument.root_element_name
        return super().setUp()


@tag('acquisition_capabilities')
class AcquisitionCapabilitiesFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'AcquisitionCapabilities_Test.xml'
        self.model = models.AcquisitionCapabilities
        self.root_element_name = models.AcquisitionCapabilities.root_element_name
        return super().setUp()


@tag('acquisition')
class AcquisitionFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Acquisition_Test.xml'
        self.model = models.Acquisition
        self.root_element_name = models.Acquisition.root_element_name
        return super().setUp()


@tag('computation_capabilities')
class ComputationCapabilitiesFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'ComputationCapabilities_Test.xml'
        self.model = models.ComputationCapabilities
        self.root_element_name = models.ComputationCapabilities.root_element_name
        return super().setUp()


@tag('computation')
class ComputationFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'Computation_Test.xml'
        self.model = models.Computation
        self.root_element_name = models.Computation.root_element_name
        return super().setUp()


@tag('process')
class ProcessFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'CompositeProcess_Test.xml'
        self.model = models.Process
        self.root_element_name = models.Process.root_element_name
        return super().setUp()


@tag('data_collection')
class DataCollectionFileTestCase(FileTestCase):
    def setUp(self) -> None:
        self.xml_file_name = 'DataCollection_Test.xml'
        self.model = models.DataCollection
        self.root_element_name = models.DataCollection.root_element_name
        return super().setUp()


class SyntaxValidationTestCase:
    @tag('fast', 'syntax')
    def test_xml_metadata_file_init(self):
        """An XMLMetadataFile instance is initialised successfully.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                XMLMetadataFile(xml_file.read(), xml_file.name)
                print(f'Passed XMLMetadataFile init for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('XMLMetadataFile() raised an exception unexpectedly!')

    @tag('fast', 'syntax')
    def test_xml_metadata_file_from_file(self):
        """An XMLMetadataFile instance is initialised successfully
        with XMLMetadataFile.from_file().
        """
        try:
            with open(self.xml_file_path) as xml_file:
                XMLMetadataFile.from_file(xml_file)
                print(f'Passed XMLMetadataFile.from_file() test for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('XMLMetadataFile.from_file() raised an exception unexpectedly!')

    @tag('fast', 'syntax')
    def test_file_with_invalid_syntax(self):
        """The file causes XMLMetadataFile() to raise an etree.XMLSyntaxError exception.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test_InvalidSyntax.xml')) as invalid_xml_file:
            try:
                XMLMetadataFile.from_file(invalid_xml_file)
            except XMLSyntaxError:
                print('Exception raised, as expected!')
            self.assertRaises(XMLSyntaxError, XMLMetadataFile.from_file, invalid_xml_file)


class XSDValidationTestCase:
    @tag('slow', 'xsd')
    def test_validate_against_own_schema(self):
        """MetadataFileXSDValidator.validate() does not raise an exception when
        passed a valid xml file.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                xml_metadata_file = XMLMetadataFile.from_file(xml_file)
            cwd_before_validation = os.getcwd()
            # Temporarily change the cwd to so the XSD
            # validator can see the schema files.
            os.chdir(os.path.join(BASE_DIR, 'validation', 'local_schema_files'))
            MetadataFileXSDValidator.validate(xml_metadata_file)
            print(f'Passed XSD validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('MetadataFileXSDValidator.validate() raised an exception unexpectedly!')
        finally:
            # Change the cwd back as XSD validation is
            # finished.
            os.chdir(cwd_before_validation)


class NewRegistrationValidationTestCase:
    @tag('fast', 'registration')
    def test_registration_validation(self):
        """MetadataFileRegistrationValidator.validate() does not raise an
        exception when passed a valid xml file.
        """
        try:
            with open(self.xml_file_path) as xml_file:
                xml_metadata_file = XMLMetadataFile.from_file(xml_file)
            MetadataFileRegistrationValidator.validate(
                xml_metadata_file,
                self.model
            )
            print(f'Passed new registration validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('MetadataFileRegistrationValidator.validate() raised an exception unexpectedly!')

    @tag('fast', 'registration')
    def test_registration_validation_fails(self):
        """MetadataFileRegistrationValidator.validate() raises an exception
        when passed an xml file that has already been registered.
        """
        xml_file_string = None
        xml_file_name = None
        with open(self.xml_file_path) as xml_file:
            xml_file_string = xml_file.read()
            xml_file_name = xml_file.name
        self.model.objects.create_from_xml_string(xml_file_string, SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        xml_metadata_file = XMLMetadataFile(xml_file_string, xml_file_name)
        self.assertRaises(
            FileRegisteredBefore,
            MetadataFileRegistrationValidator.validate,
            xml_metadata_file,
            self.model
        )
        print(f'Failed registration validation for {Path(xml_file.name).name} successfully.')


class UpdateValidationTestCase:
    @tag('fast', 'update')
    def test_update_validation(self):
        """MetadataFileUpdateValidator.validate() does not raise an exception
        when passed a valid xml_file.
        """
        try:
            xml_file_string = None
            xml_file_name = None
            with open(self.xml_file_path) as xml_file:
                xml_file_string = xml_file.read()
                xml_file_name = xml_file.name
            test_registration = self.model.objects.create_from_xml_string(xml_file_string, SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
            xml_metadata_file = XMLMetadataFile(xml_file_string, xml_file_name)
            MetadataFileUpdateValidator.validate(
                xml_metadata_file,
                self.model,
                test_registration.pk
            )
            print(f'Passed update validation for {Path(xml_file.name).name}.')
        except BaseException:
            self.fail('MetadataFileUpdateValidator.validate() raised an exception unexpectedly!')

    # @tag('fast', 'update')
    # def test_update_validation_failure(self):
    #     """
    #     MetadataFileUpdateValidator.validate() raises an exception when
    #     passed a invalid xml_file.
    #     """
    #     with open(self.xml_file_path) as xml_file:
    #         self.assertRaises(
    #             UpdateFileNotMatching,
    #             MetadataFileUpdateValidator.validate,
    #             xml_file,
    #             self.model,
    #             '',
    #         )
    #         print(f'Failed update validation for {Path(xml_file.name).name} successfully.')


class OperationalModesValidationTestCase:
    @tag('fast', 'opmodes')
    def test_operational_mode_id_validation(self):
        """InstrumentMetadataFileValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument()
        returns a result of True and an empty list with no missing operational mode IDs.
        """
        xml_file_string = None
        xml_file_name = None
        with open(self.xml_file_path) as xml_file:
            xml_file_string = xml_file.read()
            xml_file_name = xml_file.name
        xml_metadata_file = InstrumentXMLMetadataFile(xml_file_string, xml_file_name)
        instrument_registration = self.model.objects.create_from_xml_string(xml_file_string, SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        result, missing_operational_mode_urls = InstrumentMetadataFileValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
            xml_metadata_file,
            instrument_registration.pk,
            self.model
        )
        self.assertEqual(result, True)
        self.assertEqual(len(missing_operational_mode_urls), 0)
        print(f'Passed operational modes test for {Path(xml_file.name).name}.')

    @tag('fast', 'opmodes')
    def test_new_operational_mode_ids_with_validation(self):
        """InstrumentMetadataFileValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument() returns
        True when new operational modes are added and an empty list with no missing operational mode IDs.
        """
        test_registration = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Instrument_Test_NoOpModes.xml')) as xml_file:
            test_registration = self.model.objects.create_from_xml_string(xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
            
        xml_file_string = None
        xml_file_name = None
        with open(self.xml_file_path) as xml_file:
            xml_file_string = xml_file.read()
            xml_file_name = xml_file.name
        xml_metadata_file = InstrumentXMLMetadataFile(xml_file_string, xml_file_name)
        result, missing_operational_mode_urls = InstrumentMetadataFileValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
            xml_metadata_file,
            test_registration.pk,
            self.model
        )
        self.assertEqual(result, True)
        self.assertEqual(len(missing_operational_mode_urls), 0)
        print('Passed test_new_operational_mode_ids_with_validation() test.')

    @tag('fast', 'opmodes')
    def test_removal_of_operational_mode_ids_with_validation(self):
        """InstrumentMetadataFileValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument() returns
        Falsee when new operational modes are added and a list of missing operational mode IDs.
        """
        test_registration = None
        with open(self.xml_file_path) as xml_file:
            test_registration = self.model.objects.create_from_xml_string(xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
            
        xml_file_string = None
        xml_file_name = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Instrument_Test_NoOpModes.xml')) as xml_file:
            xml_file_string = xml_file.read()
            xml_file_name = xml_file.name
        xml_metadata_file = InstrumentXMLMetadataFile(xml_file_string, xml_file_name)
        result, missing_operational_mode_urls = InstrumentMetadataFileValidator.is_each_operational_mode_id_in_current_instrument_present_in_updated_instrument(
            xml_metadata_file,
            test_registration.pk,
            self.model
        )
        print('result', result)
        print('missing_operational_mode_urls', missing_operational_mode_urls)
        self.assertEqual(result, False)
        self.assertTrue(len(missing_operational_mode_urls) > 0)
        print('Passed test_removal_of_operational_mode_ids_with_validation() test.')
