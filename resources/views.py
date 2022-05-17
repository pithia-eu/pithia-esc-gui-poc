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

def detail(request, resource_collection_name, namespace, local_id):
    resource = db[resource_collection_name].find_one({
        'identifier.pithia:Identifier.localID': local_id,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    return render(request, 'resources/detail.html', {
        'resource_collection_name': resource_collection_name,
        'resource': resource
    })