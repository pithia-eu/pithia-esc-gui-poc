from django.test import SimpleTestCase
from .url_mapping import (
    convert_ontology_server_urls_to_browse_urls,
    convert_resource_server_urls_to_browse_urls,
)

# Create your tests here.

class UrlConversionTestCase(SimpleTestCase):
    def test_ontology_url_conversion(self):
        """
        convert_ontology_server_urls_to_browse_urls returns a list of dicts
        mapping the old url to an ontology term detail page url
        """
        ontology_server_urls = [
            'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_F-Region_Bottomside',
            'https://metadata.pithia.eu/ontology/2.2/featureOfInterest/Earth_Ionosphere_E-Region',
            'https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder',
            'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
            'https://metadata.pithia.eu/ontology/2.2/test/test',
        ]
        converted_ontology_server_urls = convert_ontology_server_urls_to_browse_urls(ontology_server_urls)
        self.assertNotEqual(converted_ontology_server_urls[0]['original_server_url'], converted_ontology_server_urls[0]['converted_url'])
        self.assertNotEqual(converted_ontology_server_urls[1]['original_server_url'], converted_ontology_server_urls[1]['converted_url'])
        self.assertNotEqual(converted_ontology_server_urls[2]['original_server_url'], converted_ontology_server_urls[2]['converted_url'])
        self.assertNotEqual(converted_ontology_server_urls[3]['original_server_url'], converted_ontology_server_urls[3]['converted_url'])
        self.assertEqual(converted_ontology_server_urls[4]['original_server_url'], converted_ontology_server_urls[4]['converted_url'])

    def test_resource_url_conversion(self):
        """
        convert_ontology_server_urls_to_browse_urls returns a list of dicts
        mapping the old url to an ontology term detail page url
        """
        resource_server_urls = [
            'https://metadata.pithia.eu/resources/2.2/process/lgdc/CompositeProcess_DIDBase_EvaluatedAutoscaling',
            ' 	https://metadata.pithia.eu/resources/2.2/project/lgdc/Project_LGDC_RION',
            'https://metadata.pithia.eu/resources/2.2/individual/lgdc/Individual_LGDC_Galkin',
            'https://metadata.pithia.eu/resources/2.2/organisation/pithia/Organisation_LGDC',
            'https://metadata.pithia.eu/ontology/2.2/test/test',
        ]
        converted_resource_server_urls = convert_resource_server_urls_to_browse_urls(resource_server_urls)
        self.assertNotEqual(converted_resource_server_urls[0]['original_server_url'], converted_resource_server_urls[0]['converted_url'])
        self.assertNotEqual(converted_resource_server_urls[1]['original_server_url'], converted_resource_server_urls[1]['converted_url'])
        self.assertNotEqual(converted_resource_server_urls[2]['original_server_url'], converted_resource_server_urls[2]['converted_url'])
        self.assertNotEqual(converted_resource_server_urls[3]['original_server_url'], converted_resource_server_urls[3]['converted_url'])
        self.assertEqual(converted_resource_server_urls[4]['original_server_url'], converted_resource_server_urls[4]['converted_url'])

    def test_url_conversion_for_valid_resource_urls(self):
        """
        All resource URLs used for this test should convert
        successfully.
        """
        data_collection_related_resource_url = 'https://metadata.pithia.eu/resources/2.2/process/lgdc/CompositeProcess_DIDBase_EvaluatedAutoscaling'
        instrument_resource_url_with_op_mode = 'https://metadata.pithia.eu/resources/2.2/instrument/noa/Instrument_Ionosonde_DPS4D_AT138#scanning'
        catalogue_related_resource_url = 'https://metadata.pithia.eu/resources/2.2/catalogue/pithia/VolcanoEruption/DataSubset_HungaTonga-2022-01-15_DIDBaseIonograms'

        converted_data_collection_related_resource_url = convert_resource_server_urls_to_browse_urls([data_collection_related_resource_url])[0]
        converted_instrument_resource_url_with_op_mode = convert_resource_server_urls_to_browse_urls([instrument_resource_url_with_op_mode])[0]
        converted_catalogue_related_resource_url = convert_resource_server_urls_to_browse_urls([catalogue_related_resource_url])[0]

        # converted_data_collection_related_resource_url
        self.assertNotEqual(converted_data_collection_related_resource_url['original_server_url'], '')
        self.assertNotEqual(converted_data_collection_related_resource_url['converted_url'], '')
        self.assertNotEqual(converted_data_collection_related_resource_url['converted_url_text'], '')
        self.assertNotEqual(converted_data_collection_related_resource_url['original_server_url'], converted_data_collection_related_resource_url['converted_url'])

        # converted_instrument_resource_url_with_op_mode
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['original_server_url'], '')
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['converted_url'], '')
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['converted_url_text'], '')
        self.assertNotEqual(converted_instrument_resource_url_with_op_mode['original_server_url'], converted_instrument_resource_url_with_op_mode['converted_url'])

        # converted_catalogue_related_resource_url
        self.assertNotEqual(converted_catalogue_related_resource_url['original_server_url'], '')
        self.assertNotEqual(converted_catalogue_related_resource_url['converted_url'], '')
        self.assertNotEqual(converted_catalogue_related_resource_url['converted_url_text'], '')
        self.assertNotEqual(converted_catalogue_related_resource_url['original_server_url'], converted_catalogue_related_resource_url['converted_url'])