import os
from django.test import (
    tag,
    TestCase,
)

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

@tag('metadata_dependents')
class CommonTestMixin:
    def setUp(self) -> None:
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Individual_Test.xml')) as xml_file:
            Individual.objects.create_from_xml_string(xml_file.read())
            
        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Project_Test.xml')) as xml_file:
            Project.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Platform_Test.xml')) as xml_file:
            Platform.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'Operation_Test.xml')) as xml_file:
            Operation.objects.create_from_xml_string(xml_file.read())

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

        if self.test_file_name != 'Catalogue_Test.xml':
            with open(os.path.join(_XML_METADATA_FILE_DIR, 'Catalogue_Test.xml')) as xml_file:
                Catalogue.objects.create_from_xml_string(xml_file.read())
        else:
            print('hi')

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'CatalogueEntry_Test_2023-01-01.xml')) as xml_file:
            CatalogueEntry.objects.create_from_xml_string(xml_file.read())

        with open(os.path.join(_XML_METADATA_FILE_DIR, 'DataSubset_Test-2023-01-01_DataCollectionTest.xml')) as xml_file:
            CatalogueDataSubset.objects.create_from_xml_string(xml_file.read())

        return super().setUp()
    
    def test_metadata_dependents(self):
        """
        metadata_dependents() returns all metadata
        registration dependents for a metadata
        instance.
        """
        self.metadata_registration = None
        with open(os.path.join(_XML_METADATA_FILE_DIR, self.test_file_name)) as xml_file:
            self.metadata_registration = self.model.objects.create_from_xml_string(xml_file.read())

class OrganisationTestCase(CommonTestMixin, TestCase):
    model = Organisation
    test_file_name = 'Organisation_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class IndividualTestCase(CommonTestMixin, TestCase):
    model = Individual
    test_file_name = 'Individual_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ProjectTestCase(CommonTestMixin, TestCase):
    model = Project
    test_file_name = 'Project_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class PlatformTestCase(CommonTestMixin, TestCase):
    model = Platform
    test_file_name = 'Platform_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class OperationTestCase(CommonTestMixin, TestCase):
    model = Operation
    test_file_name = 'Operation_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) == 0)

class InstrumentTestCase(CommonTestMixin, TestCase):
    model = Instrument
    test_file_name = 'Instrument_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class AcquisitionCapabilitiesTestCase(CommonTestMixin, TestCase):
    model = AcquisitionCapabilities
    test_file_name = 'AcquisitionCapabilities_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class AcquisitionTestCase(CommonTestMixin, TestCase):
    model = Acquisition
    test_file_name = 'Acquisition_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ComputationCapabilitiesTestCase(CommonTestMixin, TestCase):
    model = ComputationCapabilities
    test_file_name = 'ComputationCapabilities_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ComputationTestCase(CommonTestMixin, TestCase):
    model = Computation
    test_file_name = 'Computation_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ProcessTestCase(CommonTestMixin, TestCase):
    model = Process
    test_file_name = 'CompositeProcess_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class DataCollectionTestCase(CommonTestMixin, TestCase):
    model = DataCollection
    test_file_name = 'DataCollection_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class CatalogueTestCase(CommonTestMixin, TestCase):
    model = Catalogue
    test_file_name = 'Catalogue_Test.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class CatalogueEntryTestCase(CommonTestMixin, TestCase):
    model = CatalogueEntry
    test_file_name = 'CatalogueEntry_Test_2023-01-01.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class CatalogueDataSubsetTestCase(CommonTestMixin, TestCase):
    model = CatalogueDataSubset
    test_file_name = 'DataSubset_Test-2023-01-01_DataCollectionTest.xml'

    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) == 0)

