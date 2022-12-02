from django.test import SimpleTestCase
from search.search_helpers import get_observed_property_urls_by_instrument_types

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
        observed_property_urls = get_observed_property_urls_by_instrument_types(instrument_types)
        print(observed_property_urls)
        self.assertTrue(isinstance(observed_property_urls, list))