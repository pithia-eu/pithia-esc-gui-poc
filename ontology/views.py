import os
from django.http import (
    FileResponse,
    Http404,
    HttpResponseServerError,
    HttpResponseNotFound,
)
from django.shortcuts import render
from django.views.generic import TemplateView
from rdflib import URIRef
from rdflib.resource import Resource
from rdflib.namespace._SKOS import SKOS

from .services import (
    create_dictionary_from_pithia_ontology_component,
    get_graph_of_pithia_ontology_component,
    get_ontology_category_terms_in_xml_format,
)
from .utils import (
    LicenceOntologyTermMetadata,
    ObservedPropertyOntologyTermMetadata,
    OntologyCategoryMetadata,
    OntologyTermMetadata,
)

from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from pithiaesc.settings import BASE_DIR
from search.services import (
    get_parents_of_registered_ontology_terms,
    get_registered_computation_types,
    get_registered_features_of_interest,
    get_registered_instrument_types,
    get_registered_measurands,
    get_registered_observed_properties,
    get_registered_phenomenons
)
from utils.string_helpers import split_camel_case
from utils.url_helpers import create_ontology_term_detail_url_from_ontology_term_server_url
from utils.html_helpers import create_anchor_tag_html_from_ontology_term_details


_ONTOLOGY_INDEX_PAGE_TITLE = 'Space Physics Ontology'


# Create your views here.
def ontology(request):
    return render(request, 'ontology/index.html', {
        'title': _ONTOLOGY_INDEX_PAGE_TITLE
    })

def ontology_guide(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'ontology', 'PITHIA-NRF_SpacePhysicsOntology_1.4.pdf'), 'rb'), content_type='application/pdf')
    except IOError:
        return HttpResponseNotFound('The ontology guide was not found.')
    
def _get_ontology_category_term_list_page_title_from_category(category):
    title_base = ' '.join(split_camel_case(category)).title()
    if category.lower() == 'crs':
        title_base = 'Co-ordinate Reference System'
    elif category.lower() == 'verticalcrs':
        title_base = 'Vertical Co-ordinate Reference System'
    return f'{title_base} Terms'

def ontology_category_terms_list(request, category):
    return render(request, 'ontology/ontology_category_terms_list.html', {
        'category': category,
        'title': _get_ontology_category_term_list_page_title_from_category(category),
        'ontology_index_page_breadcrumb_text': _ONTOLOGY_INDEX_PAGE_TITLE,
    })

