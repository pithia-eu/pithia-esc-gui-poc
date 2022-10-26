from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .helpers import remove_underscore_from_id_attribute
from .ontology_helpers import create_dictionary_from_pithia_ontology_component, get_feature_of_interest_ids_from_observed_property_id, get_graph_of_pithia_ontology_component, get_measurand_ids_from_observed_property_id, get_observed_property_hrefs_from_features_of_interest, get_parent_node_ids_of_node_id, get_phenomenon_ids_from_observed_property_id
from .search_helpers import find_matching_data_collections
from common.mongodb_models import CurrentAcquisition, CurrentAcquisitionCapability, CurrentComputation, CurrentComputationCapability, CurrentInstrument

def get_tree_form_for_ontology_component(request, ontology_component):
    dictionary = create_dictionary_from_pithia_ontology_component(ontology_component)
    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []
    if ontology_component.lower() == 'observedproperty':
        registered_ontology_terms = get_registered_observed_properties()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, None, [])
    elif ontology_component.lower() == 'featureofinterest':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_features_of_interest(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, None, [])
    elif ontology_component.lower() == 'instrumenttype':
        registered_ontology_terms = get_registered_instrument_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, None, [])
    elif ontology_component.lower() == 'computationtype':
        registered_ontology_terms = get_registered_computation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, None, [])
    elif ontology_component.lower() == 'phenomenon':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_phenomenons(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, None, [])
    elif ontology_component.lower() == 'measurand':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_measurands(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, ontology_component, None, [])
    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': dictionary,
        'ontology_component_name': ontology_component,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })

def index(request):
    if request.method == 'POST':
        features_of_interests = request.POST.getlist('featureOfInterest')
        request.session['features_of_interest'] = features_of_interests
        computation_types = request.POST.getlist('computationType')
        request.session['computation_types'] = computation_types
        instrument_types = request.POST.getlist('instrumentType')
        request.session['instrument_types'] = instrument_types
        observed_properties = request.POST.getlist('observedProperty')
        request.session['observed_properties'] = observed_properties
        return HttpResponseRedirect(reverse('search:results'))
    return render(request, 'search/index.html', {
        'title': 'Search Models & Measurements'
    })

def results(request):
    data_collections = find_matching_data_collections(request)
    data_collections = list(map(remove_underscore_from_id_attribute, data_collections))

    return render(request, 'search/results.html', {
        'title': 'Search results',
        'results': data_collections
    })

def extract_localid_from_xlink_href(xlinkhref):
    return xlinkhref.split('/')[-1]

def get_registered_observed_properties():
    observed_properties_from_computation_capabilities = list(CurrentComputationCapability.aggregate([
        {
            '$unwind': {
                'path': '$capabilities.processCapability'
            }
        },
        {
            '$group': {
                '_id': None,
                'xlink_hrefs': {
                    '$addToSet': '$observedProperty.@xlink:href'
                }
            }
        }
    ]))

    observed_properties_from_acquisition_capabilities = list(CurrentAcquisitionCapability.aggregate([
        {
            '$unwind': {
                'path': '$capabilities.processCapability'
            }
        },
            {
                '$group': {
                    '_id': None,
                    'xlink_hrefs': {
                        '$addToSet': '$observedProperty.@xlink:href'
                    }
                }
            }
    ]))
    observed_property_ids = []
    if len(observed_properties_from_computation_capabilities) > 0:
        observed_property_ids.extend(list(map(extract_localid_from_xlink_href, observed_properties_from_computation_capabilities[0]['xlink_hrefs'])))
    if len(observed_properties_from_acquisition_capabilities) > 0:
        observed_property_ids.extend(list(map(extract_localid_from_xlink_href, observed_properties_from_acquisition_capabilities[0]['xlink_hrefs'])))
    return list(set(observed_property_ids))

def get_registered_features_of_interest(registered_observed_property_ids):
    feature_of_interest_ids = []
    g_op = get_graph_of_pithia_ontology_component('observedProperty')
    for id in registered_observed_property_ids:
        get_feature_of_interest_ids_from_observed_property_id(id, g_op, feature_of_interest_ids)
    return feature_of_interest_ids

def get_registered_instrument_types():
    return list(map(extract_localid_from_xlink_href, list(CurrentInstrument.find().distinct('type.@xlink:href'))))

def get_registered_computation_types():
    return list(map(extract_localid_from_xlink_href, list(CurrentComputationCapability.find().distinct('type.@xlink:href'))))

def get_registered_phenomenons(registered_observed_property_ids):
    phenomenon_ids = []
    g_op = get_graph_of_pithia_ontology_component('observedProperty')
    for id in registered_observed_property_ids:
        get_phenomenon_ids_from_observed_property_id(id, g_op, phenomenon_ids)
    return phenomenon_ids

def get_registered_measurands(registered_observed_property_ids):
    measurand_ids = []
    g_op = get_graph_of_pithia_ontology_component('observedProperty')
    for id in registered_observed_property_ids:
        get_measurand_ids_from_observed_property_id(id, g_op, measurand_ids)
    return measurand_ids

def get_parents_of_registered_ontology_terms(ontology_term_ids, ontology_component, g, parent_node_ids):
    if g is None:
        g = get_graph_of_pithia_ontology_component(ontology_component)
    for id in ontology_term_ids:
        parent_node_ids_of_id = get_parent_node_ids_of_node_id(id, ontology_component, g, [])
        if len(parent_node_ids_of_id) > 0:
            parent_node_ids.extend(parent_node_ids_of_id)
            parent_node_ids = get_parents_of_registered_ontology_terms(parent_node_ids_of_id, ontology_component, g, parent_node_ids)
    return parent_node_ids