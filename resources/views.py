from django.shortcuts import render
from mongodb import db

# Create your views here.
def index(request):
    namespaces = list(db['resources'].find({
        'dataModelType': 'observationcollection',
    }).distinct('content.identifier.pithia:Identifier.namespace'))
    return render(request, 'resources/index.html', {
        'namespaces': namespaces
    })

def list_by_namespace(request, namespace):
    resources = list(db['resources'].find({
        'dataModelType': 'observationcollection',
        'content.identifier.pithia:Identifier.namespace': namespace
    }))
    return render(request, 'resources/list_by_namespace.html', {
        'namespace': namespace,
        'resources': resources
    })

def detail(request, namespace, local_id):
    resource = db['resources'].find_one({
        'dataModelType': 'observationcollection',
        'content.identifier.pithia:Identifier.localID': local_id,
        'content.identifier.pithia:Identifier.namespace': namespace,
    })
    return render(request, 'resources/detail.html', {
        'resource': resource
    })