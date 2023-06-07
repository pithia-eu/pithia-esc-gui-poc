import environ
import mongomock
import os
from bson.objectid import ObjectId
from django.test import (
    SimpleTestCase,
    TestCase,
    tag,
)
from pathlib import Path

from .register import register_metadata_xml_file

from common.models import Organisation
from pithiaesc.settings import BASE_DIR
from validation.errors import FileRegisteredBefore

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

class ManagerTestCase(TestCase):
    def test_create_from_xml_string(self):
        """
        Model.objects.create_from_xml_string() returns a new
        registration with an ID property.
        """
        try:
            with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
                organisation = Organisation.objects.create_from_xml_string(xml_file.read())
                self.assertIn('id', organisation)
                print('organisation.id', organisation.id)
        except BaseException as err:
            print(err)
            self.fail('test_create_from_xml_string() unexpectedly raised an error!')
