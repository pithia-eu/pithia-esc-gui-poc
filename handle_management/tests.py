import environ
import mongomock
import os
from django.test import (
    SimpleTestCase,
    tag
)
from handle_management.handle_api import (
    create_and_register_handle_for_resource,
    create_handle,
    delete_handle,
    get_date_handle_was_issued_as_string,
    get_handle_raw,
    get_handle_record,
    get_handle_url,
    get_handles_with_prefix,
    get_time_handle_was_issued_as_string,
    instantiate_client_and_load_credentials,
    register_handle,
    update_handle_url,
)
from handle_management.xml_utils import (
    add_doi_xml_string_to_metadata_xml_string,
    add_handle_to_metadata_and_return_updated_xml_string,
    create_doi_xml_string_from_dict,
    get_doi_xml_string_from_metadata_xml_string,
    get_last_source_element,
    get_last_result_time_element,
    is_doi_element_present_in_xml_file,
    map_handle_to_doi_dict,
    parse_xml_string,
    remove_doi_element_from_metadata_xml_string,
)
from pathlib import Path
from pithiaesc.settings import BASE_DIR
from pyhandle.handleclient import RESTHandleClient
from pyhandle.clientcredentials import PIDClientCredentials
from register.register import register_metadata_xml_file

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')
env = environ.Env()

