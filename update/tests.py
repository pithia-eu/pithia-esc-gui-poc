import os
from django.test import SimpleTestCase, tag

from pithiaesc.settings import BASE_DIR
from handle_management.utils import (
    add_doi_xml_string_to_metadata_xml_string,
    create_doi_xml_string_from_dict,
    get_doi_xml_string_from_metadata_xml_string,
    map_handle_to_doi_dict,
    remove_doi_element_from_metadata_xml_string,
)

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')


# Create your tests here.
class DOIManagementTestCase(SimpleTestCase):
    @tag('fast', 'get_doi_xml_string_from_metadata_xml_string')
    def test_get_doi_xml_string_from_metadata_xml_string(self):
        """
        Returns the first <doi> element from an XML string.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as xml_file:
            xml_string = xml_file.read()
            doi_element_string = get_doi_xml_string_from_metadata_xml_string(xml_string)
            print('doi_element_string', doi_element_string)
            self.assertIsInstance(doi_element_string, str)
            self.assertEqual(doi_element_string[:4], '<doi')
            print('Passed get_doi_xml_string_from_metadata_xml_string() test.')

    @tag('fast', 'remove_doi_element_from_metadata_xml_string')
    def test_remove_doi_element_from_metadata_xml_string(self):
        """
        Removes all <doi> elements from an XML string.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as xml_file:
            xml_string = xml_file.read()
            updated_xml_string = remove_doi_element_from_metadata_xml_string(xml_string)
            print('updated_xml_string', updated_xml_string)
            self.assertIsInstance(updated_xml_string, str)
            self.assertLess(len(updated_xml_string), len(xml_string))
            print('Passed remove_doi_element_from_metadata_xml_string() test.')

    @tag('fast', 'replace_doi_element_from_metadata_xml_string')
    def test_replace_doi_element_from_metadata_xml_string(self):
        """
        Replaces all <doi> elements with a new single DOI element.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as xml_file:
            xml_string = xml_file.read()
            doiless_xml_string = remove_doi_element_from_metadata_xml_string(xml_string)
            doi_dict = map_handle_to_doi_dict(f'{os.environ["HANDLE_PREFIX"]}/MYTEST-HANDLE', 'https://www.example.com/')
            doi_xml_string = create_doi_xml_string_from_dict(doi_dict)
            updated_xml_string = add_doi_xml_string_to_metadata_xml_string(doiless_xml_string, doi_xml_string)
            print('updated_xml_string', updated_xml_string)
            print('Passed replace_doi_element_from_metadata_xml_string() test.')