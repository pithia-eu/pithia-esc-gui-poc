from django.shortcuts import render
from mongodb import db

# Create your views here.
def index(request):
    namespaces = list(db['observation_collections'].distinct('identifier.pithia:Identifier.namespace'))
    return render(request, 'resources/index.html', {
        'namespaces': namespaces
    })

def list_by_namespace(request, namespace):
    resources = list(db['observation_collections'].find({
        'identifier.pithia:Identifier.namespace': namespace
    }))
    return render(request, 'resources/list_by_namespace.html', {
        'resources': resources
    })

def detail(request, namespace, localID):
    resource = db['observation_collections'].find_one({
        'identifier.pithia:Identifier.localID': localID,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    return render(request, 'resources/detail.html', {
        'resource': resource
    })