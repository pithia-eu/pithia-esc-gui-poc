from django.http import HttpResponseRedirect
from django.shortcuts import render
from .ontology_helpers import nested_list_from_ontology_component
from utils import db
from pprint import pprint
import re
import json

PITHIA = 'https://vo.pithia.eu/ontology/2.2/observedProperty/'

def prefix_pithia_namespace_to_list_elems(list):
    list_with_prefixes = []
    for x in list:
        list_with_prefixes.append(f'{PITHIA}{x}')
    return list_with_prefixes

def convert_list_to_regex_list(list):
    return [re.compile(x) for x in list]

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
        observed_properties = nested_list_from_ontology_component('observedProperty')
        qualifiers = nested_list_from_ontology_component('qualifier')
        measurands = nested_list_from_ontology_component('measurand')
        phenomenons = nested_list_from_ontology_component('phenomenon')
        
        return render(request, 'search/index.html', {
            'title': 'Search Models/Datasets',
            'observed_properties': observed_properties,
            'qualifiers': qualifiers,
            'measurands': measurands,
            'phenomenons': phenomenons,
        })