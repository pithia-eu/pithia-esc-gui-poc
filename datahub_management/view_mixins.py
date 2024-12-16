import os
import pathlib
from django.urls import reverse_lazy
from typing import List

from .services import (
    CatalogueDataSubsetDataHubService,
    WorkflowDataHubService,
)

from metadata_editor.services import (
    SimpleCatalogueDataSubsetEditor,
    SimpleWorkflowEditor,
)


class WorkflowDataHubViewMixin:
    def get_workflow_details_file(self):
        return WorkflowDataHubService.get_workflow_details_file(self.resource_id)

    def get_workflow_details_file_url(self):
        return f'{os.environ["HANDLE_URL_PREFIX"]}{reverse_lazy("browse:workflow_details_file", kwargs={"workflow_id": self.resource_id})}'

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
        WorkflowDataHubService.store_or_overwrite_workflow_details_file(self.workflow_details_file, self.resource_id)
        return self.add_workflow_details_file_link_to_workflow_xml_file_string(xml_file_string)


class CatalogueDataSubsetDataHubViewMixin:
    def is_catalogue_data_subset_directory_created(self):
        return CatalogueDataSubsetDataHubService.is_catalogue_data_subset_directory_created(self.resource_id)

    def get_online_resource_file_for_catalogue_data_subset(self, online_resource_name):
        return CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            self.resource_id,
            online_resource_name
        )

    def get_online_resource_files_for_catalogue_data_subset(self):
        return CatalogueDataSubsetDataHubService.get_files_for_catalogue_data_subset(
            self.resource_id
        )

    def get_online_resource_file_url_for_catalogue_data_subset(self, online_resource_name):
        return f'{os.environ["HANDLE_URL_PREFIX"]}{reverse_lazy("browse:catalogue_data_subset_online_resource_file", kwargs={"catalogue_data_subset_id": self.resource_id, "online_resource_name": online_resource_name})}'

    def delete_online_resource_file_for_catalogue_data_subset(self, online_resource_name):
        return CatalogueDataSubsetDataHubService.delete_catalogue_data_subset_resource_file(
            self.resource_id,
            online_resource_name
        )

    def delete_catalogue_data_subset_directory(self):
        return CatalogueDataSubsetDataHubService.delete_catalogue_data_subset_directory(self.resource_id)

    def add_online_resource_file_link_to_catalogue_data_subset_xml_file_string(
            self,
            online_resource_name,
            xml_file_string):
        # Construct link to online resource
        # file and put in the catalogue data
        # subset's XML.
        online_resource_file_url = self.get_online_resource_file_url_for_catalogue_data_subset(online_resource_name)
        simple_catalogue_data_subset_editor = SimpleCatalogueDataSubsetEditor(xml_file_string)
        simple_catalogue_data_subset_editor.update_online_resource_url(online_resource_name, online_resource_file_url)
        return simple_catalogue_data_subset_editor.to_xml()

    def store_online_resource_file_and_update_catalogue_data_subset_xml_file_string(
            self,
            online_resource_file,
            online_resource_name,
            xml_file_string):
        # Store/overwrite online resource file
        CatalogueDataSubsetDataHubService.store_or_overwrite_catalogue_data_subset_resource_file(
            online_resource_file,
            online_resource_name,
            self.resource_id
        )
        return self.add_online_resource_file_link_to_catalogue_data_subset_xml_file_string(
            online_resource_name,
            xml_file_string
        )

    def rename_online_resource_file(
            self,
            current_file_name: str,
            new_file_name_no_extension: str):
        current_file_name_no_extension = pathlib.Path(current_file_name).stem
        return CatalogueDataSubsetDataHubService.rename_catalogue_data_subset_resource_file(
            self.resource_id,
            current_file_name_no_extension,
            new_file_name_no_extension
        )

    def delete_unused_online_resource_files(self, names_of_used_files: List[str]):
        return CatalogueDataSubsetDataHubService.delete_unused_catalogue_data_subset_resource_files(
            self.resource_id,
            names_of_used_files
        )