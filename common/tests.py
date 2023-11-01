from django.test import TestCase

from .models import (
    AcquisitionCapabilities,
    ComputationCapabilities,
    Instrument,
    Organisation,
)

from common.test_xml_files import (
    ACQUISITION_CAPABILITIES_METADATA_XML,
    COMPUTATION_CAPABILITIES_METADATA_XML,
    COMPUTATION_CAPABILITIES_2_METADATA_XML,
    COMPUTATION_CAPABILITIES_3_METADATA_XML,
    COMPUTATION_CAPABILITIES_4_METADATA_XML,
    COMPUTATION_CAPABILITIES_4a_METADATA_XML,
    INSTRUMENT_METADATA_XML,
    ORGANISATION_METADATA_XML,
)


# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'

# Create your tests here.
class ScientificMetadataPropertiesTestCase(TestCase):
    def test_metadata_registration_has_metadata_server_url(self):
        """
        Test that a scientific metadata registration
        has a metadata server URL.
        """
        xml_file = ORGANISATION_METADATA_XML
        xml_string = xml_file.read()
        organisation = Organisation.objects.create_from_xml_string(xml_string, SAMPLE_INSTITUTION_ID, SAMPLE_USER_ID)
        try:
            metadata_server_url = organisation.metadata_server_url
            print('metadata_server_url', metadata_server_url)
        except BaseException:
            print('Unable to get metadata server URL from registration.')


class AcquisitionCapabilitiesQuerySetSearchTestCase(TestCase):
    def setUp(self):
        acquisition_capabilities_xml_file = ACQUISITION_CAPABILITIES_METADATA_XML
        acquisition_capabilities_xml_file.seek(0)
        acquisition_capabilities_xml_string = acquisition_capabilities_xml_file.read()
        AcquisitionCapabilities.objects.create_from_xml_string(acquisition_capabilities_xml_string)
        
        instrument_xml_file = INSTRUMENT_METADATA_XML
        instrument_xml_file.seek(0)
        instrument_xml_string = instrument_xml_file.read()
        Instrument.objects.create_from_xml_string(instrument_xml_string)

        return super().setUp()

    def test_correct_registrations_retrieved_for_search(self):
        """
        Verify the subset of Acquisition Capabilities retrieved
        for the ontology-based search based on some Instrument
        URLs and Observed Properties.
        """
        # Input data
        instrument_urls = ['https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test']
        observed_property_urls = [
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization',
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift',
        ]
        acquisition_capability_sets = AcquisitionCapabilities.objects.for_search(instrument_urls, observed_property_urls)
        self.assertTrue(len(acquisition_capability_sets) > 0)

    def test_correct_registrations_retrieved_with_bad_input_data(self):
        """
        Verify that the subset of Acquisition Capabilities retrieved
        for the ontology-based search returns the correct results.
        """
        instrument_urls = ['https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test']
        bad_observed_property_urls = [
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/bad',
        ]
        acquisition_capability_sets_empty = AcquisitionCapabilities.objects.for_search(instrument_urls, bad_observed_property_urls)
        self.assertEqual(len(acquisition_capability_sets_empty), 0)

    def test_correct_registrations_retrieved_with_instrument_urls_and_no_observed_properties(self):
        """
        Verify that the subset of Acquisition Capabilities retrieved
        for the ontology-based search returns the correct results.
        """
        instrument_urls = ['https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test']
        observed_property_urls = []
        acquisition_capability_sets = AcquisitionCapabilities.objects.for_search(instrument_urls, observed_property_urls)
        self.assertEqual(len(acquisition_capability_sets), 1)


class ComputationCapabilitiesQuerySetTestCase(TestCase):
    def test_all_computation_capability_set_referers(self):
        """
        Recursively retrieve a list of Computation Capabilities
        registrations that reference other Computation Capabilities
        registrations, starting from a given Computation Capabilities
        registration.
        """
        # Register the Computation Capabilities XML files
        computation_capabilities_file_1 = COMPUTATION_CAPABILITIES_METADATA_XML
        test_computation_capability_set = ComputationCapabilities.objects.create_from_xml_string(computation_capabilities_file_1.read())

        # Each file in this list references the file
        # preceding it (e.g., CC4a references CC4,
        # CC4 references CC3, and so on) so the number
        # of resultant referers should be equal to the
        # number of files in this list.
        computation_capabilities_referer_files = [
            COMPUTATION_CAPABILITIES_2_METADATA_XML,
            COMPUTATION_CAPABILITIES_3_METADATA_XML,
            COMPUTATION_CAPABILITIES_4_METADATA_XML,
            COMPUTATION_CAPABILITIES_4a_METADATA_XML,
        ]
        for xml_file in computation_capabilities_referer_files:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())
        
        # Execute all_computation_capability_set_referers()
        ccs_referers = ComputationCapabilities.objects.all_computation_capability_set_referers(test_computation_capability_set)
        print('ccs_referers', [r.localid for r in ccs_referers])
        print('len(ccs_referers)', len(ccs_referers))
        self.assertEqual(len(ccs_referers), len(computation_capabilities_referer_files))


class ComputationCapabilitiesQuerySetSearchTestCase(TestCase):
    def setUp(self):
        # Register the Computation Capabilities XML files
        computation_capabilities_file_1 = COMPUTATION_CAPABILITIES_METADATA_XML
        computation_capabilities_file_1.seek(0)
        ComputationCapabilities.objects.create_from_xml_string(computation_capabilities_file_1.read())

        computation_capabilities_file_2 = COMPUTATION_CAPABILITIES_2_METADATA_XML
        computation_capabilities_file_2.seek(0)
        ComputationCapabilities.objects.create_from_xml_string(computation_capabilities_file_2.read())

        computation_capabilities_file_3 = COMPUTATION_CAPABILITIES_3_METADATA_XML
        computation_capabilities_file_3.seek(0)
        ComputationCapabilities.objects.create_from_xml_string(computation_capabilities_file_3.read())

        computation_capabilities_file_4 = COMPUTATION_CAPABILITIES_4_METADATA_XML
        computation_capabilities_file_4.seek(0)
        ComputationCapabilities.objects.create_from_xml_string(computation_capabilities_file_4.read())

        computation_capabilities_file_4a = COMPUTATION_CAPABILITIES_4a_METADATA_XML
        computation_capabilities_file_4a.seek(0)
        ComputationCapabilities.objects.create_from_xml_string(computation_capabilities_file_4a.read())
        
        return super().setUp()

    def test_correct_registrations_are_returned_for_search(self):
        """
        ComputationCapabilities.objects.for_search() returns
        a QuerySet of Computation Capabilities registrations.
        """
        computation_type_urls = [
            'https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual',
        ]

        search_results = ComputationCapabilities.objects.for_search(computation_type_urls, [])
        # The number of results is the (number of registrations matching) + (number of referers).
        # In this case, it is (1) + (4).
        self.assertEqual(len(search_results), 5)

    def test_referers_for_search_works_correctly(self):
        computation_type_urls_2 = [
            'https://metadata.pithia.eu/ontology/2.2/computationType/Test',
        ]

        # Only CC_4a should match here, which has no referers.
        search_results_2 = ComputationCapabilities.objects.for_search(computation_type_urls_2, [])
        self.assertEqual(len(search_results_2), 1)
