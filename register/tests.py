import os
import environ
import mongomock
from bson.objectid import ObjectId
from django.test import SimpleTestCase
from register.register import register_metadata_xml_file
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

env = environ.Env()

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.
class RegisterMetadataTestCase(SimpleTestCase):
    def test_register_organisation(self):
        """
        Ensure the organisation registration process doesn't encounter any
        unexpected errors.
        """
        client = mongomock.MongoClient()
        db = client[env('DB_NAME')]['current-organisations']
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            registration_results = register_metadata_xml_file(xml_file, db, None)
            self.assertIs(ObjectId.is_valid(registration_results._id), True)
