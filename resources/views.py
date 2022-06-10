from django.shortcuts import render
from mongodb import db
from register.resource_metadata_upload import ACQUISITION, COMPUTATION, DATA_COLLECTION, INDIVIDUAL, INSTRUMENT, OPERATION, ORGANISATION, PLATFORM, PROCESS, PROJECT, current_resource_version_collection_names

def get_resource_type_by_url_namespace(url_namespace):
    if ORGANISATION in url_namespace:
        return ORGANISATION
    if INDIVIDUAL in url_namespace:
        return INDIVIDUAL
    if PROJECT in url_namespace:
        return PROJECT
    if PLATFORM in url_namespace:
        return PLATFORM
    if INSTRUMENT in url_namespace:
        return INSTRUMENT
    if OPERATION in url_namespace:
        return OPERATION
    if ACQUISITION in url_namespace:
        return ACQUISITION
    if COMPUTATION in url_namespace:
        return COMPUTATION
    if PROCESS in url_namespace:
        return PROCESS
    if DATA_COLLECTION in url_namespace:
        return DATA_COLLECTION
    return 'Unknown'

# Create your views here.
def index(request):
    return render(request, 'resources/index.html', {
        'title': 'Resources'
    })

def list_resource_namespaces(request):
    url_namespace = request.resolver_match.namespace
    resource_type = get_resource_type_by_url_namespace(url_namespace)
    current_resource_version_collection_name = current_resource_version_collection_names.get(resource_type, None)
    namespaces = list(db[current_resource_version_collection_name].find({}).distinct('identifier.pithia:Identifier.namespace'))
    title = f'{resource_type.capitalize()} Namespaces'
    if resource_type.lower() == 'data-collection':
        title = 'Data Collection Namespaces'
    return render(request, 'resources/list_resource_namespaces.html', {
        'title': title,
        'resource_type': resource_type,
        'url_namespace': url_namespace,
        'namespaces': namespaces,
    })

def list_resources_in_namespace(request, namespace):
    url_namespace = request.resolver_match.namespace
    resource_type = get_resource_type_by_url_namespace(url_namespace)
    current_resource_version_collection_name = current_resource_version_collection_names.get(resource_type, None)
    resources_list = list(db[current_resource_version_collection_name].find({
        'identifier.pithia:Identifier.namespace': namespace
    }))
    return render(request, 'resources/list_resources_in_namespace.html', {
        'namespace': namespace,
        'resource_type': resource_type,
        'url_namespace': url_namespace,
        'resources_list': resources_list
    })

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

def detail(request, namespace, local_id):
    url_namespace = request.resolver_match.namespace
    resource_type = get_resource_type_by_url_namespace(url_namespace)
    current_resource_version_collection_name = current_resource_version_collection_names.get(resource_type, None)
    resource = db[current_resource_version_collection_name].find_one({
        'identifier.pithia:Identifier.localID': local_id,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    resource_flattened = flatten(resource)
    return render(request, 'resources/detail.html', {
        'resource_type': resource_type,
        'url_namespace': url_namespace,
        'resource': resource,
        'resource_flattened': resource_flattened
    })