import re
from ontology.utils import (
    get_observed_property_urls_from_feature_of_interest_urls,
)
from .helpers import (
    convert_list_to_regex_list,
)
from common.mongodb_models import (
    CurrentAcquisition,
    CurrentAcquisitionCapability,
    CurrentComputation,
    CurrentComputationCapability,
    CurrentDataCollection,
    CurrentInstrument,
    CurrentProcess
)

BASE_ONTOLOGY_URL = 'https://metadata.pithia.eu/ontology/2.2'
BASE_ONTOLOGY_OBSERVED_PROPERTY_URL = f'{BASE_ONTOLOGY_URL}/observedProperty'
BASE_ONTOLOGY_FEATURE_OF_INTEREST_URL = f'{BASE_ONTOLOGY_URL}/featureOfInterest'
BASE_ONTOLOGY_INSTRUMENT_TYPE_URL = f'{BASE_ONTOLOGY_URL}/instrumentType'
BASE_ONTOLOGY_COMPUTATION_TYPE_URL = f'{BASE_ONTOLOGY_URL}/computationType'

BASE_METADATA_URL = 'https://metadata.pithia.eu/resources/2.2'
BASE_INSTRUMENT_URL = f'{BASE_METADATA_URL}/instrument'
BASE_ACQUISITION_CAPABILITIES_URL = f'{BASE_METADATA_URL}/acquisitionCapabilities'
BASE_ACQUISITION_URL = f'{BASE_METADATA_URL}/acquisition'
BASE_COMPUTATION_CAPABILITIES_URL = f'{BASE_METADATA_URL}/computationCapabilities'
BASE_COMPUTATION_URL = f'{BASE_METADATA_URL}/computation'
BASE_PROCESS_URL = f'{BASE_METADATA_URL}/process'
BASE_DATA_COLLECTION_URL = f'{BASE_METADATA_URL}/collection'

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

def get_cc_set_urls_referencing_another_cc_set_url(computation_capability_set_url, cc_set_url_set):
    cc_sets_referencing_cc_set_url = list(CurrentComputationCapability.find({
        'childComputation.@xlink:href': computation_capability_set_url
    }))
    urls_from_cc_sets_referencing_cc_set_url = [create_metadata_url(BASE_COMPUTATION_CAPABILITIES_URL, cc_set) for cc_set in cc_sets_referencing_cc_set_url]
    for cc_set_url in urls_from_cc_sets_referencing_cc_set_url:
        if cc_set_url not in cc_set_url_set:
            cc_set_url_set.add(cc_set_url)
            get_cc_set_urls_referencing_another_cc_set_url(cc_set_url, cc_set_url_set)

    return urls_from_cc_sets_referencing_cc_set_url

def find_instruments_by_instrument_types(types):
    return list(CurrentInstrument.find({
        'type.@xlink:href': {
            '$in': types
        }
    }))

