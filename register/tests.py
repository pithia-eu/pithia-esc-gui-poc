import os
import environ
import mongomock
from bson.objectid import ObjectId
from django.urls import reverse
from django.test import SimpleTestCase, tag
from register.register import register_metadata_xml_file
from register.doi_registration_prototype import (
    generate_doi,
    add_doi_to_xml_file,
    create_pid,
    get_pid,
    delete_pid,
)
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

    @tag('fast', 'handles')
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
        # Also integration test
        # with instantiate_client_and_load_credentials() function
        client, credentials = instantiate_client_and_load_credentials()
        handle = create_handle(credentials, self.TEST_SUFFIX)
        self.assertIsInstance(handle, str)
        self.assertEqual(handle, f'{credentials.get_prefix()}/{self.TEST_SUFFIX}')

    @tag('fast', 'handles')
    def test_register_handle(self):
        """
        register_handle() returns the handle data passed into it and raises no exceptions.
        """
        # Also integration test
        # with instantiate_client_and_load_credentials() function
        client, credentials = instantiate_client_and_load_credentials()
        handle = create_handle(credentials, self.TEST_SUFFIX)
        register_result = register_handle(handle, self.VALUE_ORIGINAL, client)

        self.assertEqual(register_result, handle)

    @tag('fast', 'handles', 'get_handle_record')
    def test_get_handle_record(self):
        """
        get_handle_record() returns the record for the handle data and raises no exceptions.
        """
        client, credentials = instantiate_client_and_load_credentials()
        handle = create_handle(credentials, self.TEST_SUFFIX)
        handle_record = get_handle_record(handle, client)

    @tag('fast', 'handles', 'delete_handle')
    def test_delete_handle(self):
        """
        delete_handle() raises no exceptions.
        """
        client, credentials = instantiate_client_and_load_credentials()
        handle = create_handle(credentials, self.TEST_SUFFIX)
        delete_result = delete_handle(handle, client)

class DoiFunctionalityTestCase(SimpleTestCase):
    fake_resource_id = '85d32cad243eb3953dceca32'

    @tag('fast', 'doi', 'create_doi')
    def test_create_pid(self):
        """
        create_pid() adds a pid successfully.
        """
        landing_page_url = reverse('browse:catalogue_data_subset_detail', kwargs={ 'catalogue_data_subset_id': self.fake_resource_id })
        put_response = create_pid(landing_page_url)
        print('put_response.json()', put_response.json())

    @tag('fast', 'doi', 'get_doi')
    def test_get_pid(self):
        """
        get_pid() adds a pid successfully.
        """
        get_response = get_pid()
        print('get_response.json()', get_response.json())

    @tag('fast', 'doi', 'delete_doi')
    def test_delete_pid(self):
        """
        delete_pid() adds a pid successfully.
        """
        delete_response = delete_pid()
        print('delete_response.json()', delete_response.json())

    @tag('fast')
    def test_generate_fake_doi(self):
        """
        generate_doi() returns a dict representing a DOI object.
        """
        doi = generate_doi(self.fake_resource_id)
        self.assertIsInstance(doi, dict)
        print('doi', doi)
        print('Passed DOI generation test!')

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
