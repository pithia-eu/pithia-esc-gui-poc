import os
from django.test import TestCase
from pithiaesc.settings import BASE_DIR

from .models import (
    Organisation,
    AcquisitionCapabilities
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