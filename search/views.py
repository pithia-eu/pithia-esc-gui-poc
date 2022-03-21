from django.http import HttpResponseRedirect
from django.shortcuts import render
from .helpers import convert_list_to_regex_list, ONTOLOGY_COMPONENT_ENUMS
from .ontology_helpers import nested_list_from_ontology_component
from .search_helpers import find_matching_observation_collections

def get_checkbox_tree_for_ontology_component(request, ontology_component):
    nested_list = nested_list_from_ontology_component(ontology_component)
    return render(request, 'search/ontology_tree_template_outer.html', {
        'ontology_component': nested_list,
        'ontology_component_name': ONTOLOGY_COMPONENT_ENUMS[ontology_component]
    })

def results(request):
    observation_collections = find_matching_observation_collections(request)

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
            'title': 'Search Models & Data Collections'
        })