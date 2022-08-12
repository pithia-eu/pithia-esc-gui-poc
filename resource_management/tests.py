import os
from django.test import TestCase, SimpleTestCase
import environ
import mongomock
from register.register import register_metadata_xml_file
from validation import validation
from resource_management import tests

env = environ.Env()

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.
class ResourceManagementTestCase(SimpleTestCase):
    def test_update_organisation(self):
        """Update a resource and check the overwritten resource is in the revisions collection"""
        client = mongomock.MongoClient()
        db = client[env('DB_NAME')]['current-organisations']
        with open(os.path.join(os.path.curdir, 'resource_management', 'tests', 'Organisation_TEST.xml'), 'r') as file:
            validation.validate_organisation_metadata_xml_file(file)
            register_metadata_xml_file(file, db, None)