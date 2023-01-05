import re
from mongodb import db
from utils.ontology_helpers import get_localid_from_ontology_node_iri, get_observed_property_hrefs_from_features_of_interest
from .helpers import convert_list_to_regex_list, map_ontology_components_to_local_ids
from common.mongodb_models import CurrentAcquisition, CurrentAcquisitionCapability, CurrentComputation, CurrentComputationCapability, CurrentDataCollection, CurrentInstrument, CurrentProcess


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
        for url in observed_property_urls:
            observed_property_id = url.split('/')[-1]
            if observed_property_id not in computation_types_grouped_by_observed_property:
                computation_types_grouped_by_observed_property[observed_property_id] = []
            if 'type' not in cc_set:
                continue
            computation_types_grouped_by_observed_property[observed_property_id].append(f"computationType{cc_set['type']['@xlink:href'].split('/')[-1]}")
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

def find_matching_data_collections(request):
    observed_properties = []
    instrument_types = []
    computation_types = []
    features_of_interest = []

    if 'observed_properties' in request.session:
        observed_properties = convert_list_to_regex_list(request.session['observed_properties'])

    if 'instrument_types' in request.session:
        instrument_types = convert_list_to_regex_list(request.session['instrument_types'])

    if 'computation_types' in request.session:
        computation_types = convert_list_to_regex_list(request.session['computation_types'])

    if 'features_of_interest' in request.session:
        features_of_interest = convert_list_to_regex_list(request.session['features_of_interest'])
        additional_observed_property_hrefs = get_observed_property_hrefs_from_features_of_interest(request.session['features_of_interest'])
        additional_observed_properties = convert_list_to_regex_list(list(map(get_localid_from_ontology_node_iri, additional_observed_property_hrefs)))
        observed_properties += additional_observed_properties
        observed_properties = list(set(observed_properties))

    # The way in which data collections are found goes according to the
    # project data model diagram.

    # Fetch Instruments
    instruments = find_instruments_by_instrument_types(instrument_types)
    instrument_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in instruments]
    instrument_localids = convert_list_to_regex_list(instrument_localids)

    # Fetch Acquisition Capabilities/Computation Capabilities
    acquisition_capability_sets = list(CurrentAcquisitionCapability.find({
        '$or': [
            {
                'capabilities.processCapability': {
                    '$elemMatch': {
                        'observedProperty.@xlink:href': {
                            '$in': observed_properties
                        }
                    }
                }
            },
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
    acquisition_capability_set_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in acquisition_capability_sets]
    acquisition_capability_set_localids = convert_list_to_regex_list(acquisition_capability_set_localids)

    computation_capability_sets = list(CurrentComputationCapability.find({
        '$or': [
            {
                'capabilities.processCapability': {
                    '$elemMatch': {
                        'observedProperty.@xlink:href': {
                            '$in': observed_properties
                        }
                    }
                }
            },
            {
                'type.@xlink:href': {
                    '$in': computation_types
                }
            }
        ]
    }))
    cc_set_localids_referencing_other_cc_set_localids = []
    for cc_set in computation_capability_sets:
        cc_set_localids_referencing_other_cc_set_localids.extend(list(get_cc_set_localids_referencing_another_cc_set_localid(cc_set['identifier']['PITHIA_Identifier']['localID'], set())))
        cc_set_localids_referencing_other_cc_set_localids = list(set(cc_set_localids_referencing_other_cc_set_localids))

    computation_capability_set_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in computation_capability_sets]
    computation_capability_set_localids.extend(cc_set_localids_referencing_other_cc_set_localids)
    computation_capability_set_localids = list(set(computation_capability_set_localids))
    computation_capability_set_localids = convert_list_to_regex_list(computation_capability_set_localids)

    # Fetch Acquisitions/Computations
    acquisitions = list(CurrentAcquisition.find({
        'capabilityLinks.capabilityLink': {
            '$elemMatch': {
                'acquisitionCapabilities.@xlink:href': {
                    '$in': acquisition_capability_set_localids
                }
            }
        }
    }))

    computations = list(CurrentComputation.find({
        'capabilityLinks.capabilityLink': {
            '$elemMatch': {
                'computationCapabilities.@xlink:href': {
                    '$in': computation_capability_set_localids
                }
            }
        }
    }))

    # Fetch Processes
    processes = list(CurrentProcess.find({
        '$or': [
            {
                'acquisitionComponent': {
                    '$elemMatch': {
                        '@xlink:href': {
                            '$in': convert_list_to_regex_list(map_ontology_components_to_local_ids(acquisitions))
                        }
                    }
                }
            },
            {
                'computationComponent': {
                    '$elemMatch': {
                        '@xlink:href': {
                            '$in': convert_list_to_regex_list(map_ontology_components_to_local_ids(computations))
                        }
                    }
                }
            },
        ]
    }))

    # Fetch Observation Collections
    return list(CurrentDataCollection.find({
        '$or': [
            {
                'om:procedure.@xlink:href': {
                    '$in': convert_list_to_regex_list(map_ontology_components_to_local_ids(processes))
                }
            },
            {
                'om:featureOfInterest.FeatureOfInterest.namedRegion': {
                    '$elemMatch': {
                        '@xlink:href': {
                            '$in': features_of_interest
                        }
                    }
                }
            }
        ]
    }))