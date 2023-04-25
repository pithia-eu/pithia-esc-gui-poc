from django.test import SimpleTestCase
from search.search_helpers import (
    get_observed_property_urls_by_instrument_types,
    get_observed_property_urls_by_computation_types,
    group_instrument_types_by_observed_property,
    group_computation_types_by_observed_property,
)
from search.views import (
    get_registered_observed_properties,
    get_registered_features_of_interest
)
from common.mongodb_models import (
    CurrentInstrument,
    CurrentComputationCapability
)
from ontology.utils import (
    create_dictionary_from_pithia_ontology_component,
    categorise_observed_property_dict_by_top_level_phenomenons,
    get_nested_phenomenons_in_observed_property,
)

# Create your tests here.

class ObservedPropertyCategorisationTestCase(SimpleTestCase):
    def test_get_all_phenomenons_of_observed_property(self):
        """
        gen_dict_extract() returns a list of all nested phenomenons in the observed_property_dict
        """
        instruments = CurrentInstrument.find({})
        instrument_types_grouped_by_observed_property = group_instrument_types_by_observed_property(instruments)
        computation_capability_sets = CurrentComputationCapability.find({})
        computation_types_grouped_by_observed_property = group_computation_types_by_observed_property(computation_capability_sets)
        observed_property_dict = create_dictionary_from_pithia_ontology_component(
            'observedProperty',
            instrument_types_grouped_by_observed_property=instrument_types_grouped_by_observed_property,
            computation_types_grouped_by_observed_property=computation_types_grouped_by_observed_property
        )
        first_observed_property = list(observed_property_dict.values())[0]
        phenomenons = get_nested_phenomenons_in_observed_property(first_observed_property)
        self.assertIsInstance(phenomenons, list)
    
    def categorise_observed_property_dict_by_top_level_phenomenons(self):
        """
        categorise_observed_property_dict_by_top_level_phenomenons returns an observed property dict categorised by top level phenomenons, where each dict key is a top-level phenomenon
        """
        instruments = CurrentInstrument.find({})
        instrument_types_grouped_by_observed_property = group_instrument_types_by_observed_property(instruments)
        computation_capability_sets = CurrentComputationCapability.find({})
        computation_types_grouped_by_observed_property = group_computation_types_by_observed_property(computation_capability_sets)
        observed_property_dict = create_dictionary_from_pithia_ontology_component(
            'observedProperty',
            instrument_types_grouped_by_observed_property=instrument_types_grouped_by_observed_property,
            computation_types_grouped_by_observed_property=computation_types_grouped_by_observed_property
        )
        print('observed_property_dict', observed_property_dict)
        categorised_observed_property_dict = categorise_observed_property_dict_by_top_level_phenomenons(observed_property_dict)
        print('categorised_observed_property_dict', categorised_observed_property_dict)
        self.assertIsInstance(categorised_observed_property_dict, dict)


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
        computation_capability_sets = CurrentComputationCapability.find({})
        computation_types_grouped_by_observed_property = group_computation_types_by_observed_property(computation_capability_sets)
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
