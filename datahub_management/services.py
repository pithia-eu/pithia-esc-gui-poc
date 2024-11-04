import os
from django.core.files.uploadedfile import SimpleUploadedFile

from pithiaesc.settings import BASE_DIR


class DataHubService:
    @classmethod
    def store_or_overwrite_workflow_details_file(self, workflow_details_file: SimpleUploadedFile, workflow_id: str):
        # Change the name of the workflow details file
        # to the workflow id.

        # Store the file in DataHub.
        pass
    
    @classmethod
    def get_workflow_details_file(self, workflow_id: str):
        # Get the details file by the workflow ID.
        return open(os.path.join(BASE_DIR, 'datahub', f'{workflow_id}.pdf'), 'rb')