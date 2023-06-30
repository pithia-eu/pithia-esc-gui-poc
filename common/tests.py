import os
from django.test import TestCase
from pithiaesc.settings import BASE_DIR

from .models import (
    Organisation,
    AcquisitionCapabilities,
    ComputationCapabilities,
)

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.
class ScientificMetadataModelTestCase(TestCase):
    def test_metadata_server_url(self):
        """
        Model.metadata_server_url returns the metadata server
        URL for a scientific metadata registration.
        """
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            xml_string = xml_file.read()
            organisation = Organisation.objects.create_from_xml_string(xml_string)
        metadata_server_url = organisation.metadata_server_url
        print('metadata_server_url', metadata_server_url)

class AcquisitionCapabilitiesQuerySetTestCase(TestCase):
    def test_for_search(self):
        """
        AcquisitionCapabilities.objects.for_search() returns
        an intersect of the passed in Instrument URLs and
        Observed Properties.
        """
        instrument_urls = ['https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test']
        observed_property_urls = [
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_ElectricFieldStrength',
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_Polarization',
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/EM-Wave_DopplerFrequencyShift',
        ]
        bad_observed_property_urls = [
            'https://metadata.pithia.eu/ontology/2.2/observedProperty/bad',
        ]
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'AcquisitionCapabilities_Test.xml')) as xml_file:
            xml_string = xml_file.read()
            acquisition_capability_set = AcquisitionCapabilities.objects.create_from_xml_string(xml_string)
        acquisition_capability_sets = AcquisitionCapabilities.objects.for_search(instrument_urls, observed_property_urls)
        acquisition_capability_sets_empty = AcquisitionCapabilities.objects.for_search(instrument_urls, bad_observed_property_urls)
        self.assertTrue(len(acquisition_capability_sets) > 0)
        print('acquisition_capability_sets', acquisition_capability_sets)
        self.assertTrue(len(acquisition_capability_sets_empty) == 0)
        print('acquisition_capability_sets_empty', acquisition_capability_sets_empty)
        print('Passed AcquisitionCapabilitiesQuerySetTestCase.test_for_search().')

class ComputationCapabilitiesQuerySetTestCase(TestCase):
    def test_all_computation_capability_set_referers(self):
        """
        ComputationCapabilities.objects.all_computation_capability_set_referers()
        returns a list of Computation Capabilities registrations that reference a
        given Computation Capabilities registration.
        """
        # Register the Computation Capabilities XML files
        test_computation_capability_set = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test.xml')) as xml_file:
            test_computation_capability_set = ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_2.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_3.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_4.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_4a.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())
        
        # Execute all_computation_capability_set_referers()
        ccs_referers = ComputationCapabilities.objects.all_computation_capability_set_referers(test_computation_capability_set)
        print('ccs_referers', [r.localid for r in ccs_referers])
        print('len(ccs_referers)', len(ccs_referers))
        self.assertTrue(len(ccs_referers) > 0)

    def test_for_search(self):
        """
        ComputationCapabilities.objects.for_search() returns
        a QuerySet of Computation Capabilities registrations.
        """
        computation_type_urls = [
            'https://metadata.pithia.eu/ontology/2.2/computationType/IonogramScaling_Manual',
        ]
        computation_type_urls_2 = [
            'https://metadata.pithia.eu/ontology/2.2/computationType/Test',
        ]

        # Register the Computation Capabilities XML files
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_2.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_3.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_4.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test_4a.xml')) as xml_file:
            ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        search_results = ComputationCapabilities.objects.for_search(computation_type_urls, [])
        print('search_results', search_results)
        print('len(search_results)', len(search_results))
        self.assertTrue(len(search_results) > 0)

        print('Start of test 2')
        search_results_2 = ComputationCapabilities.objects.for_search(computation_type_urls_2, [])
        print('search_results_2', [sr.localid for sr in search_results_2])
        print('len(search_results_2)', len(search_results_2))
        self.assertTrue(len(search_results_2) > 0)
