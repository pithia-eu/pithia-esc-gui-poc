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
        ]
        converted_ontology_server_urls = convert_ontology_server_urls_to_browse_urls(ontology_server_urls)
        print(converted_ontology_server_urls)