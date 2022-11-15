import os
import environ
import mongomock
from lxml import etree
from genericpath import isfile
from django.test import SimpleTestCase
from validation.metadata_validation import ORGANISATION_XML_ROOT_TAG_NAME, get_schema_location_url_from_parsed_xml_file, is_xml_valid_against_schema_at_url, parse_xml_file, validate_xml_metadata_file
from validation.url_validation import get_invalid_ontology_urls_from_parsed_xml, get_invalid_resource_urls_from_parsed_xml, divide_resource_url_into_main_components, is_resource_url_structure_valid
from pithiaesc.settings import BASE_DIR

_TEST_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files')
_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

env = environ.Env()

def _is_xml_file_xsd_valid(xml_file):
    xml_file_parsed = parse_xml_file(xml_file)
    schema_url = get_schema_location_url_from_parsed_xml_file(xml_file_parsed)
    return is_xml_valid_against_schema_at_url(xml_file, schema_url)

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.
class RegistrationValidationTestCase(SimpleTestCase):
    """
    Test the validation pipeline works as expected
    """
    def test_organisation_registration_validation(self):
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            client = mongomock.MongoClient()
            db = client[env('DB_NAME')]['current-organisations']
            validation_results = validate_xml_metadata_file(xml_file, ORGANISATION_XML_ROOT_TAG_NAME, mongodb_model=db, check_file_is_unregistered=True)
            if 'error' in validation_results:
                print('error', validation_results['error'])
            self.assertNotIn('error', validation_results)

    def test_invalid_syntax_organisation_registration_validation(self):
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test_InvalidSyntax.xml')) as xml_file:
            client = mongomock.MongoClient()
            db = client[env('DB_NAME')]['current-organisations']
            validation_results = validate_xml_metadata_file(xml_file, ORGANISATION_XML_ROOT_TAG_NAME, mongodb_model=db, check_file_is_unregistered=True)
            if 'error' in validation_results:
                print('error', validation_results['error'])
            self.assertIn('error', validation_results)

    def test_multiple_file_validation(self):
        xml_file_names = [f for f in os.listdir(_XML_METADATA_FILE_DIR) if isfile(os.path.join(_XML_METADATA_FILE_DIR, f))]
        for fname in xml_file_names:
            with open(os.path.join(_XML_METADATA_FILE_DIR, fname)) as xml_file:
                client = mongomock.MongoClient()
                db = client[env('DB_NAME')]['current-organisations']
                validation_results = validate_xml_metadata_file(xml_file, ORGANISATION_XML_ROOT_TAG_NAME, mongodb_model=db, check_file_is_unregistered=True)
                if fname == 'Organisation_Test.xml':
                    if 'error' in validation_results:
                        print('error', validation_results['error'])
                    self.assertNotIn('error', validation_results)
                else:
                    if 'error' in validation_results:
                        print('error', validation_results['error'])
                    self.assertIn('error', validation_results)


class XsdValidationTestCase(SimpleTestCase):
    """
    Test XSD Schema validation works for all metadata types
    """
    def test_xml_metadata_files_validate_against_schemas(self):
        xml_file_names = [f for f in os.listdir(_XML_METADATA_FILE_DIR) if isfile(os.path.join(_XML_METADATA_FILE_DIR, f))]
        for fname in xml_file_names:
            if fname == 'Organisation_Test_InvalidSyntax.xml':
                continue
            with open(os.path.join(_XML_METADATA_FILE_DIR, fname)) as xml_file:
                self.assertEqual(f'{fname} is valid: {_is_xml_file_xsd_valid(xml_file)}', f'{fname} is valid: {True}')

class UrlValidationTestCase(SimpleTestCase):
    def test_invalid_ontology_urls_are_detected(self):
        """
        get_invalid_ontology_urls() returns a list of invalid ontology urls
        """
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_parsed = etree.parse(xml_file)
            invalid_ontology_urls = get_invalid_ontology_urls_from_parsed_xml(xml_file_parsed)
            self.assertEquals(len(invalid_ontology_urls), 1)

    def test_invalid_resource_urls_are_detected(self):
        """
        get_invalid_resource_urls() returns a list of invalid resource urls
        """
        with open(os.path.join(_TEST_FILE_DIR, 'invalid_and_valid_urls.xml')) as xml_file:
            xml_file_parsed = etree.parse(xml_file)
            invalid_resource_urls = get_invalid_resource_urls_from_parsed_xml(xml_file_parsed)
            print('invalid_resource_urls', invalid_resource_urls)
            self.assertEquals(len(invalid_resource_urls), 1)

class UrlStructureValidationTestCase(SimpleTestCase):
    def test_resource_urls_are_divided_correctly(self):
        """
        divide_resource_url_into_main_components() divides resources as expected
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

    def test_invalid_resource_url_structures_are_detected(self):
        """
        is_resource_url_structure_valid() returns False if a resource url is invalid
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
        acquisition_capabilities_incorrect_casing_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/AcquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        computation_capabilities_incorrect_casing_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/ComputationCapabilities/pithia/AcquisitionCapabilities_TEST')

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
        self.assertEquals(acquisition_capabilities_incorrect_casing_result, False)
        self.assertEquals(computation_capabilities_incorrect_casing_result, False)

    def test_valid_resource_urls_pass_validation(self):
        """
        is_resource_url_structure_valid() returns True if a resource url is valid
        """

        valid_organisation_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        valid_individual_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/individual/pithia/Individual_TEST')
        valid_project_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/project/pithia/Project_TEST')
        valid_platform_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/platform/pithia/Platform_TEST')
        valid_operation_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/operation/pithia/Operation_TEST')
        valid_instrument_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/instrument/pithia/Instrument_TEST')
        valid_aqcuisition_capabilities_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisitionCapabilities/pithia/AcquisitionCapabilities_TEST')
        valid_acquisition_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/acquisition/pithia/Acquisition_TEST')
        valid_computation_capabilities_url_result = is_resource_url_structure_valid('https://metadata.pithia.eu/resources/2.2/computationCapabilities/pithia/ComputationCapabilities_TEST')
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
        self.assertEquals(valid_computation_capabilities_url_result, True)
        self.assertEquals(valid_computation_url_result, True)
        self.assertEquals(valid_process_url_result, True)
        self.assertEquals(valid_data_collection_url_result, True)