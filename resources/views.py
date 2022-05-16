from django.shortcuts import render
from mongodb import db

# Create your views here.
def index(request):
    return render(request, 'resources/index.html', {})

def list_resource_namespaces(request, resources):
    namespaces = list(db[resources].find({}).distinct('identifier.pithia:Identifier.namespace'))
    return render(request, 'resources/list_resource_namespaces.html', {
        'resources': resources,
        'namespaces': namespaces,
    })

def list_resources_in_namespace(request, resources, namespace):
    resources_list = list(db[resources].find({
        'identifier.pithia:Identifier.namespace': namespace
    }))
    return render(request, 'resources/list_resources_in_namespace.html', {
        'namespace': namespace,
        'resources': resources,
        'resources_list': resources_list
    })

def detail(request, resources, namespace, local_id):
    resource = db[resources].find_one({
        'identifier.pithia:Identifier.localID': local_id,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    return render(request, 'resources/detail.html', {
        'resources': resources,
        'resource': resource
    })