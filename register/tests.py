import environ
from django.test import (
    SimpleTestCase,
    TestCase,
)

from .metadata_builder.metadata_structures import (
    AcquisitionCapabilitiesMetadata,
    AcquisitionMetadata,
    CatalogueDataSubsetMetadata,
    CatalogueEntryMetadata,
    CatalogueMetadata,
    ComputationCapabilitiesMetadata,
    ComputationMetadata,
    DataCollectionMetadata,
    IndividualMetadata,
    InstrumentMetadata,
    OperationMetadata,
    OrganisationMetadata,
    PlatformMetadata,
    ProcessMetadata,
    ProjectMetadata,
    WorkflowMetadata,
)
from .test_data_structures import *

from common.models import InteractionMethod
from common.test_setup import (
    register_data_collection_for_test,
    register_organisation_for_test,
)

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'

env = environ.Env()

# Create your tests here.

class ManagerTestCase(TestCase):
    def test_create_from_xml_string(self):
        """
        Model.objects.create_from_xml_string() returns a new
        registration with an ID property.
        """
        try:
            organisation = register_organisation_for_test()
            print('organisation.id', organisation.id)
        except AttributeError as err:
            print(err)
            self.fail("'id' property was not found in ScientificMetadata type object.")

class InteractionMethodTestCase(TestCase):
    def test_create_api_interaction_method(self):
        """
        InteractionMethod.objects.create() returns a new
        API Interaction Method.
        """
        try:
            data_collection = register_data_collection_for_test()
            interaction_method = InteractionMethod.api_interaction_methods.create_api_interaction_method(
                'https://www.example.com',
                '',
                data_collection
            )
            print('interaction_method', interaction_method)
            print('interaction_method.type', interaction_method.type)
            print('interaction_method.config', interaction_method.config)
            print('interaction_method.scientific_metadata', interaction_method.scientific_metadata)
            print('data_collection.interactionmethod_set.all()', data_collection.interactionmethod_set.all())
            self.assertTrue(len(list(data_collection.interactionmethod_set.all())) > 0)
            print('Passed create_api_interaction_method() test.')
        except BaseException as err:
            print(err)
            self.fail('test_api_interaction_method_create() unexpectedly raised an error!')


class MetadataBuilderTestCase(SimpleTestCase):
    def test_organisation(self):
        organisation = OrganisationMetadata(ORGANISATION_PROPERTIES)
        print('organisation.xml', organisation.xml)

    def test_individual(self):
        individual = IndividualMetadata(INDIVIDUAL_PROPERTIES)
        print('individual.xml', individual.xml)

    def test_project(self):
        project = ProjectMetadata(PROJECT_PROPERTIES)
        print('project.xml', project.xml)

    def test_platform(self):
        platform = PlatformMetadata(PLATFORM_PROPERTIES)
        print('platform.xml', platform.xml)

    def test_operation(self):
        operation = OperationMetadata(OPERATION_PROPERTIES)
        print('operation.xml', operation.xml)

    def test_instrument(self):
        instrument = InstrumentMetadata(INSTRUMENT_PROPERTIES)
        print('instrument.xml', instrument.xml)

    def test_acquisition_capabilities(self):
        acquisition_capabilities = AcquisitionCapabilitiesMetadata(ACQUISITION_CAPABILITIES_PROPERTIES)
        print('acquisition_capabilities.xml', acquisition_capabilities.xml)

    def test_acquisition(self):
        acquisition = AcquisitionMetadata(ACQUISITION_PROPERTIES)
        print('acquisition.xml', acquisition.xml)

    def test_computation_capabilities(self):
        computation_capabilities = ComputationCapabilitiesMetadata(COMPUTATION_CAPABILITIES_PROPERTIES)
        print('computation_capabilities.xml', computation_capabilities.xml)

    def test_computation(self):
        computation = ComputationMetadata(COMPUTATION_PROPERTIES)
        print('computation.xml', computation.xml)

    def test_process(self):
        process = ProcessMetadata(PROCESS_PROPERTIES)
        print('process.xml', process.xml)

    def test_data_collection(self):
        data_collection = DataCollectionMetadata(DATA_COLLECTION_PROPERTIES)
        print('data_collection.xml', data_collection.xml)

    def test_catalogue(self):
        catalogue = CatalogueMetadata(CATALOGUE_PROPERTIES)
        print('catalogue.xml', catalogue.xml)

    def test_catalogue_entry(self):
        catalogue_entry = CatalogueEntryMetadata(CATALOGUE_ENTRY_PROPERTIES)
        print('catalogue_entry.xml', catalogue_entry.xml)

    def test_catalogue_data_subset(self):
        catalogue_data_subset = CatalogueDataSubsetMetadata(CATALOGUE_DATA_SUBSET_PROPERTIES)
        print('catalogue_data_subset.xml', catalogue_data_subset.xml)

    def test_workflow(self):
        workflow = WorkflowMetadata(WORKFLOW_PROPERTIES)
        print('workflow.xml', workflow.xml)