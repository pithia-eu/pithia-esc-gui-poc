from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from bson.objectid import ObjectId
from search.helpers import remove_underscore_from_id_attribute, get_view_helper_variables_by_url_namespace

# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': 'Manage Resources'
    })

def list_resources_of_type(request):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resources_list = list(view_helper_vars['current_version_mongodb_model'].find({}))
    resources_list = list(map(remove_underscore_from_id_attribute, resources_list))
    return render(request, 'resource_management/list_resources_of_type.html', {
        'title': view_helper_vars["resource_type_plural"],
        'breadcrumb_item_list_resources_of_type_text': view_helper_vars["resource_type_plural"],
        'resource_type_plural': view_helper_vars['resource_type_plural'],
        'url_namespace': url_namespace,
        'resources_list': resources_list
    })

@require_http_methods(["GET", "POST"])
def update(request, resource_id):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resource_to_update = view_helper_vars['current_version_mongodb_model'].find_one({
        '_id': ObjectId(resource_id)
    })
    resource_name = resource_to_update['identifier']['pithia:Identifier']['localID']
    if 'name' in resource_to_update:
        resource_name = resource_to_update['name']
    return render(request, 'resource_management/update.html', {
        'title': f'Update a Resource',
        'breadcrumb_item_list_resources_of_type_text': view_helper_vars["resource_type_plural"],
        'url_namespace': url_namespace
    })

@require_POST
def delete(request, resource_id):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resource_to_delete = view_helper_vars['current_version_mongodb_model'].find_one({
        '_id': ObjectId(resource_id)
    })
    view_helper_vars['current_version_mongodb_model'].delete_one({
        '_id': ObjectId(resource_id)
    })
    view_helper_vars['resource_revision_mongodb_model'].delete_many({
        'identifier.PITHIA_Identifier.localID': resource_to_delete['identifier']['PITHIA_Identifier']['localID'],
        'identifier.PITHIA_Identifier.namespace': resource_to_delete['identifier']['PITHIA_Identifier']['namespace'],
    })
    return HttpResponseRedirect(reverse(f'{url_namespace}:list_resources_of_type'))