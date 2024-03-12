import environ
from django.test import TestCase

from common.models import InteractionMethod
from common.test_setup import (
    register_data_collection_for_test,
    register_organisation_for_test,
)

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'

env = environ.Env()

# Create your tests here.

class ManagerTestCase(TestCase):
    def test_create_from_xml_string(self):
        """
        Model.objects.create_from_xml_string() returns a new
        registration with an ID property.
        """
        try:
            organisation = register_organisation_for_test()
            print('organisation.id', organisation.id)
        except AttributeError as err:
            print(err)
            self.fail("'id' property was not found in ScientificMetadata type object.")

class InteractionMethodTestCase(TestCase):
    def test_create_api_interaction_method(self):
        """
        InteractionMethod.objects.create() returns a new
        API Interaction Method.
        """
        try:
            data_collection = register_data_collection_for_test()
            interaction_method = InteractionMethod.api_interaction_methods.create_api_interaction_method(
                'https://www.example.com',
                '',
                data_collection
            )
            print('interaction_method', interaction_method)
            print('interaction_method.type', interaction_method.type)
            print('interaction_method.config', interaction_method.config)
            print('interaction_method.scientific_metadata', interaction_method.scientific_metadata)
            print('data_collection.interactionmethod_set.all()', data_collection.interactionmethod_set.all())
            self.assertTrue(len(list(data_collection.interactionmethod_set.all())) > 0)
            print('Passed create_api_interaction_method() test.')
        except BaseException as err:
            print(err)
            self.fail('test_api_interaction_method_create() unexpectedly raised an error!')