import re

from common.constants import (
    ANNOTATION_TYPE_URL_BASE,
    COMPUTATION_TYPE_URL_BASE,
    INSTRUMENT_TYPE_URL_BASE,
)
from common.models import (
    Acquisition,
    AcquisitionCapabilities,
    ComputationCapabilities,
    Computation,
    DataCollection,
    Instrument,
    Process,
)
from ontology.services import (
    get_feature_of_interest_ids_from_observed_property_id,
    get_graph_of_pithia_ontology_component,
    get_measurand_ids_from_observed_property_id,
    get_observed_property_urls_from_feature_of_interest_urls,
    get_parent_node_ids_of_node_id,
    get_phenomenon_ids_from_observed_property_id,
)


def get_data_collections_for_search(
        feature_of_interest_urls: list = [],
        instrument_type_urls: list = [],
        computation_type_urls: list = [],
        annotation_type_urls: list = [],
        observed_property_urls: list = []):
    if len(feature_of_interest_urls) > 0:
        # Retrives observed properties that also
        # reference the features of interest that
        # were selected.
        additional_observed_property_urls = get_observed_property_urls_from_feature_of_interest_urls(feature_of_interest_urls)
        observed_property_urls += additional_observed_property_urls
        observed_property_urls = list(set(observed_property_urls))

    # The way in which data collections are found goes according to the
    # project data model diagram.


    # Search by instrument type
    # fbit = found by instrument type
    # Instruments
    instruments_found_by_instrument_type = Instrument.objects.for_search_by_instrument_type_urls(instrument_type_urls)
    ifbit_urls = [i.metadata_server_url for i in instruments_found_by_instrument_type]

    # Acquisition Capabilities
    acquisition_capabilities_found_by_instrument_type = AcquisitionCapabilities.objects.for_search_by_instrument_type_urls(ifbit_urls)
    acfbit_urls = [ac.metadata_server_url for ac in acquisition_capabilities_found_by_instrument_type]

    # Acquisitions
    acquisitions_found_by_instrument_type = Acquisition.objects.for_search_by_instrument_type_urls(acfbit_urls)
    afbit_urls = [a.metadata_server_url for a in acquisitions_found_by_instrument_type]

    # Processes
    processes_found_by_instrument_type = Process.objects.for_search_by_instrument_type_urls(afbit_urls)
    pfbit_urls = [p.metadata_server_url for p in processes_found_by_instrument_type]

    # Data Collections
    data_collections_found_by_instrument_type = DataCollection.objects.for_search_by_instrument_type_urls(instrument_type_urls, pfbit_urls)


    # Search by computation type
    # fbct = found by computation type
    # Computation Capabilities
    computation_capabilities_found_by_computation_type = ComputationCapabilities.objects.for_search_by_computation_type_urls(computation_type_urls)
    ccfbct_urls = [cc.metadata_server_url for cc in computation_capabilities_found_by_computation_type]

    # Computations
    computations_found_by_computation_type = Computation.objects.for_search_by_computation_type_urls(ccfbct_urls)
    cfbct_urls = [c.metadata_server_url for c in computations_found_by_computation_type]

    # Processes
    processes_found_by_computation_type = Process.objects.for_search_by_computation_type_urls(cfbct_urls)
    pfbct_urls = [p.metadata_server_url for p in processes_found_by_computation_type]

    # Data Collections
    data_collections_found_by_computation_type = DataCollection.objects.for_search_by_computation_type_urls(computation_type_urls, pfbct_urls)

    
    # Search by annotation type
    # Annotation types should only be found
    # in Data Collections - not in any capabilities.
    # Data Collections
    data_collections_found_by_annotation_type = DataCollection.objects.for_search_by_annotation_type_urls(annotation_type_urls)


    # Search by observed property
    # fbop = found by observed property
    # Acquisition Capabilities
    acquisition_capabilities_found_by_observed_property = AcquisitionCapabilities.objects.for_search_by_observed_property_urls(observed_property_urls)
    acfbop_urls = [ac.metadata_server_url for ac in acquisition_capabilities_found_by_observed_property]

    # Acquisitions
    acquisitions_found_by_observed_property = Acquisition.objects.for_search_by_observed_property_urls(acfbop_urls)
    afbop_urls = [a.metadata_server_url for a in acquisitions_found_by_observed_property]

    # Computation Capabilities
    computation_capabilities_found_by_observed_property = ComputationCapabilities.objects.for_search_by_observed_property_urls(observed_property_urls)
    ccfbop_urls = [cc.metadata_server_url for cc in computation_capabilities_found_by_observed_property]

    # Computations
    computations_found_by_observed_property = Computation.objects.for_search_by_observed_property_urls(ccfbop_urls)
    cfbop_urls = [c.metadata_server_url for c in computations_found_by_observed_property]

    # Processes
    processes_found_by_observed_property = Process.objects.for_search_by_observed_property_urls(afbop_urls, cfbop_urls)
    pfbop_urls = [p.metadata_server_url for p in processes_found_by_observed_property]

    # Data Collections
    data_collections_found_by_feature_of_interest = DataCollection.objects.for_search_by_feature_of_interest_urls(feature_of_interest_urls)
    data_collections_found_by_observed_property = DataCollection.objects.for_search_by_observed_property_urls(pfbop_urls)


    # Merge data collections from prerequisite steps
    data_collections = DataCollection.objects.for_final_search_step(
        data_collections_found_by_feature_of_interest,
        data_collections_found_by_instrument_type,
        data_collections_found_by_computation_type,
        data_collections_found_by_annotation_type,
        data_collections_found_by_observed_property
    )

    return list(data_collections)