# Create your tests here.
class PyHandleTestCase(SimpleTestCase):
    TEST_SUFFIX = 'MYTEST-HANDLE'
    VALUE_ORIGINAL = 'https://www.example.com/1'
    VALUE_AFTER = 'https://www.example.com/2'

    def setUp(self) -> None:
        # Also acts as integration test
        # for instantiate_client_and_load_credentials() function
        self.client, self.credentials = instantiate_client_and_load_credentials()
        return super().setUp()

    @tag('fast', 'handles', 'instantiate_client_and_load_credentials')
    def test_instantiate_client_and_load_credentials(self):
        """
        instantiate_client_and_load_credentials() returns a tuple containing a client of type "RESTHandleClient "and credentials of type "PIDClientCredentials"
        """
        client, credentials = instantiate_client_and_load_credentials()
        self.assertIsInstance(client, RESTHandleClient)
        self.assertIsInstance(credentials, PIDClientCredentials)
        print('Passed instantiate_client_and_load_credentials() test.')

    @tag('fast', 'handles')
    def test_create_handle(self):
        """
        create_handle() returns a string with format "{handle_prefix}/{handle_suffix}"
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        self.assertIsInstance(handle, str)
        self.assertEqual(handle, f'{self.credentials.get_prefix()}/{self.TEST_SUFFIX}')
        print('Passed create_handle() test.')

    @tag('fast', 'handles', 'register_handle')
    def test_register_handle(self):
        """
        register_handle() returns the handle data passed into it and raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_result = register_handle(handle, self.VALUE_ORIGINAL, self.client)
        self.assertEqual(register_result, handle)
        delete_handle(handle, self.client)
        print('Passed register_handle() test.')

    @tag('fast', 'handles', 'get_handle_record')
    def test_get_handle_record(self):
        """
        get_handle_record() returns the record for the handle data and raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        handle_record = get_handle_record(handle, self.client)
        print('handle_record', handle_record)
        self.assertIsInstance(handle_record, dict)
        delete_handle(handle, self.client)
        print('Passed get_handle_record() test.')

    @tag('fast', 'handles', 'get_handle_url')
    def test_get_handle_url(self):
        """
        get_handle_url() returns the URL for the handle and raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        handle_url = get_handle_url(handle, self.client)
        print('handle_url', handle_url)
        self.assertEqual(handle_url, self.VALUE_ORIGINAL)
        self.assertIsInstance(handle_url, str)
        delete_handle(handle, self.client)
        print('Passed get_handle_url() test.')

    @tag('fast', 'handles', 'get_handle_raw')
    def test_get_handle_raw(self):
        """
        get_handle_raw() returns the handle without being formatted by the API.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        handle_raw = get_handle_raw(handle)
        print('handle_raw', handle_raw)
        self.assertIsInstance(handle_raw, dict)
        delete_handle(handle, self.client)
        print('Passed get_handle_raw() test.')

    @tag('fast', 'handles', 'get_time_handle_was_issued_as_string')
    def test_get_time_handle_was_issued_as_string(self):
        """
        get_time_handle_was_issued_as_string() returns the time the handle was issued in str format.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        issue_time_string = get_time_handle_was_issued_as_string(handle)
        print('issue_time_string', issue_time_string)
        self.assertIsInstance(issue_time_string, str)
        delete_handle(handle, self.client)
        print('Passed get_time_handle_was_issued_as_string() test.')

    @tag('fast', 'handles', 'get_date_handle_was_issued_as_string')
    def test_get_date_handle_was_issued_as_string(self):
        """
        get_date_handle_was_issued_as_string() returns the date the handle was issued.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        issue_date_as_string = get_date_handle_was_issued_as_string(handle)
        print('issue_date_as_string', issue_date_as_string)
        self.assertIsInstance(issue_date_as_string, str)
        delete_handle(handle, self.client)
        print('Passed get_date_handle_was_issued_as_string() test.')

    @tag('fast', 'handles', 'delete_handle')
    def test_delete_handle(self):
        """
        delete_handle() returns the handle of the deleted record and raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        delete_result = delete_handle(handle, self.client)
        self.assertEqual(handle, delete_result)
        print('Passed delete_handle() test.')

    @tag('fast', 'handles', 'update_handle_url')
    def test_update_handle_url(self):
        """
        update_handle_url() raises no exception.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        update_result = update_handle_url(handle, self.VALUE_AFTER, self.client)
        handle_url = get_handle_url(handle, self.client)
        self.assertEqual(update_result, handle)
        self.assertEqual(handle_url, self.VALUE_AFTER)
        delete_handle(handle, self.client)
        print('Passed update_handle_url() test.')

class DOIXMLRegistrationTestCase(SimpleTestCase):
    @tag('fast', 'register_handle_and_add_to_metadata')
    def test_register_handle_and_add_to_metadata(self):
        """
        register_handle_and_add_to_metadata() raises no exceptions.
        """
        client = mongomock.MongoClient()
        MockCurrentCatalogueDataSubset= client[env('DB_NAME')]['current-catalogue-data-subsets']
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            registered_resource = register_metadata_xml_file(
                xml_file,
                MockCurrentCatalogueDataSubset,
                None
            )
            resource_id = registered_resource['_id']
            handle, client, credentials = create_and_register_handle_for_resource(resource_id)
            print('xml_file', xml_file)
            add_handle_to_metadata_and_return_updated_xml_string(
                handle,
                client,
                resource_id,
                xml_file,
                MockCurrentCatalogueDataSubset
            )
            delete_handle(handle, client)
            print(f'Passed handle registration for {Path(xml_file.name).name}.')

    @tag('fast', 'add_doi_xml_string_to_metadata_xml_string')
    def test_add_doi_xml_string_to_metadata_xml_string(self):
        """
        add_doi_xml_string_to_metadata_xml_string() adds a filled out <doi> element to the XML string.
        """
        # This test assumes that this handle exists
        doi_dict = map_handle_to_doi_dict(f'{os.environ["HANDLE_PREFIX"]}/MYTEST-HANDLE', 'https://www.example.com/')
        doi_xml_string = create_doi_xml_string_from_dict(doi_dict)
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            xml_string = xml_file.read()
            updated_xml_string = add_doi_xml_string_to_metadata_xml_string(xml_string, doi_xml_string)
            print('updated_xml_string', updated_xml_string)
            print(f'Passed new DOI element addition for {Path(xml_file.name).name}.')

    @tag('fast', 'get_handles_with_prefix')
    def test_get_handles_with_prefix(self):
        """
        get_handles_with_prefix() returns all handles under a given prefix.
        """
        prefix = env('HANDLE_PREFIX')
        handles = get_handles_with_prefix(prefix)
        print('handles', handles)

    @tag('fast', 'get_last_result_time_element')
    def test_get_last_result_time_element(self):
        """
        Gets the last <resultTime> element in a Data Subset XML string.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            xml_string = xml_file.read()
            xml_string_parsed = parse_xml_string(xml_string)
            last_result_time_element = get_last_result_time_element(xml_string_parsed)
            print('last_result_time_element', last_result_time_element)

    @tag('fast', 'get_last_source_element')
    def test_get_last_source_element(self):
        """
        Gets the last <source> element in a Data Subset XML string.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            xml_string = xml_file.read()
            xml_string_parsed = parse_xml_string(xml_string)
            last_source_element = get_last_source_element(xml_string_parsed)
            print('last_source_element', last_source_element)

    @tag('fast', 'doi_element_is_not_present_in_xml_file', 'is_doi_element_present_in_xml_file')
    def test_doi_element_is_not_present_in_xml_file(self):
        """
        is_doi_element_present_in_xml_file() returns False for the given XML file.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            result = is_doi_element_present_in_xml_file(xml_file)
            print('result', result)
            self.assertEqual(result, False)

    @tag('fast', 'doi_element_is_present_in_xml_file', 'is_doi_element_present_in_xml_file')
    def test_doi_element_is_present_in_xml_file(self):
        """
        is_doi_element_present_in_xml_file() returns True for the given XML file.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest_with_DOI.xml')) as xml_file:
            result = is_doi_element_present_in_xml_file(xml_file)
            print('result', result)
            self.assertEqual(result, True)

class DOIXMLUpdateTestCase(SimpleTestCase):
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