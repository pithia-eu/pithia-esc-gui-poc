from django.test import SimpleTestCase

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

from validation.services import MetadataFileXSDValidator

# Create your tests here.

class MetadataBuilderTestCase(SimpleTestCase):
    def test_organisation(self):
        organisation = OrganisationMetadata(ORGANISATION_PROPERTIES_FULL)
        print('organisation.xml', organisation.xml)

    def test_individual(self):
        individual = IndividualMetadata(INDIVIDUAL_PROPERTIES_FULL)
        print('individual.xml', individual.xml)

    def test_project(self):
        project = ProjectMetadata(PROJECT_PROPERTIES_FULL)
        print('project.xml', project.xml)

    def test_platform(self):
        platform = PlatformMetadata(PLATFORM_PROPERTIES_FULL)
        print('platform.xml', platform.xml)

    def test_operation(self):
        operation = OperationMetadata(OPERATION_PROPERTIES_FULL)
        print('operation.xml', operation.xml)

    def test_instrument(self):
        instrument = InstrumentMetadata(INSTRUMENT_PROPERTIES_FULL)
        print('instrument.xml', instrument.xml)

    def test_acquisition_capabilities(self):
        acquisition_capabilities = AcquisitionCapabilitiesMetadata(ACQUISITION_CAPABILITIES_PROPERTIES_FULL)
        print('acquisition_capabilities.xml', acquisition_capabilities.xml)

    def test_acquisition(self):
        acquisition = AcquisitionMetadata(ACQUISITION_PROPERTIES_FULL)
        print('acquisition.xml', acquisition.xml)

    def test_computation_capabilities(self):
        computation_capabilities = ComputationCapabilitiesMetadata(COMPUTATION_CAPABILITIES_PROPERTIES_FULL)
        print('computation_capabilities.xml', computation_capabilities.xml)

    def test_computation(self):
        computation = ComputationMetadata(COMPUTATION_PROPERTIES_FULL)
        print('computation.xml', computation.xml)

    def test_process(self):
        process = ProcessMetadata(PROCESS_PROPERTIES_FULL)
        print('process.xml', process.xml)

    def test_data_collection(self):
        data_collection = DataCollectionMetadata(DATA_COLLECTION_PROPERTIES_FULL)
        print('data_collection.xml', data_collection.xml)

    def test_catalogue(self):
        catalogue = CatalogueMetadata(CATALOGUE_PROPERTIES_FULL)
        print('catalogue.xml', catalogue.xml)

    def test_catalogue_entry(self):
        catalogue_entry = CatalogueEntryMetadata(CATALOGUE_ENTRY_PROPERTIES_FULL)
        print('catalogue_entry.xml', catalogue_entry.xml)

    def test_catalogue_data_subset(self):
        catalogue_data_subset = CatalogueDataSubsetMetadata(CATALOGUE_DATA_SUBSET_PROPERTIES_FULL)
        print('catalogue_data_subset.xml', catalogue_data_subset.xml)

    def test_workflow(self):
        workflow = WorkflowMetadata(WORKFLOW_PROPERTIES_FULL)
        print('workflow.xml', workflow.xml)

class MetadataBuilderXSDComplianceTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.schema = MetadataFileXSDValidator._instantiate_pithia_schema()
        return super().setUp()

    def create_xml_and_validate_against_schema(self, metadata_builder, properties):
        metadata = metadata_builder(properties)
        xml = metadata.xml
        print('xml', xml)
        MetadataFileXSDValidator._validate_xml_file_string_against_schema(xml, self.schema)

    # Organisation
    def test_organisation(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_FULL)

    def test_organisation_no_contact_info(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_NO_CONTACT_INFO)

    def test_organisation_partial_contact_info(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_PARTIAL_CONTACT_INFO)

    def test_organisation_no_address(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_NO_ADDRESS)

    def test_organisation_partial_address(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_PARTIAL_ADDRESS)

    # Individual
    def test_individual(self):
        self.create_xml_and_validate_against_schema(IndividualMetadata, INDIVIDUAL_PROPERTIES_FULL)

    def test_individual_no_contact_info(self):
        self.create_xml_and_validate_against_schema(IndividualMetadata, INDIVIDUAL_PROPERTIES_NO_CONTACT_INFO)

    # Project
    def test_project(self):
        self.create_xml_and_validate_against_schema(ProjectMetadata, PROJECT_PROPERTIES_FULL)