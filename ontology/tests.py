from django.test import SimpleTestCase

from .services import (
    get_xml_of_ontology_category_terms_locally,
    OntologyCategoryMetadataService,
)
from .utils import (
    OntologyCategoryMetadata,
    OntologyTermMetadata,
)

# Create your tests here.
class OntologyFileRetrievalTestCase(SimpleTestCase):
    def test_get_xml_of_ontology_category_terms_locally(self):
        """Returns the XML string of a given ontology category
        from a locally stored XML file.
        """
        ontology_category = 'observedProperty'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        self.assertIsInstance(xml_for_ontology_category, str)


class OntologyTermMetadataTestCase(SimpleTestCase):
    xml_string = '''<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF
        xmlns:skos="http://www.w3.org/2004/02/skos/core#"
        xmlns:pithia="https://metadata.pithia.eu/ontology/2.2/"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:owlxml="http://www.w3.org/2006/12/owl2-xml#"
    >
    <skos:Concept rdf:about="https://metadata.pithia.eu/ontology/2.2/observedProperty/ElectronDensity">
        <skos:prefLabel xml:lang="en">Electron Density</skos:prefLabel>
        <skos:altLabel xml:lang="en">Ne</skos:altLabel>
        <skos:definition xml:lang="en">Number density of electrons</skos:definition>
        <dc:date>2013-10-10 09:43:00.0</dc:date>
        <owlxml:versionInfo>0.1</owlxml:versionInfo>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/HalfDensityHeight"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/PeakDensity"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/PeakHeight"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/PlasmaBoundaryPosition"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/PlasmaLayerType"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/ProfileShapeParameter"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/"/>
        <skos:narrower rdf:resource="https://metadata.pithia.eu/ontology/2.2/observedProperty/DensityOverVTEC"/>
        <pithia:phenomenon rdf:resource="https://metadata.pithia.eu/ontology/2.2/phenomenon/Electron"/>
        <pithia:measurand rdf:resource="https://metadata.pithia.eu/ontology/2.2/measurand/NumberDensity"/>
    </skos:Concept>
    </rdf:RDF>
    '''

    def test_pref_label_property(self):
        """Returns the text of the prefLabel element from the
        XML element for an ontology term.
        """
        ontology_term_metadata = OntologyTermMetadata(self.xml_string)
        self.assertIsInstance(ontology_term_metadata.pref_label, str)

    def test_get_names_and_ontology_browser_urls_of_ontology_term_urls(self):
        """Returns a dictionary of names and ontology browser
        URLs by the ontology term URLs passed in.
        """
        ontology_term_metadata = OntologyTermMetadata(self.xml_string)
        results = ontology_term_metadata.get_names_and_ontology_browser_urls_of_ontology_term_urls()
        print('results', results)


class OntologyCategoryMetadataTestCase(SimpleTestCase):
    def test_get_term_with_iri(self):
        """Returns the XML string of a given ontology term's
        URL from the XML string of a given ontology category.
        """
        ontology_category = 'observedProperty'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        observed_property_terms = OntologyCategoryMetadata(xml_for_ontology_category)
        xml_for_electron_density_term = observed_property_terms.get_term_with_iri('https://metadata.pithia.eu/ontology/2.2/observedProperty/ElectronDensity')
        print('xml_for_electron_density_term', xml_for_electron_density_term)
        self.assertIsNot(xml_for_electron_density_term, '')

    def test_get_term_with_id(self):
        """Returns the XML string of a given ontology term's
        ID from the XML string of a given ontology category.
        """
        ontology_category = 'observedProperty'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        observed_property_terms = OntologyCategoryMetadata(xml_for_ontology_category)
        xml_for_electron_density_term = observed_property_terms.get_term_with_id('ElectronDensity')
        print('xml_for_electron_density_term', xml_for_electron_density_term)
        self.assertIsNot(xml_for_electron_density_term, '')


class OntologyCategoryMetadataServiceTestCase(SimpleTestCase):
    def test_get_immediate_descendents_by_skos_narrower_for_ontology_term(self):
        """Returns the URLs of ontology terms that are SKOS
        narrowers of a given ontology term .
        """
        ontology_category = 'computationType'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        ontology_category_metadata = OntologyCategoryMetadataService(xml_for_ontology_category)
        descendents_by_skos_narrower = ontology_category_metadata._get_immediate_descendents_by_skos_narrower_for_ontology_term(
            'https://metadata.pithia.eu/ontology/2.2/computationType/ActivityIndicator'
        )
        self.assertGreater(len(descendents_by_skos_narrower), 1)

    def test_get_immediate_descendents_by_skos_broader_for_ontology_term(self):
        """Returns the URLs of ontology terms that have the
        URL of a given ontology term as a SKOS broader.
        """
        ontology_category = 'computationType'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        ontology_category_metadata = OntologyCategoryMetadataService(xml_for_ontology_category)
        descendents_by_skos_broader = ontology_category_metadata._get_immediate_descendents_by_skos_broader_for_ontology_term(
            'https://metadata.pithia.eu/ontology/2.2/computationType/ActivityIndicator'
        )
        self.assertGreater(len(descendents_by_skos_broader), 1)

    def test_get_immediate_descendents_of_ontology_term(self):
        """Returns the URLs of immediate descendents of a given
        ontology term.
        """
        ontology_category = 'computationType'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        ontology_category_metadata = OntologyCategoryMetadataService(xml_for_ontology_category)
        immediate_descendents = ontology_category_metadata._get_immediate_descendents_of_ontology_term(
            'https://metadata.pithia.eu/ontology/2.2/computationType/ActivityIndicator'
        )
        self.assertGreater(len(immediate_descendents), 1)

    def test_get_all_descendents_of_ontology_term(self):
        """Returns the URLs of all descendents of a given ontology term.
        """
        ontology_category = 'computationType'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        ontology_category_metadata = OntologyCategoryMetadataService(xml_for_ontology_category)
        all_descendents = ontology_category_metadata.get_all_descendents_of_ontology_term(
            'https://metadata.pithia.eu/ontology/2.2/computationType/ActivityIndicator'
        )
        self.assertGreater(len(all_descendents), 1)
