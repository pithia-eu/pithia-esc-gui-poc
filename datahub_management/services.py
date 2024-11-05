import os
import pathlib
from django.core.files.uploadedfile import SimpleUploadedFile

from pithiaesc.settings import BASE_DIR


class WorkflowDataHubService:
    @classmethod
    def _get_workflow_details_file_path(self, workflow_id):
        return os.path.join(BASE_DIR, 'datahub', 'workflow_details', f'{workflow_id}.pdf')

    @classmethod
    def store_or_overwrite_workflow_details_file(cls, workflow_details_file: SimpleUploadedFile, workflow_id: str):
        # Change the name of the workflow details file
        # to the workflow ID and store in DataHub.
        with open(cls._get_workflow_details_file_path(workflow_id), 'wb+') as destination:
            for chunk in workflow_details_file.chunks():
                destination.write(chunk)

        return pathlib.Path(cls._get_workflow_details_file_path(workflow_id))
    
    @classmethod
    def get_workflow_details_file(cls, workflow_id: str):
        # Get the details file by the workflow ID.
        return open(cls._get_workflow_details_file_path(workflow_id), 'rb')

    @classmethod
    def delete_workflow_details_file(cls, workflow_id: str):
        workflow_details_file_to_remove = pathlib.Path(cls._get_workflow_details_file_path(workflow_id))
        return workflow_details_file_to_remove.unlink()