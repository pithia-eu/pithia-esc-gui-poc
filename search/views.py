from django.http import HttpResponseRedirect
from django.shortcuts import render
from .ontology_helpers import nested_list_from_ontology_component
from utils import db
import re

ONTOLOGY_COMPONENT_ENUMS = {
    'measurand': 'measurands',
    'observedProperty': 'observed_properties',
    'phenomenon': 'phenomenons',
    'qualifier': 'qualifiers'
}

def convert_list_to_regex_list(list):
    return [re.compile(x) for x in list]

def map_ontology_components_to_local_ids(list):
    local_ids_list = []
    for x in list:
        local_ids_list.append(x['identifier']['pithia:Identifier']['localID'])
    return local_ids_list

def get_checkbox_tree_for_ontology_component(request, ontology_component):
    nested_list = nested_list_from_ontology_component(ontology_component)
    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': nested_list,
        'ontology_component_name': ONTOLOGY_COMPONENT_ENUMS[ontology_component]
    })

def results(request):
    observed_properties = []
    if 'observed_properties' in request.GET:
        observed_properties = convert_list_to_regex_list(request.GET['observed_properties'].split(','))
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
    observation_collections = list(db['observation_collections'].find({
        'om:procedure.@xlink:href': {
            '$in': convert_list_to_regex_list(map_ontology_components_to_local_ids(processes))
        }
    }))

    return render(request, 'search/results.html', {
        'results': observation_collections
    })

def index(request):
    if request.method == 'POST':
        observed_properties = request.POST.getlist('observed_properties')
        measurands = convert_list_to_regex_list(request.POST.getlist('measurands'))
        qualifiers = convert_list_to_regex_list(request.POST.getlist('qualifiers'))
        phenomenons = convert_list_to_regex_list(request.POST.getlist('phenomenons'))
        query_string = '?'
        if len(observed_properties) > 0:
            query_string += f'observed_properties={",".join(observed_properties)}'
        if query_string == '?':
            query_string = ''

        return HttpResponseRedirect('/search/results/' + query_string)
    else:
        return render(request, 'search/index.html', {
            'title': 'Search Models/Data Collections'
        })