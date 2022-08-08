from django.test import TestCase, SimpleTestCase
import environ
import mongomock

env = environ.Env()

# Create your tests here.
# The SimpleTestCase class is used to disable the automatic SQL database
# create/destroy that Django automatically does with the default
# TestCase class. MongoDB is still used.
class ResourceManagementTestCase(SimpleTestCase):
    def test_update_resource(self):
        """Update a resource and check the overwritten resource is in the revisions collection"""
        client = mongomock.MongoClient()
        db = client[env('DB_NAME')]
        db.insert_one({
            
        })