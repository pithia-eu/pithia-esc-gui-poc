import os
import environ
import mongomock
from lxml import etree
from .base_tests import *
from django.test import SimpleTestCase
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
    CATALOGUE_XML_ROOT_TAG_NAME,
)
from validation.url_validation import (
    get_invalid_ontology_urls_from_parsed_xml,
    get_invalid_resource_urls_from_parsed_xml,
    divide_resource_url_into_main_components,
    is_resource_url_base_structure_valid,
    divide_resource_url_from_op_mode_id,
    get_invalid_resource_urls_with_op_mode_ids_from_parsed_xml,
    validate_ontology_term_url,
    is_catalogue_related_url_structure_valid,
)
from validation.url_validation_utils import divide_catalogue_related_resource_url_into_main_components
from register.xml_conversion_checks_and_fixes import format_instrument_dictionary
from pithiaesc.settings import BASE_DIR

_TEST_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files')

env = environ.Env()

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.

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


class InstrumentOperationalModesValidationTestCase(InstrumentFileTestCase, OperationalModesValidationTestCase, SimpleTestCase):
    def setUp(self) -> None:
        client = mongomock.MongoClient()
        self.mongodb_model = client[env('DB_NAME')]['current-instruments']
        self.fix_conversion_errors_if_any = format_instrument_dictionary
        return super().setUp()


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
        self.assertEquals(resource_url_division_1['localid'], 'Project_TEST')
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
