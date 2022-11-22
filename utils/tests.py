from django.test import SimpleTestCase
from .url_helpers import convert_ontology_server_urls_to_browse_urls, convert_resource_server_urls_to_browse_urls

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
        self.assertEqual(len(converted_ontology_server_urls[4]['converted_url']), 0)

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
        self.assertEquals(len(converted_resource_server_urls[4]['converted_url']), 0)