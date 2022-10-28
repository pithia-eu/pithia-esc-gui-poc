from mongodb import db
from search.ontology_helpers import get_localid_from_ontology_node_uri, get_observed_property_hrefs_from_features_of_interest
from .helpers import convert_list_to_regex_list, map_ontology_components_to_local_ids
from common.mongodb_models import CurrentAcquisition, CurrentAcquisitionCapability, CurrentComputation, CurrentComputationCapability, CurrentDataCollection, CurrentInstrument, CurrentProcess

def find_matching_data_collections(request):
    observed_properties = []
    instrument_types = []
    computation_types = []

    if 'observed_properties' in request.session:
        observed_properties = convert_list_to_regex_list(request.session['observed_properties'])

    if 'instrument_types' in request.session:
        instrument_types = convert_list_to_regex_list(request.session['instrument_types'])

    if 'computation_types' in request.session:
        computation_types = convert_list_to_regex_list(request.session['computation_types'])

    if 'features_of_interest' in request.session:
        additional_observed_property_hrefs = get_observed_property_hrefs_from_features_of_interest(request.session['features_of_interest'])
        additional_observed_properties = convert_list_to_regex_list(list(map(get_localid_from_ontology_node_uri, additional_observed_property_hrefs)))
        observed_properties += additional_observed_properties
        observed_properties = list(set(observed_properties))

    # The way in which data collections are found goes according to the
    # project data model diagram.

    # Fetch Instruments
    instruments = list(CurrentInstrument.find({
        'type.@xlink:href': {
            '$in': instrument_types
        }
    }))
    instrument_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in instruments]

    # Fetch Acquisition Capabilities/Computation Capabilities
    acquisition_capabilities = list(CurrentAcquisitionCapability.find({
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
    acquisition_capability_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in acquisition_capabilities]

    computation_capabilities = list(CurrentComputationCapability.find({
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
    computation_capability_localids = [i['identifier']['PITHIA_Identifier']['localID'] for i in computation_capabilities]

    # Fetch Acquisitions/Computations
    acquisitions = list(CurrentAcquisition.find({
        'capabilityLinks.capabilityLink': {
            '$elemMatch': {
                'acquisitionCapabilities.@xlink:href': {
                    '$in': acquisition_capability_localids
                }
            }
        }
    }))

    computations = list(CurrentComputation.find({
        'capabilityLinks.capabilityLink': {
            '$elemMatch': {
                'computationCapabilities.@xlink:href': {
                    '$in': computation_capability_localids
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
        'om:procedure.@xlink:href': {
            '$in': convert_list_to_regex_list(map_ontology_components_to_local_ids(processes))
        }
    }))