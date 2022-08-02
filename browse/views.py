from register import mongodb_models
from django.shortcuts import render
from bson.objectid import ObjectId

from search.helpers import remove_underscore_from_id_attribute, get_view_helper_variables_by_url_namespace

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

def list_resources_of_type(request):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resources_list = list(view_helper_vars['mongodb_model'].find({}))
    resources_list = list(map(remove_underscore_from_id_attribute, resources_list))
    return render(request, 'browse/list_resources_of_type.html', {
        'title': view_helper_vars["resource_type_plural"],
        'breadcrumb_item_list_resources_of_type_text': view_helper_vars["resource_type_plural"],
        'resource_type_plural': view_helper_vars['resource_type_plural'],
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

def detail(request, resource_id):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resource = view_helper_vars['mongodb_model'].find_one({
        '_id': ObjectId(resource_id)
    })
    resource_flattened = flatten(resource)
    return render(request, 'browse/detail.html', {
        'breadcrumb_item_list_resources_of_type_text': f'{view_helper_vars["resource_type_plural"]}',
        'url_namespace': url_namespace,
        'resource': resource,
        'resource_flattened': resource_flattened
    })