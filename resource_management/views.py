from importlib import resources
from django.shortcuts import render
from django.views.generic import TemplateView
from common.mongodb_models import CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject

from search.helpers import remove_underscore_from_id_attribute


# Create your views here.
def index(request):
    return render(request, 'resource_management/index.html', {
        'title': 'Manage Resources'
    })

class ManageResourcesView(TemplateView):
    template_name = 'resource_management/list_resources_of_type.html'
    resource_mongodb_model = None
    resource_type_plural = 'Resources'
    title = f'Manage {resource_type_plural}'
    resources_list = []
    delete_resource_view_name = ''
    update_resource_view_name = ''

    def get_resources_list(self):
        resources_list = list(self.resource_mongodb_model.find({}))
        return list(map(remove_underscore_from_id_attribute, resources_list))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['resource_type_plural'] = self.resource_type_plural
        context['resources_list'] = self.get_resources_list()
        context['delete_resource_view_name'] = self.delete_resource_view_name
        context['update_resource_view_name'] = self.update_resource_view_name
        return context

class organisations(ManageResourcesView):
    title = 'Manage Organisations'
    resource_mongodb_model = CurrentOrganisation
    resource_type_plural = 'Organisations'
    delete_resource_view_name = 'delete:organisation'
    update_resource_view_name = 'update:organisation'

class individuals(ManageResourcesView):
    title = 'Manage Individuals'
    resource_mongodb_model = CurrentIndividual
    resource_type_plural = 'Individuals'
    delete_resource_view_name = 'delete:individual'
    update_resource_view_name = 'update:individual'

class projects(ManageResourcesView):
    title = 'Manage Projects'
    resource_mongodb_model = CurrentProject
    resource_type_plural = 'Projects'
    delete_resource_view_name = 'delete:project'
    update_resource_view_name = 'update:project'

class platforms(ManageResourcesView):
    title = 'Manage Platforms'
    resource_mongodb_model = CurrentPlatform
    resource_type_plural = 'PLatforms'
    delete_resource_view_name = 'delete:platform'
    update_resource_view_name = 'update:platform'

class instruments(ManageResourcesView):
    title = 'Manage Instruments'
    resource_mongodb_model = CurrentInstrument
    resource_type_plural = 'Instruments'
    delete_resource_view_name = 'delete:instrument'
    update_resource_view_name = 'update:instrument'

class operations(ManageResourcesView):
    title = 'Manage Operations'
    resource_mongodb_model = CurrentOperation
    resource_type_plural = 'Operations'
    delete_resource_view_name = 'delete:operation'
    update_resource_view_name = 'update:operation'

class acquisitions(ManageResourcesView):
    title = 'Manage Acquisitions'
    resource_mongodb_model = CurrentAcquisition
    resource_type_plural = 'Acquisitions'
    delete_resource_view_name = 'delete:acquisition'
    update_resource_view_name = 'update:acquisition'

class computations(ManageResourcesView):
    title = 'Manage Computations'
    resource_mongodb_model = CurrentComputation
    resource_type_plural = 'Computations'
    delete_resource_view_name = 'delete:computation'
    update_resource_view_name = 'update:computation'

class processes(ManageResourcesView):
    title = 'Manage Processes'
    resource_mongodb_model = CurrentProcess
    resource_type_plural = 'Processes'
    delete_resource_view_name = 'delete:process'
    update_resource_view_name = 'update:process'

class data_collections(ManageResourcesView):
    title = 'Manage Data Collections'
    resource_mongodb_model = CurrentDataCollection
    resource_type_plural = 'Data Collections'
    delete_resource_view_name = 'delete:data_collection'
    update_resource_view_name = 'update:data_collection'
