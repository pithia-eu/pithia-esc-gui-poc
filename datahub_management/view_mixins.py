import os
import shutil
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse_lazy
from django.utils.text import slugify
from pathlib import Path

from .dataclasses import CatalogueDataSubsetOnlineResource
from .services import (
    CatalogueDataSubsetDataHubService,
    WorkflowDataHubService,
)

from metadata_editor.editor_dataclasses import CatalogueDataSubsetSourceMetadataUpdate
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

    def get_catalogue_data_subset_datahub_directory_path(self):
        return CatalogueDataSubsetDataHubService._get_catalogue_data_subset_directory_path(
            self.resource_id
        )

    def get_online_resource_file_for_catalogue_data_subset_by_file_name(self, file_name_no_extension: str):
        return CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            self.resource_id,
            file_name_no_extension
        )

    def get_online_resource_files_for_catalogue_data_subset(self):
        return CatalogueDataSubsetDataHubService.get_files_for_catalogue_data_subset(
            self.resource_id
        )

    def get_online_resource_file_url_for_catalogue_data_subset(self, online_resource_name):
        return f'{os.environ["HANDLE_URL_PREFIX"]}{reverse_lazy("browse:catalogue_data_subset_online_resource_file", kwargs={"catalogue_data_subset_id": self.resource_id, "online_resource_name": online_resource_name})}'

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
    
    def _get_file_for_online_resource(self, online_resource: CatalogueDataSubsetOnlineResource|CatalogueDataSubsetSourceMetadataUpdate):
        return self.source_files.get(online_resource.file_input_name)

    def add_source_file_to_temporary_directory(self, source_file: InMemoryUploadedFile, source_file_write_path: str):
        with open(source_file_write_path, 'wb+') as destination:
            for chunk in source_file.chunks():
                destination.write(chunk)

    def _configure_and_add_source_file_to_temporary_directory(
            self,
            online_resource_name: str,
            file_for_online_resource: InMemoryUploadedFile,
            temporary_directory_path: str):
        file_name_with_no_extension, file_extension = os.path.splitext(file_for_online_resource.name)
        slugified_online_resource_name = slugify(online_resource_name)
        slugified_file_name = f'{slugified_online_resource_name}{file_extension}'
        file_for_online_resource_path = os.path.join(temporary_directory_path, slugified_file_name)
        self.add_source_file_to_temporary_directory(
            file_for_online_resource,
            file_for_online_resource_path
        )

    def configure_and_add_source_files_to_temporary_directory(self, temporary_directory_path: str):
        for online_resource in self.valid_sources:
            online_resource_name = online_resource.name
            # Add links to each online resource source
            # file in the XML.
            self.xml_string = self.add_online_resource_file_link_to_catalogue_data_subset_xml_file_string(
                online_resource_name,
                self.xml_string
            )

            # Add the source files to a temporary directory,
            # preparing them to move all at once to DataHub.
            file_for_online_resource = self._get_file_for_online_resource(online_resource)
            self._configure_and_add_source_file_to_temporary_directory(
                online_resource_name,
                file_for_online_resource,
                temporary_directory_path
            )

    # Credit: https://stackoverflow.com/a/60430804
    def copy_temporary_directory_to_datahub(self, temporary_directory_path: str, datahub_directory_path: str):
        destination = Path(datahub_directory_path)
        if not destination.exists():
            return shutil.move(temporary_directory_path, destination)

        if destination.is_dir():
            shutil.rmtree(destination)
        else:
            destination.unlink()
        return shutil.move(temporary_directory_path, destination)