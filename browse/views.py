from common import mongodb_models
from django.shortcuts import render
from bson.objectid import ObjectId

from search.helpers import remove_underscore_from_id_attribute
from search.ontology_helpers import create_dictionary_from_pithia_ontology_component
from search.views import get_parents_of_registered_ontology_terms, get_registered_computation_types, get_registered_features_of_interest, get_registered_instrument_types, get_registered_measurands, get_registered_observed_properties, get_registered_phenomenons

# Create your views here.
def index(request):
    return render(request, 'browse/index.html', {
        'title': 'Browse'
    })

def resources(request):
    return render(request, 'browse/resources.html', {
        'title': 'Browse Resources'
    })

def schemas(request):
    return render(request, 'browse/schemas.html', {
        'title': 'Browse Schemas'
    })

def ontology(request):
    return render(request, 'browse/ontology.html', {
        'title': 'Browse PITHIA Ontology'
    })

def _split_camel_case(string):
    current_string = string[0]
    string_split = []
    for c in string[1:]:
        if c.isupper():
            string_split.append(current_string)
            current_string = c
        else:
            current_string += c
    string_split.append(current_string)
    return string_split

def ontology_category_terms_list(request, category):
    title = ' '.join(_split_camel_case(category)).title()
    if category.lower() == 'crs':
        title = 'Co-ordinate Reference System'
    return render(request, 'browse/ontology_category_terms_list.html', {
        'category': category,
        'title': title
    })

def ontology_category_terms_list_only(request, category):
    dictionary = create_dictionary_from_pithia_ontology_component(category)
    registered_ontology_terms = []
    parents_of_registered_ontology_terms = []
    if category.lower() == 'observedproperty':
        registered_ontology_terms = get_registered_observed_properties()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'featureofinterest':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_features_of_interest(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'instrumenttype':
        registered_ontology_terms = get_registered_instrument_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'computationtype':
        registered_ontology_terms = get_registered_computation_types()
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'phenomenon':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_phenomenons(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    elif category.lower() == 'measurand':
        registered_observed_property_ids = get_registered_observed_properties()
        registered_ontology_terms = get_registered_measurands(registered_observed_property_ids)
        parents_of_registered_ontology_terms = get_parents_of_registered_ontology_terms(registered_ontology_terms, category, None, [])
    return render(request, 'browse/ontology_tree_template_outer.html', {
        'category': dictionary,
        'registered_ontology_terms': registered_ontology_terms,
        'parents_of_registered_ontology_terms': parents_of_registered_ontology_terms,
    })

def ontology_term_detail(request, category, term_id):
    return render(request, 'browse/ontology_term_detail.html', {
        'title': 'Ontology Term'
    })

def list_resources_of_type(request, resource_mongodb_model, resource_type_plural, resource_detail_view_name):
    url_namespace = request.resolver_match.namespace
    resources_list = list(resource_mongodb_model.find({}))
    resources_list = list(map(remove_underscore_from_id_attribute, resources_list))
    return render(request, 'browse/list_resources_of_type.html', {
        'title': resource_type_plural,
        'breadcrumb_item_list_resources_of_type_text': resource_type_plural,
        'resource_type_plural': resource_type_plural,
        'resource_detail_view_name': resource_detail_view_name,
        'url_namespace': url_namespace,
        'resources_list': resources_list
    })

def list_organisations(request):
    return list_resources_of_type(request, mongodb_models.CurrentOrganisation, 'Organisations', 'browse:organisation_detail')

def list_individuals(request):
    return list_resources_of_type(request, mongodb_models.CurrentIndividual, 'Individuals', 'browse:individual_detail')

def list_projects(request):
    return list_resources_of_type(request, mongodb_models.CurrentProject, 'Projects', 'browse:project_detail')

def list_platforms(request):
    return list_resources_of_type(request, mongodb_models.CurrentPlatform, 'Platforms', 'browse:platform_detail')

def list_instruments(request):
    return list_resources_of_type(request, mongodb_models.CurrentInstrument, 'Instruments', 'browse:instrument_detail')

def list_operations(request):
    return list_resources_of_type(request, mongodb_models.CurrentOperation, 'Operations', 'browse:operation_detail')

def list_acquisitions(request):
    return list_resources_of_type(request, mongodb_models.CurrentAcquisition, 'Acquisitions', 'browse:acquisition_detail')

def list_computations(request):
    return list_resources_of_type(request, mongodb_models.CurrentComputation, 'Computations', 'browse:computation_detail')

def list_processes(request):
    return list_resources_of_type(request, mongodb_models.CurrentProcess, 'Processes', 'browse:process_detail')

def list_data_collections(request):
    return list_resources_of_type(request, mongodb_models.CurrentDataCollection, 'Data Collections', 'browse:data_collection_detail')

def flatten(d):
    out = {}
    for key, value in d.items():
        if isinstance(value, dict):
            value = [value]
        if isinstance(value, list):
            for subdict in value:
                deeper = flatten(subdict).items()
                out.update({
                    key + '.' + key2: value2 for key2, value2 in deeper
                })
        else:
            out[key] = value
    return out

def resource_detail(request, resource_id, resource_mongodb_model, resource_type_plural, list_resources_of_type_view_name):
    resource = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_flattened = flatten(resource)
    title = resource['identifier']['PITHIA_Identifier']['localID']
    if 'name' in resource:
        title = resource['name']
    return render(request, 'browse/detail.html', {
        'title': title,
        'breadcrumb_item_list_resources_of_type_text': f'{resource_type_plural}',
        'resource': resource,
        'resource_flattened': resource_flattened,
        'list_resources_of_type_view_name': list_resources_of_type_view_name
    })

def organisation_detail(request, organisation_id):
    return resource_detail(request, organisation_id, mongodb_models.CurrentOrganisation, 'Organisations', 'browse:list_organisations')

def individual_detail(request, individual_id):
    return resource_detail(request, individual_id, mongodb_models.CurrentIndividual, 'Individuals', 'browse:list_individuals')

def project_detail(request, project_id):
    return resource_detail(request, project_id, mongodb_models.CurrentProject, 'Projects', 'browse:list_projects')

def platform_detail(request, platform_id):
    return resource_detail(request, platform_id, mongodb_models.CurrentPlatform, 'Platforms', 'browse:list_platforms')

def instrument_detail(request, instrument_id):
    return resource_detail(request, instrument_id, mongodb_models.CurrentInstrument, 'Instruments', 'browse:list_instruments')

def operation_detail(request, operation_id):
    return resource_detail(request, operation_id, mongodb_models.CurrentOperation, 'Operations', 'browse:list_operations')

def acquisition_detail(request, acquisition_id):
    return resource_detail(request, acquisition_id, mongodb_models.CurrentAcquisition, 'Acquisitions', 'browse:list_acquisitions')

def computation_detail(request, computation_id):
    return resource_detail(request, computation_id, mongodb_models.CurrentComputation, 'Computations', 'browse:list_computations')

def process_detail(request, process_id):
    return resource_detail(request, process_id, mongodb_models.CurrentProcess, 'Processes', 'browse:list_processes')

def data_collection_detail(request, data_collection_id):
    return resource_detail(request, data_collection_id, mongodb_models.CurrentDataCollection, 'Data Collections', 'browse:list_data_collections')