import os

from django.test import SimpleTestCase
from lxml import etree

from .base_tests import *
from .metadata_validation import (
    validate_and_parse_xml_file,
    get_schema_location_url_from_parsed_xml_file,
    validate_xml_with_doi_against_schema_at_url,
)
from .services import (
    DataSubsetXMLMetadataFile,
    MetadataFileXSDValidator,
    XMLMetadataFile,
)
from .url_validation import (
    get_invalid_ontology_urls_from_parsed_xml,
    get_invalid_resource_urls_from_parsed_xml,
    get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml,
    is_catalogue_related_url_structure_valid,
    is_resource_url_base_structure_valid,
    validate_ontology_term_url,
)

from pithiaesc.settings import BASE_DIR
from utils.url_helpers import divide_catalogue_related_resource_url_into_main_components

_TEST_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files')
_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.

class OrganisationSyntaxValidationTestCase(OrganisationFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class OrganisationRootElementValidationTestCase(OrganisationFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class OrganisationXSDValidationTestCase(OrganisationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class OrganisationFileNameValidationTestCase(OrganisationFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class OrganisationNewRegistrationValidationTestCase(OrganisationFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class OrganisationUpdateValidationTestCase(OrganisationFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class OrganisationValidationChecklistTestCase(OrganisationFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class IndividualSyntaxValidationTestCase(IndividualFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class IndividualRootElementValidationTestCase(IndividualFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class IndividualXSDValidationTestCase(IndividualFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class IndividualFileNameValidationTestCase(IndividualFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class IndividualNewRegistrationValidationTestCase(IndividualFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class IndividualUpdateValidationTestCase(IndividualFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class IndividualValidationChecklistTestCase(IndividualFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class ProjectSyntaxValidationTestCase(ProjectFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class ProjectRootElementValidationTestCase(ProjectFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class ProjectXSDValidationTestCase(ProjectFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ProjectFileNameValidationTestCase(ProjectFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class ProjectNewRegistrationValidationTestCase(ProjectFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class ProjectUpdateValidationTestCase(ProjectFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class ProjectValidationChecklistTestCase(ProjectFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class PlatformSyntaxValidationTestCase(PlatformFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class PlatformRootElementValidationTestCase(PlatformFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class PlatformXSDValidationTestCase(PlatformFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class PlatformFileNameValidationTestCase(PlatformFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class PlatformNewRegistrationValidationTestCase(PlatformFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class PlatformUpdateValidationTestCase(PlatformFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class PlatformValidationChecklistTestCase(PlatformFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class OperationSyntaxValidationTestCase(OperationFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class OperationRootElementValidationTestCase(OperationFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class OperationXSDValidationTestCase(OperationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class OperationFileNameValidationTestCase(OperationFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class OperationNewRegistrationValidationTestCase(OperationFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class OperationUpdateValidationTestCase(OperationFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class OperationValidationChecklistTestCase(OperationFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class InstrumentSyntaxValidationTestCase(InstrumentFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class InstrumentRootElementValidationTestCase(InstrumentFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class InstrumentXSDValidationTestCase(InstrumentFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class InstrumentFileNameValidationTestCase(InstrumentFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class InstrumentNewRegistrationValidationTestCase(InstrumentFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class InstrumentUpdateValidationTestCase(InstrumentFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class InstrumentValidationChecklistTestCase(InstrumentFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass
class InstrumentOperationalModesValidationTestCase(InstrumentFileTestCase, OperationalModesValidationTestCase, SimpleTestCase):
    pass


class AcquisitionCapabilitiesSyntaxValidationTestCase(AcquisitionCapabilitiesFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesRootElementValidationTestCase(AcquisitionCapabilitiesFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesXSDValidationTestCase(AcquisitionCapabilitiesFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesFileNameValidationTestCase(AcquisitionCapabilitiesFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesNewRegistrationValidationTestCase(AcquisitionCapabilitiesFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesUpdateValidationTestCase(AcquisitionCapabilitiesFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class AcquisitionCapabilitiesValidationChecklistTestCase(AcquisitionCapabilitiesFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class AcquisitionSyntaxValidationTestCase(AcquisitionFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class AcquisitionRootElementValidationTestCase(AcquisitionFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class AcquisitionXSDValidationTestCase(AcquisitionFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class AcquisitionFileNameValidationTestCase(AcquisitionFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class AcquisitionNewRegistrationValidationTestCase(AcquisitionFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class AcquisitionUpdateValidationTestCase(AcquisitionFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class AcquisitionValidationChecklistTestCase(AcquisitionFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class ComputationCapabilitiesSyntaxValidationTestCase(ComputationCapabilitiesFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesRootElementValidationTestCase(ComputationCapabilitiesFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesXSDValidationTestCase(ComputationCapabilitiesFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesFileNameValidationTestCase(ComputationCapabilitiesFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesNewRegistrationValidationTestCase(ComputationCapabilitiesFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesUpdateValidationTestCase(ComputationCapabilitiesFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class ComputationCapabilitiesValidationChecklistTestCase(ComputationCapabilitiesFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class ComputationSyntaxValidationTestCase(ComputationFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class ComputationRootElementValidationTestCase(ComputationFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class ComputationXSDValidationTestCase(ComputationFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ComputationFileNameValidationTestCase(ComputationFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class ComputationNewRegistrationValidationTestCase(ComputationFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class ComputationUpdateValidationTestCase(ComputationFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class ComputationValidationChecklistTestCase(ComputationFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class ProcessSyntaxValidationTestCase(ProcessFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class ProcessRootElementValidationTestCase(ProcessFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class ProcessXSDValidationTestCase(ProcessFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class ProcessFileNameValidationTestCase(ProcessFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class ProcessNewRegistrationValidationTestCase(ProcessFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class ProcessUpdateValidationTestCase(ProcessFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class ProcessValidationChecklistTestCase(ProcessFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
    pass


class DataCollectionSyntaxValidationTestCase(DataCollectionFileTestCase, SyntaxValidationTestCase, SimpleTestCase):
    pass
class DataCollectionRootElementValidationTestCase(DataCollectionFileTestCase, RootElementValidationTestCase, SimpleTestCase):
    pass
class DataCollectionXSDValidationTestCase(DataCollectionFileTestCase, XSDValidationTestCase, SimpleTestCase):
    pass
class DataCollectionFileNameValidationTestCase(DataCollectionFileTestCase, FileNameValidationTestCase, SimpleTestCase):
    pass
class DataCollectionNewRegistrationValidationTestCase(DataCollectionFileTestCase, NewRegistrationValidationTestCase, SimpleTestCase):
    pass
class DataCollectionUpdateValidationTestCase(DataCollectionFileTestCase, UpdateValidationTestCase, SimpleTestCase):
    pass
class DataCollectionValidationChecklistTestCase(DataCollectionFileTestCase, ValidationChecklistTestCase, SimpleTestCase):
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

    def test_invalid_resource_url_structures_are_detected(self):
        """
        is_resource_url_structure_valid() returns False
        for all URLs provided for this test.
        """

        blank_string_result = is_resource_url_base_structure_valid('')
        swapped_namespace_and_resource_type_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        random_string_result_1 = is_resource_url_base_structure_valid('////')
        random_string_result_2 = is_resource_url_base_structure_valid('///')
        random_string_result_3 = is_resource_url_base_structure_valid('//')
        random_string_result_4 = is_resource_url_base_structure_valid('/')
        non_resource_url_result = is_resource_url_base_structure_valid('http://www.google')
        http_resource_url_result = is_resource_url_base_structure_valid('http://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        no_url_protocol_result = is_resource_url_base_structure_valid('metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        domain_name_duplication_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        acquisition_capability_sets_incorrect_casing_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/AcquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        computation_capability_sets_incorrect_casing_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/ComputationCapabilities/pithia/AcquisitionCapabilities_TEST')

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

        valid_organisation_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        valid_individual_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/individual/pithia/Individual_TEST')
        valid_project_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        valid_platform_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/platform/pithia/Platform_TEST')
        valid_operation_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/operation/pithia/Operation_TEST')
        valid_instrument_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_TEST')
        valid_aqcuisition_capabilities_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        valid_acquisition_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisition/pithia/Acquisition_TEST')
        valid_computation_capability_sets_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_TEST')
        valid_computation_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/computation/pithia/Computation_TEST')
        valid_process_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/process/pithia/CompositeProcess_TEST')
        valid_data_collection_url_result = is_resource_url_base_structure_valid('https://metadata.pithia.eu/resources/2.2/collection/pithia/DataCollection_TEST')

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

class CategoryUrlValidationTestCase(SimpleTestCase):
    def test_category_url_splitting_function(self):
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

    def test_valid_category_related_resource_url_structure_validation(self):
        """
        Test is_catalogue_related_url_structure_valid returns
        True for all the resource urls provided below.
        """
        catalogue_resource_url = 'https://metadata.pithia.eu/resources/2.2/catalogue/pithia/VolcanoEruption/Catalogue_VolcanoEruption'

        self.assertEquals(is_catalogue_related_url_structure_valid(catalogue_resource_url), True)

    def test_invalid_category_related_resource_url_structure_validation(self):
        """
        Test is_catalogue_related_url_structure_valid returns
        True for all the resource urls provided below.
        """
        catalogue_resource_url_collection_as_resource_type = 'https://metadata.pithia.eu/resources/2.2/collection/pithia/VolcanoEruption/Catalogue_VolcanoEruption'
        catalogue_resource_url_double_namespace = 'https://metadata.pithia.eu/resources/2.2/catalogue/pithia/pithia/VolcanoEruption/Catalogue_VolcanoEruption'
        catalogue_resource_url_double_resource_type = 'https://metadata.pithia.eu/resources/2.2/catalogue/catalogue/pithia/VolcanoEruption/Catalogue_VolcanoEruption'

        self.assertEquals(is_catalogue_related_url_structure_valid(catalogue_resource_url_collection_as_resource_type), False)
        self.assertEquals(is_catalogue_related_url_structure_valid(catalogue_resource_url_double_namespace), False)
        self.assertEquals(is_catalogue_related_url_structure_valid(catalogue_resource_url_double_resource_type), False)

class DoiValidationTestCase(SimpleTestCase):
    def test_validate_xml_with_doi_against_schema_at_url(self):
        """
        Test validate_xml_with_doi_against_schema_at_url modifies any referentDoiName
        and registrationAgencyDoiName element text to pass DOI XSD validation. The original
        XML file contents are not modified.
        """
        with open(os.path.join(_TEST_FILE_DIR, 'xml_metadata_files', 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as xml_file:
            parsed_xml_file = validate_and_parse_xml_file(xml_file)
            schema_url = get_schema_location_url_from_parsed_xml_file(parsed_xml_file)
            validate_xml_with_doi_against_schema_at_url(xml_file, schema_url)

class XMLMetadataFileTestCase(SimpleTestCase):
    def test_contents_with_spoofed_doi(self):
        xml_file = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as test_file:
            xml_file = DataSubsetXMLMetadataFile.from_file(test_file)
        print('xml_file.contents', xml_file.contents)
        self.assertTrue('10.000' in xml_file.contents)

    def test_data_subset_xsd_validation(self):
        xml_file = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as test_file:
            xml_file = DataSubsetXMLMetadataFile.from_file(test_file)
        MetadataFileXSDValidator.validate(xml_file)
