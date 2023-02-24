import os
import environ
import mongomock
from bson.objectid import ObjectId
from django.urls import reverse
from django.test import SimpleTestCase, tag
from register.register import register_metadata_xml_file
from register.handle_management import (
    instantiate_client_and_load_credentials,
    create_handle,
    register_handle,
    delete_handle,
    update_handle_url,
    get_handle_url,
    get_handle_record,
)
from validation.errors import FileRegisteredBefore
from pithiaesc.settings import BASE_DIR
from pathlib import Path
from pyhandle.handleclient import RESTHandleClient
from pyhandle.clientcredentials import PIDClientCredentials

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

env = environ.Env()

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.
class RegisterMetadataTestCase(SimpleTestCase):
    @tag('fast')
    def test_register_organisation(self):
        """
        register_metadata_xml_file() returns a dict with an auto-generated '_id' property
        """
        try:
            client = mongomock.MongoClient()
            MockCurrentOrganisation = client[env('DB_NAME')]['current-organisations']
            with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
                registered_resource = register_metadata_xml_file(
                    xml_file,
                    MockCurrentOrganisation,
                    None
                )
                self.assertIs(ObjectId.is_valid(registered_resource['_id']), True)
                print(f'Passed registration validation for {Path(xml_file.name).name}.')
        except FileRegisteredBefore as err:
            print(err)
            self.fail('register_metadata_xml_file() unexpectedly raised an error!')

class HandleManagementTestCase(SimpleTestCase):
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

    @tag('fast', 'handles')
    def test_create_handle(self):
        """
        create_handle() returns a string with format "{handle_prefix}/{handle_suffix}"
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        self.assertIsInstance(handle, str)
        self.assertEqual(handle, f'{self.credentials.get_prefix()}/{self.TEST_SUFFIX}')

    @tag('fast', 'handles', 'register_handle')
    def test_register_handle(self):
        """
        register_handle() returns the handle data passed into it and raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_result = register_handle(handle, self.VALUE_ORIGINAL, self.client)
        self.assertEqual(register_result, handle)
        # delete_handle(handle, self.client)

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

    @tag('fast', 'handles', 'get_handle_url')
    def test_get_handle_url(self):
        """
        get_handle_url() returns the record for the handle data and raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        handle_url = get_handle_url(handle, self.client)
        print('handle_url', handle_url)
        self.assertEqual(handle_url, self.VALUE_ORIGINAL)
        self.assertIsInstance(handle_url, str)
        delete_handle(handle, self.client)

    @tag('fast', 'handles', 'delete_handle')
    def test_delete_handle(self):
        """
        delete_handle() raises no exceptions.
        """
        handle = create_handle(self.credentials, self.TEST_SUFFIX)
        register_handle(handle, self.VALUE_ORIGINAL, self.client)
        delete_result = delete_handle(handle, self.client)
        self.assertEqual(handle, delete_result)

    @tag('fast')
    def test_add_doi_tag_to_xml_file(self):
        """
        add_doi_to_xml_file() adds a filled out <doi> element to the XML file.
        """
        doi = generate_doi(self.fake_resource_id)
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            updated_xml_file = add_doi_to_xml_file(xml_file, doi)
            print('updated_xml_file', updated_xml_file)
            print(f'Passed new DOI element addition for {Path(xml_file.name).name}.')
