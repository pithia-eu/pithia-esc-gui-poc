from django.test import SimpleTestCase, TestCase

from .form_to_metadata_mappers import (
    AcquisitionCapabilitiesFormFieldsToMetadataMapper,
    AcquisitionFormFieldsToMetadataMapper,
    ComputationCapabilitiesFormFieldsToMetadataMapper,
    ComputationFormFieldsToMetadataMapper,
    DataCollectionFormFieldsToMetadataMapper,
    ProcessFormFieldsToMetadataMapper,
    WorkflowFormFieldsToMetadataMapper,
)

from common.test_xml_files import (
    ACQUISITION_CAPABILITIES_METADATA_XML,
    ACQUISITION_WITH_TIME_SPANS_METADATA_XML,
    COMPUTATION_CAPABILITIES_FULL_METADATA_XML,
    COMPUTATION_METADATA_XML,
    DATA_COLLECTION_METADATA_XML,
    PROCESS_FULL_METADATA_XML,
    WORKFLOW_METADATA_XML,
)


# Create your tests here.
class AcquisitionCapabilitiesFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        ACQUISITION_CAPABILITIES_METADATA_XML.seek(0)
        mapper = AcquisitionCapabilitiesFormFieldsToMetadataMapper(ACQUISITION_CAPABILITIES_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)


class AcquisitionFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper_capability_links(self):
        ACQUISITION_WITH_TIME_SPANS_METADATA_XML.seek(0)
        mapper = AcquisitionFormFieldsToMetadataMapper(ACQUISITION_WITH_TIME_SPANS_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)

    
class ComputationCapabilitiesFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        COMPUTATION_CAPABILITIES_FULL_METADATA_XML.seek(0)
        mapper = ComputationCapabilitiesFormFieldsToMetadataMapper(COMPUTATION_CAPABILITIES_FULL_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)


class ComputationFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        COMPUTATION_METADATA_XML.seek(0)
        mapper = ComputationFormFieldsToMetadataMapper(COMPUTATION_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)


class ProcessFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        PROCESS_FULL_METADATA_XML.seek(0)
        mapper = ProcessFormFieldsToMetadataMapper(PROCESS_FULL_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)


class DataCollectionFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        DATA_COLLECTION_METADATA_XML.seek(0)
        mapper = DataCollectionFormFieldsToMetadataMapper(DATA_COLLECTION_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)


class WorkflowFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        WORKFLOW_METADATA_XML.seek(0)
        mapper = WorkflowFormFieldsToMetadataMapper(WORKFLOW_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)