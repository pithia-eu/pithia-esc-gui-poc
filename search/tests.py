import os
from django.test import (
    SimpleTestCase,
    TestCase,
)

from .services import (
    find_matching_data_collections,
    get_observed_property_urls_by_instrument_types,
    get_observed_property_urls_by_computation_types,
    group_instrument_types_by_observed_property,
    group_computation_types_by_observed_property,
)
from .views import (
    get_registered_observed_properties,
    get_registered_features_of_interest
)

from common.models import (
    Instrument,
    AcquisitionCapabilities,
    Acquisition,
    ComputationCapabilities,
    Computation,
    Process,
    DataCollection,
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
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.

class SearchTestCase(TestCase):
    def setUp(self) -> None:
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Instrument_Test.xml')) as xml_file:
            Instrument.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'AcquisitionCapabilities_Test.xml')) as xml_file:
            AcquisitionCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Acquisition_Test.xml')) as xml_file:
            Acquisition.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Computation_Test.xml')) as xml_file:
            Computation.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'CompositeProcess_Test.xml')) as xml_file:
            Process.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_Test.xml')) as xml_file:
            DataCollection.objects.create_from_xml_string(xml_file.read())

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
    def test_find_matching_data_collections_with_instrument_types(self):
        """
        find_matching_data_collections() returns a list of
        data collections when passing in just instrument
        types.
        """
        # Register XML files
        # Pass in instrument types
        data_collections = find_matching_data_collections(feature_of_interest_urls=self.feature_of_interest_urls)
        # Pass in computation types
        # Pass in observed properties
        print('data_collections', data_collections)
        print('len(data_collections)', len(data_collections))
        self.assertTrue(len(data_collections) > 0)


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
