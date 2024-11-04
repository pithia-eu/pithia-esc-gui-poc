from django.shortcuts import render
from django.http import (
    FileResponse,
    HttpResponseNotFound,
)
from django.utils.html import escape

from .services import DataHubService


# Create your views here.
def get_workflow_details_file(request, workflow_id):
    try:
        workflow_details_file = DataHubService.get_workflow_details_file(workflow_id)
        return FileResponse(workflow_details_file, content_type='application/pdf')
    except IOError:
        return HttpResponseNotFound(f'The details file for workflow with ID "<i>{escape(workflow_id)}</i>" was not found.')