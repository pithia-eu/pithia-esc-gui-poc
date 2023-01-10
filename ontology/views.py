from django.shortcuts import render
from rdflib import URIRef
from rdflib.resource import Resource
from rdflib.namespace._SKOS import SKOS
from utils.string_helpers import _split_camel_case
from utils.url_helpers import create_ontology_term_detail_url_from_ontology_term_server_url
from utils.html_helpers import create_anchor_tag_html_from_ontology_term_details
from utils.ontology_helpers import (
    create_dictionary_from_pithia_ontology_component,
    get_graph_of_pithia_ontology_component,
    ONTOLOGY_SERVER_BASE_URL
)
from search.views import (
    get_parents_of_registered_ontology_terms,
    get_registered_computation_types,
    get_registered_features_of_interest,
    get_registered_instrument_types,
    get_registered_measurands,
    get_registered_observed_properties,
    get_registered_phenomenons
)

_ONTOLOGY_PAGE_TITLE = 'Space Physics Ontology'

# Create your views here.
def ontology(request):
    return render(request, 'browse/ontology.html', {
        'title': _ONTOLOGY_PAGE_TITLE
    })
    
def _get_ontology_category_term_list_page_title_from_category(category):
    title_base = ' '.join(_split_camel_case(category)).title()
    if category.lower() == 'crs':
        title_base = 'Co-ordinate Reference System'
    elif category.lower() == 'verticalcrs':
        title_base = 'Vertical Co-ordinate Reference System'
    return f'{title_base} Terms'

def ontology_category_terms_list(request, category):
    return render(request, 'browse/ontology_category_terms_list.html', {
        'category': category,
        'title': _get_ontology_category_term_list_page_title_from_category(category),
        'ontology_index_page_breadcrumb_text': _ONTOLOGY_PAGE_TITLE,
    })

def ontology_category_terms_list_only(request, category):
    dictionary = create_dictionary_from_pithia_ontology_component(category)
    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []
    if category.lower() == 'observedproperty':
        registered_ontology_terms = get_registered_observed_properties()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'featureofinterest':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_features_of_interest(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'instrumenttype':
        registered_ontology_terms = get_registered_instrument_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'computationtype':
        registered_ontology_terms = get_registered_computation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'phenomenon':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_phenomenons(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'measurand':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_measurands(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    return render(request, 'browse/ontology_tree_template_outer.html', {
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
    resource_uriref = URIRef(f'{ONTOLOGY_SERVER_BASE_URL}{category}/{term_id}')
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
            resource_predicates_readable[p] = ' '.join(_split_camel_case(p)).title() 
    return render(request, 'browse/ontology_term_detail.html', {
        'title': resource_dictionary['prefLabel'],
        'resource_ontology_url': f'{ONTOLOGY_SERVER_BASE_URL}{category}/{term_id}',
        'resource_dictionary': resource_dictionary,
        'resource_predicates_no_prefix': resource_predicates_no_prefix,
        'resource_predicates_readable': resource_predicates_readable,
        'category': category,
        'ontology_index_page_breadcrumb_text': _ONTOLOGY_PAGE_TITLE,
        'ontology_category_term_list_page_breadcrumb_text': _get_ontology_category_term_list_page_title_from_category(category),
    })