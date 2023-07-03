import environ
import os
from django.test import (
    SimpleTestCase,
    TestCase,
)

from common.models import (
    Organisation,
    DataCollection,
    InteractionMethod,
)
from pithiaesc.settings import BASE_DIR

# TODO: remove old code
import mongomock
from .pymongo_api import _register_with_pymongo

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

env = environ.Env()

# Create your tests here.

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

class InteractionMethodTestCase(TestCase):
    def test_create_api_interaction_method(self):
        """
        InteractionMethod.objects.create() returns a new
        API Interaction Method.
        """
        try:
            data_collection = None
            with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_Test.xml')) as xml_file:
                data_collection = DataCollection.objects.create_from_xml_string(xml_file.read())
            interaction_method = InteractionMethod.api_interaction_methods.create_api_interaction_method(
                'https://www.example.com',
                '',
                data_collection
            )
            print('interaction_method.type', interaction_method.type)
            print('interaction_method.config', interaction_method.config)
            print('interaction_method.data_collection', interaction_method.data_collection)
            print('data_collection.interactionmethod_set.all()', data_collection.interactionmethod_set.all())
            self.assertTrue(len(list(data_collection.interactionmethod_set.all())) > 0)
            print('Passed create_api_interaction_method() test.')
        except BaseException as err:
            print(err)
            self.fail('test_api_interaction_method_create() unexpectedly raised an error!')

class PyMongoApiTestCase(SimpleTestCase):
    def test_register_with_pymongo(self):
        """
        _register_with_pymongo() registers
        an XML metadata file and creates an OriginalMetadataXml
        entry alongside it.
        """
        client = mongomock.MongoClient()
        MockCurrentOrganisation = client[env('DB_NAME')]['current-organisations']
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            _register_with_pymongo(
                xml_file,
                MockCurrentOrganisation,
            )
        print('Passed _register_with_pymongo() test.')
