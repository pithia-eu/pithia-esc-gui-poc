import environ
from django.test import TestCase, SimpleTestCase
import mongomock

env = environ.Env()

# Create your tests here.

class PymongoTestCase(SimpleTestCase):
    def test_pymongo_sessions(self):
        """
        pymongo undoes a MongoDB transaction
        if an error occurs during an operation.

        TEST DOES NOT WORK AS MONGOMOCK DOES NOT
        SUPPORT SESSIONS YET.
        """
        client = mongomock.MongoClient()
        MockCurrentDataCollection = client[env('DB_NAME')]['current-data-collections']
        test_data_collection_name = 'Test Data Collection'
        MockCurrentDataCollection.insert_one({
            'name': test_data_collection_name
        })
        try:
            with client.start_session() as s:
                def cb(s):
                    MockCurrentDataCollection.delete_one({
                        'name': test_data_collection_name
                    })
                    raise BaseException('Test exception')
                s.with_transaction(cb)
        except BaseException as e:
            print(e)
            test_data_collection = MockCurrentDataCollection.find_one({
                'name': test_data_collection_name
            })
            self.assertNotEqual(test_data_collection, None)
