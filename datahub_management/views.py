from django.http import FileResponse
from django.http import Http404
from django.shortcuts import render
from django.utils.html import escape

from .services import WorkflowDataHubService


# Create your views here.
def get_workflow_details_file(request, workflow_id):
    workflow_details_file = WorkflowDataHubService.get_workflow_details_file(workflow_id)
    if not workflow_details_file:
        raise Http404(f'A details file for workflow with ID "<i>{escape(workflow_id)}</i>" was not found in the e-Science Centre.')
    return FileResponse(workflow_details_file, content_type='application/pdf')