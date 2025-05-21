from django.test import TestCase

from .services import (
    get_data_collections_for_search,
    get_distinct_computation_type_urls_from_data_collections,
    get_distinct_instrument_type_urls_from_data_collections,
)
from .views import (
    get_registered_observed_properties,
    get_registered_features_of_interest
)

from common.models import (
    DataCollection,
)
from common.test_setup import (
    register_acquisition_capabilities_for_test,
    register_acquisition_for_test,
    register_computation_capabilities_for_test,
    register_computation_for_test,
    register_data_collection_for_test,
    register_instrument_for_test,
    register_process_for_test,
)

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'


# Create your tests here.

class SearchBehaviourTestCase(TestCase):
    def setUp(self) -> None:
        register_instrument_for_test()
        register_acquisition_capabilities_for_test()
        register_acquisition_for_test()
        register_computation_capabilities_for_test()
        register_computation_for_test()
        register_process_for_test()
        register_data_collection_for_test()
        return super().setUp()

    instrument_type_urls = [
        'https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder',
    ]
    computation_type_urls = [
        'https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual',
    ]
    observed_property_urls = [
        'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
        'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization',
        'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift',
        'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Direction',
    ]
    feature_of_interest_urls = [
        'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_F-Region_Bottomside',
        'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_E-Region',
    ]

    def test_data_collections_are_found_with_features_of_interest(self):
        """A list of data collections matching any of the
        features of interest in the list are returned.
        """
        data_collections = get_data_collections_for_search(feature_of_interest_urls=self.feature_of_interest_urls)
        print('data_collections', data_collections)
        print('len(data_collections)', len(data_collections))
        self.assertEqual(len(data_collections), 1)

    def test_data_collections_are_found_with_instrument_types(self):
        """A list of data collections matching any of the
        instrument types in the list are returned.
        """
        data_collections = get_data_collections_for_search(instrument_type_urls=self.instrument_type_urls)
        print('data_collections', data_collections)
        print('len(data_collections)', len(data_collections))
        self.assertEqual(len(data_collections), 1)

    def test_data_collections_are_found_with_computation_types(self):
        """A list of data collections matching any of the
        computation types in the list are returned.
        """
        data_collections = get_data_collections_for_search(computation_type_urls=self.computation_type_urls)
        print('data_collections', data_collections)
        print('len(data_collections)', len(data_collections))
        self.assertEqual(len(data_collections), 1)

    def test_data_collections_are_found_with_observed_properties(self):
        """A list of data collections matching any of the
        observed properties in the list are returned.
        """
        data_collections = get_data_collections_for_search(observed_property_urls=self.observed_property_urls)
        print('data_collections', data_collections)
        print('len(data_collections)', len(data_collections))
        self.assertEqual(len(data_collections), 1)

    def test_data_collections_are_found_with_combined_search_criteria(self):
        """A list of data collections which match at least
        one URL from each category is returned.
        """
        data_collections = get_data_collections_for_search(
            feature_of_interest_urls=self.feature_of_interest_urls,
            instrument_type_urls=self.instrument_type_urls,
            computation_type_urls=self.computation_type_urls,
            observed_property_urls=self.observed_property_urls
        )
        print('data_collections', data_collections)
        print('len(data_collections)', len(data_collections))
        self.assertEqual(len(data_collections), 1)


class SearchFormSetupTestCase(TestCase):
    # Distinct instrument/model URLs are used as part of
    # classifying which instrument types and model types
    # are registered. The registration status of each of
    # these types are displayed in the search form.
    def test_distinct_instrument_urls_are_retrieved_from_data_collections(self):
        """Returns a list of unique instrument type URLs
        from all registered data collections.
        """
        register_data_collection_for_test()
        data_collections = DataCollection.objects.all()
        distinct_instrument_type_urls = get_distinct_instrument_type_urls_from_data_collections(data_collections)
        print('distinct_instrument_type_urls', distinct_instrument_type_urls)
        self.assertGreater(len(distinct_instrument_type_urls), 0)
        self.assertEqual(len(distinct_instrument_type_urls), len(set(distinct_instrument_type_urls)))

    def test_distinct_model_urls_are_retrieved_from_data_collections(self):
        """Returns a list of unique computation type URLs
        from all registered data collections.
        """
        register_data_collection_for_test()
        data_collections = DataCollection.objects.all()
        distinct_model_urls = get_distinct_computation_type_urls_from_data_collections(data_collections)
        print('distinct_model_urls', distinct_model_urls)
        self.assertEqual(len(distinct_model_urls), 0)
        self.assertEqual(len(distinct_model_urls), len(set(distinct_model_urls)))


class RegisteredOntologyTermsTestCase(TestCase):
    def test_registered_observed_properties_are_correct(self):
        """Returns a list of observed properties mentioned
        in registered metadata.
        """
        registered_observed_properties = get_registered_observed_properties()
        # print('registered_observed_properties', registered_observed_properties)
        self.assertTrue(isinstance(registered_observed_properties, list))

    def test_registered_features_of_interest_are_correct(self):
        """Returns a list of features of interest mentioned
        in registered metadata.
        """
        registered_observed_property_ids = get_registered_observed_properties()
        registered_features_of_interest = get_registered_features_of_interest(registered_observed_property_ids)
        # print('registered_features_of_interest', registered_features_of_interest)
        self.assertTrue(isinstance(registered_features_of_interest, list))
