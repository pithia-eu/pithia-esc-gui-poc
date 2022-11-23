from rdflib import URIRef
from rdflib.namespace._SKOS import SKOS

def create_anchor_tag_html_from_ontology_term_details(ontology_term_readable, ontology_term_ontology_iri, ontology_term_detail_url, graph_for_ontology_term):
    pref_label_triples = list(graph_for_ontology_term.triples((URIRef(ontology_term_ontology_iri), SKOS.prefLabel, None)))
    # Not having a prefLabel implies the ontology term doesn't exist
    if len(pref_label_triples) > 0:
        ontology_term_readable = str(pref_label_triples[0][2])
        return f'<a href="{ontology_term_detail_url}">{ontology_term_readable}</a>'
    else:
        return ontology_term_readable