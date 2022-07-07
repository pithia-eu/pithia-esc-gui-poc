from register import mongodb_models
from django.shortcuts import render

def _get_view_helper_variables_by_url_namespace(url_namespace):
    mongodb_model = None
    resource_type = ''
    resource_type_plural = ''
    if 'organisation' in url_namespace:
        mongodb_model = mongodb_models.CurrentOrganisation
        resource_type = 'Organisation'
        resource_type_plural = 'Organisations'
    if 'individual' in url_namespace:
        mongodb_model = mongodb_models.CurrentIndividual
        resource_type = 'Individual'
        resource_type_plural = 'Individuals'
    if 'project' in url_namespace:
        mongodb_model = mongodb_models.CurrentProject
        resource_type = 'Project'
        resource_type_plural = 'Projects'
    if 'platform' in url_namespace:
        mongodb_model = mongodb_models.CurrentPlatform
        resource_type = 'Platform'
        resource_type_plural = 'Platforms'
    if 'instrument' in url_namespace:
        mongodb_model = mongodb_models.CurrentInstrument
        resource_type = 'Instrument'
        resource_type_plural = 'Instruments'
    if 'operation' in url_namespace:
        mongodb_model = mongodb_models.CurrentOperation
        resource_type = 'Operation'
        resource_type_plural = 'Operations'
    if 'acquisition' in url_namespace:
        mongodb_model = mongodb_models.CurrentAcquisition
        resource_type = 'Acquisition'
        resource_type_plural = 'Acquisitions'
    if 'computation' in url_namespace:
        mongodb_model = mongodb_models.CurrentComputation
        resource_type = 'Computation'
        resource_type_plural = 'Computations'
    if 'process' in url_namespace:
        mongodb_model = mongodb_models.CurrentProcess
        resource_type = 'Process'
        resource_type_plural = 'Processes'
    if 'data-collection' in url_namespace:
        mongodb_model = mongodb_models.CurrentDataCollection
        resource_type = 'Data Collection'
        resource_type_plural = 'Data Collections'
    return {
        'mongodb_model': mongodb_model,
        'resource_type': resource_type,
        'resource_type_plural': resource_type_plural,
    }

# Create your views here.
def index(request):
    return render(request, 'browse/index.html', {
        'title': 'Browse'
    })

def resource_types(request):
    return render(request, 'browse/resource_types.html', {
        'title': 'Browse Resource Types'
    })

def schemas(request):
    return render(request, 'browse/schemas.html', {
        'title': 'Browse Schemas'
    })

def list_resource_namespaces(request):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = _get_view_helper_variables_by_url_namespace(url_namespace)
    namespaces = list(view_helper_vars['mongodb_model'].find({}).distinct('identifier.pithia:Identifier.namespace'))
    return render(request, 'browse/list_resource_namespaces.html', {
        'title': f'{view_helper_vars["resource_type"]} Namespaces',
        'resource_type_plural': view_helper_vars['resource_type_plural'],
        'url_namespace': url_namespace,
        'namespaces': namespaces,
    })

def list_resources_in_namespace(request, namespace):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = _get_view_helper_variables_by_url_namespace(url_namespace)
    resources_list = list(view_helper_vars['mongodb_model'].find({
        'identifier.pithia:Identifier.namespace': namespace
    }))
    return render(request, 'browse/list_resources_in_namespace.html', {
        'title': f'{view_helper_vars["resource_type_plural"]} in the {namespace} namespace',
        'breadcrumb_item_list_resource_namespaces_text': f'{view_helper_vars["resource_type"]} Namespaces',
        'resource_type_plural': view_helper_vars['resource_type_plural'],
        'namespace': namespace,
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

def detail(request, namespace, local_id):
    url_namespace = request.resolver_match.namespace
    view_helper_vars = _get_view_helper_variables_by_url_namespace(url_namespace)
    resource = view_helper_vars['mongodb_model'].find_one({
        'identifier.pithia:Identifier.localID': local_id,
        'identifier.pithia:Identifier.namespace': namespace,
    })
    resource_flattened = flatten(resource)
    return render(request, 'browse/detail.html', {
        'breadcrumb_item_list_resource_namespaces_text': f'{view_helper_vars["resource_type"]} Namespaces',
        'url_namespace': url_namespace,
        'resource': resource,
        'resource_flattened': resource_flattened
    })