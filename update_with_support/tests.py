from django.test import SimpleTestCase, TestCase

from .form_to_metadata_mappers import (
    AcquisitionFormFieldsToMetadataMapper,
)

from common.test_xml_files import (
    ACQUISITION_METADATA_XML,
    ACQUISITION_WITH_TIME_SPANS_METADATA_XML,
)


# Create your tests here.
class AcquisitionFormToMetadataMapperTestCase(SimpleTestCase):
    def test_mapper_capability_links(self):
        mapper = AcquisitionFormFieldsToMetadataMapper(ACQUISITION_WITH_TIME_SPANS_METADATA_XML.read().decode())
        initial_values = mapper.get_initial_form_values()
        print('initial_values', initial_values)