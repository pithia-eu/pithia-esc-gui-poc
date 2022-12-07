from django.test import SimpleTestCase
from search.views import get_registered_observed_properties, get_registered_features_of_interest

# Create your tests here.

class RegisteredResourcesTestCase(SimpleTestCase):
    def test_get_registered_observed_properties(self):
        """
        Test get_registered_observed_properties()
        returns an accurate list of registered
        observed properties
        """
        registered_observed_properties = get_registered_observed_properties()
        # print('registered_observed_properties', registered_observed_properties)
        self.assertTrue(isinstance(registered_observed_properties, list))

    def test_get_registered_features_of_interest(self):
        """
        Test get_registered_features_of_interest()
        returns an accurate list of registered
        features of interest
        """
        registered_observed_property_ids = get_registered_observed_properties()
        registered_features_of_interest = get_registered_features_of_interest(registered_observed_property_ids)
        print('registered_features_of_interest', registered_features_of_interest)
        self.assertTrue(isinstance(registered_features_of_interest, list))