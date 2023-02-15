import os
import environ
import mongomock
from bson.objectid import ObjectId
from django.urls import reverse
from django.test import SimpleTestCase, tag
from register.register import register_metadata_xml_file
from register.doi_registration import (
    generate_doi,
    add_doi_to_xml_file,
    get_pid,
)
from validation.errors import FileRegisteredBefore
from pithiaesc.settings import BASE_DIR
from pathlib import Path

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

class DoiFunctionalityTestCase(SimpleTestCase):
    fake_resource_id = '85d32cad243eb3953dceca32'

    @tag('fast')
    def test_get_pid(self):
        """
        get_pid() returns a pid.
        """
        landing_page_url = reverse('browse:catalogue_data_subset_detail', kwargs={ 'data_collection_id': self.fake_resource_id })
        pid = get_pid(landing_page_url)

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
