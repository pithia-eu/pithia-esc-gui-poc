from django.test import SimpleTestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .services import WorkflowDataHubService


# Create your tests here.
class WorkflowDataHubServiceTestCase(SimpleTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        if self.workflow_id:
            WorkflowDataHubService.delete_workflow_details_file(self.workflow_id)
        return super().tearDown()

    def test_store_or_overwrite_workflow_details_file(self):
        """The workflow details file is stored in DataHub
        and renamed to a workflow ID.
        """
        self.workflow_id = 'workflow_id'
        test_uploaded_file = SimpleUploadedFile('test.pdf', b'')
        workflow_details_file = WorkflowDataHubService.store_or_overwrite_workflow_details_file(
            test_uploaded_file,
            self.workflow_id
        )
        self.assertEqual(workflow_details_file.name, f'{self.workflow_id}.pdf')

    def test_delete_workflow_details_file(self):
        """The workflow details file is removed from
        DataHub by a given workflow ID.
        """
        self.workflow_id = 'workflow_id'
        test_uploaded_file = SimpleUploadedFile('test.pdf', b'')
        WorkflowDataHubService.store_or_overwrite_workflow_details_file(
            test_uploaded_file,
            self.workflow_id
        )
        WorkflowDataHubService.delete_workflow_details_file(self.workflow_id)
        self.workflow_id = None
