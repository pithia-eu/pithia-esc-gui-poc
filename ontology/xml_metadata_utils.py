from rdflib.namespace._DC import DC
from rdflib.namespace._OWL import OWL
from rdflib.namespace._RDF import RDF
from rdflib.namespace._SKOS import SKOS

from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE


class NamespacePrefix:
    DC = 'dc'
    OWLXML = 'owlxml'
    PITHIA = 'pithia'
    RDF = 'rdf'
    SKOS = 'skos'

class Namespace:
    DC = str(DC)
    OWLXML = str(OWL)
    PITHIA = SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE + '/'
    RDF = str(RDF)
    SKOS = str(SKOS)


ontology_namespaces = {
    NamespacePrefix.DC: Namespace.DC,
    NamespacePrefix.OWLXML: Namespace.OWLXML,
    NamespacePrefix.PITHIA: Namespace.PITHIA,
    NamespacePrefix.RDF: Namespace.RDF,
    NamespacePrefix.SKOS: Namespace.SKOS,
}