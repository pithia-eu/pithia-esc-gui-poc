from django.http import FileResponse
from django.http import Http404
from django.shortcuts import render
from django.utils.html import escape

from .services import (
    DataSubsetDataHubService,
    WorkflowDataHubService,
)


# Create your views here.
def get_workflow_details_file(request, workflow_id):
    workflow_details_file = WorkflowDataHubService.get_workflow_details_file(workflow_id)
    if not workflow_details_file:
        raise Http404(f'A details file for workflow with ID "<i>{escape(workflow_id)}</i>" was not found in the e-Science Centre.')
    return FileResponse(workflow_details_file, content_type='application/pdf')


def get_data_subset_online_resource_file(request, data_subset_id, online_resource_name):
    online_resource_file = DataSubsetDataHubService.get_data_subset_file(
        data_subset_id,
        online_resource_name
    )
    if not online_resource_file:
        raise Http404(f'A file for <i>{online_resource_name}</i> (<i>data subset {data_subset_id}</i>) was not found in the e-Science Centre.')
    return FileResponse(online_resource_file)