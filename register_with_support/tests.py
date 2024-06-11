from django.test import (
    SimpleTestCase,
    tag,
)
from lxml import etree
from xmlschema.validators.exceptions import (
    XMLSchemaChildrenValidationError,
    XMLSchemaDecodeError,
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

from validation.services import MetadataFileXSDValidator

# Create your tests here.

class MetadataBuilderTestCase(SimpleTestCase):
    def test_organisation(self):
        organisation = OrganisationMetadata(ORGANISATION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in organisation.xml)
        print('organisation.xml', organisation.xml)

    def test_individual(self):
        individual = IndividualMetadata(INDIVIDUAL_PROPERTIES_FULL)
        self.assertFalse('<ns1' in individual.xml)
        print('individual.xml', individual.xml)

    def test_project(self):
        project = ProjectMetadata(PROJECT_PROPERTIES_FULL)
        self.assertFalse('<ns1' in project.xml)
        print('project.xml', project.xml)

    def test_platform(self):
        platform = PlatformMetadata(PLATFORM_PROPERTIES_FULL)
        self.assertFalse('<ns1' in platform.xml)
        print('platform.xml', platform.xml)

    def test_platform_no_url(self):
        platform = PlatformMetadata(PLATFORM_PROPERTIES_NO_URL)
        platform_parsed = etree.fromstring(platform.xml)
        self.assertFalse(hasattr(platform_parsed, 'URL'))

    def test_platform_no_geometry_location(self):
        platform = PlatformMetadata(PLATFORM_PROPERTIES_NO_GEOMETRY_LOCATION)
        platform_parsed = etree.fromstring(platform.xml)
        self.assertEqual(len(platform_parsed.xpath('//geometryLocation')), 0)

    def test_operation(self):
        operation = OperationMetadata(OPERATION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in operation.xml)
        print('operation.xml', operation.xml)

    def test_instrument(self):
        instrument = InstrumentMetadata(INSTRUMENT_PROPERTIES_FULL)
        self.assertFalse('<ns1' in instrument.xml)
        print('instrument.xml', instrument.xml)

    def test_acquisition_capabilities(self):
        acquisition_capabilities = AcquisitionCapabilitiesMetadata(ACQUISITION_CAPABILITIES_PROPERTIES_FULL)
        self.assertFalse('<ns1' in acquisition_capabilities.xml)
        print('acquisition_capabilities.xml', acquisition_capabilities.xml)

    def test_acquisition(self):
        acquisition = AcquisitionMetadata(ACQUISITION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in acquisition.xml)
        print('acquisition.xml', acquisition.xml)

    def test_acquisition_with_blank_acq_caps(self):
        acquisition = AcquisitionMetadata(ACQUISITION_PROPERTIES_WITH_BLANK_ACQ_CAPS)
        print('acquisition.xml', acquisition.xml)

    def test_computation_capabilities(self):
        computation_capabilities = ComputationCapabilitiesMetadata(COMPUTATION_CAPABILITIES_PROPERTIES_FULL)
        self.assertFalse('<ns1' in computation_capabilities.xml)
        print('computation_capabilities.xml', computation_capabilities.xml)

    def test_computation(self):
        computation = ComputationMetadata(COMPUTATION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in computation.xml)
        print('computation.xml', computation.xml)

    def test_process(self):
        process = ProcessMetadata(PROCESS_PROPERTIES_FULL)
        self.assertFalse('<ns1' in process.xml)
        print('process.xml', process.xml)

    @tag('data_collection')
    def test_data_collection(self):
        data_collection = DataCollectionMetadata(DATA_COLLECTION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in data_collection.xml)
        print('data_collection.xml', data_collection.xml)

    @tag('data_collection')
    def test_data_collection_with_html_in_localid(self):
        data_collection = DataCollectionMetadata(DATA_COLLECTION_WITH_LOCALID_HTML)
        print('data_collection.xml', data_collection.xml)

    @tag('data_collection')
    def test_data_collection_with_html(self):
        data_collection = DataCollectionMetadata(DATA_COLLECTION_WITH_HTML)
        print('data_collection.xml', data_collection.xml)

    def test_catalogue(self):
        catalogue = CatalogueMetadata(CATALOGUE_PROPERTIES_FULL)
        self.assertFalse('<ns1' in catalogue.xml)
        print('catalogue.xml', catalogue.xml)

    def test_catalogue_entry(self):
        catalogue_entry = CatalogueEntryMetadata(CATALOGUE_ENTRY_PROPERTIES_FULL)
        self.assertFalse('<ns1' in catalogue_entry.xml)
        print('catalogue_entry.xml', catalogue_entry.xml)

    def test_catalogue_data_subset(self):
        catalogue_data_subset = CatalogueDataSubsetMetadata(CATALOGUE_DATA_SUBSET_PROPERTIES_FULL)
        self.assertFalse('<ns1' in catalogue_data_subset.xml)
        print('catalogue_data_subset.xml', catalogue_data_subset.xml)

    def test_workflow(self):
        workflow = WorkflowMetadata(WORKFLOW_PROPERTIES_FULL)
        self.assertFalse('<ns1' in workflow.xml)
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
    @tag('organisation', 'slow')
    def test_organisation(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_FULL)

    @tag('organisation', 'slow')
    def test_organisation_no_contact_info(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_NO_CONTACT_INFO)

    @tag('organisation', 'slow')
    def test_organisation_partial_contact_info(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_PARTIAL_CONTACT_INFO)

    @tag('organisation', 'slow')
    def test_organisation_no_address(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_NO_ADDRESS)

    @tag('organisation', 'slow')
    def test_organisation_partial_address(self):
        self.create_xml_and_validate_against_schema(OrganisationMetadata, ORGANISATION_PROPERTIES_PARTIAL_ADDRESS)

    # Individual
    @tag('individual', 'slow')
    def test_individual(self):
        self.create_xml_and_validate_against_schema(IndividualMetadata, INDIVIDUAL_PROPERTIES_FULL)

    @tag('individual', 'slow')
    def test_individual_no_contact_info(self):
        self.create_xml_and_validate_against_schema(IndividualMetadata, INDIVIDUAL_PROPERTIES_NO_CONTACT_INFO)

    # Project
    @tag('project', 'slow')
    def test_project(self):
        self.create_xml_and_validate_against_schema(ProjectMetadata, PROJECT_PROPERTIES_FULL)

    @tag('project', 'slow')
    def test_project_no_citation_title(self):
        self.create_xml_and_validate_against_schema(ProjectMetadata, PROJECT_PROPERTIES_NO_CITATION_TITLE)

    @tag('project', 'slow')
    def test_project_no_citation_date_fails(self):
        """
        Fails the test as a valid date is required if
        other citation details are provided.
        """
        self.assertRaises(XMLSchemaDecodeError, self.create_xml_and_validate_against_schema, ProjectMetadata, PROJECT_PROPERTIES_NO_CITATION_DATE)

    # Platform
    @tag('platform', 'slow')
    def test_platform(self):
        self.create_xml_and_validate_against_schema(PlatformMetadata, PLATFORM_PROPERTIES_FULL)

    @tag('platform', 'slow')
    def test_platform_no_url(self):
        self.create_xml_and_validate_against_schema(PlatformMetadata, PLATFORM_PROPERTIES_NO_URL)

    @tag('platform', 'slow')
    def test_platform_no_geometry_location(self):
        self.create_xml_and_validate_against_schema(PlatformMetadata, PLATFORM_PROPERTIES_NO_GEOMETRY_LOCATION)

    # Operation
    @tag('operation', 'slow')
    def test_operation(self):
        self.create_xml_and_validate_against_schema(OperationMetadata, OPERATION_PROPERTIES_FULL)

    # Instrument
    @tag('instrument', 'slow')
    def test_instrument(self):
        self.create_xml_and_validate_against_schema(InstrumentMetadata, INSTRUMENT_PROPERTIES_FULL)

    @tag('instrument', 'slow')
    def test_instrument_no_type(self):
        """
        Test fails as type is a required a field.
        """
        self.assertRaises(XMLSchemaChildrenValidationError, self.create_xml_and_validate_against_schema, InstrumentMetadata, INSTRUMENT_PROPERTIES_NO_TYPE)

    # Acquisition Capabilities
    @tag('acquisition_capabilities', 'slow')
    def test_acquisition_capabilities(self):
        self.create_xml_and_validate_against_schema(AcquisitionCapabilitiesMetadata, ACQUISITION_CAPABILITIES_PROPERTIES_FULL)
    
    @tag('acquisition_capabilities', 'slow')
    def test_acquisition_capabilities_blank_cadence_unit(self):
        self.assertRaises(XMLSchemaDecodeError, self.create_xml_and_validate_against_schema, AcquisitionCapabilitiesMetadata, ACQUISITION_CAPABILITIES_BLANK_CADENCE_UNIT)

    # Acquisition
    @tag('acquisition', 'slow')
    def test_acquisition(self):
        self.create_xml_and_validate_against_schema(AcquisitionMetadata, ACQUISITION_PROPERTIES_FULL)

    @tag('acquisition', 'slow')
    def test_acquisition_with_blank_acq_caps(self):
        self.assertRaises(XMLSchemaChildrenValidationError, self.create_xml_and_validate_against_schema, AcquisitionMetadata, ACQUISITION_PROPERTIES_WITH_BLANK_ACQ_CAPS)

    # Computation Capabilities
    @tag('computation_capabilities', 'slow')
    def test_computation_capabilities(self):
        self.create_xml_and_validate_against_schema(ComputationCapabilitiesMetadata, COMPUTATION_CAPABILITIES_PROPERTIES_FULL)
    
    # Computation
    @tag('computation', 'slow')
    def test_computation(self):
        self.create_xml_and_validate_against_schema(ComputationMetadata, COMPUTATION_PROPERTIES_FULL)

    # Process
    @tag('process', 'slow')
    def test_process(self):
        self.create_xml_and_validate_against_schema(ProcessMetadata, PROCESS_PROPERTIES_FULL)

    # Data Collection
    @tag('data_collection', 'slow')
    def test_data_collection(self):
        self.create_xml_and_validate_against_schema(DataCollectionMetadata, DATA_COLLECTION_PROPERTIES_FULL)

    # Workflow
    @tag('workflow', 'slow')
    def test_workflow(self):
        self.create_xml_and_validate_against_schema(WorkflowMetadata, WORKFLOW_PROPERTIES_FULL)

    @tag('workflow', 'slow')
    def test_workflow_no_data_collections(self):
        self.assertRaises(XMLSchemaChildrenValidationError, self.create_xml_and_validate_against_schema, WorkflowMetadata, WORKFLOW_PROPERTIES_NO_DATA_COLLECTIONS)

    @tag('workflow', 'slow')
    def test_workflow_no_workflow_details(self):
        self.assertRaises(XMLSchemaChildrenValidationError, self.create_xml_and_validate_against_schema, WorkflowMetadata, WORKFLOW_PROPERTIES_NO_WORKFLOW_DETAILS)