import logging
from lxml import etree

from .xml_metadata_utils import (
    Namespace,
    NamespacePrefix,
)


logger = logging.getLogger(__name__)


class OntologyXmlMixin:
    def __init__(self) -> None:
        self.namespaces = {
            NamespacePrefix.DC: Namespace.DC,
            NamespacePrefix.OWLXML: Namespace.OWLXML,
            NamespacePrefix.PITHIA: Namespace.PITHIA,
            NamespacePrefix.RDF: Namespace.RDF,
            NamespacePrefix.SKOS: Namespace.SKOS,
        }

    def _get_elements_with_xpath_query(self, xpath_query: str, parent_element=None):
        if not parent_element:
            parent_element = self.xml_parsed
        return parent_element.xpath(xpath_query, namespaces=self.namespaces)

    def _get_element_value_or_blank_string(self, element):
        try:
            return element.text
        except AttributeError as err:
            # Remove logging as errors are expected here
            # if element does not have text.
            # logger.exception(err)
            return element
        except Exception as err:
            logger.exception(err)
            return ''

    def _get_first_element_from_list(self, element_list: list):
        return next(iter(element_list), '')

    def _get_first_element_value_or_blank_string_with_xpath_query(self, xpath_query: str, parent_element=None):
        element_list = self._get_elements_with_xpath_query(xpath_query, parent_element=parent_element)
        if not len(element_list):
            return ''

        first_element = self._get_first_element_from_list(element_list)
        return self._get_element_value_or_blank_string(first_element)


class OntologyCategoryMetadata(OntologyXmlMixin):
    def __init__(self, xml_string_for_ontology_category: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.xml_parsed = etree.fromstring(xml_string_for_ontology_category.encode('utf-8'))

    def get_term_with_iri(self, ontology_iri: str):
        return self._get_first_element_from_list(
            self._get_elements_with_xpath_query(
                './/%s:Concept[@%s:about="%s"]' %
                (NamespacePrefix.SKOS, NamespacePrefix.RDF, ontology_iri)
            )
        )


class OntologyTermMetadata(OntologyXmlMixin):
    def __init__(self, xml_string_for_ontology_term: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.xml_parsed = etree.fromstring(xml_string_for_ontology_term.encode('utf-8'))

    @property
    def pref_label(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:prefLabel' % NamespacePrefix.SKOS)

    @property
    def alt_label(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:altLabel' % NamespacePrefix.SKOS)

    @property
    def definition(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:definition' % NamespacePrefix.SKOS)

    @property
    def narrower_terms(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:narrower' % NamespacePrefix.SKOS)

    @property
    def broader_terms(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:broader' % NamespacePrefix.SKOS)


class ObservedPropertyOntologyTermMetadata(OntologyTermMetadata):
    @property
    def licence_deeds(self):
        return self._get_elements_with_xpath_query('.//%s:licenceDeed' % NamespacePrefix.PITHIA)


class ObservedPropertyOntologyTermMetadata(OntologyTermMetadata):
    @property
    def features_of_interest(self):
        return self._get_elements_with_xpath_query('.//%s:featureOfInterest' % NamespacePrefix.PITHIA)

    @property
    def interactions(self):
        return self._get_elements_with_xpath_query('.//%s:interaction' % NamespacePrefix.PITHIA)

    @property
    def measurands(self):
        return self._get_elements_with_xpath_query('.//%s:measurand' % NamespacePrefix.PITHIA)

    @property
    def phenomenons(self):
        return self._get_elements_with_xpath_query('.//%s:phenomenon' % NamespacePrefix.PITHIA)

    @property
    def propagation_modes(self):
        return self._get_elements_with_xpath_query('.//%s:propagationMode' % NamespacePrefix.PITHIA)

    @property
    def qualifiers(self):
        return self._get_elements_with_xpath_query('.//%s:qualifier' % NamespacePrefix.PITHIA)