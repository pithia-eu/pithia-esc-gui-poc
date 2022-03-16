from django.http import HttpResponseRedirect
from django.shortcuts import render
from .ontology_helpers import nested_list_from_ontology_component
from utils import db


def index(request):
    if request.method == 'POST':
        observed_properties = request.POST.getlist('observed_properties')
        measurands = request.POST.getlist('measurands')
        qualifiers = request.POST.getlist('qualifiers')
        phenomenons = request.POST.getlist('phenomenons')
        # db.observation_collections.find()
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