from django.shortcuts import render
from mongodb import db

# Create your views here.
def index(request):
    return render(request, 'resources/index.html', {})

def detail(request, namespace, localID):
    resource = db['observation_collections'].find_one({
        'identifier.pithia:Identifier.localID': localID,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    return render(request, 'resources/detail.html', {
        'resource': resource
    })