def find_matching_data_collections(
    feature_of_interest_urls: list = [],
    instrument_type_urls: list = [],
    computation_type_urls: list = [],
    observed_property_urls: list = []
):
    if len(feature_of_interest_urls) > 0:
        additional_observed_property_urls = get_observed_property_urls_from_feature_of_interest_urls(feature_of_interest_urls)
        observed_property_urls += additional_observed_property_urls
        observed_property_urls = list(set(observed_property_urls))

    # The way in which data collections are found goes according to the
    # project data model diagram.


    # Fetch Instruments
    instruments = Instrument.objects.for_search(instrument_type_urls)
    instrument_urls = [i.metadata_server_url for i in instruments]


    # Fetch Acquisition Capabilities/Computation Capabilities
    acquisition_capability_sets = AcquisitionCapabilities.objects.for_search(
        instrument_urls,
        observed_property_urls
    )
    acquisition_capability_set_urls = [ac.metadata_server_url for ac in acquisition_capability_sets]

    computation_capability_sets = ComputationCapabilities.objects.for_search(
        computation_type_urls,
        observed_property_urls
    )
    computation_capability_set_urls = [cc.metadata_server_url for cc in computation_capability_sets]


    # Fetch Acquisitions/Computations
    acquisitions = Acquisition.objects.for_search(acquisition_capability_set_urls)
    computations = Computation.objects.for_search(computation_capability_set_urls)


    # Fetch Processes
    processes = Process.objects.for_search(
        [a.metadata_server_url for a in acquisitions],
        [c.metadata_server_url for c in computations]
    )


    # Fetch Data Collections
    data_collections = DataCollection.objects.for_search(
        [p.metadata_server_url for p in processes],
        feature_of_interest_urls,
        instrument_type_urls,
        computation_type_urls
    )

    return list(data_collections)

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

def get_distinct_computation_type_urls_from_computation_capability_sets(computation_capability_sets):
    distinct_model_urls = [url for cc in computation_capability_sets for url in cc.computation_type_urls if re.match(f'^{COMPUTATION_TYPE_URL_BASE}', url)]
    return distinct_model_urls

def get_distinct_instrument_type_urls_from_data_collections(data_collections):
    instrument_type_urls = [url for dc in data_collections for url in dc.type_urls if re.match(f'^{INSTRUMENT_TYPE_URL_BASE}', url)]
    return list(set(instrument_type_urls))

def get_distinct_computation_type_urls_from_data_collections(data_collections):
    model_urls = [url for dc in data_collections for url in dc.type_urls if re.match(f'^{COMPUTATION_TYPE_URL_BASE}', url)]
    return list(set(model_urls))

