import os
from django.test import TestCase
from pithiaesc.settings import BASE_DIR

from .models import (
    Organisation
)

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.
class ScientificMetadataModelTestCase(TestCase):
    def test_metadata_server_url(self):
        """
        Model.metadata_server_url returns the metadata server
        URL for a scientific metadata registration.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            xml_string = xml_file.read()
            organisation = Organisation.objects.create_from_xml_string(xml_string)
        metadata_server_url = organisation.metadata_server_url
        print('metadata_server_url', metadata_server_url)