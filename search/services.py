import re
from ontology.utils import (
    get_observed_property_urls_from_feature_of_interest_urls,
)

from .helpers import (
    convert_list_to_regex_list,
)

from common.constants import SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE
from common.models import (
    Acquisition,
    AcquisitionCapabilities,
    ComputationCapabilities,
    Computation,
    DataCollection,
    Instrument,
    Process,
)
from common.mongodb_models import (
    CurrentAcquisitionCapability,
    CurrentComputationCapability,
    CurrentInstrument,
)
BASE_ONTOLOGY_INSTRUMENT_TYPE_URL = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/instrumentType'
BASE_ONTOLOGY_COMPUTATION_TYPE_URL = f'{SPACE_PHYSICS_ONTOLOGY_SERVER_HTTPS_URL_BASE}/computationType'


# cc = computation capability

# Computation Capability Sets may make references to other Computation Capability Sets.
# This function ensures that, for example, if Computation A references Computation Capability Set A
# that the Computation Capability Sets that Computation Capability Set A references are
# also included in that reference.
def get_cc_set_localids_referencing_another_cc_set_localid(computation_capability_set_localid, cc_set_localid_set):
    cc_sets_referencing_cc_set_id = list(CurrentComputationCapability.find({
        'childComputation.@xlink:href': re.compile(computation_capability_set_localid)
    }))
    localids_from_cc_sets_referencing_cc_set_id = [cc_set['identifier']['PITHIA_Identifier']['localID'] for cc_set in cc_sets_referencing_cc_set_id]
    for cc_set_localid in localids_from_cc_sets_referencing_cc_set_id:
        if cc_set_localid not in cc_set_localid_set:
            cc_set_localid_set.add(cc_set_localid)
            get_cc_set_localids_referencing_another_cc_set_localid(cc_set_localid, cc_set_localid_set)

    return localids_from_cc_sets_referencing_cc_set_id

def find_instruments_by_instrument_types(types):
    return list(CurrentInstrument.find({
        'type.@xlink:href': {
            '$in': types
        }
    }))

def find_acquisition_capability_sets_by_instrument_localids(instrument_localids):
    return list(CurrentAcquisitionCapability.find({
        'capabilities': {
            '$exists': True
        },
        '$or': [
            {
                'instrumentModePair.InstrumentOperationalModePair.instrument.@xlink:href': {
                    '$in': instrument_localids
                }
            },
            {
                'instrumentModePair.InstrumentOperationalModePair.mode.@xlink:href': {
                    '$in': instrument_localids
                }
            },
        ]
    }))

def find_computation_capability_sets_by_computation_types(computation_types):
    return list(CurrentComputationCapability.find({
        'type.@xlink:href': {
            '$in': computation_types
        }
    }))

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
        computation_type_id = cc_set.computation_type_url.split('/')[-1]
        for url in observed_property_urls:
            # Map the Computation Type URLs of the Computation Capabilities
            # registration to each Observed Property URL of the Computation
            # Capabilities registration.
            observed_property_id = url.split('/')[-1]
            if observed_property_id not in computation_types_grouped_by_observed_property:
                computation_types_grouped_by_observed_property[observed_property_id] = []
            computation_types_grouped_by_observed_property[observed_property_id].append(f"computationType{computation_type_id}")
            computation_types_grouped_by_observed_property[observed_property_id] = list(set(computation_types_grouped_by_observed_property[observed_property_id]))

    return computation_types_grouped_by_observed_property

def get_observed_property_urls_from_instruments(instruments):
    instrument_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in instruments]
    instrument_localid_regex_list = convert_list_to_regex_list(instrument_localids)
    acquisition_capability_sets = find_acquisition_capability_sets_by_instrument_localids(instrument_localid_regex_list)
    process_capabilities_from_acquisition_capability_sets = [ac_set['capabilities']['processCapability'] for ac_set in acquisition_capability_sets]
    process_capabilities_from_acquisition_capability_sets_flattened = [item for sublist in process_capabilities_from_acquisition_capability_sets for item in sublist]
    observed_property_urls_from_acquisition_capability_sets = [pc['observedProperty']['@xlink:href'] for pc in process_capabilities_from_acquisition_capability_sets_flattened]
    return observed_property_urls_from_acquisition_capability_sets

def get_observed_property_urls_from_computation_capability_sets(computation_capability_sets):
    observed_property_urls_from_computation_capability_sets = []
    for cc_set in computation_capability_sets:
        if 'capabilities' in cc_set:
            observed_property_urls_from_computation_capability_sets.extend([pc['observedProperty']['@xlink:href'] for pc in cc_set['capabilities']['processCapability']])
    return list(set(observed_property_urls_from_computation_capability_sets))

def get_observed_property_urls_by_instrument_types(instrument_types):
    instrument_type_regex_list = convert_list_to_regex_list(instrument_types)
    instruments = find_instruments_by_instrument_types(instrument_type_regex_list)
    return get_observed_property_urls_from_instruments(instruments)

def get_observed_property_urls_by_computation_types(computation_types):
    regexes_of_computation_types = convert_list_to_regex_list(computation_types)
    computation_capability_sets = find_computation_capability_sets_by_computation_types(regexes_of_computation_types)
    cc_set_localids_referencing_other_cc_set_localids = []
    for cc_set in computation_capability_sets:
        cc_set_localids_referencing_other_cc_set_localids.extend(list(get_cc_set_localids_referencing_another_cc_set_localid(cc_set['identifier']['PITHIA_Identifier']['localID'], set())))
        cc_set_localids_referencing_other_cc_set_localids = list(set(cc_set_localids_referencing_other_cc_set_localids))
    regexes_of_cc_set_localids_referencing_other_cc_set_localids = convert_list_to_regex_list(cc_set_localids_referencing_other_cc_set_localids)
    ccs_referencing_cc = CurrentComputationCapability.find({
        'identifier.PITHIA_Identifier.localID': {
            '$in': regexes_of_cc_set_localids_referencing_other_cc_set_localids
        }
    })
    computation_capability_sets.extend(ccs_referencing_cc)
    return get_observed_property_urls_from_computation_capability_sets(computation_capability_sets)

def find_matching_data_collections(feature_of_interest_urls: list = [], instrument_type_urls: list = [], computation_type_urls: list = [], observed_property_urls: list = []):
    # observed_property_urls = [f'{BASE_ONTOLOGY_OBSERVED_PROPERTY_URL}/{op_localid}' for op_localid in request.session.get('observed_properties', [])]
    # instrument_type_urls = [f'{BASE_ONTOLOGY_INSTRUMENT_TYPE_URL}/{instrument_type_localid}' for instrument_type_localid in request.session.get('instrument_types', [])]
    # computation_type_urls = [f'{BASE_ONTOLOGY_COMPUTATION_TYPE_URL}/{computation_type_localid}' for computation_type_localid in request.session.get('computation_types', [])]
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