def get_distinct_annotation_type_urls_from_data_collections(data_collections):
    distinct_urls = [url for dc in data_collections for url in dc.type_urls if re.match(f'^{ANNOTATION_TYPE_URL_BASE}', url)]
    return list(set(distinct_urls))

def extract_localid_from_xlink_href(xlinkhref):
    return xlinkhref.split('/')[-1]

def get_registered_observed_properties():
    acquisition_capability_sets = list(AcquisitionCapabilities.objects.all())
    computation_capability_sets = list(ComputationCapabilities.objects.all())
    registered_observed_property_urls = []
    for ac in acquisition_capability_sets:
        registered_observed_property_urls = registered_observed_property_urls + ac.observed_property_urls
    for cc in computation_capability_sets:
        registered_observed_property_urls = registered_observed_property_urls + cc.observed_property_urls
    registered_observed_property_ids = [extract_localid_from_xlink_href(url) for url in registered_observed_property_urls]
    return list(set(registered_observed_property_ids))

def get_registered_features_of_interest(registered_observed_property_ids):
    feature_of_interest_ids = []
    g_op = get_graph_of_pithia_ontology_component('observedProperty')
    for id in registered_observed_property_ids:
        get_feature_of_interest_ids_from_observed_property_id(id, g_op, feature_of_interest_ids)
    registered_data_collections = list(DataCollection.objects.all())
    feature_of_interest_ids_from_data_collections = [extract_localid_from_xlink_href(url) for dc in registered_data_collections for url in dc.feature_of_interest_urls]
    feature_of_interest_ids.extend(feature_of_interest_ids_from_data_collections)
    return list(set(feature_of_interest_ids))

def get_registered_instrument_types():
    # Get Instrument Type URLs from all Instruments
    types_from_instruments = list(map(extract_localid_from_xlink_href, list(Instrument.objects.distinct_instrument_type_urls())))
    # Get Instrument Type URLs from all Data Collections
    data_collections = DataCollection.objects.all()
    instrument_type_urls_from_data_collections = get_distinct_instrument_type_urls_from_data_collections(data_collections)
    types_from_data_collections = list(map(extract_localid_from_xlink_href, instrument_type_urls_from_data_collections))
    # Join the two lists
    all_registered_instrument_types = list(set(types_from_instruments + types_from_data_collections))
    return all_registered_instrument_types

def get_registered_computation_types():
    # Get Computation Type URLs from all Computation Capabilities
    computation_capability_sets = ComputationCapabilities.objects.all()
    computation_type_urls_from_computation_capability_sets = get_distinct_computation_type_urls_from_computation_capability_sets(computation_capability_sets)
    types_from_computation_capability_sets = list(map(extract_localid_from_xlink_href, computation_type_urls_from_computation_capability_sets))
    # Get Computation Type URLs from all Data Collections
    data_collections = DataCollection.objects.all()
    computation_type_urls_from_data_collections = get_distinct_computation_type_urls_from_data_collections(data_collections)
    types_from_data_collections = list(map(extract_localid_from_xlink_href, computation_type_urls_from_data_collections))
    # Join the two lists
    all_registered_computation_types = list(set(types_from_computation_capability_sets + types_from_data_collections))
    return all_registered_computation_types

def get_registered_annotation_types():
    # Get Annotation Type URLs from all Data Collections
    data_collections = DataCollection.objects.all()
    annotation_type_urls_from_data_collections = get_distinct_annotation_type_urls_from_data_collections(data_collections)
    all_registered_annotation_types = list(map(extract_localid_from_xlink_href, annotation_type_urls_from_data_collections))
    return all_registered_annotation_types

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

def get_parents_of_registered_ontology_terms(ontology_term_ids, ontology_component, parent_node_ids, g=None):
    if g is None:
        g = get_graph_of_pithia_ontology_component(ontology_component)
    for id in ontology_term_ids:
        parent_node_ids_of_id = get_parent_node_ids_of_node_id(id, ontology_component, [], g)
        if len(parent_node_ids_of_id) > 0:
            parent_node_ids.extend(parent_node_ids_of_id)
            parent_node_ids = get_parents_of_registered_ontology_terms(parent_node_ids_of_id, ontology_component, parent_node_ids, g=g)
    return parent_node_ids