from django.shortcuts import render
from .ontology_helpers import nested_list_from_ontology_component


def index(request):
    if request.method == 'POST':
        weg = ''
    else:
        observed_properties = nested_list_from_ontology_component('observedProperty')
        qualifiers = nested_list_from_ontology_component('qualifier')
        measurands = nested_list_from_ontology_component('measurand')
        phenomenons = nested_list_from_ontology_component('phenomenon')
        
        return render(request, 'search/index.html', {
            'observed_properties': observed_properties,
            'qualifiers': qualifiers,
            'measurands': measurands,
            'phenomenons': phenomenons,
        })