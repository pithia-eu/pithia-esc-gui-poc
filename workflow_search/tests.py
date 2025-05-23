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

    def test_get_registered_features_of_interest(self):
        """Returns a list of feature of interest IDs taken
        from ontology IRIs registered with workflows.
        """
        foi_ids = OntologyTermsRegisteredWithWorkflows.get_registered_features_of_interest()
        self.assertIsInstance(foi_ids, list)
        self.assertGreater(len(foi_ids), 0)
        
    def test_get_registered_annotation_types(self):
        """Returns a list of annotation type IDs taken
        from ontology IRIs registered with workflows."""
        annotation_type_ids = OntologyTermsRegisteredWithWorkflows.get_registered_annotation_types()
        self.assertIsInstance(annotation_type_ids, list)
        self.assertEqual(len(annotation_type_ids), 0)


    def test_get_registered_computation_types(self):
        """Returns a list of type computation IDs taken
        from ontology IRIs registered with workflows."""
        computation_type_ids = OntologyTermsRegisteredWithWorkflows.get_registered_computation_types()
        self.assertIsInstance(computation_type_ids, list)
        self.assertGreater(len(computation_type_ids), 0)


    def test_get_registered_instrument_types(self):
        """Returns a list of instrument type IDs taken
        from ontology IRIs registered with workflows."""
        instrument_type_ids = OntologyTermsRegisteredWithWorkflows.get_registered_instrument_types()
        self.assertIsInstance(instrument_type_ids, list)
        self.assertGreater(len(instrument_type_ids), 0)


    def test_get_registered_observed_properties(self):
        """Returns a list of observed property IDs taken
        from ontology IRIs registered with workflows."""
        observed_property_ids = OntologyTermsRegisteredWithWorkflows.get_registered_observed_properties()
        self.assertIsInstance(observed_property_ids, list)
        self.assertGreater(len(observed_property_ids), 0)


    def test_get_registered_measurands(self):
        """Returns a list of tymeasurandpe IDs taken
        from ontology IRIs registered with workflows."""
        measurand_ids = OntologyTermsRegisteredWithWorkflows.get_registered_measurands()
        self.assertIsInstance(measurand_ids, list)
        self.assertGreater(len(measurand_ids), 0)


    def test_get_registered_phenomenons(self):
        """Returns a list of phenomenon IDs taken from
        ontology IRIs registered with workflows."""
        phenomenon_ids = OntologyTermsRegisteredWithWorkflows.get_registered_phenomenons()
        self.assertIsInstance(phenomenon_ids, list)
        self.assertGreater(len(phenomenon_ids), 0)

