import os
from django.test import TestCase

from .services import (
    find_data_collections_for_simple_search,
    find_metadata_registrations_matching_query,
    find_metadata_registrations_matching_query_exactly,
)

from common import models
from pithiaesc.settings import BASE_DIR


_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.
class SimpleSearchTestCase(TestCase):
    def setUp(self) -> None:
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            models.Organisation.objects.create_from_xml_string(xml_file.read())
            
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Individual_Test.xml')) as xml_file:
            models.Individual.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Project_Test.xml')) as xml_file:
            models.Project.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Platform_Test.xml')) as xml_file:
            models.Platform.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Operation_Test.xml')) as xml_file:
            models.Operation.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Instrument_Test.xml')) as xml_file:
            models.Instrument.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'AcquisitionCapabilities_Test.xml')) as xml_file:
            models.AcquisitionCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Acquisition_Test.xml')) as xml_file:
            models.Acquisition.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Computation_Test.xml')) as xml_file:
            models.ComputationCapabilities.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'ComputationCapabilities_Test.xml')) as xml_file:
            models.Computation.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'CompositeProcess_Test.xml')) as xml_file:
            models.Process.objects.create_from_xml_string(xml_file.read())
            
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_Test.xml')) as xml_file:
            models.DataCollection.objects.create_from_xml_string(xml_file.read())

        return super().setUp()

    
    def test_find_metadata_registrations_matching_query(self):
        """
        Searches only the given Model's registrations and returns
        registrations matching the query.
        """
        organisations = find_metadata_registrations_matching_query('lorem', models.Organisation)
        data_collections = find_metadata_registrations_matching_query('lorem', models.DataCollection)

        self.assertEqual(len(organisations), 1)
        self.assertEqual(len(data_collections), 1)

    def test_find_registrations_matching_query_exactly(self):
        """
        Searches on the given Model's registrations and returns
        registrations matching the query exactly.
        """
        data_collections_1 = find_metadata_registrations_matching_query_exactly('Lorem', models.DataCollection)
        data_collections_2 = find_metadata_registrations_matching_query_exactly('lorem', models.DataCollection)
        data_collections_3 = find_metadata_registrations_matching_query_exactly('Lorem  ', models.DataCollection)
        data_collections_4 = find_metadata_registrations_matching_query_exactly('Lorem ', models.DataCollection)

        print('len(data_collections_1)', len(data_collections_1))
        print('len(data_collections_2)', len(data_collections_2))
        print('len(data_collections_3)', len(data_collections_3))
        print('len(data_collections_4)', len(data_collections_4))

        self.assertEqual(len(data_collections_1), 1)
        self.assertEqual(len(data_collections_2), 0)
        self.assertEqual(len(data_collections_3), 0)


    def test_for_simple_search(self):
        """
        Performs a simple search returning Data Collections matching
        the query.
        """
        # Disable "using" parameter in managers.py before running test
        # Case-insensitive match
        data_collections_1 = find_data_collections_for_simple_search('lorem')

        # Partial case-insensitive match
        data_collections_2 = find_data_collections_for_simple_search('lor')

        # No match
        data_collections_3 = find_data_collections_for_simple_search('xyz')

        # Attribute matching shouldn't work
        data_collections_4 = find_data_collections_for_simple_search('image-png')

        print('len(data_collections_1)', len(data_collections_1))
        print('len(data_collections_2)', len(data_collections_2))
        print('len(data_collections_3)', len(data_collections_3))
        print('len(data_collections_4)', len(data_collections_4))

        self.assertEqual(len(data_collections_1), 1)
        self.assertEqual(len(data_collections_2), 1)
        self.assertEqual(len(data_collections_3), 1)
        self.assertEqual(len(data_collections_4), 0)
        