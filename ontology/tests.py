from django.test import TestCase

from .utils import get_xml_of_ontology_category_terms_locally

# Create your tests here.
class OntologyFileRetrievalTestCase(TestCase):
    def test_get_xml_of_ontology_category_terms_locally(self):
        ontology_category = 'observedProperty'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        self.assertIsInstance(xml_for_ontology_category, str)