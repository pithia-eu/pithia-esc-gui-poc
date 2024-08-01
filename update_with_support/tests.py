from django.test import SimpleTestCase, TestCase

from .form_to_metadata_mappers import (
    AcquisitionCapabilitiesFormFieldsToMetadataMapper,
    AcquisitionFormFieldsToMetadataMapper,
    ComputationCapabilitiesFormFieldsToMetadataMapper,
)

from common.test_xml_files import (
    ACQUISITION_CAPABILITIES_METADATA_XML,
    ACQUISITION_WITH_TIME_SPANS_METADATA_XML,
    COMPUTATION_CAPABILITIES_FULL_METADATA_XML,
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
        mapper = AcquisitionFormFieldsToMetadataMapper(ACQUISITION_WITH_TIME_SPANS_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)

    
class ComputationCapabilitiesFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper(self):
        mapper = ComputationCapabilitiesFormFieldsToMetadataMapper(COMPUTATION_CAPABILITIES_FULL_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)