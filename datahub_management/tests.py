import os
from django.test import SimpleTestCase, tag
from django.core.files.uploadedfile import SimpleUploadedFile

from .services import (
    CatalogueDataSubsetDataHubService,
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


class CatalogueDataSubsetDataHubServiceTestCase(SimpleTestCase):
    def _create_and_store_catalogue_data_subset_test_resource_file(self):
        self.catalogue_data_subset_id = 'catalogue_data_subset_id'
        self.resource_name = 'resource_name'
        test_uploaded_file = SimpleUploadedFile('test.pdf', b'')
        return CatalogueDataSubsetDataHubService.store_or_overwrite_catalogue_data_subset_resource_file(
            test_uploaded_file,
            self.resource_name,
            self.catalogue_data_subset_id
        )

    def tearDown(self) -> None:
        if self.catalogue_data_subset_id:
            CatalogueDataSubsetDataHubService.delete_catalogue_data_subset_directory(self.catalogue_data_subset_id)
        return super().tearDown()

    def test_store_or_overwrite_catalogue_data_subset_resource_file(self):
        """The catalogue data subset resource file
        is stored in the DataHub directory and renamed
        to the name of a resource.
        """
        cds_resource_file = self._create_and_store_catalogue_data_subset_test_resource_file()
        self.assertEqual(cds_resource_file.name, f'{self.resource_name}.pdf')

    def test_get_catalogue_data_subset_file(self):
        """A catalogue data subset resource file
        is retrieved by its name (no extension is
        provided).
        """
        cds_resource_file = self._create_and_store_catalogue_data_subset_test_resource_file()
        retrieved_cds_resource_file = CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            self.catalogue_data_subset_id,
            self.resource_name
        )
        self.assertEqual(
            os.path.basename(cds_resource_file.name),
            os.path.basename(retrieved_cds_resource_file.name)
        )
