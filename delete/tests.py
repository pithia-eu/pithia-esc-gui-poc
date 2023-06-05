import os
from django.test import TestCase

from common.models import (
    Organisation,
    Individual,
    Project,
    Platform,
    Operation,
    Instrument,
    AcquisitionCapabilities,
    Acquisition,
    ComputationCapabilities,
    Computation,
    Process,
    DataCollection,
    Catalogue,
    CatalogueEntry,
    CatalogueDataSubset,
)
from pithiaesc.settings import BASE_DIR

_XML_METADATA_FILE_DIR = os.path.join(BASE_DIR, 'common', 'test_files', 'xml_metadata_files')

# Create your tests here.

class OrganisationTestCase(TestCase):
    def setUp(self) -> None:
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Individual_Test.xml')) as xml_file:
            Individual.objects.create_from_xml_string(xml_file.read())
            
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Project_Test.xml')) as xml_file:
            project = Project.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Platform_Test.xml')) as xml_file:
            Platform.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Instrument_Test.xml')) as xml_file:
            Instrument.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataCollection_Test.xml')) as xml_file:
            DataCollection.objects.create_from_xml_string(xml_file.read())

        return super().setUp()
    
    def test_metadata_dependents(self):
        """
        metadata_dependents() returns all metadata
        registration dependents for an
        Organisation.
        """
        organisation = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Organisation_Test.xml')) as xml_file:
            organisation = Organisation.objects.create_from_xml_string(xml_file.read())
        print('organisation.metadata_dependents' , organisation.metadata_dependents)
        print('len(organisation.metadata_dependents)' , len(organisation.metadata_dependents))
        self.assertTrue(len(organisation.metadata_dependents) > 0)

