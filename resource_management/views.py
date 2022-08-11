from pyexpat import ExpatError
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from bson.objectid import ObjectId
from register.register import move_current_version_of_resource_to_revisions, register_metadata_xml_file
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from resource_management.forms import UploadUpdatedFileForm
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
    redirect_url = reverse(f'{url_namespace}:list_resources_of_type')
    if request.method == 'POST':
        view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
        # Form validation
        form = UploadUpdatedFileForm(request.POST, request.FILES)
        xml_file = request.FILES['file']
        if form.is_valid():
            # XML should have already been validated at
            # the template, but do it again just to be
            # safe.
            validation_results = view_helper_vars['validation_function'](xml_file)
            if True:
                try:
                    converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
                    converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
                    move_current_version_of_resource_to_revisions(converted_xml_file['identifier']['pithia:Identifier'], view_helper_vars['current_version_mongodb_model'], view_helper_vars['resource_revision_mongodb_model'])
                    register_metadata_xml_file(xml_file, view_helper_vars['current_version_mongodb_model'], view_helper_vars['conversion_validation_and_fixing_function'])
                except ExpatError as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An error occurred whilst parsing the XML.')
                except BaseException as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An unexpected error occurred.')
        return HttpResponseRedirect(redirect_url)
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    resource_to_update = view_helper_vars['current_version_mongodb_model'].find_one({
        '_id': ObjectId(resource_id)
    })
    resource_to_update_name = resource_to_update['identifier']['pithia:Identifier']['localID']
    if 'name' in resource_to_update:
        resource_to_update_name = resource_to_update['name']
    a_or_an = 'a'
    if view_helper_vars["resource_type"].lower().startswith(('a', 'e', 'i',  'o', 'u' )):
        a_or_an = 'an'
    return render(request, 'resource_management/update.html', {
        'title': f'Update {a_or_an} {view_helper_vars["resource_type"].title()}',
        'breadcrumb_item_list_resources_of_type_text': view_helper_vars["resource_type_plural"],
        'url_namespace': url_namespace,
        'form': UploadUpdatedFileForm(),
        'resource_id': resource_id,
        'resource_to_update_name': resource_to_update_name,
        'validation_url': view_helper_vars['validation_url'],
    })

@require_POST
def delete(request, resource_id):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = get_view_helper_variables_by_url_namespace(url_namespace)
    
    # Find the resource to delete, so it can be referenced later when deleting from
    # the revisions collection
    resource_to_delete = view_helper_vars['current_version_mongodb_model'].find_one({
        '_id': ObjectId(resource_id)
    })

    # Delete the current version of the resource
    view_helper_vars['current_version_mongodb_model'].delete_one({
        '_id': ObjectId(resource_id)
    })

    # Delete revisions stored as version control
    view_helper_vars['resource_revision_mongodb_model'].delete_many({
        'identifier.pithia:Identifier.localID': resource_to_delete['identifier']['pithia:Identifier']['localID'],
        'identifier.pithia:Identifier.namespace': resource_to_delete['identifier']['pithia:Identifier']['namespace'],
    })

    # Delete resources that are referencing the resource to be deleted. These should not
    # be able to exist without the resource being deleted.
    

    return HttpResponseRedirect(reverse(f'{url_namespace}:list_resources_of_type'))