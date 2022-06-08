from mongodb import db
from search.ontology_helpers import get_observed_property_hrefs_from_features_of_interest
from .helpers import convert_list_to_regex_list, map_ontology_components_to_local_ids

def find_matching_observation_collections(request):
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
        additional_observed_properties = get_observed_property_hrefs_from_features_of_interest(request.session['features_of_interest'])
        observed_properties += additional_observed_properties
        observed_properties = list(set(observed_properties))

    # Process is:
    # Features of interest map to observed properties
    # Observed properties map to acquisition and computations
    # Acquisition/Computation maps to
    # Process maps to
    # Observation Collection, which is what we want

    # Fetch Instruments
    instruments = list(db['instruments'].find({
        'type.@xlink:href': {
            '$in': instrument_types
        }
    }))
    instrument_localids = [i['identifier']['pithia:Identifier']['localID'] for i in instruments]

    # Fetch Acquisitions/Computations
    acquisitions = list(db['acquisitions'].find({
        '$or': [
            {
                'capability': {
                    '$elemMatch': {
                        'pithia:processCapability.observedProperty.@xlink:href': {
                            '$in': observed_properties
                        }
                    }
                }
            },
            {
                'instrument.@xlink:href': {
                    '$in': instrument_localids
                }
            }
        ]
    }))
    computations = list(db['computations'].find({
        '$or': [
            {
                'capability': {
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

    # Fetch Processes
    processes = list(db['processes'].find({
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
    return list(db['data-collections'].find({
        'om:procedure.@xlink:href': {
            '$in': convert_list_to_regex_list(map_ontology_components_to_local_ids(processes))
        }
    }))