def ontology_category_terms_list_only(request, category):
    try:
        dictionary = create_dictionary_from_pithia_ontology_component(category)
    except FileNotFoundError:
        return HttpResponseServerError('Could not load terms due to a server error.')
    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []
    if category.lower() == 'observedproperty':
        registered_ontology_terms = get_registered_observed_properties()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    elif category.lower() == 'featureofinterest':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_features_of_interest(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    elif category.lower() == 'instrumenttype':
        registered_ontology_terms = get_registered_instrument_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    elif category.lower() == 'computationtype':
        registered_ontology_terms = get_registered_computation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    elif category.lower() == 'phenomenon':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_phenomenons(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    elif category.lower() == 'measurand':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_measurands(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, [])
    return render(request, 'ontology/ontology_tree_template_outer.html', {
        'dictionary': dictionary,
        'category': category,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })

def _remove_namespace_prefix_from_predicate(p):
    p_identifier_no_prefix = p.identifier.split('#')[-1]
    if len(p.identifier.split('#')) == 1:
        p_identifier_no_prefix = p.identifier.split('/')[-1]
    return p_identifier_no_prefix

def ontology_term_detail(request, category, term_id):
    g = get_graph_of_pithia_ontology_component(category)
    resource = None
    resource_uriref = URIRef(f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{category}/{term_id}')
    triples = list(g.triples((None, SKOS.member, resource_uriref)))
    if len(triples) > 0:
        resource = Resource(g, triples[0][2])
    if resource is None:
        return HttpResponseNotFound(f'Details for the ontology term ID <b>"{term_id}"</b> were not found.')
    resource_predicates_no_prefix = list(set(map(_remove_namespace_prefix_from_predicate, resource.predicates())))
    # Turn resource into a dictionary for easier usage
    resource_dictionary = {}
    resource_predicates_readable = {}
    for p in resource.predicates():
        p_identifier_no_prefix = p.identifier.split('#')[-1]
        if len(p.identifier.split('#')) == 1:
            p_identifier_no_prefix = p.identifier.split('/')[-1]
        if p_identifier_no_prefix not in resource_dictionary and (p_identifier_no_prefix == 'observedProperty' or p_identifier_no_prefix == 'phenomenon' or p_identifier_no_prefix == 'measurand' or p_identifier_no_prefix == 'featureOfInterest' or p_identifier_no_prefix == 'propagationMode' or p_identifier_no_prefix == 'interaction' or p_identifier_no_prefix == 'qualifier' or p_identifier_no_prefix == 'narrower' or p_identifier_no_prefix == 'broader'):
            # Other ontology terms referenced by the resource
            if p_identifier_no_prefix == 'narrower' or p_identifier_no_prefix == 'broader':
                g_other_ontology_term = g
            else:
                g_other_ontology_term = get_graph_of_pithia_ontology_component(p_identifier_no_prefix)
            urls_of_referenced_terms = []
            urls_of_referenced_terms_with_preflabels = []
            for s2, p2, o2 in g.triples((resource_uriref, p.identifier, None)):
                urls_of_referenced_terms.append(str(o2))
            for u in urls_of_referenced_terms:
                ontology_term_detail_url_for_referenced_term = create_ontology_term_detail_url_from_ontology_term_server_url(u)
                term_pref_label = u.split('/')[-1]
                anchor_tag_of_term = create_anchor_tag_html_from_ontology_term_details(term_pref_label, u, ontology_term_detail_url_for_referenced_term, g_other_ontology_term)
                urls_of_referenced_terms_with_preflabels.append(anchor_tag_of_term)
            resource_dictionary[p_identifier_no_prefix]= urls_of_referenced_terms_with_preflabels
        if p_identifier_no_prefix not in resource_dictionary:
            if len(list(g.triples((resource_uriref, p.identifier, None)))) > 1:
                resource_dictionary[p_identifier_no_prefix] = []
                for s2, p2, o2 in g.triples((resource_uriref, p.identifier, None)):
                    resource_dictionary[p_identifier_no_prefix].append(str(o2))
            else:
                resource_dictionary[p_identifier_no_prefix] = str(list(g.triples((resource_uriref, p.identifier, None)))[0][2])
    # Have a human-readable version of the predicates to display in the front-end.
    for p in resource_predicates_no_prefix:
        if p == 'broader':
            resource_predicates_readable[p] = 'Broader Terms' 
        elif p == 'narrower':
            resource_predicates_readable[p] = 'Narrower Terms' 
        elif p == 'observedProperty':
            resource_predicates_readable[p] = 'Observed Properties' 
        elif p == 'phenomenon':
            resource_predicates_readable[p] = 'Phenomenons' 
        elif p == 'measurand':
            resource_predicates_readable[p] = 'Measurands' 
        elif p == 'featureOfInterest':
            resource_predicates_readable[p] = 'Features of Interest' 
        elif p == 'interaction':
            resource_predicates_readable[p] = 'Interactions' 
        elif p == 'qualifier':
            resource_predicates_readable[p] = 'Qualifiers'
        else:
            resource_predicates_readable[p] = ' '.join(split_camel_case(p)).title() 
    return render(request, 'ontology/ontology_term_detail.html', {
        'title': resource_dictionary['prefLabel'],
        'resource_ontology_url': f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{category}/{term_id}',
        'resource_dictionary': resource_dictionary,
        'resource_predicates_no_prefix': resource_predicates_no_prefix,
        'resource_predicates_readable': resource_predicates_readable,
        'category': category,
        'ontology_index_page_breadcrumb_text': _ONTOLOGY_INDEX_PAGE_TITLE,
        'ontology_category_term_list_page_breadcrumb_text': _get_ontology_category_term_list_page_title_from_category(category),
    })
 
class OntologyTermDetailView(TemplateView):
    template_name = 'ontology/detail/base.html'

    def apply_wrapper_to_ontology_term_metadata(self, xml_string_for_ontology_term: str):
        return OntologyTermMetadata(xml_string_for_ontology_term)

    def get(self, request, *args, **kwargs):
        if not hasattr(self, 'category'):
            self.category = self.kwargs['category']
        self.term_id = self.kwargs['term_id']
        xml_string_for_ontology_category_terms = get_ontology_category_terms_in_xml_format(self.category)
        self.ontology_category_metadata = OntologyCategoryMetadata(xml_string_for_ontology_category_terms)
        xml_string_for_ontology_term = self.ontology_category_metadata.get_term_with_id(self.term_id)
        if not xml_string_for_ontology_term:
            raise Http404(f'An ontology term with ID, <b>"{self.term_id}"</b>, was not found.')
        self.ontology_term_metadata = self.apply_wrapper_to_ontology_term_metadata(xml_string_for_ontology_term)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.ontology_term_metadata.pref_label,
            'resource_ontology_url': f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/{self.category}/{self.term_id}',
            'ontology_term_metadata': self.ontology_term_metadata,
            # Get names and ontology browser URLs for
            # ontology server URLs.
            'names_and_ontology_browser_urls': self.ontology_term_metadata.get_names_and_ontology_browser_urls_of_ontology_term_urls(
                fetched_ontology_categories={
                    self.category: self.ontology_category_metadata,
                }
            ),
            'category': self.category,
            'ontology_index_page_breadcrumb_text': _ONTOLOGY_INDEX_PAGE_TITLE,
            'ontology_category_term_list_page_breadcrumb_text': _get_ontology_category_term_list_page_title_from_category(self.category),
        })
        return context


class LicenceTermDetailView(OntologyTermDetailView):
    def apply_wrapper_to_ontology_term_metadata(self, xml_string_for_ontology_term: str):
        return LicenceOntologyTermMetadata(xml_string_for_ontology_term)

    def get(self, request, *args, **kwargs):
        self.category = 'licence'
        return super().get(request, *args, **kwargs)


class ObservedPropertyTermDetailView(OntologyTermDetailView):
    def apply_wrapper_to_ontology_term_metadata(self, xml_string_for_ontology_term: str):
        return ObservedPropertyOntologyTermMetadata(xml_string_for_ontology_term)

    def get(self, request, *args, **kwargs):
        self.category = 'observedProperty'
        return super().get(request, *args, **kwargs)