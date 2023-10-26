from django.test import SimpleTestCase
from .url_helpers import (
    divide_resource_url_from_op_mode_id,
    divide_resource_url_into_main_components,
)

# Create your tests here.

class MetadataUrlDivisionTestCase(SimpleTestCase):
    def test_valid_metadata_url_is_divided_correctly(self):
        """
        A given metadata URL is split up into:
        - URL base (https://metadata.pithia.eu/resources/2.2)
        - resource type (e.g. organisation)
        - namespace (e.g. pithia)
        - localID (e.g. Organisation_PITHIA)
        """
        url_division = divide_resource_url_into_main_components('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        self.assertEquals(url_division['url_base'], 'https://metadata.pithia.eu/resources/2.2')
        self.assertEquals(url_division['resource_type'], 'pithia')
        self.assertEquals(url_division['namespace'], 'project')
        self.assertEquals(url_division['localid'], 'Project_TEST')

    def test_unexpected_metadata_url_is_divided_as_expected_1(self):
        """
        A metadata URL with an unusual sequence is divided
        into separate components, despite not being valid.
        """
        url_division = divide_resource_url_into_main_components('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        self.assertEquals(url_division['url_base'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2')

    def test_unexpected_metadata_url_is_divided_as_expected_2(self):
        """
        A metadata URL with an unusual sequence is divided
        into separate components, despite not being valid.
        """
        url_division = divide_resource_url_into_main_components('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST')
        self.assertEquals(url_division['url_base'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST')
        self.assertEquals(url_division['resource_type'], 'organisation')
        self.assertEquals(url_division['namespace'], 'pithia')


class OperationalModeUrlDivisionTestCase(SimpleTestCase):
    def test_valid_operational_mode_url_is_divided_correctly(self):
        """
        A given operational mode URL is split up into:
        - URL base (https://metadata.pithia.eu/resources/2.2)
        - resource type (e.g. organisation)
        - namespace (e.g. pithia)
        - localID (e.g. Organisation_PITHIA)
        - operational mode (e.g. ionogram)
        """
        url_division = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST#ionogram')
        self.assertEquals(url_division['resource_url'], 'https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST')
        self.assertEquals(url_division['op_mode_id'], 'ionogram')

    def test_unexpected_operational_mode_url_is_divided_as_expected_1(self):
        """
        An operational mode URL with an unusual sequence is
        divded into separate components, despite not being
        valid.
        """
        url_division = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST#sweep')
        self.assertEquals(url_division['resource_url'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST')
        self.assertEquals(url_division['op_mode_id'], 'sweep')

    def test_unexpected_operational_mode_url_is_divided_as_expected_2(self):
        """
        An operational mode URL with an unusual sequence is
        divded into separate components, despite not being
        valid.
        """
        url_division = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST#test')
        self.assertEquals(url_division['resource_url'], 'https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST/organisation/pithia/Organisation_TEST')
        self.assertEquals(url_division['op_mode_id'], 'test')

    def test_unexpected_operational_mode_url_is_divided_as_expected_3(self):
        """
        An operational mode URL with an unusual sequence is
        divded into separate components, despite not being
        valid.
        """
        url_division = divide_resource_url_from_op_mode_id('https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST#ionogram#ionogram#ionogram#ionogram')
        self.assertEquals(url_division['resource_url'], 'https://metadata.pithia.eu/resources/2.2/pithia/project/Project_TEST#ionogram#ionogram#ionogram')
        self.assertEquals(url_division['op_mode_id'], 'ionogram')