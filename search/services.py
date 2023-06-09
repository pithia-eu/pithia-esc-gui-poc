import re
from common.constants import (
    COMPUTATION_TYPE_URL_BASE,
    FEATURE_OF_INTEREST_URL_BASE,
    INSTRUMENT_TYPE_URL_BASE,
    OBSERVED_PROPERTY_URL_BASE,
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
from ontology.utils import (
    get_observed_property_urls_from_feature_of_interest_urls,
)


def find_matching_data_collections(feature_of_interest_urls: list = [], instrument_type_urls: list = [], computation_type_urls: list = [], observed_property_urls: list = []):
    # observed_property_urls = [f'{BASE_ONTOLOGY_OBSERVED_PROPERTY_URL}/{op_localid}' for op_localid in request.session.get('observed_properties', [])]
    # instrument_type_urls = [f'{INSTRUMENT_TYPE_URL_BASE}/{instrument_type_localid}' for instrument_type_localid in request.session.get('instrument_types', [])]
    # computation_type_urls = [f'{COMPUTATION_TYPE_URL_BASE}/{computation_type_localid}' for computation_type_localid in request.session.get('computation_types', [])]
    # feature_of_interest_urls = [f'{BASE_ONTOLOGY_FEATURE_OF_INTEREST_URL}/{feature_of_interest_localid}' for feature_of_interest_localid in request.session.get('features_of_interest', [])]

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
    distinct_instrument_type_urls = [url for dc in data_collections for url in dc.type_urls if re.match(f'^{INSTRUMENT_TYPE_URL_BASE}', url)]
    return distinct_instrument_type_urls

def get_distinct_computation_type_urls_from_data_collections(data_collections):
    distinct_model_urls = [url for dc in data_collections for url in dc.type_urls if re.match(f'^{COMPUTATION_TYPE_URL_BASE}', url)]
    return distinct_model_urls