from django.test import TestCase

from .services import (
    setup_computation_types_for_observed_property_search_form,
    setup_instrument_types_for_observed_property_search_form,
)

from ontology.services import (
    create_dictionary_from_pithia_ontology_component,
    categorise_observed_property_dict_by_top_level_phenomenons,
    get_nested_phenomenons_in_observed_property,
)


# Create your tests here.
class ObservedPropertyCategorisationForSearchFormTestCase(TestCase):
    def test_phenomenons_are_retrieved_from_observed_property_child_terms(self):
        """Returns a flat list of the phenomenons of an observed property
        and the observed properties child terms.
        """
        instrument_types_grouped_by_observed_property = setup_instrument_types_for_observed_property_search_form()
        computation_types_grouped_by_observed_property = setup_computation_types_for_observed_property_search_form()
        observed_property_dict = create_dictionary_from_pithia_ontology_component(
            'observedProperty',
            instrument_types_grouped_by_observed_property=instrument_types_grouped_by_observed_property,
            computation_types_grouped_by_observed_property=computation_types_grouped_by_observed_property
        )
        first_observed_property = list(observed_property_dict.values())[0]
        phenomenons = get_nested_phenomenons_in_observed_property(first_observed_property)
        print('phenomenons', phenomenons)
        self.assertIsInstance(phenomenons, list)
    
    def test_observed_properties_are_categorised_by_top_level_phenomenons(self):
        """Returns a dict of observed properties where each dict
        key is a top-level phenomenon that each observed property
        corresponds to.
        """
        # The Observed Properties search form is broken up
        # into sections by headings. These headings are the
        # highest level phenomenons (e.g. Field, Particle).
        instrument_types_grouped_by_observed_property = setup_instrument_types_for_observed_property_search_form()
        computation_types_grouped_by_observed_property = setup_computation_types_for_observed_property_search_form()
        observed_property_dict = create_dictionary_from_pithia_ontology_component(
            'observedProperty',
            instrument_types_grouped_by_observed_property=instrument_types_grouped_by_observed_property,
            computation_types_grouped_by_observed_property=computation_types_grouped_by_observed_property
        )
        categorised_observed_property_dict = categorise_observed_property_dict_by_top_level_phenomenons(observed_property_dict)
        self.assertIsInstance(categorised_observed_property_dict, dict)


class ObservedPropertySearchFormSetupTestCase(TestCase):
    def test_instrument_types_are_grouped_by_observed_property(self):
        """Returns a dict of instrument types correctly
        grouped by their observed properties.
        """
        instrument_types_grouped_by_observed_property = setup_instrument_types_for_observed_property_search_form()
        # print('instrument_types_grouped_by_observed_property', instrument_types_grouped_by_observed_property)
        self.assertTrue(isinstance(instrument_types_grouped_by_observed_property, dict))

    def test_computation_types_are_grouped_by_observed_property(self):
        """Returns a dict of computation types correctly
        grouped by their observed properties.
        """
        computation_types_grouped_by_observed_property = setup_computation_types_for_observed_property_search_form()
        # print('computation_types_grouped_by_observed_property', computation_types_grouped_by_observed_property)
        self.assertTrue(isinstance(computation_types_grouped_by_observed_property, dict))