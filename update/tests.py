import os
from django.test import TestCase

from common.models import Organisation
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')


# Create your tests here.

class XMLMetadataFileUpdateTestCase(TestCase):
    def test_update_from_xml_string(self):
        """
        """
        organisation_original = None
        organisation_updated = None
        organisation_id = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            organisation_original = Organisation.objects.create_from_xml_string(xml_file.read())
            organisation_id = organisation_original.pk

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test_Update.xml')) as xml_file:
            organisation_updated = Organisation.objects.update_from_xml_string(organisation_id, xml_file.read())

        print('organisation_original.pk', organisation_original.pk)
        print('organisation_original.name', organisation_original.name)
        print('organisation_updated.pk', organisation_updated.pk)
        print('organisation_updated.name', organisation_updated.name)
        self.assertEqual(organisation_original.pk, organisation_updated.pk)
        self.assertNotEqual(organisation_original.name, organisation_updated.name)
        