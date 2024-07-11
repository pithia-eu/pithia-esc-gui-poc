from django.test import (
    SimpleTestCase,
    tag,
)
from lxml import etree
from xmlschema.validators.exceptions import (
    XMLSchemaChildrenValidationError,
    XMLSchemaDecodeError,
)

from .test_data_structures import *

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
from validation.services import MetadataFileXSDValidator

# Create your tests here.

class MetadataEditorTestCase(SimpleTestCase):
    def initialise_and_add_properties_to_metadata_editor(self, metadata_editor_class, properties):
        metadata_editor = metadata_editor_class(properties)
        return metadata_editor

    def test_organisation(self):
        organisation_editor = self.initialise_and_add_properties_to_metadata_editor(OrganisationMetadata, ORGANISATION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in organisation_editor.xml)
        print('organisation_editor.xml', organisation_editor.xml)

    def test_individual(self):
        individual_editor = self.initialise_and_add_properties_to_metadata_editor(IndividualMetadata, INDIVIDUAL_PROPERTIES_FULL)
        self.assertFalse('<ns1' in individual_editor.xml)
        print('individual_editor.xml', individual_editor.xml)

    def test_project(self):
        project_editor = self.initialise_and_add_properties_to_metadata_editor(ProjectMetadata, PROJECT_PROPERTIES_FULL)
        self.assertFalse('<ns1' in project_editor.xml)
        print('project_editor.xml', project_editor.xml)

    def test_platform(self):
        platform_editor = self.initialise_and_add_properties_to_metadata_editor(PlatformMetadata, PLATFORM_PROPERTIES_FULL)
        self.assertFalse('<ns1' in platform_editor.xml)
        print('platform_editor.xml', platform_editor.xml)

    def test_platform_no_url(self):
        platform_editor = self.initialise_and_add_properties_to_metadata_editor(PlatformMetadata, PLATFORM_PROPERTIES_NO_URL)
        platform_editor_xml_parsed = etree.fromstring(platform_editor.xml)
        self.assertFalse(hasattr(platform_editor_xml_parsed, 'URL'))

    def test_platform_no_geometry_location(self):
        platform_editor = self.initialise_and_add_properties_to_metadata_editor(PlatformMetadata, PLATFORM_PROPERTIES_NO_GEOMETRY_LOCATION)
        platform_editor_xml_parsed = etree.fromstring(platform_editor.xml)
        self.assertEqual(len(platform_editor_xml_parsed.xpath('//geometryLocation')), 0)

    def test_operation(self):
        operation_editor = self.initialise_and_add_properties_to_metadata_editor(OperationMetadata, OPERATION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in operation_editor.xml)
        print('operation_editor.xml', operation_editor.xml)

    def test_instrument(self):
        instrument_editor = self.initialise_and_add_properties_to_metadata_editor(InstrumentMetadata, INSTRUMENT_PROPERTIES_FULL)
        self.assertFalse('<ns1' in instrument_editor.xml)
        print('instrument_editor.xml', instrument_editor.xml)

    def test_acquisition_capabilities(self):
        acquisition_capabilities_editor = self.initialise_and_add_properties_to_metadata_editor(AcquisitionCapabilitiesMetadata, ACQUISITION_CAPABILITIES_PROPERTIES_FULL)
        self.assertFalse('<ns1' in acquisition_capabilities_editor.xml)
        print('acquisition_capabilities_editor.xml', acquisition_capabilities_editor.xml)

    def test_acquisition(self):
        acquisition_editor = self.initialise_and_add_properties_to_metadata_editor(AcquisitionMetadata, ACQUISITION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in acquisition_editor.xml)
        print('acquisition_editor.xml', acquisition_editor.xml)

    def test_acquisition_with_blank_acq_caps(self):
        acquisition_editor = self.initialise_and_add_properties_to_metadata_editor(AcquisitionMetadata, ACQUISITION_PROPERTIES_WITH_BLANK_ACQ_CAPS)
        print('acquisition_editor.xml', acquisition_editor.xml)

    def test_computation_capabilities(self):
        computation_capabilities_editor = self.initialise_and_add_properties_to_metadata_editor(ComputationCapabilitiesMetadata, COMPUTATION_CAPABILITIES_PROPERTIES_FULL)
        self.assertFalse('<ns1' in computation_capabilities_editor.xml)
        print('computation_capabilities_editor.xml', computation_capabilities_editor.xml)

    def test_computation(self):
        computation_editor = self.initialise_and_add_properties_to_metadata_editor(ComputationMetadata, COMPUTATION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in computation_editor.xml)
        print('computation_editor.xml', computation_editor.xml)

    def test_process(self):
        process_editor = self.initialise_and_add_properties_to_metadata_editor(ProcessMetadata, PROCESS_PROPERTIES_FULL)
        self.assertFalse('<ns1' in process_editor.xml)
        print('process_editor.xml', process_editor.xml)

    @tag('data_collection')
    def test_data_collection(self):
        data_collection_editor = self.initialise_and_add_properties_to_metadata_editor(DataCollectionMetadata, DATA_COLLECTION_PROPERTIES_FULL)
        self.assertFalse('<ns1' in data_collection_editor.xml)
        print('data_collection_editor.xml', data_collection_editor.xml)

    @tag('data_collection')
    def test_data_collection_with_html_in_localid(self):
        data_collection_editor = self.initialise_and_add_properties_to_metadata_editor(DataCollectionMetadata, DATA_COLLECTION_WITH_LOCALID_HTML)
        print('data_collection_editor.xml', data_collection_editor.xml)

    @tag('data_collection')
    def test_data_collection_with_html(self):
        data_collection_editor = self.initialise_and_add_properties_to_metadata_editor(DataCollectionMetadata, DATA_COLLECTION_WITH_HTML)
        print('data_collection_editor.xml', data_collection_editor.xml)

    def test_catalogue(self):
        catalogue_editor = self.initialise_and_add_properties_to_metadata_editor(CatalogueMetadata, CATALOGUE_PROPERTIES_FULL)
        self.assertFalse('<ns1' in catalogue_editor.xml)
        print('catalogue_editor.xml', catalogue_editor.xml)

    def test_catalogue_entry(self):
        catalogue_entry_editor = self.initialise_and_add_properties_to_metadata_editor(CatalogueEntryMetadata, CATALOGUE_ENTRY_PROPERTIES_FULL)
        self.assertFalse('<ns1' in catalogue_entry_editor.xml)
        print('catalogue_entry_editor.xml', catalogue_entry_editor.xml)

    def test_catalogue_data_subset(self):
        catalogue_data_subset_editor = self.initialise_and_add_properties_to_metadata_editor(CatalogueDataSubsetMetadata, CATALOGUE_DATA_SUBSET_PROPERTIES_FULL)
        self.assertFalse('<ns1' in catalogue_data_subset_editor.xml)
        print('catalogue_data_subset_editor.xml', catalogue_data_subset_editor.xml)

    def test_workflow(self):
        workflow_editor = self.initialise_and_add_properties_to_metadata_editor(WorkflowMetadata, WORKFLOW_PROPERTIES_FULL)
        self.assertFalse('<ns1' in workflow_editor.xml)
        print('workflow_editor.xml', workflow_editor.xml)

class MetadataEditorXSDComplianceTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.schema = MetadataFileXSDValidator._instantiate_pithia_schema()
        return super().setUp()

    def create_xml_and_validate_against_schema(self, metadata_editor_class, properties):
        metadata_editor = metadata_editor_class(properties)
        xml = metadata_editor.xml
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