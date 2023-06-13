import environ
import os
from django.test import (
    TestCase,
)

from common.models import Organisation
from pithiaesc.settings import BASE_DIR

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
