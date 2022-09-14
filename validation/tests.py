import os
import environ
import mongomock
from genericpath import isfile
from django.test import SimpleTestCase
from validation.metadata_validation import ORGANISATION_XML_ROOT_TAG_NAME, get_schema_location_url_from_parsed_xml_file, is_xml_valid_against_schema_at_url, parse_xml_file, validate_xml_metadata_file
from pithiaesc.settings import BASE_DIR

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
