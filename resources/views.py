from django.shortcuts import render
from mongodb import db
from register.resource_metadata_upload import ORGANISATION, current_resource_version_collection_names

# Create your views here.
def index(request):
    return render(request, 'resources/index.html', {
        'title': 'Resources'
    })

def list_resource_namespaces(request):
    url_namespace = request.resolver_match.namespace
    resource_type = ORGANISATION
    current_organisation_version_collection_name = current_resource_version_collection_names.get(ORGANISATION, None)
    namespaces = list(db[current_organisation_version_collection_name].find({}).distinct('identifier.pithia:Identifier.namespace'))
    return render(request, 'resources/list_resource_namespaces.html', {
        'title': None,
        'resource_type': resource_type,
        'url_namespace': url_namespace,
        'namespaces': namespaces,
    })

def list_resources_in_namespace(request, namespace):
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

def detail(request, namespace, local_id):
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