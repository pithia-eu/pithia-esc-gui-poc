from django.test import (
    tag,
    TestCase,
)

from common.models import (
    ScientificMetadata,
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
    StaticDatasetEntry,
    DataSubset,
)
from common.test_setup import (
    register_acquisition_capabilities_for_test,
    register_acquisition_for_test,
    register_acquisition_with_instrument_for_test,
    register_all_metadata_types,
    register_data_subset_for_test,
    register_static_dataset_entry_for_test,
    register_static_dataset_for_test,
    register_computation_capabilities_2_for_test,
    register_computation_capabilities_for_test,
    register_computation_for_test,
    register_data_collection_for_test,
    register_individual_for_test,
    register_instrument_for_test,
    register_operation_for_test,
    register_organisation_for_test,
    register_platform_for_test,
    register_platform_with_child_platforms_for_test,
    register_process_for_test,
    register_project_for_test,
)


# Create your tests here.

class BulkDeleteByMetadataURLTestCase(TestCase):
    def setUp(self) -> None:
        register_all_metadata_types()
        return super().setUp()

    def test_delete_by_metadata_server_urls(self):
        """
        A registration is deleted if it corresponds with
        a URL within a list of metadata URLs.
        """
        metadata_server_urls = [m.metadata_server_url for m in list(ScientificMetadata.objects.all())]
        ScientificMetadata.objects.delete_by_metadata_server_urls(metadata_server_urls)
        remaining_registrations = list(ScientificMetadata.objects.all())
        self.assertEqual(len(remaining_registrations), 0)

class OrganisationDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.organisation = register_organisation_for_test()
        register_individual_for_test()
        register_project_for_test()
        register_platform_for_test()
        register_operation_for_test()
        register_instrument_for_test()
        register_data_collection_for_test()
        return super().setUp()

    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing an
        organisation are included in the delete chain.
        """
        immediate_metadata_dependents = self.organisation._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, Individual) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Project) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Platform) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Operation) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Instrument) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, DataCollection) for md in immediate_metadata_dependents))


class IndividualDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.individual = register_individual_for_test()
        register_project_for_test()
        register_platform_for_test()
        register_operation_for_test()
        register_instrument_for_test()
        register_data_collection_for_test()
        return super().setUp()
    
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing an
        individual are included in the delete chain.
        """
        immediate_metadata_dependents = self.individual._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, Project) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Platform) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Operation) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Instrument) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, DataCollection) for md in immediate_metadata_dependents))

class ProjectDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.project = register_project_for_test()
        register_data_collection_for_test()
        return super().setUp()

    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        project are included in the delete chain.
        """
        immediate_metadata_dependents = self.project._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, DataCollection) for md in immediate_metadata_dependents))

class PlatformDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.platform = register_platform_for_test()
        register_operation_for_test()
        register_platform_with_child_platforms_for_test()
        return super().setUp()

    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        platform are included in the delete chain.
        """
        immediate_metadata_dependents = self.platform._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, Operation) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Platform) for md in immediate_metadata_dependents))

class OperationDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        register_all_metadata_types()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing an
        operation are included in the delete chain.
        """
        operation = Operation.objects.all()[0]
        immediate_metadata_dependents = operation._immediate_metadata_dependents
        self.assertTrue(len(immediate_metadata_dependents) == 0)

class InstrumentDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.instrument = register_instrument_for_test()
        register_acquisition_capabilities_for_test()
        register_acquisition_with_instrument_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing an
        instrument are included in the delete chain.
        """
        immediate_metadata_dependents = self.instrument._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, AcquisitionCapabilities) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Acquisition) for md in immediate_metadata_dependents))

class AcquisitionCapabilitiesDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.acquisition_capabilities = register_acquisition_capabilities_for_test()
        register_acquisition_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing
        acquisition capabilities are included in the
        delete chain.
        """
        immediate_metadata_dependents = self.acquisition_capabilities._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, Acquisition) for md in immediate_metadata_dependents))

class AcquisitionDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.acquisition = register_acquisition_for_test()
        register_process_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing an
        acquisition are included in the delete chain.
        """
        immediate_metadata_dependents = self.acquisition._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, Process) for md in immediate_metadata_dependents))

class ComputationCapabilitiesDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.computation_capabilities = register_computation_capabilities_for_test()
        register_computation_capabilities_2_for_test()
        register_computation_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing
        computation capabilities are included in the
        delete chain.
        """
        immediate_metadata_dependents = self.computation_capabilities._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, ComputationCapabilities) for md in immediate_metadata_dependents))
        self.assertTrue(any(isinstance(md, Computation) for md in immediate_metadata_dependents))

class ComputationDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.computation = register_computation_for_test()
        register_process_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        computation are included in the delete chain.
        """
        immediate_metadata_dependents = self.computation._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, Process) for md in immediate_metadata_dependents))

class ProcessDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.process = register_process_for_test()
        register_data_collection_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        process are included in the delete chain.
        """
        immediate_metadata_dependents = self.process._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, DataCollection) for md in immediate_metadata_dependents))

class DataCollectionDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.data_collection = register_data_collection_for_test()
        register_data_subset_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        data collection are included in the delete
        chain.
        """
        immediate_metadata_dependents = self.data_collection._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, DataSubset) for md in immediate_metadata_dependents))

class StaticDatasetDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        self.catalogue = register_static_dataset_for_test()
        register_static_dataset_entry_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        static dataset are included in the delete chain.
        """
        immediate_metadata_dependents = self.catalogue._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, StaticDatasetEntry) for md in immediate_metadata_dependents))

class StaticDatasetEntryDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        register_static_dataset_for_test()
        self.static_dataset_entry = register_static_dataset_entry_for_test()
        register_data_subset_for_test()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        static dataset entry are included in the delete
        chain.
        """
        immediate_metadata_dependents = self.static_dataset_entry._immediate_metadata_dependents
        self.assertTrue(any(isinstance(md, DataSubset) for md in immediate_metadata_dependents))

class DataSubsetDeleteChainTestCase(TestCase):
    def setUp(self) -> None:
        register_all_metadata_types()
        return super().setUp()
        
    @tag('immediate_metadata_dependents')
    def test_delete_chain_contains_correct_metadata_types(self):
        """
        Metadata with a possibility of referencing a
        data subset are included in the delete chain.
        """
        data_subset = DataSubset.objects.all()[0]
        immediate_metadata_dependents = data_subset._immediate_metadata_dependents
        self.assertEqual(len(immediate_metadata_dependents), 0)

