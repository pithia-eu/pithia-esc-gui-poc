from django.test import TestCase

from .services import OntologyTermsRegisteredWithWorkflows

from common.models import (
    Acquisition,
    AcquisitionCapabilities,
    Computation,
    ComputationCapabilities,
    DataCollection,
    Instrument,
    Process,
    Workflow,
)
from common.test_xml_files import (
    INSTRUMENT_METADATA_XML,
    ACQUISITION_CAPABILITIES_METADATA_XML,
    ACQUISITION_METADATA_XML,
    COMPUTATION_CAPABILITIES_METADATA_XML,
    COMPUTATION_METADATA_XML,
    PROCESS_METADATA_XML,
    DATA_COLLECTION_METADATA_XML,
    WORKFLOW_METADATA_XML,
)

# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'


# Create your tests here.

class OntologyTermsRegisteredWithWorkflowsTestCase(TestCase):
    def setUp(self) -> None:
        self._register_xml_file_for_test(
            INSTRUMENT_METADATA_XML,
            Instrument
        )
        self._register_xml_file_for_test(
            ACQUISITION_CAPABILITIES_METADATA_XML,
            AcquisitionCapabilities
        )
        self._register_xml_file_for_test(
            ACQUISITION_METADATA_XML,
            Acquisition
        )
        self._register_xml_file_for_test(
            COMPUTATION_CAPABILITIES_METADATA_XML,
            ComputationCapabilities
        )
        self._register_xml_file_for_test(
            COMPUTATION_METADATA_XML,
            Computation
        )
        self._register_xml_file_for_test(
            PROCESS_METADATA_XML,
            Process
        )
        self._register_xml_file_for_test(
            DATA_COLLECTION_METADATA_XML,
            DataCollection
        )
        self._register_xml_file_for_test(
            WORKFLOW_METADATA_XML,
            Workflow
        )
        return super().setUp()
    
    def _register_xml_file_for_test(self, xml_file, model):
        xml_file.seek(0)
        model.objects.create_from_xml_string(
            xml_file.read(),
            SAMPLE_INSTITUTION_ID,
            SAMPLE_USER_ID
        )

    def test_get_metadata_urls_of_type_from_registrations(self):
        """Returns a list of type IDs taken from type ontology IRIs
        that are registered with workflows.
        """
        print('OntologyTermsRegisteredWithWorkflows', OntologyTermsRegisteredWithWorkflows)
        type_ids = OntologyTermsRegisteredWithWorkflows._get_type_urls_from_workflow_data_collections()
        print('type_ids', type_ids)