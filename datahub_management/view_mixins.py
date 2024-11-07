import os
from django.urls import reverse_lazy

from .services import WorkflowDataHubService

from metadata_editor.services import SimpleWorkflowEditor
from validation.file_wrappers import XMLMetadataFile


class WorkflowDataHubViewMixin:
    def store_workflow_details_file_and_update_xml_file_string(self, xml_file_string):
        # Store/overwrite workflow details file
        wrapped_xml_file = XMLMetadataFile(xml_file_string, '')
        self.workflow_id = wrapped_xml_file.localid
        WorkflowDataHubService.store_or_overwrite_workflow_details_file(self.details_file, self.workflow_id)
        # Construct link to workflow details file
        # and put in the new workflow's XML.
        workflow_details_url = f'{os.environ["HANDLE_URL_PREFIX"]}{reverse_lazy("browse:workflow_detail", kwargs={"workflow_id": self.workflow_id})}details/'
        simple_workflow_editor = SimpleWorkflowEditor(xml_file_string)
        simple_workflow_editor.update_workflow_details_url(workflow_details_url)
        return simple_workflow_editor.to_xml()

    def delete_workflow_details_file(self, workflow_id):
        return WorkflowDataHubService.delete_workflow_details_file(workflow_id)