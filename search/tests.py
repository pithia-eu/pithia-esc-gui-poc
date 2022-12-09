from django.test import SimpleTestCase
from search.search_helpers import get_observed_property_urls_by_instrument_types, get_observed_property_urls_by_computation_types, group_instrument_types_by_observed_property, group_computation_types_by_observed_property
from search.views import get_registered_observed_properties, get_registered_features_of_interest
from common.mongodb_models import CurrentInstrument, CurrentComputationCapability

# Create your tests here.

class ObservedPropertySearchFormUpdateTestCase(SimpleTestCase):
    def test_observed_properties_are_fetched_by_instrument_type(self):
        """
        get_observed_property_urls_by_instrument_types() returns a list
        of observed property urls when passed in a list of instrument
        types
        """
        instrument_types = [
            'GNSS-receiver',
            'GNSS-receiverScintillation',
            'InSituRelaxationSounder',
        ]
        observed_property_urls_by_instrument_types = get_observed_property_urls_by_instrument_types(instrument_types)
        # print('observed_property_urls_by_instrument_types', observed_property_urls_by_instrument_types)
        self.assertTrue(isinstance(observed_property_urls_by_instrument_types, list))

    def test_observed_properties_are_fetched_by_computation_type(self):
        """
        get_observed_property_urls_by_computation_types() returns a list
        of observed property urls when passed in a list of computation
        types
        """
        computation_types = [
            'EmpiricalModel',
        ]
        observed_property_urls_by_computation_types = get_observed_property_urls_by_computation_types(computation_types)
        # print('observed_property_urls_by_computation_types', observed_property_urls_by_computation_types)
        self.assertTrue(isinstance(observed_property_urls_by_computation_types, list))

    def test_instrument_types_are_grouped_by_observed_property(self):
        """
        group_instrument_types_by_observed_property() returns a dict
        of instrument types grouped by observed property when passed
        in a list of instruments
        """
        instruments = CurrentInstrument.find({})
        instrument_types_grouped_by_observed_property = group_instrument_types_by_observed_property(instruments)
        # print('instrument_types_grouped_by_observed_property', instrument_types_grouped_by_observed_property)
        self.assertTrue(isinstance(instrument_types_grouped_by_observed_property, dict))

    def test_computation_types_are_grouped_by_observed_property(self):
        """
        group_computation_types_by_observed_property() returns a dict
        of computation types grouped by observed property when passed
        in a list of computation capabilities
        """
        computation_capabilities = CurrentComputationCapability.find({})
        computation_types_grouped_by_observed_property = group_computation_types_by_observed_property(computation_capabilities)
        # print('computation_types_grouped_by_observed_property', computation_types_grouped_by_observed_property)
        self.assertTrue(isinstance(computation_types_grouped_by_observed_property, dict))

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
