import os
from django.test import TestCase

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
            DataCollection.objects.create_from_xml_string(xml_file.read())
        results = DataCollection.objects.for_simple_search('Test')
        print('results', results)
        return self.assertTrue(len(results) > 0)