from django.test import SimpleTestCase

from .services import get_xml_of_ontology_category_terms_locally
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
    def test_pref_label_property(self):
        """Returns the text of the prefLabel element from the
        XML element for an ontology term.
        """
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
        ontology_term_metadata = OntologyTermMetadata(xml_string)
        self.assertIsInstance(ontology_term_metadata.pref_label, str)


class OntologyCategoryMetadataTestCase(SimpleTestCase):
    def test_get_term_with_iri(self):
        """Returns the XML string of a given ontology term
        from the XML string of a given ontology category.
        """
        ontology_category = 'observedProperty'
        xml_for_ontology_category = get_xml_of_ontology_category_terms_locally(ontology_category)
        observed_property_terms = OntologyCategoryMetadata(xml_for_ontology_category)
        xml_for_electron_density_term = observed_property_terms.get_term_with_iri('https://metadata.pithia.eu/ontology/2.2/observedProperty/ElectronDensity')
        print('xml_for_electron_density_term', xml_for_electron_density_term)
        self.assertIsNot(xml_for_electron_density_term, '')