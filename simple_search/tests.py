import os
from django.test import TestCase

from .services import find_data_collections_for_simple_search

from common.models import DataCollection
from pithiaesc.settings import BASE_DIR


_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.
class SimpleSearchTestCase(TestCase):
    def test_for_simple_search(self):
        """
        Returns Data Collections matching the
        simple search query.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_Test.xml')) as xml_file:
            data_collection = DataCollection.objects.create_from_xml_string(xml_file.read())
            print('data_collection.name', data_collection.name)
            
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_DEMO_Stim.xml')) as xml_file:
            data_collection = DataCollection.objects.create_from_xml_string(xml_file.read())
            print('data_collection.name', data_collection.name)

        # Case-insensitive match
        data_collections_1 = find_data_collections_for_simple_search('lorem')

        # Partial case-insensitive match
        data_collections_2 = find_data_collections_for_simple_search('lor')

        # No match
        data_collections_3 = find_data_collections_for_simple_search('xyz')

        # Attribute matching shouldn't work
        data_collections_4 = find_data_collections_for_simple_search('image-png')

        print('len(data_collections_1)', len(data_collections_1))
        print('len(data_collections_2)', len(data_collections_2))
        print('len(data_collections_3)', len(data_collections_3))
        print('len(data_collections_4)', len(data_collections_4))

        self.assertEqual(len(data_collections_1), 1)
        self.assertEqual(len(data_collections_2), 1)
        self.assertEqual(len(data_collections_3), 0)
        self.assertEqual(len(data_collections_4), 0)
        