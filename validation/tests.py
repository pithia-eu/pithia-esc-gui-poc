from django.test import (
    SimpleTestCase,
    TestCase,
)
from xmlschema.validators.exceptions import XMLSchemaValidationError

from .base_tests import *
from .file_wrappers import (
    AcquisitionCapabilitiesXMLMetadataFile,
    DataSubsetXMLMetadataFile,
    XMLMetadataFile,
)
from .services import (
    InstrumentMetadataFileValidator,
    MetadataFileRegistrationValidator,
    MetadataFileUpdateValidator,
    MetadataFileXSDValidator,
)
from .url_validation_services import (
    MetadataFileOntologyURLReferencesValidator,
    MetadataFileMetadataURLReferencesValidator,
)

from common import test_xml_files
from common.models import (
    DataCollection,
    Organisation,
    ScientificMetadata,
    StaticDatasetEntry,
)
from common.test_setup import (
    register_instrument_for_test,
    register_organisation_for_test,
)
from utils.url_helpers import divide_static_dataset_related_resource_url_into_main_components

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'
# Create your tests here.


# Syntax validation tests, based on metadata type.
class OrganisationSyntaxValidationTestCase(OrganisationFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class IndividualSyntaxValidationTestCase(IndividualFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ProjectSyntaxValidationTestCase(ProjectFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class PlatformSyntaxValidationTestCase(PlatformFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class OperationSyntaxValidationTestCase(OperationFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class InstrumentSyntaxValidationTestCase(InstrumentFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesSyntaxValidationTestCase(AcquisitionCapabilitiesFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class AcquisitionSyntaxValidationTestCase(AcquisitionFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesSyntaxValidationTestCase(ComputationCapabilitiesFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ComputationSyntaxValidationTestCase(ComputationFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class ProcessSyntaxValidationTestCase(ProcessFileTestCase, SyntaxValidationTestCase, TestCase):
    pass
class DataCollectionSyntaxValidationTestCase(DataCollectionFileTestCase, SyntaxValidationTestCase, TestCase):
    pass


# XSD validation tests, based on metadata type.
class OrganisationXSDValidationTestCase(OrganisationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class IndividualXSDValidationTestCase(IndividualFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ProjectXSDValidationTestCase(ProjectFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class PlatformXSDValidationTestCase(PlatformFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class OperationXSDValidationTestCase(OperationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class InstrumentXSDValidationTestCase(InstrumentFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesXSDValidationTestCase(AcquisitionCapabilitiesFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class AcquisitionXSDValidationTestCase(AcquisitionFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesXSDValidationTestCase(ComputationCapabilitiesFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ComputationXSDValidationTestCase(ComputationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ProcessXSDValidationTestCase(ProcessFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class DataCollectionXSDValidationTestCase(DataCollectionFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass


# New registration check tests, based on metadata type.
class OrganisationNewRegistrationValidationTestCase(OrganisationFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class IndividualNewRegistrationValidationTestCase(IndividualFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ProjectNewRegistrationValidationTestCase(ProjectFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class PlatformNewRegistrationValidationTestCase(PlatformFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class OperationNewRegistrationValidationTestCase(OperationFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class InstrumentNewRegistrationValidationTestCase(InstrumentFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesNewRegistrationValidationTestCase(AcquisitionCapabilitiesFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class AcquisitionNewRegistrationValidationTestCase(AcquisitionFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesNewRegistrationValidationTestCase(ComputationCapabilitiesFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ComputationNewRegistrationValidationTestCase(ComputationFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class ProcessNewRegistrationValidationTestCase(ProcessFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass
class DataCollectionNewRegistrationValidationTestCase(DataCollectionFileTestCase, NewRegistrationValidationTestCase, TestCase):
    pass


# Update (matching localID and namespace) check tests, based on metadata type.
class OrganisationUpdateValidationTestCase(OrganisationFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class IndividualUpdateValidationTestCase(IndividualFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ProjectUpdateValidationTestCase(ProjectFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class PlatformUpdateValidationTestCase(PlatformFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class OperationUpdateValidationTestCase(OperationFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class InstrumentUpdateValidationTestCase(InstrumentFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class AcquisitionCapabilitiesUpdateValidationTestCase(AcquisitionCapabilitiesFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class AcquisitionUpdateValidationTestCase(AcquisitionFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ComputationCapabilitiesUpdateValidationTestCase(ComputationCapabilitiesFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ComputationUpdateValidationTestCase(ComputationFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class ProcessUpdateValidationTestCase(ProcessFileTestCase, UpdateValidationTestCase, TestCase):
    pass
class DataCollectionUpdateValidationTestCase(DataCollectionFileTestCase, UpdateValidationTestCase, TestCase):
    pass


# Instrument-specific validation test
class InstrumentOperationalModesValidationTestCase(InstrumentFileTestCase, OperationalModesValidationTestCase, TestCase):
    pass


@tag('slow')
class OntologyUrlValidationTestCase(SimpleTestCase):
    def test_valid_ontology_url_passes(self):
        """Valid ontology URLs pass validation.
        """
        result_1 = MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid('https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider')
        result_2 = MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid('https://metadata.pithia.eu/ontology/2.2/serviceFunction/ViewOnly')
        self.assertTrue(result_1)
        self.assertTrue(result_2)

    def test_non_existant_ontology_terms_are_detected(self):
        """URLs not corresponding to any terms in the Space
        Physics Ontology fail validation.
        """
        result_1 = MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid('https://metadata.pithia.eu/ontology/2.2/invalid/test')
        result_2 = MetadataFileOntologyURLReferencesValidator._is_ontology_term_url_valid('https://metadata.pithia.eu/ontology/2.2/serviceFunction/DataProvider')

        self.assertFalse(result_1)
        self.assertFalse(result_2)


class InvalidMetadataUrlStructureValidationTestCase(SimpleTestCase):
    def test_blank_string_fails(self):
        """A blank string fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('')
        self.assertFalse(result)

    def test_url_with_namespace_and_resource_type_swapped_fails(self):
        """A metadata URL with the namespace and resource
        type in the wrong locations fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        self.assertFalse(result)

    def test_just_forward_slashes_fails(self):
        """A metadata URL containing just '/' fails
        validation.
        """
        result_1 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('////')
        result_2 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('///')
        result_3 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('//')
        result_4 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('/')
        self.assertFalse(result_1)
        self.assertFalse(result_2)
        self.assertFalse(result_3)
        self.assertFalse(result_4)

    def test_incorrectly_formatted_url_fails(self):
        """A metadata URL that is not correctly
        formatted fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('http://www.google')
        self.assertFalse(result)

    def test_http_url_fails(self):
        """A metadata URL using HTTP instead of
        HTTPS fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('http://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        self.assertFalse(result)

    def test_url_with_no_protocol_fails(self):
        """A metadata URL that hasn't specified
        a protocol fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        self.assertFalse(result)

    def test_metadata_url_with_duplicate_domain_fails(self):
        """A metadata URL with the domain duplicated
        multiple times fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        self.assertFalse(result)

    def test_wrong_acquisition_capabilities_casing_fails(self):
        """A metadata URL using the wrong casing for
        'acquisitionCapabilities' fails.
        """
        result_1 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/AcquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        result_2 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisitioncapabilities/pithia/AcquisitionCapabilities_TEST')
        result_3 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/ACQUISITIONCAPABILITIES/pithia/AcquisitionCapabilities_TEST')
        self.assertFalse(result_1)
        self.assertFalse(result_2)
        self.assertFalse(result_3)

    def test_wrong_computation_capabilities_casing_fails(self):
        """A metadata URL using the wrong casing for
        'computationCapabilities' fails.
        """
        result_1 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/ComputationCapabilities/pithia/ComputationCapabilities_TEST')
        result_2 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computationcapabilities/pithia/ComputationCapabilities_TEST')
        result_3 = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/COMPUTATIONCAPABILITIES/pithia/ComputationCapabilities_TEST')
        self.assertFalse(result_1)
        self.assertFalse(result_2)
        self.assertFalse(result_3)

    def test_no_metadata_version_fails(self):
        """A metadata URL that doesn't contain
        the version number fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/individual/abc/Individual_ABC_123')
        self.assertFalse(result)

    def test_multiple_errors_fails(self):
        """A metadata URL containing multiple
        errors fails validation.
        """
        # Missing the '2.2' part with swapped namespace and resource type.
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/abc/individual/Individual_ABC_123')
        self.assertFalse(result)

    def test_collection_resource_type_in_static_dataset_metadata_url_fails(self):
        """A static dataset entry metadata URL with 'collection'
        as the resource type fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/collection/pithia/VolcanoEruption/StaticDatasetEntry_VolcanoEruption')
        self.assertFalse(result)
    
    def test_multiple_namespaces_in_static_dataset_metadata_url_fails(self):
        """A static dataset entry metadata URL with multiple
        namespaces fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/staticDataset/pithia/pithia/VolcanoEruption/StaticDatasetEntry_VolcanoEruption')
        self.assertFalse(result)
    
    def test_multiple_resource_types_in_static_dataset_metadata_url_fails(self):
        """A static dataset entry metadata URL with multiple
        resource types fails validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/staticDataset/staticDataset/pithia/VolcanoEruption/StaticDatasetEntry_VolcanoEruption')
        self.assertFalse(result)


class ValidMetadataUrlStructureValidationTestCase(SimpleTestCase):
    def test_valid_organisation_metadata_url_passes(self):
        """A valid organisation metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        self.assertTrue(result)

    def test_valid_individual_metadata_url_passes(self):
        """A valid individual metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/individual/pithia/Individual_TEST')
        self.assertTrue(result)

    def test_valid_project_metadata_url_passes(self):
        """A valid project metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        self.assertTrue(result)

    def test_valid_platform_metadata_url_passes(self):
        """A valid platform metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/platform/pithia/Platform_TEST')
        self.assertTrue(result)

    def test_valid_operation_metadata_url_passes(self):
        """A valid operation metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/operation/pithia/Operation_TEST')
        self.assertTrue(result)

    def test_valid_instrument_metadata_url_passes(self):
        """A valid instrument metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_TEST')
        self.assertTrue(result)

    def test_valid_acquisition_capabilities_metadata_url_passes(self):
        """A valid acquisition capabilities metadata
        URL passes validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        self.assertTrue(result)

    def test_valid_acquisition_metadata_url_passes(self):
        """A valid acquisition metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisition/pithia/Acquisition_TEST')
        self.assertTrue(result)

    def test_valid_computation_capabilities_metadata_url_passes(self):
        """A valid computation capabilities metadata
        URL passes validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_TEST')
        self.assertTrue(result)

    def test_valid_computation_metadata_url_passes(self):
        """A valid computation metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computation/pithia/Computation_TEST')
        self.assertTrue(result)

    def test_valid_process_metadata_url_passes(self):
        """A valid process metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/process/pithia/CompositeProcess_TEST')
        self.assertTrue(result)

    def test_valid_data_collection_metadata_url_passes(self):
        """A valid data collection metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/collection/pithia/DataCollection_TEST')
        self.assertTrue(result)

    def test_valid_static_dataset_entry_metadata_url_passes(self):
        """A valid static dataset entry metadata URL passes
        validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/staticDataset/test/Test/StaticDatasetEntry_Test')
        self.assertTrue(result)

    def test_valid_data_subset_metadata_url_passes(self):
        """A valid data subset metadata URL passes validation.
        """
        result = MetadataFileMetadataURLReferencesValidator._is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/staticDataset/test/Test/DataSubset_Test')
        self.assertTrue(result)


class StaticDatasetMetadataUrlSplittingFunctionTestCase(SimpleTestCase):
    def test_static_dataset_entry_metadata_url_splits_correctly(self):
        """A static dataset-related metadata URL is split up into
        its components correctly.
        """
        # A static dataset-related metadata URL should have the following structure:
        # "staticDataset/<namespace>/<Event>/<localid>" (i.e. StaticDatasetEntry,
        # DataSubset).
        static_dataset_entry_resource_url = 'https://metadata.pithia.eu/resources/2.2/staticDataset/pithia/VolcanoEruption/StaticDatasetEntry_VolcanoEruption'
        static_dataset_entry_resource_url_components = divide_static_dataset_related_resource_url_into_main_components(static_dataset_entry_resource_url)
        static_dataset_entry_url_base = static_dataset_entry_resource_url_components['url_base']
        static_dataset_entry_url_resource_type = static_dataset_entry_resource_url_components['resource_type']
        static_dataset_entry_url_namespace = static_dataset_entry_resource_url_components['namespace']
        static_dataset_entry_url_event = static_dataset_entry_resource_url_components['event']
        static_dataset_entry_url_localid = static_dataset_entry_resource_url_components['localid']

        self.assertEquals(static_dataset_entry_url_base, 'https://metadata.pithia.eu/resources/2.2')
        self.assertEquals(static_dataset_entry_url_resource_type, 'staticDataset')
        self.assertEquals(static_dataset_entry_url_namespace, 'pithia')
        self.assertEquals(static_dataset_entry_url_event, 'VolcanoEruption')
        self.assertEquals(static_dataset_entry_url_localid, 'StaticDatasetEntry_VolcanoEruption')


class DoiValidationTestCase(SimpleTestCase):
    @tag('slow')
    def test_data_subset_with_handle_fails(self):
        """Data subset validation fails with a handle in the
        DOI metadata kernel element.
        """
        xml_file = XMLMetadataFile.from_file(test_xml_files.DATA_SUBSET_WITH_HANDLE_METADATA_XML)
        self.assertRaises(XMLSchemaValidationError, MetadataFileXSDValidator.validate, xml_file)

    def test_contents_with_spoofed_doi(self):
        """DataSubsetXMLMetadataFile.contents returns an XML string with a DOI XMLSchema-
        compliant element.
        """
        xml_file = DataSubsetXMLMetadataFile.from_file(test_xml_files.DATA_SUBSET_WITH_DOI_METADATA_XML)
        self.assertTrue('10.000' in xml_file.contents)

    @tag('slow')
    def test_data_subset_xsd_validation(self):
        """XML Data Subset XSD validation passes DOI XML Schema validation with
        a spoofed DOI element.
        """
        xml_file = DataSubsetXMLMetadataFile.from_file(test_xml_files.DATA_SUBSET_WITH_DOI_METADATA_XML)
        MetadataFileXSDValidator.validate(xml_file)


class XMLMetadataFileIntegrationTestCase(TestCase):
    def setUp(self) -> None:
        xml_file = test_xml_files.METADATA_AND_ONTOLOGY_URLS_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        self.xml_metadata_file_with_invalid_urls = XMLMetadataFile(xml_file_string, xml_file.name)
        return super().setUp()

    def test_no_invalid_metadata_urls_found_within_valid_file(self):
        """The validator returns no invalid metadata URLs when validating
        a valid data collection-related metadata file.
        """
        organisation_xml_file = test_xml_files.ORGANISATION_METADATA_XML
        organisation_xml_file.seek(0)
        Organisation.objects.create_from_xml_string(organisation_xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        
        individual_xml_file = test_xml_files.INDIVIDUAL_METADATA_XML
        invalid_resource_urls_dict = MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid(
            XMLMetadataFile.from_file(individual_xml_file)
        )
        for key in invalid_resource_urls_dict.keys():
            self.assertEqual(len(invalid_resource_urls_dict[key]), 0)

    def test_no_invalid_metadata_urls_found_within_valid_static_dataset_related_file(self):
        """The validator returns no invalid metadata URLs when validating
        a valid static dataset-related metadata file.
        """
        data_collection_xml_file = test_xml_files.DATA_COLLECTION_METADATA_XML
        data_collection_xml_file.seek(0)
        DataCollection.objects.create_from_xml_string(data_collection_xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        static_dataset_entry_xml_file = test_xml_files.STATIC_DATASET_ENTRY_METADATA_XML
        static_dataset_entry_xml_file.seek(0)
        StaticDatasetEntry.objects.create_from_xml_string(static_dataset_entry_xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        
        data_subset_xml_file = test_xml_files.DATA_SUBSET_METADATA_XML
        invalid_resource_urls_dict = MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid(
            XMLMetadataFile.from_file(data_subset_xml_file)
        )
        for key in invalid_resource_urls_dict.keys():
            self.assertEqual(len(invalid_resource_urls_dict[key]), 0)

    @tag('slow')
    def test_invalid_ontology_urls_in_file_are_found(self):
        """The validator returns invalid ontology URLs
        within a metadata file.
        """
        invalid_ontology_urls = MetadataFileOntologyURLReferencesValidator.is_each_ontology_url_in_xml_file_valid(
            self.xml_metadata_file_with_invalid_urls
        )
        self.assertEquals(len(invalid_ontology_urls), 1)

    def test_invalid_resource_urls_in_file_are_found(self):
        """The validator returns invalid metadata files
        from a metadata file.
        """
        invalid_resource_urls = MetadataFileMetadataURLReferencesValidator.is_each_resource_url_valid(
            self.xml_metadata_file_with_invalid_urls
        )
        self.assertEquals(len(invalid_resource_urls['urls_pointing_to_unregistered_resources']), 2)

    def test_invalid_op_mode_urls_in_file_are_found(self):
        """The validator returns lists of invalid operational
        mode URLs sorted into categories.
        """
        xml_file = test_xml_files.METADATA_AND_ONTOLOGY_URLS_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        self.xml_metadata_file_with_invalid_urls = AcquisitionCapabilitiesXMLMetadataFile(xml_file_string, xml_file.name)
        
        invalid_resource_urls_with_op_mode_ids = MetadataFileMetadataURLReferencesValidator.is_each_operational_mode_url_valid(self.xml_metadata_file_with_invalid_urls)
        self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_with_incorrect_structure']), 1)
        self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_pointing_to_unregistered_resources']), 1)
        self.assertEquals(len(invalid_resource_urls_with_op_mode_ids['urls_pointing_to_registered_resources_with_missing_op_modes']), 2)


class XMLMetadataFileTestCase(TestCase):
    def test_potential_ontology_urls_are_retrieved_correctly(self):
        """Returns a list of potential ontology URLs.
        """
        xml_file = test_xml_files.PROJECT_METADATA_WITH_INVALID_METADATA_URLS_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        self.test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        potential_ontology_urls = self.test_xml_file.potential_ontology_urls
        self.assertTrue(any('http://' in url for url in potential_ontology_urls))
        self.assertTrue(all('metadata.pithia.eu' in url for url in potential_ontology_urls))
        self.assertTrue(all('metadata.pithia.eu/ontology' in url for url in potential_ontology_urls))
        self.assertTrue(not all('metadata.pithia.eu/ontology/2.2' in url for url in potential_ontology_urls))
        self.assertTrue(not any('metadata.pithia.eu/resources' in url for url in potential_ontology_urls))

    def test_potential_metadata_urls_are_retrieved_correctly(self):
        """Returns a list of potential metadata URLs.
        """
        xml_file = test_xml_files.PROJECT_METADATA_WITH_INVALID_METADATA_URLS_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        self.test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        potential_metadata_urls = self.test_xml_file.potential_metadata_urls
        self.assertTrue(any('http://' in url for url in potential_metadata_urls))
        self.assertTrue(all('metadata.pithia.eu/resources' in url for url in potential_metadata_urls))
        self.assertTrue(not all('metadata.pithia.eu/resources/2.2' in url for url in potential_metadata_urls))
        self.assertTrue(not any('metadata.pithia.eu/ontology' in url for url in potential_metadata_urls))

    def test_potential_operational_mode_urls_are_retrieved_correctly(self):
        """Returns a list of potential operational
        mode URLs.
        """
        xml_file = test_xml_files.ACQUISITION_CAPABILITIES_WITH_INVALID_OP_MODE_URLS_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        self.test_xml_file = AcquisitionCapabilitiesXMLMetadataFile(xml_file_string, xml_file.name)

        potential_op_mode_urls = self.test_xml_file.potential_operational_mode_urls
        self.assertTrue(any('metadata.pithia.eu/resources' in url and '#' in url for url in potential_op_mode_urls))
        self.assertTrue(all('metadata.pithia.eu/resources' in url and '#' in url for url in potential_op_mode_urls))

    def test_is_each_potential_operational_mode_url_valid(self):
        """Validator returns lists of invalid opertional
        mode URLs sorted into categories. 
        """
        xml_file = test_xml_files.ACQUISITION_CAPABILITIES_WITH_INVALID_OP_MODE_URLS_METADATA_XML
        xml_file_string = xml_file.read()
        self.test_xml_file = AcquisitionCapabilitiesXMLMetadataFile(xml_file_string, xml_file.name)

        validation_results = MetadataFileMetadataURLReferencesValidator.is_each_potential_operational_mode_url_valid(self.test_xml_file)
        self.assertEqual(len(validation_results['urls_with_incorrect_structure']), 1)

class InlineValidationTestCase(TestCase):
    def test_inline_reference_validation_returns_no_errors(self):
        """Returns errors found whilst validating an XML file's
        references, organised into a dict.
        """
        xml_file = test_xml_files.ORGANISATION_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        results = MetadataFileMetadataURLReferencesValidator.validate_and_return_errors(test_xml_file)
        print('results', results)
        self.assertIs(type(results), dict)
        self.assertFalse(any(results.values()))

    def test_inline_new_registration_validation_returns_errors(self):
        """Returns a list of errors found whilst validating a new XML file
        registration.
        """
        register_organisation_for_test()
        # Attempt to register the same organisation
        # registered at test setup.
        xml_file = test_xml_files.ORGANISATION_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        results = MetadataFileRegistrationValidator.validate_and_return_errors(test_xml_file, ScientificMetadata)
        print('results', results)
        self.assertIs(type(results), list)
        self.assertGreater(len(results), 0)

    def test_inline_new_registration_validation_does_not_return_errors(self):
        """Returns an empty list of errors found whilst validating a new XML file
        registration.
        """
        xml_file = test_xml_files.ORGANISATION_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        results = MetadataFileRegistrationValidator.validate_and_return_errors(test_xml_file, ScientificMetadata)
        print('results', results)
        self.assertIs(type(results), list)
        self.assertEqual(len(results), 0)

    def test_inline_update_validation_returns_errors(self):
        """Returns a list of errors found whilst validating a XML file
        update.
        """
        register_organisation_for_test()
        # Attempt to submit an updated metadata file with a
        # different localID to the one registered.
        xml_file = test_xml_files.ORGANISATION_2_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        results = MetadataFileUpdateValidator.validate_and_return_errors(test_xml_file, ScientificMetadata, "Organisation_Test")
        print('results', results)
        self.assertIs(type(results), list)
        self.assertGreater(len(results), 0)

    def test_inline_update_validation_does_not_return_errors(self):
        """Returns an empty list of errors found whilst validating a XML file
        update.
        """
        register_organisation_for_test()
        xml_file = test_xml_files.ORGANISATION_UPDATED_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = XMLMetadataFile(xml_file_string, xml_file.name)

        results = MetadataFileUpdateValidator.validate_and_return_errors(test_xml_file, ScientificMetadata, "Organisation_Test")
        print('results', results)
        self.assertIs(type(results), list)
        self.assertEqual(len(results), 0)

    def test_inline_instrument_validation_returns_errors(self):
        """Returns a list of errors found whilst validating an instrument XML
        file update.
        """
        register_instrument_for_test()
        # Attempt to submit an updated metadata file with all
        # of the operational modes missing.
        xml_file = test_xml_files.INSTRUMENT_WITH_NO_OP_MODES_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = InstrumentXMLMetadataFile(xml_file_string, xml_file.name)

        results = InstrumentMetadataFileValidator.validate_and_return_errors(test_xml_file, test_xml_file.localid)
        print('results', results)
        self.assertIs(type(results), list)

    def test_inline_instrument_validation_does_not_return_errors(self):
        """Returns an empty list of errors found whilst validating an instrument XML
        file update.
        """
        register_instrument_for_test()
        xml_file = test_xml_files.INSTRUMENT_METADATA_XML
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        test_xml_file = InstrumentXMLMetadataFile(xml_file_string, xml_file.name)

        results = InstrumentMetadataFileValidator.validate_and_return_errors(test_xml_file, test_xml_file.localid)
        print('results', results)
        self.assertIs(type(results), list)

class LocalIDServiceTestCase(TestCase):
    def setUp(self) -> None:
        organisation_xml_file = test_xml_files.ORGANISATION_METADATA_XML
        organisation_xml_file.seek(0)
        self.organisation = Organisation.objects.create_from_xml_string(organisation_xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        return super().setUp()

    def test_is_localid_taken_suggestion(self):
        results = MetadataFileRegistrationValidator.check_if_localid_is_already_in_use_and_return_suggestion_if_taken(self.organisation.localid)
        print('results', results)


@tag('slow')
class AcquisitionCapabilitiesXSDValidationTestCase(SimpleTestCase):
    def test_acquisition_capabilities_with_multiple_imps_fails(self):
        xml_file = AcquisitionCapabilitiesXMLMetadataFile.from_file(test_xml_files.ACQUISITION_CAPABILITIES_MULTIPLE_INSTRUMENT_MODE_PAIRS_METADATA_XML)
        try:
            MetadataFileXSDValidator.validate(xml_file)
        except BaseException as err:
            print(err)
        self.assertRaises(XMLSchemaValidationError, MetadataFileXSDValidator.validate, xml_file)

    def test_acquisition_capabilities_with_multiple_imps_2_fails(self):
        xml_file = AcquisitionCapabilitiesXMLMetadataFile.from_file(test_xml_files.ACQUISITION_CAPABILITIES_MULTIPLE_INSTRUMENT_MODE_PAIRS_2_METADATA_XML)
        try:
            MetadataFileXSDValidator.validate(xml_file)
        except BaseException as err:
            print(err)
        self.assertRaises(XMLSchemaValidationError, MetadataFileXSDValidator.validate, xml_file)