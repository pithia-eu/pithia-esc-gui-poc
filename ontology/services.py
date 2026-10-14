import logging
import os
from lxml import etree
from requests import get
from rdflib import (
    Graph,
    Namespace,
    URIRef,
)
from rdflib.namespace._SKOS import SKOS
from rdflib.resource import Resource

from .xml_metadata_utils import (
    NamespacePrefix as PithiaOntologyNamespacePrefix,
    ontology_namespaces,
)

from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from pithiaesc.settings import BASE_DIR

logger = logging.getLogger(__name__)

PITHIA = Namespace(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/')
    

def get_rdf_text_remotely(ontology_component):
    ontology_component_url = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{ontology_component}/'
    ontology_response = get(ontology_component_url)
    return ontology_response.text


def get_rdf_text_locally(ontology_component):
    local_ontology_files_path = os.path.join(BASE_DIR, 'ontology', 'local_ontology_files')
    local_ontology_file_name = None
    for filename in os.listdir(local_ontology_files_path):
        if filename[:-4].lower() == ontology_component.lower():
            local_ontology_file_name = filename
    ontology_file = open(os.path.join(BASE_DIR, 'ontology', 'local_ontology_files', local_ontology_file_name), 'r', encoding='utf-8')
    return ontology_file.read()


class OntologyCategoryMetadataService:
    def __init__(self, xml_of_ontology_category_terms: str) -> None:
        self.xml_parsed = etree.fromstring(xml_of_ontology_category_terms.encode('utf-8'))
        self.namespaces = ontology_namespaces

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

    def _get_elements_by_xpath_query(self, xpath_query: str, parent_element=None):
        if not parent_element:
            parent_element = self.xml_parsed
        return parent_element.xpath(
            xpath_query,
            namespaces=self.namespaces
        )

    def _create_base_xpath_query_selector_for_iris(self, iris: list[str] | set[str]):
        attribute_xpath_selector_condition = ''
        for counter, observed_property_url in enumerate(iris):
            if counter != 0:
                attribute_xpath_selector_condition += ' or '
            attribute_xpath_selector_condition += "@%s:about='%s'" % (
                PithiaOntologyNamespacePrefix.RDF,
                observed_property_url
            )
        return './/%s:Concept[%s]' % (
            PithiaOntologyNamespacePrefix.SKOS,
            attribute_xpath_selector_condition,
        )

    def _get_term_elements_with_iris(self, iris: list[str]):
        selector_for_elements_with_iris = self._create_base_xpath_query_selector_for_iris(
            iris
        )
        return self._get_elements_by_xpath_query(selector_for_elements_with_iris)

    def _get_immediate_descendents_by_skos_narrower_for_ontology_term(self, url_of_ontology_term: str) -> set:
        return set(self._get_elements_by_xpath_query(
            './/%s:Concept[@%s:about="%s"]/%s:narrower/@%s:resource' % (
                PithiaOntologyNamespacePrefix.SKOS,
                PithiaOntologyNamespacePrefix.RDF,
                url_of_ontology_term,
                PithiaOntologyNamespacePrefix.SKOS,
                PithiaOntologyNamespacePrefix.RDF,
            )
        ))

    def _get_immediate_descendents_by_skos_broader_for_ontology_term(self, url_of_ontology_term: str) -> set:
        return set(self._get_elements_by_xpath_query(
            './/%s:Concept[%s:broader[@%s:resource="%s"]]/@%s:about' % (
                PithiaOntologyNamespacePrefix.SKOS,
                PithiaOntologyNamespacePrefix.SKOS,
                PithiaOntologyNamespacePrefix.RDF,
                url_of_ontology_term,
                PithiaOntologyNamespacePrefix.RDF,
            )
        ))

    def _get_immediate_descendents_of_ontology_term(self, url_of_ontology_term: str) -> set:
        immediate_descendents_by_skos_narrower = self._get_immediate_descendents_by_skos_narrower_for_ontology_term(
            url_of_ontology_term
        )
        immediate_descendents_by_skos_broader = self._get_immediate_descendents_by_skos_broader_for_ontology_term(
            url_of_ontology_term
        )
        return immediate_descendents_by_skos_narrower.union(immediate_descendents_by_skos_broader)

    def get_name_and_definition_of_ontology_terms_by_iri(self) -> list:
        names_of_ontology_terms_by_iri = {}
        for element in self._get_elements_by_xpath_query('.//%s:Concept' % PithiaOntologyNamespacePrefix.SKOS):
            iri = next(iter(self._get_elements_by_xpath_query('.//@%s:about' % PithiaOntologyNamespacePrefix.RDF, parent_element=element)), '')
            if not iri:
                continue
            name_element = next(iter(self._get_elements_by_xpath_query('.//%s:prefLabel' % PithiaOntologyNamespacePrefix.SKOS, parent_element=element)), '')
            if name_element is None:
                continue
            definition_element = next(iter(self._get_elements_by_xpath_query('.//%s:definition' % PithiaOntologyNamespacePrefix.SKOS, parent_element=element)), '')
            definition = ''
            try:
                definition = definition_element.text
            except AttributeError:
                pass
            if iri in names_of_ontology_terms_by_iri:
                continue
            names_of_ontology_terms_by_iri.update({
                iri: {
                    'name': name_element.text,
                    'definition': definition,
                },
            })
        return names_of_ontology_terms_by_iri

    def get_all_descendents_of_ontology_term(self, url_of_ontology_term: str) -> set:
        immediate_descendents = self._get_immediate_descendents_of_ontology_term(url_of_ontology_term)
        all_descendents = immediate_descendents
        for descendent_url in immediate_descendents:
            ims_of_immediate_descendents = self.get_all_descendents_of_ontology_term(descendent_url)
            all_descendents = all_descendents.union(ims_of_immediate_descendents)
        return all_descendents

    def _get_url_and_name_from_ontology_term_element(self, element):
        url = self._get_element_value_or_blank_string(self._get_first_element_from_list(self._get_elements_by_xpath_query(
            './/@%s:about' % PithiaOntologyNamespacePrefix.RDF,
            parent_element=element
        )))
        name = self._get_element_value_or_blank_string(self._get_first_element_from_list(self._get_elements_by_xpath_query(
            './/%s:prefLabel' % PithiaOntologyNamespacePrefix.SKOS,
            parent_element=element
        )))
        return (url, name)

    def _map_ontology_term_elements_to_dictionary(
            self,
            ontology_term_elements: list,
            parent_term_name: str = None):
        terms_dict = {}
        for element in ontology_term_elements:
            term_url, term_name = self._get_url_and_name_from_ontology_term_element(element)
            if parent_term_name:
                term_name = f'{parent_term_name}: {term_name}'
            terms_dict.update({
                term_url: {
                    'name': term_name,
                    'descendents': list(self.get_all_descendents_of_ontology_term(term_url)),
                    'count': 0,
                },
            })
        return terms_dict

    def get_first_two_layers_of_ontology_category(self):
        elements_of_first_layer_terms = self._get_elements_by_xpath_query(
            './/%s:Concept[not(%s:broader)]' % (
                PithiaOntologyNamespacePrefix.SKOS,
                PithiaOntologyNamespacePrefix.SKOS,
            )
        )
        if not len(elements_of_first_layer_terms):
            return []

        first_layer_terms_by_url = self._map_ontology_term_elements_to_dictionary(
            elements_of_first_layer_terms
        )

        second_layer_terms_by_url = {}
        for first_layer_term_url, first_layer_term_properties in first_layer_terms_by_url.items():
            # SKOS broader
            elements_of_child_terms_by_skos_broader = self._get_elements_by_xpath_query(
                './/%s:Concept[%s:broader[@%s:resource="%s"]]' % (
                    PithiaOntologyNamespacePrefix.SKOS,
                    PithiaOntologyNamespacePrefix.SKOS,
                    PithiaOntologyNamespacePrefix.RDF,
                    first_layer_term_url,
                )
            )
            second_layer_terms_by_url.update(self._map_ontology_term_elements_to_dictionary(
                elements_of_child_terms_by_skos_broader,
                parent_term_name=first_layer_term_properties.get('name')
            ))

            # SKOS narrower
            urls_of_child_terms_by_skos_narrower = self._get_elements_by_xpath_query(
                './/%s:Concept[@%s:about="%s"]/%s:narrower/@%s:resource' % (
                    PithiaOntologyNamespacePrefix.SKOS,
                    PithiaOntologyNamespacePrefix.RDF,
                    first_layer_term_url,
                    PithiaOntologyNamespacePrefix.SKOS,
                    PithiaOntologyNamespacePrefix.RDF,
                )
            )
            if not len(urls_of_child_terms_by_skos_narrower):
                continue

            _ = [
                '@%s:about="%s"' % (PithiaOntologyNamespacePrefix.RDF, url)
                for url in urls_of_child_terms_by_skos_narrower
            ]

            elements_of_child_terms_by_skos_narrower = self._get_elements_by_xpath_query(
                './/%s:Concept[%s]' % (
                    PithiaOntologyNamespacePrefix.SKOS,
                    ' or '.join(_),
                )
            )
            second_layer_terms_by_url.update(self._map_ontology_term_elements_to_dictionary(
                elements_of_child_terms_by_skos_narrower,
                parent_term_name=first_layer_term_properties.get('name')
            ))

        return first_layer_terms_by_url | second_layer_terms_by_url


class ObservedPropertyMetadataService(OntologyCategoryMetadataService):
    def __init__(self) -> None:
        xml_of_observed_property_terms = get_ontology_category_terms_in_xml_format('observedProperty')
        super().__init__(xml_of_observed_property_terms)

    def get_measurands_from_observed_properties(self, observed_property_urls: list[str] | set[str]):
        base_xpath_selector = self._create_base_xpath_query_selector_for_iris(
            observed_property_urls
        )
        return list(set(self._get_elements_by_xpath_query(
            '%s/%s:measurand/@%s:resource' % (
                base_xpath_selector,
                PithiaOntologyNamespacePrefix.PITHIA,
                PithiaOntologyNamespacePrefix.RDF,
            )
        )))

    def get_phenomenons_from_observed_properties(self, observed_property_urls: list[str] | set[str]):
        base_xpath_selector = self._create_base_xpath_query_selector_for_iris(
            observed_property_urls
        )
        return list(set(self._get_elements_by_xpath_query(
            '%s/%s:phenomenon/@%s:resource' % (
                base_xpath_selector,
                PithiaOntologyNamespacePrefix.PITHIA,
                PithiaOntologyNamespacePrefix.RDF,
            )
        )))


def get_xml_of_ontology_category_terms_locally(ontology_category):
    try:
        local_ontology_files_path = os.path.join(BASE_DIR, 'ontology', 'local_ontology_files')
        local_ontology_file_name = None
        for filename in os.listdir(local_ontology_files_path):
            # The casing of the ontology category may not
            # always be the same.
            if filename[:-4].lower() != ontology_category.lower():
                continue
            local_ontology_file_name = filename
        ontology_file = open(os.path.join(BASE_DIR, 'ontology', 'local_ontology_files', local_ontology_file_name), 'r', encoding='utf-8')
        return ontology_file.read()
    except FileNotFoundError:
        logger.exception(f'An offline XML file for the ontology category, "{ontology_category}", was not found.')
    return None


def get_ontology_category_terms_in_xml_format(ontology_category):
    try:
        return get_rdf_text_remotely(ontology_category)
    except BaseException as err:
        logger.exception('Encountered error whilst fetching RDF for ontology category.')
    
    # If fetching from the ontology XML file server
    # fails, use a locally stored version of the
    # XML file instead.
    return get_rdf_text_locally(ontology_category)


# Continued - existing
def get_rdf_text_for_ontology_component(ontology_component):
    try:
        return get_rdf_text_remotely(ontology_component)
    except BaseException as err:
        logger.exception('Encountered error whilst fetching RDF for ontology category.')
    
    # Read ontology from file - alt method if connection to ontology server fails
    return get_rdf_text_locally(ontology_component)


def get_graph_of_pithia_ontology_component(ontology_component):
    ontology_text = get_rdf_text_for_ontology_component(ontology_component)

    # Create a graph object with rdflib and parse fetched text
    g = Graph()
    return g.parse(data=ontology_text, format='application/rdf+xml')


def get_phenomenon_ids_from_observed_property_id(observed_property_id, g, phenomenon_ids):
    for s, p, o in g.triples((URIRef(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/observedProperty/{observed_property_id}'), PITHIA.phenomenon, None)):
        phenomenon_ids.append(o.split('/')[-1])
    return phenomenon_ids


def get_measurand_ids_from_observed_property_id(observed_property_id, g, measurand_ids):
    for s, p, o in g.triples((URIRef(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/observedProperty/{observed_property_id}'), PITHIA.measurand, None)):
        measurand_ids.append(o.split('/')[-1])
    return measurand_ids


def get_parent_node_ids_of_node_id(node_id, ontology_component, parent_node_ids, g):
    for s, p, o in g.triples((URIRef(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{ontology_component}/{node_id}'), SKOS.broader, None)):
        parent_node_ids.append(o.split('/')[-1])
    return parent_node_ids


def get_pref_label_from_ontology_node_iri(ontology_node_iri, g=None):
    if g is None:
        ontology_term_category = ontology_node_iri.split('/')[-2]
        g = get_graph_of_pithia_ontology_component(ontology_term_category)
    pref_label = g.value(URIRef(ontology_node_iri), SKOS.prefLabel)
    if not pref_label:
        return None
    return str(pref_label)


def get_skos_properties_from_ontology_node(iri, skos_properties, g=None):
    if not g:
        g = get_graph_of_pithia_ontology_component(iri.split('/')[-2])
    property_dict = {
        sp: str(g.value(URIRef(iri), SKOS[sp]))
    for sp in skos_properties}
    return property_dict


# Credit for get_path: https://stackoverflow.com/a/22171182
def getpath(nested_dict, value, prepath=()):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if value in v: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = getpath(v, value, path) # recursive call
            if p is not None:
                return p


# Credit for gen_dict_extract: https://stackoverflow.com/a/29652561
def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result


def get_nested_phenomenons_in_observed_property(observed_property):
    all_phenomenons_of_observed_property = list(gen_dict_extract('phenomenon', observed_property))
    # Credit for list flattening code: https://stackoverflow.com/a/952952
    all_phenomenons_of_observed_property_flattened = [item for sublist in all_phenomenons_of_observed_property for item in sublist]
    return all_phenomenons_of_observed_property_flattened


def categorise_observed_property_dict_by_top_level_phenomenons(observed_property_dict):
    categorised_observed_property_dict = {}
    phenomen_dict = create_dictionary_from_pithia_ontology_component('phenomenon')
    added_observed_properties = []

    def add_observed_property_to_category(key, observed_property, category):
        if category not in categorised_observed_property_dict:
            categorised_observed_property_dict[category] = {}
        if (category != 'None' and
            'None' in categorised_observed_property_dict and
            key in categorised_observed_property_dict['None'] and
            key in added_observed_properties):
            categorised_observed_property_dict[category][key] = observed_property
            categorised_observed_property_dict['None'].pop(key)
        if key not in added_observed_properties:
            categorised_observed_property_dict[category][key] = observed_property
            added_observed_properties.append(key)

    for key, value in observed_property_dict.items():
        all_phenomenons_for_observed_property = get_nested_phenomenons_in_observed_property(value)
        if len(all_phenomenons_for_observed_property) == 0:
            add_observed_property_to_category(key, value, 'None')
            continue
        for phenomenon in all_phenomenons_for_observed_property:
            path_of_phenomenon = getpath(phenomen_dict, phenomenon.replace('phenomenon', ''))
            if path_of_phenomenon is None:
                add_observed_property_to_category(key, value, 'None')
            else:
                top_level_phenomenon = path_of_phenomenon[0]
                add_observed_property_to_category(key, value, top_level_phenomenon)
    if 'None' in categorised_observed_property_dict and len(categorised_observed_property_dict['None']) == 0:
        categorised_observed_property_dict.pop('None', None)
    return categorised_observed_property_dict


def create_dictionary_from_pithia_ontology_component(
        ontology_component: str,
        instrument_types_grouped_by_observed_property: dict | None = None,
        computation_types_grouped_by_observed_property: dict | None = None):
    result = {}
    graph = get_graph_of_pithia_ontology_component(ontology_component)
    for term_url in graph.objects(predicate=SKOS.member):
        # Extract the localID from the last part of the term URL.
        # e.g., ../featureOfInterest/SolarSystem
        local_id = term_url.split('/')[-1]
        if local_id in result:
            continue
        result[local_id] = {
            'id': f'{ontology_component}{local_id}',
            'value': local_id,
            'narrowers': {},
            'iri': f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{ontology_component}/{local_id}',
        }
        term = Resource(graph, term_url)
        for predicate in term.predicates():
            # Extract the property name from the last part of the
            # predicate identifier.
            # e.g., http://www.w3.org/1999/02/22-rdf-syntax-ns#type
            property = predicate.identifier.split('#')[-1]
            if len(predicate.identifier.split('#')) == 1:
                property = predicate.identifier.split('/')[-1]
            if property in result[local_id]:
                continue
            # The property's value may become a string if only one
            # instance of the property value is found.
            result[local_id][property] = []
            if property == 'phenomenon':
                for s, p, phenomenon_url in graph.triples((term_url, predicate.identifier, None)):
                    labelled_local_id = f'phenomenon{phenomenon_url.split("/")[-1]}'
                    result[local_id][property].append(labelled_local_id)
                continue
            if property == 'featureOfInterest':
                for s, p, feature_of_interest_url in graph.triples((term_url, predicate.identifier, None)):
                    labelled_local_id = f'featureOfInterest{feature_of_interest_url.split("/")[-1]}'
                    result[local_id][property].append(labelled_local_id)
                continue
            if property == 'measurand':
                for s, p, measurand_url in graph.triples((term_url, predicate.identifier, None)):
                    labelled_local_id = f'measurand{measurand_url.split("/")[-1]}'
                    result[local_id][property].append(labelled_local_id)
                continue
            for s, p, property_item in graph.triples((term_url, predicate.identifier, None)):
                result[local_id][property].append(str(property_item))
            if len(result[local_id][property]) == 1:
                result[local_id][property] = next(iter(result[local_id][property]), None)

        # Find child terms of the current term by doing searching backwards with SKOS.broader.
        for child_term_url, p, o in graph.triples((None, SKOS.broader, term_url)):
            child_term_local_id = child_term_url.split('/')[-1]
            if child_term_local_id == local_id:
                continue
            if child_term_local_id in result[local_id]['narrowers']:
                continue
            result[local_id]['narrowers'][child_term_local_id] = {
                'id': f'{ontology_component}{child_term_local_id}',
                'value': child_term_local_id,
                'narrowers': {},
            }

        # Find more child terms by doing a forward search with SKOS.narrower. Usually, the above
        # check with SKOS.broader finds everything this check does and more, but there may be cases
        # where this doesn't happen.
        for s, p, child_term_url in graph.triples((term_url, SKOS.narrower, None)):
            child_term_local_id = child_term_url.split('/')[-1]
            if child_term_local_id == local_id:
                continue
            if child_term_local_id in result[local_id]['narrowers']:
                continue
            result[local_id]['narrowers'][child_term_local_id] = {
                'id': f'{ontology_component}{child_term_local_id}',
                'value': child_term_local_id,
                'narrowers': {},
            }

    # Assumes that the ontology component is "Observed Property".
    if instrument_types_grouped_by_observed_property is None:
        instrument_types_grouped_by_observed_property = dict()
    if len(instrument_types_grouped_by_observed_property) > 0:
        for local_id, instrument_types in instrument_types_grouped_by_observed_property.items():
            if local_id not in result:
                continue
            result[local_id]['instrumentType'] = instrument_types

    # Assumes that the ontology component is "Observed Property".
    if computation_types_grouped_by_observed_property is None:
        computation_types_grouped_by_observed_property = dict()
    if len(computation_types_grouped_by_observed_property) > 0:
        for local_id, computation_types in computation_types_grouped_by_observed_property.items():
            if local_id not in result:
                continue
            result[local_id]['computationType'] = computation_types

    # If a term in "result" appears as a child of another term, then
    # it will be moved within that term. The move happens in two steps:
    # copy over to the parent term, then delete the child term from the
    # top-level of "result".
    top_level_local_ids_to_remove = []
    for local_id in result:
        for child_term_local_id in result[local_id]['narrowers']:
            if child_term_local_id not in result:
                continue
            result[local_id]['narrowers'][child_term_local_id] = result[child_term_local_id]
            top_level_local_ids_to_remove.append(child_term_local_id)
    for local_id in top_level_local_ids_to_remove:
        result.pop(local_id, None)

    return result