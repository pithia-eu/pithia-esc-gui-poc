from django.shortcuts import render
from mongodb import db

# Create your views here.
def index(request):
    return render(request, 'resources/index.html', {})

def list_resource_namespaces(request, resource_collection_name):
    namespaces = list(db[resource_collection_name].find({}).distinct('identifier.pithia:Identifier.namespace'))
    return render(request, 'resources/list_resource_namespaces.html', {
        'resource_collection_name': resource_collection_name,
        'namespaces': namespaces,
    })

def list_resources_in_namespace(request, resource_collection_name, namespace):
    resources_list = list(db[resource_collection_name].find({
        'identifier.pithia:Identifier.namespace': namespace
    }))
    return render(request, 'resources/list_resources_in_namespace.html', {
        'namespace': namespace,
        'resource_collection_name': resource_collection_name,
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

def detail(request, resource_collection_name, namespace, local_id):
    resource = db[resource_collection_name].find_one({
        'identifier.pithia:Identifier.localID': local_id,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    resource_flattened = flatten(resource)
    return render(request, 'resources/detail.html', {
        'resource_collection_name': resource_collection_name,
        'resource': resource,
        'resource_flattened': resource_flattened
    })