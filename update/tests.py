import os
from django.test import TestCase

from common.models import (
    Organisation,
    DataCollection,
    InteractionMethod,
    APIInteractionMethod,
)
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'


# Create your tests here.

class XMLMetadataFileUpdateTestCase(TestCase):
    def test_update_from_xml_string(self):
        """
        """
        organisation_original = None
        organisation_updated = None
        organisation_id = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            organisation_original = Organisation.objects.create_from_xml_string(xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
            organisation_id = organisation_original.pk

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test_Update.xml')) as xml_file:
            organisation_updated = Organisation.objects.update_from_xml_string(
                organisation_id,
                xml_file.read(),
                SAMPLE_USER_ID
            )

        print('organisation_original.pk', organisation_original.pk)
        print('organisation_original.name', organisation_original.name)
        print('organisation_updated.pk', organisation_updated.pk)
        print('organisation_updated.name', organisation_updated.name)
        self.assertEqual(organisation_original.pk, organisation_updated.pk)
        self.assertNotEqual(organisation_original.name, organisation_updated.name)

class InteractionMethodTestCase(TestCase):
    def test_update_config(self):
        data_collection = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_Test.xml')) as xml_file:
            data_collection = DataCollection.objects.create_from_xml_string(xml_file.read(), SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        interaction_method = InteractionMethod.api_interaction_methods.create_api_interaction_method(
            'https://www.example.com',
            '',
            data_collection
        )

        new_specification_url = 'https://www.example-updated.com'
        new_description = 'description updated'
        updated_interaction_method = APIInteractionMethod.objects.update_config(
            interaction_method.pk,
            new_specification_url,
            new_description
        )
        print('updated_interaction_method.specification_url', updated_interaction_method.specification_url)
        print('updated_interaction_method.description', updated_interaction_method.description)
        self.assertEqual(updated_interaction_method.specification_url, new_specification_url)
        self.assertEqual(updated_interaction_method.description, new_description)