from mongodb import db
from .helpers import convert_list_to_regex_list, map_ontology_components_to_local_ids

def find_matching_observation_collections(request):
    observed_properties = []
    if 'observed-properties' in request.GET:
        observed_properties = convert_list_to_regex_list(request.GET['observed-properties'].split(','))
    # Route is:
    # Acquisition/Computation maps to,
    # Process maps to,
    # Observation Collection, which is what we want.

    # Fetch Acquisitions/Computations
    acquisitions = list(db['acquisitions'].find({
        'capability': {
            '$elemMatch': {
                'pithia:processCapability.observedProperty.@xlink:href': {
                    '$in': observed_properties
                }
            }
        }
    }))
    computations = list(db['computations'].find({
        'capability': {
            '$elemMatch': {
                'observedProperty.@xlink:href': {
                    '$in': observed_properties
                }
            }
        }
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