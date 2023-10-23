import os

from django.test import (
    SimpleTestCase,
    TestCase,
)

from .base_tests import *
from .file_wrappers import (
    AcquisitionCapabilitiesXMLMetadataFile,
    DataSubsetXMLMetadataFile,
    XMLMetadataFile,
)
from .services import (
    MetadataFileXSDValidator,
)
from .url_validation_services import (
    MetadataFileOntologyURLReferencesValidator,
    MetadataFileMetadataURLReferencesValidator,
)

from common.models import (
    Organisation,
    Catalogue,
)
from pithiaesc.settings import BASE_DIR
from utils.url_helpers import divide_catalogue_related_resource_url_into_main_components

_TEST_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files')
_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.

class OrganisationSyntaxValidationTestCase(OrganisationFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class OrganisationRootElementValidationTestCase(OrganisationFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class OrganisationXSDValidationTestCase(OrganisationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class OrganisationFileNameValidationTestCase(OrganisationFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class OrganisationNewRegistrationValidationTestCase(OrganisationFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class OrganisationUpdateValidationTestCase(OrganisationFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class OrganisationValidationChecklistTestCase(OrganisationFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class IndividualSyntaxValidationTestCase(IndividualFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class IndividualRootElementValidationTestCase(IndividualFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class IndividualXSDValidationTestCase(IndividualFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class IndividualFileNameValidationTestCase(IndividualFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class IndividualNewRegistrationValidationTestCase(IndividualFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class IndividualUpdateValidationTestCase(IndividualFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class IndividualValidationChecklistTestCase(IndividualFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class ProjectSyntaxValidationTestCase(ProjectFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ProjectRootElementValidationTestCase(ProjectFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class ProjectXSDValidationTestCase(ProjectFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ProjectFileNameValidationTestCase(ProjectFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class ProjectNewRegistrationValidationTestCase(ProjectFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ProjectUpdateValidationTestCase(ProjectFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ProjectValidationChecklistTestCase(ProjectFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class PlatformSyntaxValidationTestCase(PlatformFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class PlatformRootElementValidationTestCase(PlatformFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class PlatformXSDValidationTestCase(PlatformFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class PlatformFileNameValidationTestCase(PlatformFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class PlatformNewRegistrationValidationTestCase(PlatformFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class PlatformUpdateValidationTestCase(PlatformFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class PlatformValidationChecklistTestCase(PlatformFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class OperationSyntaxValidationTestCase(OperationFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class OperationRootElementValidationTestCase(OperationFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class OperationXSDValidationTestCase(OperationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class OperationFileNameValidationTestCase(OperationFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class OperationNewRegistrationValidationTestCase(OperationFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class OperationUpdateValidationTestCase(OperationFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class OperationValidationChecklistTestCase(OperationFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class InstrumentSyntaxValidationTestCase(InstrumentFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class InstrumentRootElementValidationTestCase(InstrumentFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class InstrumentXSDValidationTestCase(InstrumentFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class InstrumentFileNameValidationTestCase(InstrumentFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class InstrumentNewRegistrationValidationTestCase(InstrumentFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class InstrumentUpdateValidationTestCase(InstrumentFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class InstrumentValidationChecklistTestCase(InstrumentFileTestCase, ValidationChecklistTestCase, TestCase):
    pass
class InstrumentOperationalModesValidationTestCase(InstrumentFileTestCase, OperationalModesValidationTestCase, TestCase):
    pass


class AcquisitionCapabilitiesSyntaxValidationTestCase(AcquisitionCapabilitiesFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesRootElementValidationTestCase(AcquisitionCapabilitiesFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesXSDValidationTestCase(AcquisitionCapabilitiesFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesFileNameValidationTestCase(AcquisitionCapabilitiesFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesNewRegistrationValidationTestCase(AcquisitionCapabilitiesFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesUpdateValidationTestCase(AcquisitionCapabilitiesFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesValidationChecklistTestCase(AcquisitionCapabilitiesFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class AcquisitionSyntaxValidationTestCase(AcquisitionFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class AcquisitionRootElementValidationTestCase(AcquisitionFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class AcquisitionXSDValidationTestCase(AcquisitionFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class AcquisitionFileNameValidationTestCase(AcquisitionFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class AcquisitionNewRegistrationValidationTestCase(AcquisitionFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class AcquisitionUpdateValidationTestCase(AcquisitionFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class AcquisitionValidationChecklistTestCase(AcquisitionFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class ComputationCapabilitiesSyntaxValidationTestCase(ComputationCapabilitiesFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesRootElementValidationTestCase(ComputationCapabilitiesFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesXSDValidationTestCase(ComputationCapabilitiesFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesFileNameValidationTestCase(ComputationCapabilitiesFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesNewRegistrationValidationTestCase(ComputationCapabilitiesFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesUpdateValidationTestCase(ComputationCapabilitiesFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesValidationChecklistTestCase(ComputationCapabilitiesFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class ComputationSyntaxValidationTestCase(ComputationFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ComputationRootElementValidationTestCase(ComputationFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class ComputationXSDValidationTestCase(ComputationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ComputationFileNameValidationTestCase(ComputationFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class ComputationNewRegistrationValidationTestCase(ComputationFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ComputationUpdateValidationTestCase(ComputationFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ComputationValidationChecklistTestCase(ComputationFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class ProcessSyntaxValidationTestCase(ProcessFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ProcessRootElementValidationTestCase(ProcessFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class ProcessXSDValidationTestCase(ProcessFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ProcessFileNameValidationTestCase(ProcessFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class ProcessNewRegistrationValidationTestCase(ProcessFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ProcessUpdateValidationTestCase(ProcessFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ProcessValidationChecklistTestCase(ProcessFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class DataCollectionSyntaxValidationTestCase(DataCollectionFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class DataCollectionRootElementValidationTestCase(DataCollectionFileTestCase, RootElementValidationTestCase, TestCase):
    pass
class DataCollectionXSDValidationTestCase(DataCollectionFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class DataCollectionFileNameValidationTestCase(DataCollectionFileTestCase, FileNameValidationTestCase, TestCase):
    pass
class DataCollectionNewRegistrationValidationTestCase(DataCollectionFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class DataCollectionUpdateValidationTestCase(DataCollectionFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class DataCollectionValidationChecklistTestCase(DataCollectionFileTestCase, ValidationChecklistTestCase, TestCase):
    pass


class UrlValidationTestCase(SimpleTestCase):
    def test_is_ontology_term_url_valid(self):
        """
        MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid() returns an
        True if valid and False if not.
        """
        valid_ontology_url_1 = 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider'
        valid_ontology_url_2 = 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/ViewOnly'
        invalid_ontology_url_1 = 'https://metadata.pithia.eu/ontology/2.2/invalid/test'
        invalid_ontology_url_2 = 'https://metadata.pithia.eu/ontology/2.2/serviceFunction/DataProvider'

        print(MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid(valid_ontology_url_1))
        self.assertEquals(MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid(valid_ontology_url_1), True)
        self.assertEquals(MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid(valid_ontology_url_2), True)
        self.assertEquals(MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid(invalid_ontology_url_1), False)
        self.assertEquals(MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid(invalid_ontology_url_2), False)

    def test_is_resource_url_structure_valid_with_invalid_urls(self):
        """
        MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid() returns
        False for all URLs provided for this test.
        """

        blank_string_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('')
        swapped_namespace_and_resource_type_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        random_string_result_1 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('////')
        random_string_result_2 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('///')
        random_string_result_3 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('//')
        random_string_result_4 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('/')
        non_resource_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('http://www.google')
        http_resource_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('http://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        no_url_protocol_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        domain_name_duplication_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        acquisition_capability_sets_incorrect_casing_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/AcquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        computation_capability_sets_incorrect_casing_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/ComputationCapabilities/pithia/AcquisitionCapabilities_TEST')
        invalid_individual_url_result_1 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/abc/individual/Individual_ABC_123')
        invalid_individual_url_result_2 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/abc/individual/Individual_ABC_123')
        invalid_individual_url_result_3 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/individual/abc/Individual_ABC_123')
        invalid_individual_url_result_4 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/individual/abc/Individual_ABC_123')

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
        self.assertEquals(invalid_individual_url_result_1, False)
        self.assertEquals(invalid_individual_url_result_2, False)
        self.assertEquals(invalid_individual_url_result_3, False)
        self.assertEquals(invalid_individual_url_result_4, False)

    def test_is_resource_url_structure_valid_with_valid_urls(self):
        """
        MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid() returns
        True for all URLs provided for this test.
        """

        valid_organisation_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        valid_individual_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/individual/pithia/Individual_TEST')
        valid_project_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        valid_platform_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/platform/pithia/Platform_TEST')
        valid_operation_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/operation/pithia/Operation_TEST')
        valid_instrument_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_TEST')
        valid_aqcuisition_capabilities_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        valid_acquisition_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisition/pithia/Acquisition_TEST')
        valid_computation_capability_sets_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_TEST')
        valid_computation_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computation/pithia/Computation_TEST')
        valid_process_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/process/pithia/CompositeProcess_TEST')
        valid_data_collection_url_result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/collection/pithia/DataCollection_TEST')

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


class CatalogueUrlValidationTestCase(SimpleTestCase):
    def test_catalogue_url_splitting_function(self):
        """
        Test divide_catalogue_related_resource_url_into_main_components
        returns the expected main URL components.
        catalogue/namespace/Event?/Catalogue metadata type (i.e. Catalogue, CatalogueEntry, CatalogueDataSubset)
        """
        catalogue_resource_url = 'https://metadata.pithia.eu/resources/2.2/catalogue/pithia/VolcanoEruption/Catalogue_VolcanoEruption'
        catalogue_resource_url_components = divide_catalogue_related_resource_url_into_main_components(catalogue_resource_url)
        catalogue_url_base = catalogue_resource_url_components['url_base']
        catalogue_url_resource_type = catalogue_resource_url_components['resource_type']
        catalogue_url_namespace = catalogue_resource_url_components['namespace']
        catalogue_url_event = catalogue_resource_url_components['event']
        catalogue_url_localid = catalogue_resource_url_components['localid']

        print('catalogue_resource_url_components', catalogue_resource_url_components)
        self.assertEquals(catalogue_url_base, 'https://metadata.pithia.eu/resources/2.2')
        self.assertEquals(catalogue_url_resource_type, 'catalogue')
        self.assertEquals(catalogue_url_namespace, 'pithia')
        self.assertEquals(catalogue_url_event, 'VolcanoEruption')
        self.assertEquals(catalogue_url_localid, 'Catalogue_VolcanoEruption')

    def test_valid_catalogue_related_resource_url_structure_validation(self):
        """
        MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid() returns
        True for all the resource urls provided below.
        """
        catalogue_resource_url = 'https://metadata.pithia.eu/resources/2.2/catalogue/pithia/VolcanoEruption/Catalogue_VolcanoEruption'

        self.assertEquals(MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid(catalogue_resource_url), True)

    def test_invalid_catalogue_related_resource_url_structure_validation(self):
        """
        MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid() returns
        True for all the resource urls provided below.
        """
        catalogue_resource_url_collection_as_resource_type = 'https://metadata.pithia.eu/resources/2.2/collection/pithia/VolcanoEruption/Catalogue_VolcanoEruption'
        catalogue_resource_url_double_namespace = 'https://metadata.pithia.eu/resources/2.2/catalogue/pithia/pithia/VolcanoEruption/Catalogue_VolcanoEruption'
        catalogue_resource_url_double_resource_type = 'https://metadata.pithia.eu/resources/2.2/catalogue/catalogue/pithia/VolcanoEruption/Catalogue_VolcanoEruption'

        self.assertEquals(MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid(catalogue_resource_url_collection_as_resource_type), False)
        self.assertEquals(MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid(catalogue_resource_url_double_namespace), False)
        self.assertEquals(MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid(catalogue_resource_url_double_resource_type), False)


class DoiValidationTestCase(SimpleTestCase):
    def test_contents_with_spoofed_doi(self):
        """
        DataSubsetXMLMetadataFile.contents returns an XML string with a DOI XMLSchema-
        compliant element.
        """
        xml_file = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as test_file:
            xml_file = DataSubsetXMLMetadataFile.from_file(test_file)
        print('xml_file.contents', xml_file.contents)
        self.assertTrue('10.000' in xml_file.contents)

    def test_data_subset_xsd_validation(self):
        """
        XML Catalogue Data Subset XSD validation passes DOI XML Schema validation with
        a spoofed DOI element.
        """
        xml_file = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as test_file:
            xml_file = DataSubsetXMLMetadataFile.from_file(test_file)
        MetadataFileXSDValidator.validate(xml_file)


class URLReferencesValidatorTestCase(TestCase):
    def setUp(self) -> None:
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_string = xml_file.read()
            self.xml_metadata_file_with_invalid_urls = XMLMetadataFile(xml_file_string, xml_file.name)
        return super().setUp()

    def test_is_each_resource_url_valid_on_individual(self):
        """
        MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid()
        returns a dict where each value is a list of invalid resource URLs.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            Organisation.objects.create_from_xml_string(xml_file.read())
        
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Individual_Test.xml')) as xml_file:
            invalid_resource_urls_dict = MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid(XMLMetadataFile.from_file(xml_file))
            print('invalid_resource_urls_dict', invalid_resource_urls_dict)
            for value in invalid_resource_urls_dict.values():
                self.assertTrue(len(value) == 0)

    def test_is_each_resource_url_valid_on_catalogue_entry(self):
        """
        MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid()
        returns a dict where each value is a list of invalid resource URLs.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Catalogue_Test.xml')) as xml_file:
            Catalogue.objects.create_from_xml_string(xml_file.read())
        
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'CatalogueEntry_Test_2023-01-01.xml')) as xml_file:
            invalid_resource_urls_dict = MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid(XMLMetadataFile.from_file(xml_file))
            for value in invalid_resource_urls_dict.values():
                self.assertTrue(len(value) == 0)

    def test_invalid_ontology_urls_are_detected(self):
        """
        MetadataFileOntologyURLReferencesValidator.is_each_ontology_url_in_xml_file_valid()
        returns a list of invalid ontology URLs.
        """
        invalid_ontology_urls = MetadataFileOntologyURLReferencesValidator.is_each_ontology_url_in_xml_file_valid(self.xml_metadata_file_with_invalid_urls)
        self.assertEquals(len(invalid_ontology_urls), 1)

    def test_invalid_resource_urls_are_detected(self):
        """
        MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid()
        returns a dict where each value is a list of invalid resource URLs.
        """
        invalid_resource_urls = MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid(self.xml_metadata_file_with_invalid_urls)
        self.assertEquals(len(invalid_resource_urls['urls_pointing_to_unregistered_resources']), 2)

    def test_invalid_resource_urls_with_op_mode_ids_are_detected(self):
        """
        MetadataFileMetadataURLReferencesValidator.is_each_operational_mode_url_valid()
        returns a dict where each value is a list of invalid operational mode URLs.
        """
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_string = xml_file.read()
            self.xml_metadata_file_with_invalid_urls = AcquisitionCapabilitiesXMLMetadataFile(xml_file_string, xml_file.name)
        
        invalid_resource_urls_with_op_mode_ids = MetadataFileMetadataURLReferencesValidator.is_each_operational_mode_url_valid(self.xml_metadata_file_with_invalid_urls)
        print('invalid_resource_urls_with_op_mode_ids', invalid_resource_urls_with_op_mode_ids)
        self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_with_incorrect_structure']), 1)
        self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_pointing_to_unregistered_resources']), 1)
        self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_pointing_to_registered_resources_with_missing_op_modes']), 2)

class XMLMetadataFileTestCase(TestCase):
    def test_potential_ontology_urls(self):
        """
        Returns a list of potential ontology URLs.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Project_Test_InvalidDocumentURLs.xml')) as xml_file:
            xml_file_string = xml_file.read()
            self.test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        potential_ontology_urls = self.test_xml_file.potential_ontology_urls
        print('potential_ontology_urls', potential_ontology_urls)
        self.assertTrue(any('http://' in url for url in potential_ontology_urls))
        self.assertTrue(all('metadata.pithia.eu' in url for url in potential_ontology_urls))
        self.assertTrue(all('metadata.pithia.eu/ontology' in url for url in potential_ontology_urls))
        self.assertTrue(not all('metadata.pithia.eu/ontology/2.2' in url for url in potential_ontology_urls))
        self.assertTrue(not any('metadata.pithia.eu/resources' in url for url in potential_ontology_urls))

    def test_potential_metadata_urls(self):
        """
        Returns a list of potential metadata URLs.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Project_Test_InvalidDocumentURLs.xml')) as xml_file:
            xml_file_string = xml_file.read()
            self.test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        potential_metadata_urls = self.test_xml_file.potential_metadata_urls
        print('potential_metadata_urls', potential_metadata_urls)
        self.assertTrue(any('http://' in url for url in potential_metadata_urls))
        self.assertTrue(all('metadata.pithia.eu/resources' in url for url in potential_metadata_urls))
        self.assertTrue(not all('metadata.pithia.eu/resources/2.2' in url for url in potential_metadata_urls))
        self.assertTrue(not any('metadata.pithia.eu/ontology' in url for url in potential_metadata_urls))

    def test_potential_operational_mode_urls(self):
        """
        Returns a list of potential operational
        mode URLs.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'AcquisitionCapabilities_Test_InvalidOpModeURLs.xml')) as xml_file:
            xml_file_string = xml_file.read()
            self.test_xml_file = AcquisitionCapabilitiesXMLMetadataFile(xml_file_string, xml_file.name)

        potential_op_mode_urls = self.test_xml_file.potential_operational_mode_urls
        print('potential_op_mode_urls', potential_op_mode_urls)
        self.assertTrue(any('metadata.pithia.eu/resources' in url and '#' in url for url in potential_op_mode_urls))
        self.assertTrue(all('metadata.pithia.eu/resources' in url and '#' in url for url in potential_op_mode_urls))

    def test_is_each_potential_operational_mode_url_valid(self):
        """
        MetadataFileMetadataURLReferencesValidator._is_each_potential_operational_mode_url_valid()
        returns False for all URLs provided for this test.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'AcquisitionCapabilities_Test_InvalidOpModeURLs.xml')) as xml_file:
            xml_file_string = xml_file.read()
            self.test_xml_file = AcquisitionCapabilitiesXMLMetadataFile(xml_file_string, xml_file.name)

        validation_results = MetadataFileMetadataURLReferencesValidator.is_each_potential_operational_mode_url_valid(self.test_xml_file)
        self.assertEqual(len(validation_results['urls_with_incorrect_structure']), 1)