def find_instruments_by_instrument_type_urls(instrument_type_urls):
    return list(CurrentInstrument.find({
        'type.@xlink:href': {
            '$in': instrument_type_urls
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

def group_instrument_types_by_observed_property(instruments):
    instrument_types_grouped_by_observed_property = {}
    for i in instruments:
        observed_property_urls = get_observed_property_urls_from_instruments([i])
        for url in observed_property_urls:
            observed_property_id = url.split('/')[-1]
            if observed_property_id not in instrument_types_grouped_by_observed_property:
                instrument_types_grouped_by_observed_property[observed_property_id] = []
            instrument_types_grouped_by_observed_property[observed_property_id].append(f"instrumentType{i['type']['@xlink:href'].split('/')[-1]}")
            instrument_types_grouped_by_observed_property[observed_property_id] = list(set(instrument_types_grouped_by_observed_property[observed_property_id]))

    return instrument_types_grouped_by_observed_property

def group_computation_types_by_observed_property(computation_capability_sets):
    computation_types_grouped_by_observed_property = {}
    for cc_set in computation_capability_sets:
        observed_property_urls = get_observed_property_urls_from_computation_capability_sets([cc_set])
        try:
            computation_type_urls = [type['@xlink:href'] for type in cc_set['type']]
        except:
            pass
        try:
            computation_type_urls = [cc_set['type']['@xlink:href']]
        except:
            continue
        for url in observed_property_urls:
            observed_property_id = url.split('/')[-1]
            if observed_property_id not in computation_types_grouped_by_observed_property:
                computation_types_grouped_by_observed_property[observed_property_id] = []
            if 'type' not in cc_set:
                continue
            computation_types_grouped_by_observed_property[observed_property_id] = computation_types_grouped_by_observed_property[observed_property_id] + [f"computationType{url.split('/')[-1]}" for url in computation_type_urls]
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

def create_metadata_url(base_metadata_url, metadata_registration):
    namespace = metadata_registration['identifier']['PITHIA_Identifier']['namespace']
    localid = metadata_registration['identifier']['PITHIA_Identifier']['localID']
    return f'{base_metadata_url}/{namespace}/{localid}'

def find_matching_data_collections(request):
    observed_property_urls = []
    instrument_type_urls = []
    computation_type_urls = []
    features_of_interest_urls = []

    if 'observed_properties' in request.session:
        observed_property_urls = [f'{BASE_ONTOLOGY_OBSERVED_PROPERTY_URL}/{op_localid}' for op_localid in request.session['observed_properties']]

    if 'instrument_types' in request.session:
        instrument_type_urls = [f'{BASE_ONTOLOGY_INSTRUMENT_TYPE_URL}/{instrument_type_localid}' for instrument_type_localid in request.session['instrument_types']]

    if 'computation_types' in request.session:
        computation_type_urls = [f'{BASE_ONTOLOGY_COMPUTATION_TYPE_URL}/{computation_type_localid}' for computation_type_localid in request.session['computation_types']]

    if 'features_of_interest' in request.session:
        features_of_interest_urls = [f'{BASE_ONTOLOGY_FEATURE_OF_INTEREST_URL}/{feature_of_interest_localid}' for feature_of_interest_localid in request.session['features_of_interest']]
        additional_observed_property_urls = get_observed_property_urls_from_feature_of_interest_urls(features_of_interest_urls)
        observed_property_urls += additional_observed_property_urls
        observed_property_urls = list(set(observed_property_urls))

    # The way in which data collections are found goes according to the
    # project data model diagram.


    # Fetch Instruments
    instruments = find_instruments_by_instrument_type_urls(instrument_type_urls)
    instrument_urls = [create_metadata_url(BASE_INSTRUMENT_URL, i) for i in instruments]


    # Fetch Acquisition Capabilities/Computation Capabilities
    acquisition_capability_sets = []
    acquisition_capability_sets_query = None
    ac_observed_properties_query = {
        'capabilities.processCapability': {
            '$elemMatch': {
                'observedProperty.@xlink:href': {
                    '$in': observed_property_urls
                }
            }
        }
    }
    ac_instruments_query = {
        'instrumentModePair.InstrumentOperationalModePair.instrument.@xlink:href': {
            '$in': instrument_urls
        }
    }
    if len(observed_property_urls) > 0 and len(instrument_urls) > 0:
        acquisition_capability_sets_query = {
            '$and': [
                ac_observed_properties_query,
                ac_instruments_query,
            ]
        }
    elif len(observed_property_urls) > 0:
        acquisition_capability_sets_query = ac_observed_properties_query
    elif len(instrument_urls) > 0:
        acquisition_capability_sets_query = ac_instruments_query
    
    if acquisition_capability_sets_query is not None:
        acquisition_capability_sets = list(CurrentAcquisitionCapability.find(acquisition_capability_sets_query))
    acquisition_capability_set_urls = [create_metadata_url(BASE_ACQUISITION_CAPABILITIES_URL, ac) for ac in acquisition_capability_sets]

    computation_capability_sets = []
    computation_capability_sets_query = None
    cc_observed_properties_query = {
        'capabilities.processCapability': {
            '$elemMatch': {
                'observedProperty.@xlink:href': {
                    '$in': observed_property_urls
                }
            }
        }
    }
    cc_types_query = {
        'type.@xlink:href': {
            '$in': computation_type_urls
        }
    }
    if len(observed_property_urls) > 0 and len(computation_type_urls) > 0:
        computation_capability_sets_query = {
            '$and': [
                cc_observed_properties_query,
                cc_types_query
            ]
        }
    elif len(observed_property_urls) > 0:
        computation_capability_sets_query = cc_observed_properties_query
    elif len(computation_type_urls) > 0:
        computation_capability_sets_query = cc_types_query
    if computation_capability_sets_query is not None:
        computation_capability_sets = list(CurrentComputationCapability.find(computation_capability_sets_query))
    
    cc_set_urls_referencing_other_cc_set_urls = []
    for cc_set in computation_capability_sets:
        cc_set_urls_referencing_other_cc_set_urls.extend(list(get_cc_set_urls_referencing_another_cc_set_url(create_metadata_url(BASE_COMPUTATION_CAPABILITIES_URL, cc_set), set())))
        cc_set_urls_referencing_other_cc_set_urls = list(set(cc_set_urls_referencing_other_cc_set_urls))

    computation_capability_set_urls = [create_metadata_url(BASE_COMPUTATION_CAPABILITIES_URL, cc) for cc in computation_capability_sets]
    computation_capability_set_urls.extend(cc_set_urls_referencing_other_cc_set_urls)
    computation_capability_set_urls = list(set(computation_capability_set_urls))


    # Fetch Acquisitions/Computations
    acquisitions = list(CurrentAcquisition.find({
        'capabilityLinks.capabilityLink': {
            '$elemMatch': {
                'acquisitionCapabilities.@xlink:href': {
                    '$in': acquisition_capability_set_urls
                }
            }
        }
    }))

    computations = list(CurrentComputation.find({
        'capabilityLinks.capabilityLink': {
            '$elemMatch': {
                'computationCapabilities.@xlink:href': {
                    '$in': computation_capability_set_urls
                }
            }
        }
    }))


    # Fetch Processes
    processes = []
    processes_query = None
    process_acquisitions_query = {
        'acquisitionComponent': {
            '$elemMatch': {
                '@xlink:href': {
                    '$in': [create_metadata_url(BASE_ACQUISITION_URL, a) for a in acquisitions]
                }
            }
        }
    }
    process_computations_query = {
        'computationComponent': {
            '$elemMatch': {
                '@xlink:href': {
                    '$in': [create_metadata_url(BASE_COMPUTATION_URL, c) for c in computations]
                }
            }
        }
    }
    if len(acquisitions) > 0 and len(computations) > 0:
        processes_query = {
            '$or': [
                process_acquisitions_query,
                process_computations_query,
            ]
        }
    elif len(acquisitions) > 0:
        processes_query = process_acquisitions_query
    elif len(computations) > 0:
        processes_query = process_computations_query
    if processes_query is not None:
        processes = list(CurrentProcess.find(processes_query))


    # Fetch Data Collections
    data_collections = []
    data_collections_query = {
        '$or': [
            {
                'type.@xlink:href': {
                    '$in': computation_type_urls
                }
            },
            {
                'type.@xlink:href': {
                    '$in': instrument_type_urls
                }
            }
        ]
    }
    dc_features_of_interest_query = {
        'om:featureOfInterest.FeatureOfInterest.namedRegion': {
            '$elemMatch': {
                '@xlink:href': {
                    '$in': features_of_interest_urls
                }
            }
        }
    }
    dc_processes_query = {
        'om:procedure.@xlink:href': {
            '$in': [create_metadata_url(BASE_PROCESS_URL, p) for p in processes]
        }
    }
    if len(features_of_interest_urls) > 0 and len(processes) > 0:
        data_collections_query['$or'].append(dc_processes_query)
        data_collections_query['$or'].append(dc_features_of_interest_query)
    elif len(features_of_interest_urls) > 0:
        data_collections_query['$or'].append(dc_features_of_interest_query)
    elif len(processes) > 0:
        data_collections_query['$or'].append(dc_processes_query)
    
    data_collections = list(CurrentDataCollection.find(data_collections_query))

    return data_collections