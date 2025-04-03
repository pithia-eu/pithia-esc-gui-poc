import json
from django.test import (
    SimpleTestCase,
    TestCase,
)

from .services import (
    map_ontology_server_urls_to_browse_urls,
    map_metadata_server_urls_to_browse_urls,
)

from common.test_setup import (
    register_data_subset_for_test,
    register_individual_for_test,
    register_instrument_for_test,
    register_organisation_for_test,
    register_project_for_test,
    register_process_for_test,
)

# Create your tests here.
class BulkOntologyUrlMappingTestCase(SimpleTestCase):
    def test_bulk_ontology_url_mapping_with_real_and_fake_urls(self):
        """Returns a list of dicts containing a mapping of the original
        ontology URL to its corresponding eSC ontology browser page URL.
        """
        ontology_server_urls = [
            'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_F-Region_Bottomside',
            'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_E-Region',
            'https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder',
            'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'https://metadata.pithia.eu/ontology/2.2/test/test',
        ]
        # Real ontology server URLs
        converted_ontology_server_urls = map_ontology_server_urls_to_browse_urls(ontology_server_urls)
        real_ontology_url_mappings = converted_ontology_server_urls[:-1]
        for mapping in real_ontology_url_mappings:
            real_ontology_url = mapping.get('original_server_url')
            real_ontology_url_id = real_ontology_url.split('/')[-1]
            self.assertNotEqual(real_ontology_url_id, mapping.get('converted_url_text'))
        # Fake ontology server URL
        fake_ontology_url_mapping = converted_ontology_server_urls[-1]
        fake_ontology_url = fake_ontology_url_mapping.get('original_server_url')
        fake_ontology_url_id = fake_ontology_url.split('/')[-1]
        self.assertEqual(fake_ontology_url_id, fake_ontology_url_mapping.get('converted_url_text'))


class MultipleMetadataUrlMappingTestCase(TestCase):
    def test_multiple_metadata_url_mapping_with_real_and_fake_urls(self):
        """Returns a list of dicts containing a mapping of the original
        metadata server URL to its corresponding eSC metadata detail page
        URL for some URLs passed into the test.
        """
        # Register the test metadata first.
        register_organisation_for_test()
        register_individual_for_test()
        register_project_for_test()
        register_process_for_test()

        resource_server_urls = [
            'https://metadata.pithia.eu/resources/2.2/process/test/CompositeProcess_Test',
            'https://metadata.pithia.eu/resources/2.2/project/test/Project_Test',
            'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
            'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
            'https://metadata.pithia.eu/ontology/2.2/test/test',
        ]
        converted_resource_server_urls = map_metadata_server_urls_to_browse_urls(resource_server_urls)
        print('converted_resource_server_urls', json.dumps(converted_resource_server_urls, indent='  '))
        # The "converted_url" is the same as the "original_server_url" if a
        # corresponding eSC metadata detail page URL cannot be found.
        self.assertNotEqual(converted_resource_server_urls[0]['original_server_url'], converted_resource_server_urls[0]['converted_url'])
        self.assertNotEqual(converted_resource_server_urls[1]['original_server_url'], converted_resource_server_urls[1]['converted_url'])
        self.assertNotEqual(converted_resource_server_urls[2]['original_server_url'], converted_resource_server_urls[2]['converted_url'])
        self.assertNotEqual(converted_resource_server_urls[3]['original_server_url'], converted_resource_server_urls[3]['converted_url'])
        self.assertEqual(converted_resource_server_urls[4]['original_server_url'], converted_resource_server_urls[4]['converted_url'])

    def test_multiple_metadata_url_mapping_with_mix_of_valid_url_types(self):
        """Returns a list of dicts containing a mapping
        of all the metadata URLs for this test.
        """
        # Register the test metadata first.
        register_instrument_for_test()
        register_process_for_test()
        register_data_subset_for_test()

        # Test data
        instrument_resource_url_with_op_mode = 'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test#instrumentoperationalmode1'
        process_metadata_url = 'https://metadata.pithia.eu/resources/2.2/process/test/CompositeProcess_Test'
        static_dataset_related_resource_url = 'https://metadata.pithia.eu/resources/2.2/staticDataset/test/Test/DataSubset_Test-2023-01-01_DataCollectionTest'

        # Operational mode URL
        converted_instrument_resource_url_with_op_mode = map_metadata_server_urls_to_browse_urls([instrument_resource_url_with_op_mode])[0]
        print('converted_instrument_resource_url_with_op_mode', json.dumps(converted_instrument_resource_url_with_op_mode, indent='  '))
        # Data Collection-related metadata URL
        converted_process_metadata_url = map_metadata_server_urls_to_browse_urls([process_metadata_url])[0]
        print('converted_process_metadata_url', json.dumps(converted_process_metadata_url, indent='  '))
        # Static Dataset-related metadata URL
        converted_static_dataset_related_resource_url = map_metadata_server_urls_to_browse_urls([static_dataset_related_resource_url])[0]
        print('converted_static_dataset_related_resource_url', json.dumps(converted_static_dataset_related_resource_url, indent='  '))

        # The "converted_url" is the same as the "original_server_url" if a
        # corresponding eSC metadata detail page URL cannot be found.

        # Instrument operational mode URL
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['original_server_url'], '')
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['converted_url'], '')
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['converted_url_text'], '')
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['original_server_url'], converted_instrument_resource_url_with_op_mode['converted_url'])

        # Process URL
        self.assertNotEqual(converted_process_metadata_url['original_server_url'], '')
        self.assertNotEqual(converted_process_metadata_url['converted_url'], '')
        self.assertNotEqual(converted_process_metadata_url['converted_url_text'], '')
        self.assertNotEqual(converted_process_metadata_url['original_server_url'], converted_process_metadata_url['converted_url'])

        # Static dataset URL
        self.assertNotEqual(converted_static_dataset_related_resource_url['original_server_url'], '')
        self.assertNotEqual(converted_static_dataset_related_resource_url['converted_url'], '')
        self.assertNotEqual(converted_static_dataset_related_resource_url['converted_url_text'], '')
        self.assertNotEqual(converted_static_dataset_related_resource_url['original_server_url'], converted_static_dataset_related_resource_url['converted_url'])