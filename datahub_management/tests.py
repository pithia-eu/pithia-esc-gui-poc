import os
from django.test import SimpleTestCase, tag
from django.core.files.uploadedfile import SimpleUploadedFile

from .services import (
    DataSubsetDataHubService,
    WorkflowDataHubService,
)


# Create your tests here.
@tag('manual')
class WorkflowDataHubServiceTestCase(SimpleTestCase):
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


@tag('manual')
class DataSubsetDataHubServiceTestCase(SimpleTestCase):
    def setUp(self) -> None:
        self.data_subset_ids_teardown = set()
        return super().setUp()

    def tearDown(self) -> None:
        if not self.data_subset_ids_teardown:
            return super().tearDown()
        for cds_id in self.data_subset_ids_teardown:
            DataSubsetDataHubService.delete_data_subset_directory(cds_id)
        return super().tearDown()

    def _create_and_store_data_subset_test_resource_file(
            self,
            data_subset_id: str = 'data_subset_id_default',
            resource_name: str = 'resource_name_default'
        ):
        self.data_subset_ids_teardown.add(data_subset_id)
        test_uploaded_file = SimpleUploadedFile('test.pdf', b'')
        return DataSubsetDataHubService.store_or_overwrite_data_subset_resource_file(
            test_uploaded_file,
            resource_name,
            data_subset_id
        )

    def test_store_or_overwrite_data_subset_resource_file(self):
        """The data subset resource file is stored
        in the DataHub directory and renamed to the
        name of a resource.
        """
        resource_name = 'resource_name'
        cds_resource_file = self._create_and_store_data_subset_test_resource_file(
            resource_name=resource_name
        )
        self.assertEqual(cds_resource_file.name, f'{resource_name}.pdf')

    def test_get_data_subset_file(self):
        """A data subset resource file is retrieved
        by its name (no extension is provided).
        """
        data_subset_id = 'data_subset_id'
        resource_name = 'resource_name'
        cds_resource_file = self._create_and_store_data_subset_test_resource_file(
            data_subset_id,
            resource_name
        )
        retrieved_cds_resource_file = DataSubsetDataHubService.get_data_subset_file(
            data_subset_id,
            resource_name
        )
        self.assertEqual(
            os.path.basename(cds_resource_file.name),
            os.path.basename(retrieved_cds_resource_file.name)
        )

    def test_get_files_for_data_subset(self):
        """Retrieves a list of all the resource files
        for a data subset.
        """
        data_subset_id = 'data_subset_id'
        resource_name_1 = 'resource_name_1'
        resource_name_2 = 'resource_name_2'
        resource_file_1 = self._create_and_store_data_subset_test_resource_file(
            data_subset_id=data_subset_id,
            resource_name=resource_name_1
        )
        resource_file_2 = self._create_and_store_data_subset_test_resource_file(
            data_subset_id=data_subset_id,
            resource_name=resource_name_2
        )
        cds_resource_files = DataSubsetDataHubService.get_files_for_data_subset(
            data_subset_id
        )
        cds_resource_file_names = [os.path.basename(file.name) for file in cds_resource_files]
        self.assertEqual(len(cds_resource_files), 2)
        self.assertIn(resource_file_1.name, cds_resource_file_names)
        self.assertIn(resource_file_2.name, cds_resource_file_names)

    def test_delete_data_subset_directory(self):
        """Deletes the directory for a data subset's
        resource files.
        """
        data_subset_id = 'data_subset_id'
        DataSubsetDataHubService._create_directory_for_data_subset(data_subset_id)
        data_subset_directory_path = DataSubsetDataHubService._get_data_subset_directory_path(
            data_subset_id
        )
        self.assertTrue(os.path.isdir(data_subset_directory_path))
        DataSubsetDataHubService.delete_data_subset_directory(data_subset_id)
        self.assertFalse(os.path.isdir(data_subset_directory_path))
