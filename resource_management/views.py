from django.shortcuts import render
from search.helpers import remove_underscore_from_id_attribute, get_view_helper_variables_by_url_namespace

# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': 'Manage Resources'
    })

def list_resources_of_type(request):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resources_list = list(view_helper_vars['mongodb_model'].find({}))
    resources_list = list(map(remove_underscore_from_id_attribute, resources_list))
    return render(request, 'resource_management/list_resources_of_type.html', {
        'title': view_helper_vars["resource_type_plural"],
        'breadcrumb_item_list_resources_of_type_text': view_helper_vars["resource_type_plural"],
        'resource_type_plural': view_helper_vars['resource_type_plural'],
        'url_namespace': url_namespace,
        'resources_list': resources_list
    })

def upload_new_file_for_resource(request):
    return render(request, 'resource_management/index.html', {
        'title': 'Upload new file for resource'
    })

def delete_resource(request):
    return render(request, 'resource_management/index.html', {
        'title': ''
    })