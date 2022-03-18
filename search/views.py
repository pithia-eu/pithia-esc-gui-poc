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

def get_checkbox_tree_for_ontology_component(request, ontology_component):
    nested_list = nested_list_from_ontology_component(ontology_component)
    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': nested_list,
        'ontology_component_name': ONTOLOGY_COMPONENT_ENUMS[ontology_component]
    })

def index(request):
    if request.method == 'POST':
        observed_properties = convert_list_to_regex_list(request.POST.getlist('observed_properties'))
        measurands = convert_list_to_regex_list(request.POST.getlist('measurands'))
        qualifiers = convert_list_to_regex_list(request.POST.getlist('qualifiers'))
        phenomenons = convert_list_to_regex_list(request.POST.getlist('phenomenons'))
        
        acquisitions = list(db['acquisitions'].find({
            'capability': {
                '$elemMatch': {
                    'observedProperty.@xlink:href': {
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
        for c in computations:
            if 'name' in list(c.keys()):
                print(f'name: {c["name"]}')
        return HttpResponseRedirect('/search/')
    else:
        return render(request, 'search/index.html', {
            'title': 'Search Models/Data Collections'
        })