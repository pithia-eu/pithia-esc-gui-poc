import os
from django.urls import reverse_lazy

from .services import WorkflowDataHubService

from metadata_editor.services import SimpleWorkflowEditor
from validation.file_wrappers import XMLMetadataFile


class WorkflowDataHubViewMixin:
    def get_workflow_details_file(self):
        return WorkflowDataHubService.get_workflow_details_file(self.resource_id)

    def get_workflow_details_file_url(self):
        return f'{os.environ["HANDLE_URL_PREFIX"]}{reverse_lazy("browse:workflow_detail", kwargs={"workflow_id": self.resource_id})}details/'

    def delete_workflow_details_file(self):
        return WorkflowDataHubService.delete_workflow_details_file(self.resource_id)

    def add_workflow_details_file_link_to_workflow_xml_file_string(self, xml_file_string):
        # Construct link to workflow details file
        # and put in the new workflow's XML.
        workflow_details_url = self.get_workflow_details_file_url()
        simple_workflow_editor = SimpleWorkflowEditor(xml_file_string)
        simple_workflow_editor.update_workflow_details_url(workflow_details_url)
        return simple_workflow_editor.to_xml()

    def store_workflow_details_file_and_update_xml_file_string(self, xml_file_string):
        # Store/overwrite workflow details file
        wrapped_xml_file = XMLMetadataFile(xml_file_string, '')
        self.resource_id = wrapped_xml_file.localid
        WorkflowDataHubService.store_or_overwrite_workflow_details_file(self.workflow_details_file, self.resource_id)
        return self.add_workflow_details_file_link_to_workflow_xml_file_string(xml_file_string)