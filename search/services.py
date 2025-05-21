from common.models import (
    AcquisitionCapabilities,
    ComputationCapabilities,
    Instrument,
)
from ontology.services import (
    get_graph_of_pithia_ontology_component,
    get_parent_node_ids_of_node_id,
)


# Search form setup
def setup_instrument_types_for_observed_property_search_form():
    instrument_types_grouped_by_observed_property = {}
    instruments = Instrument.objects.all()
    for i in instruments:
        # Find the Acquisition Capabilities relating to each Instrument.
        acquisition_capability_sets = AcquisitionCapabilities.objects.referencing_instrument_url(i.metadata_server_url)
        
        # If any Acquisition Capabilities are found, return its Observed
        # Property URLs.
        observed_property_urls = []
        for ac in acquisition_capability_sets:
            observed_property_urls = list(set(observed_property_urls + ac.observed_property_urls))
        
        instrument_type_id = i.instrument_type_url.split('/')[-1]
        for url in observed_property_urls:
            # Map the Instrument Type URL of
            # the Instrument to each Observed Property URL.
            observed_property_id = url.split('/')[-1]
            if observed_property_id not in instrument_types_grouped_by_observed_property:
                instrument_types_grouped_by_observed_property[observed_property_id] = []
            instrument_types_grouped_by_observed_property[observed_property_id].append(f'instrumentType{instrument_type_id}')
            instrument_types_grouped_by_observed_property[observed_property_id] = list(set(instrument_types_grouped_by_observed_property[observed_property_id]))
    return instrument_types_grouped_by_observed_property


def setup_computation_types_for_observed_property_search_form():
    computation_types_grouped_by_observed_property = {}
    computation_capability_sets = ComputationCapabilities.objects.all()
    for cc_set in computation_capability_sets:
        # Get the Observed Property URLs for each Computation Capabilities
        # registration.
        observed_property_urls = cc_set.observed_property_urls
        computation_type_ids = [url.split('/')[-1] for url in cc_set.computation_type_urls]
        for url in observed_property_urls:
            # Map the Computation Type URLs of the Computation Capabilities
            # registration to each Observed Property URL of the Computation
            # Capabilities registration.
            observed_property_id = url.split('/')[-1]
            if observed_property_id not in computation_types_grouped_by_observed_property:
                computation_types_grouped_by_observed_property[observed_property_id] = []
            computation_types_grouped_by_observed_property[observed_property_id] = list(set(
                computation_types_grouped_by_observed_property[observed_property_id] + [f'computationType{id}' for id in computation_type_ids]
            ))
    return computation_types_grouped_by_observed_property


def get_parents_of_registered_ontology_terms(ontology_term_ids, ontology_component, parent_node_ids, g=None):
    if g is None:
        g = get_graph_of_pithia_ontology_component(ontology_component)
    for id in ontology_term_ids:
        parent_node_ids_of_id = get_parent_node_ids_of_node_id(id, ontology_component, [], g)
        if len(parent_node_ids_of_id) == 0:
            continue
        parent_node_ids.extend(parent_node_ids_of_id)
        parent_node_ids = get_parents_of_registered_ontology_terms(parent_node_ids_of_id, ontology_component, parent_node_ids, g=g)
    return parent_node_ids