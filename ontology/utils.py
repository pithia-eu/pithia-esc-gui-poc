import logging

from dateutil.parser import isoparse
from django.urls import reverse_lazy
from lxml import etree

from .services import get_ontology_category_terms_in_xml_format
from .xml_metadata_utils import Namespace, NamespacePrefix

from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE


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
        self.ontology_category_base_url = self._get_first_element_value_or_blank_string_with_xpath_query(
            './/%s:ConceptScheme/@%s:about' %
            (NamespacePrefix.SKOS, NamespacePrefix.RDF)
        )

    def get_term_with_iri(self, ontology_iri: str):
        element_for_term = self._get_first_element_from_list(
            self._get_elements_with_xpath_query(
                './/%s:Concept[@%s:about="%s"]' %
                (NamespacePrefix.SKOS, NamespacePrefix.RDF, ontology_iri)
            )
        )
        if not element_for_term:
            # element_for_term is ''
            return element_for_term
        return etree.tostring(element_for_term).decode()

    def get_term_with_id(self, ontology_term_id: str):
        return self.get_term_with_iri(f'{self.ontology_category_base_url}/{ontology_term_id}')


class OntologyTermMetadata(OntologyXmlMixin):
    def __init__(self, xml_string_for_ontology_term: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.xml_parsed = etree.fromstring(xml_string_for_ontology_term.encode('utf-8'))

    @property
    def last_modified_date(self):
        value_of_last_modified_date = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:date' % NamespacePrefix.DC)
        try:
            return isoparse(value_of_last_modified_date)
        except Exception:
            logger.exception('Could not parse ontology term\'s last modified date')
            return value_of_last_modified_date

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
    def urls_of_narrower_terms(self):
        return self._get_elements_with_xpath_query('.//%s:narrower/@%s:resource' % (NamespacePrefix.SKOS, NamespacePrefix.RDF))

    @property
    def urls_of_broader_terms(self):
        return self._get_elements_with_xpath_query('.//%s:broader/@%s:resource' % (NamespacePrefix.SKOS, NamespacePrefix.RDF))

    def get_names_and_ontology_browser_urls_of_ontology_term_urls(self, fetched_ontology_categories: dict = dict()):
        ontology_term_urls = self._get_elements_with_xpath_query('.//*[contains(@*, "%s")]/@*' % SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE)
        names_and_ontology_browser_urls = {}
        for url in ontology_term_urls:
            # In case an element has one of multiple
            # attributes that doesn't contain the
            # ontology server URL base.
            if SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE not in url:
                continue
            # Get the ontology category right after
            # the ontology server URL base.
            ontology_category_in_url = next(iter(url.replace(SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE + '/', '').split('/')), None)
            if not ontology_category_in_url:
                continue
            if ontology_category_in_url not in fetched_ontology_categories:
                # Get the XML for the ontology category
                # if not fetched yet.
                fetched_ontology_categories.update({
                    ontology_category_in_url: OntologyCategoryMetadata(
                        get_ontology_category_terms_in_xml_format(ontology_category_in_url)
                    )
                })
            ontology_category_metadata = fetched_ontology_categories.get(ontology_category_in_url)
            xml_of_ontology_term = ontology_category_metadata.get_term_with_iri(url)
            if not xml_of_ontology_term:
                continue
            ontology_term_metadata = OntologyTermMetadata(xml_of_ontology_term)
            names_and_ontology_browser_urls.update({
                url: {
                    'pref_label': ontology_term_metadata.pref_label,
                    'alt_label': ontology_term_metadata.alt_label,
                    'ontology_browser_url': reverse_lazy('ontology:ontology_term_detail', kwargs={
                        'category': ontology_category_in_url,
                        'term_id': url.split('/')[-1],
                    }),
                },
            })
        return names_and_ontology_browser_urls


class LicenceOntologyTermMetadata(OntologyTermMetadata):
    @property
    def licence_deeds(self):
        return self._get_elements_with_xpath_query('.//%s:licenceDeed/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))


class ObservedPropertyOntologyTermMetadata(OntologyTermMetadata):
    @property
    def features_of_interest(self):
        return self._get_elements_with_xpath_query('.//%s:featureOfInterest/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))

    @property
    def interactions(self):
        return self._get_elements_with_xpath_query('.//%s:interaction/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))

    @property
    def measurands(self):
        return self._get_elements_with_xpath_query('.//%s:measurand/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))

    @property
    def phenomenons(self):
        return self._get_elements_with_xpath_query('.//%s:phenomenon/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))

    @property
    def propagation_modes(self):
        return self._get_elements_with_xpath_query('.//%s:propagationMode/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))

    @property
    def qualifiers(self):
        return self._get_elements_with_xpath_query('.//%s:qualifier/@%s:resource' % (NamespacePrefix.PITHIA, NamespacePrefix.RDF))
