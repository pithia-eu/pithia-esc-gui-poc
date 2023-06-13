import os
from django.test import (
    tag,
    TestCase,
)

from common.models import (
    ScientificMetadata,
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

def _register_metadata_file_for_test(test_file_name, model):
    metadata_registration = None
    with open(os.path.join(_XML_METADATA_FILE_DIR, test_file_name)) as xml_file:
        metadata_registration = model.objects.create_from_xml_string(xml_file.read())
    return metadata_registration

def _register_organisation_for_test():
    return _register_metadata_file_for_test('Organisation_Test.xml', Organisation)

def _register_individual_for_test():
    return _register_metadata_file_for_test('Individual_Test.xml', Individual)

def _register_project_for_test():
    return _register_metadata_file_for_test('Project_Test.xml', Project)

def _register_platform_for_test():
    return _register_metadata_file_for_test('Platform_Test.xml', Platform)

def _register_operation_for_test():
    return _register_metadata_file_for_test('Operation_Test.xml', Operation)

def _register_instrument_for_test():
    return _register_metadata_file_for_test('Instrument_Test.xml', Instrument)

def _register_acquisition_capabilities_for_test():
    return _register_metadata_file_for_test('AcquisitionCapabilities_Test.xml', AcquisitionCapabilities)

def _register_acquisition_for_test():
    return _register_metadata_file_for_test('Acquisition_Test.xml', Acquisition)

def _register_computation_capabilities_for_test():
    return _register_metadata_file_for_test('ComputationCapabilities_Test.xml', ComputationCapabilities)

def _register_computation_for_test():
    return _register_metadata_file_for_test('Computation_Test.xml', Computation)

def _register_process_for_test():
    return _register_metadata_file_for_test('CompositeProcess_Test.xml', Process)

def _register_data_collection_for_test():
    return _register_metadata_file_for_test('DataCollection_Test.xml', DataCollection)

def _register_catalogue_for_test():
    return _register_metadata_file_for_test('Catalogue_Test.xml', Catalogue)

def _register_catalogue_entry_for_test():
    return _register_metadata_file_for_test('CatalogueEntry_Test_2023-01-01.xml', CatalogueEntry)

def _register_catalogue_data_subset_for_test():
    return _register_metadata_file_for_test('DataSubset_Test-2023-01-01_DataCollectionTest.xml', CatalogueDataSubset)

def _register_all_metadata_types():
    _register_organisation_for_test()
    _register_individual_for_test()
    _register_project_for_test()
    _register_platform_for_test()
    _register_operation_for_test()
    _register_instrument_for_test()
    _register_acquisition_capabilities_for_test()
    _register_acquisition_for_test()
    _register_computation_capabilities_for_test()
    _register_computation_for_test()
    _register_process_for_test()
    _register_data_collection_for_test()
    _register_catalogue_for_test()
    _register_catalogue_entry_for_test()
    _register_catalogue_data_subset_for_test()

class MetadataTestCase(TestCase):
    def setUp(self) -> None:
        _register_all_metadata_types()
        return super().setUp()

    def test_delete_by_metadata_server_urls(self):
        """
        Model.objects.delete_by_metadata_server_urls() deletes all
        metadata registrations corresponding to at least one URL
        from a list of metadata server URLs.
        """
        metadata_server_urls = [m.metadata_server_url for m in list(ScientificMetadata.objects.all())]
        ScientificMetadata.objects.delete_by_metadata_server_urls(metadata_server_urls)
        remaining_registrations = list(ScientificMetadata.objects.all())
        self.assertTrue(len(remaining_registrations) == 0)

class OrganisationTestCase(TestCase):
    def setUp(self) -> None:
        self.organisation = _register_organisation_for_test()
        _register_individual_for_test()
        _register_project_for_test()
        _register_platform_for_test()
        _register_operation_for_test()
        _register_instrument_for_test()
        _register_data_collection_for_test()
        return super().setUp()

    def test_immediate_metadata_dependents(self):
        immediate_metadata_dependents = self.organisation._immediate_metadata_dependents
        print('immediate_metadata_dependents', immediate_metadata_dependents)
        self.assertTrue(any(isinstance(md, Individual) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Project) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Platform) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Operation) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Instrument) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, DataCollection) for md in immediate_metadata_dependents))

class IndividualTestCase(TestCase):
    def setUp(self) -> None:
        self.individual = _register_individual_for_test()
        _register_project_for_test()
        _register_platform_for_test()
        _register_operation_for_test()
        _register_instrument_for_test()
        _register_data_collection_for_test()
        return super().setUp()
    
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ProjectTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class PlatformTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class OperationTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) == 0)

class InstrumentTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class AcquisitionCapabilitiesTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class AcquisitionTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ComputationCapabilitiesTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ComputationTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class ProcessTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class DataCollectionTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class CatalogueTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class CatalogueEntryTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) > 0)

class CatalogueDataSubsetTestCase(TestCase):
    def test_metadata_dependents(self):
        super().test_metadata_dependents()
        self.assertTrue(len(self.metadata_registration.metadata_dependents) == 0)

