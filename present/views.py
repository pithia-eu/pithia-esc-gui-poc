import logging
import os
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from .forms import SwaggerViewModeForm

from common.models import (
    APIInteractionMethod,
    DataCollection,
    Workflow,
    WorkflowAPIInteractionMethod,
)
from browse.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE,
)
from user_management.services import get_institution_id_for_login_session


logger = logging.getLogger(__name__)


# Create your views here.

class APIInteractionMethodView(TemplateView):
    template_name = ''

    scientific_metadata = None
    api_interaction_method = None
    api_specification_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Interact with {self.scientific_metadata.name} via API'
        context['scientific_metadata'] = self.scientific_metadata
        context['api_specification_url'] = self.api_specification_url
        context['browse_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        if (os.environ.get('API_INTERACTION_METHOD_DEV_GROUP')
            and os.environ.get('API_INTERACTION_METHOD_DEV_GROUP') == get_institution_id_for_login_session(self.request.session)):
            context['form'] = SwaggerViewModeForm(initial={'mode': 'dev'})
            context['developer'] = True
        return context
    

class DataCollectionAPIInteractionMethodView(APIInteractionMethodView):
    template_name = 'present/index.html'

    def get(self, request, *args, **kwargs):
        data_collection_id = self.kwargs['data_collection_id']
        try:
            self.scientific_metadata = DataCollection.objects.get(pk=data_collection_id)
        except DataCollection.DoesNotExist:
            messages.error(request, 'A data collection matching the specified ID was not found.')
            return HttpResponseRedirect(reverse('browse:list_data_collections'))

        online_resource_name = request.GET.get('name')
        if online_resource_name:
            try:
                online_resources = self.scientific_metadata.properties.online_resources
                corresponding_online_resource = next((online_resource for online_resource in online_resources if online_resource.get('name') == online_resource_name), {})
                self.api_specification_url = corresponding_online_resource.get('linkage')
                return super().get(request, *args, **kwargs)
            except Exception as err:
                logger.exception(err)
                messages.error(request, 'An unexpected error occurred whilst trying to retrieve API information for this data collection.')
                return HttpResponseRedirect(reverse('browse:data_collection_detail', kwargs={'data_collection_id': data_collection_id}))

        try:
            self.api_interaction_method = APIInteractionMethod.objects.get(scientific_metadata=self.scientific_metadata)
            self.api_specification_url = self.api_interaction_method.specification_url
        except APIInteractionMethod.DoesNotExist:
            messages.error(request, 'No API interaction method was found for this data collection.')
            return HttpResponseRedirect(reverse('browse:data_collection_detail', kwargs={'data_collection_id': data_collection_id}))
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_type_list_page_breadcrumb_text'] = _DATA_COLLECTION_RELATED_RESOURCE_TYPES_PAGE_TITLE
        context['resource_list_page_breadcrumb_text'] = DataCollection.type_plural_readable.title()
        return context

class WorkflowAPIInteractionMethodView(APIInteractionMethodView):
    template_name = 'present/index_workflow.html'

    def get(self, request, *args, **kwargs):
        workflow_id = self.kwargs['workflow_id']
        try:
            self.scientific_metadata = Workflow.objects.get(pk=workflow_id)
        except Workflow.DoesNotExist:
            messages.error(request, 'A workflow matching the specified ID was not found.')
            return HttpResponseRedirect(reverse('browse:list_workflows'))
        
        try:
            self.api_interaction_method = WorkflowAPIInteractionMethod.objects.get(scientific_metadata=self.scientific_metadata)
            self.api_specification_url = self.api_interaction_method.specification_url
        except WorkflowAPIInteractionMethod.DoesNotExist:
            messages.error(request, 'No API interaction method was found for this workflow.')
            return HttpResponseRedirect(reverse('browse:workflow_detail', kwargs={'workflow_id': workflow_id}))
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_list_page_breadcrumb_text'] = Workflow.type_plural_readable.title()
        return context