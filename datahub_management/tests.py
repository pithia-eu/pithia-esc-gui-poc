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
    def setUp(self) -> None:
        self.catalogue_data_subset_ids_teardown = set()
        return super().setUp()

    def tearDown(self) -> None:
        if not self.catalogue_data_subset_ids_teardown:
            return super().tearDown()
        for cds_id in self.catalogue_data_subset_ids_teardown:
            CatalogueDataSubsetDataHubService.delete_catalogue_data_subset_directory(cds_id)
        return super().tearDown()

    def _create_and_store_catalogue_data_subset_test_resource_file(
            self,
            catalogue_data_subset_id: str = 'catalogue_data_subset_id_default',
            resource_name: str = 'resource_name_default'
        ):
        self.catalogue_data_subset_ids_teardown.add(catalogue_data_subset_id)
        test_uploaded_file = SimpleUploadedFile('test.pdf', b'')
        return CatalogueDataSubsetDataHubService.store_or_overwrite_catalogue_data_subset_resource_file(
            test_uploaded_file,
            resource_name,
            catalogue_data_subset_id
        )

    def test_store_or_overwrite_catalogue_data_subset_resource_file(self):
        """The catalogue data subset resource file
        is stored in the DataHub directory and renamed
        to the name of a resource.
        """
        resource_name = 'resource_name'
        cds_resource_file = self._create_and_store_catalogue_data_subset_test_resource_file(
            resource_name=resource_name
        )
        self.assertEqual(cds_resource_file.name, f'{resource_name}.pdf')

    def test_get_catalogue_data_subset_file(self):
        """A catalogue data subset resource file
        is retrieved by its name (no extension is
        provided).
        """
        catalogue_data_subset_id = 'catalogue_data_subset_id'
        resource_name = 'resource_name'
        cds_resource_file = self._create_and_store_catalogue_data_subset_test_resource_file(
            catalogue_data_subset_id,
            resource_name
        )
        retrieved_cds_resource_file = CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            catalogue_data_subset_id,
            resource_name
        )
        self.assertEqual(
            os.path.basename(cds_resource_file.name),
            os.path.basename(retrieved_cds_resource_file.name)
        )

    def test_rename_catalogue_data_subset_resource_file(self):
        """A catalogue data subset resource file
        is renamed to a new given name.
        """
        catalogue_data_subset_id = 'catalogue_data_subset_id'
        resource_name = 'resource_name'
        cds_resource_file = self._create_and_store_catalogue_data_subset_test_resource_file(
            catalogue_data_subset_id,
            resource_name
        )
        cds_resource_file_name_no_extension = os.path.splitext(cds_resource_file.name)[0]
        self.assertEqual(
            resource_name,
            cds_resource_file_name_no_extension
        )
        new_file_name = 'new_resource_name'
        CatalogueDataSubsetDataHubService.rename_catalogue_data_subset_resource_file(
            catalogue_data_subset_id,
            cds_resource_file_name_no_extension,
            new_file_name
        )
        renamed_cds_resource_file = CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            catalogue_data_subset_id,
            new_file_name
        )
        renamed_cds_resource_file_no_extension = os.path.splitext(os.path.basename(renamed_cds_resource_file.name))[0]
        self.assertEqual(
            new_file_name,
            renamed_cds_resource_file_no_extension
        )
        self.assertNotEqual(
            cds_resource_file_name_no_extension,
            renamed_cds_resource_file_no_extension
        )

    def test_get_files_for_catalogue_data_subset(self):
        """Retrieves a list of all the resource files
        for a catalogue data subset.
        """
        catalogue_data_subset_id = 'catalogue_data_subset_id'
        resource_name_1 = 'resource_name_1'
        resource_name_2 = 'resource_name_2'
        resource_file_1 = self._create_and_store_catalogue_data_subset_test_resource_file(
            catalogue_data_subset_id=catalogue_data_subset_id,
            resource_name=resource_name_1
        )
        resource_file_2 = self._create_and_store_catalogue_data_subset_test_resource_file(
            catalogue_data_subset_id=catalogue_data_subset_id,
            resource_name=resource_name_2
        )
        cds_resource_files = CatalogueDataSubsetDataHubService.get_files_for_catalogue_data_subset(
            catalogue_data_subset_id
        )
        cds_resource_file_names = [os.path.basename(file.name) for file in cds_resource_files]
        self.assertEqual(len(cds_resource_files), 2)
        self.assertIn(resource_file_1.name, cds_resource_file_names)
        self.assertIn(resource_file_2.name, cds_resource_file_names)

    def test_delete_catalogue_data_subset_resource_file(self):
        """Deletes a catalogue data subset's resource
        file by its name.
        """
        catalogue_data_subset_id = 'catalogue_data_subset_id'
        resource_name = 'resource_name'
        cds_resource_file = self._create_and_store_catalogue_data_subset_test_resource_file(
            catalogue_data_subset_id=catalogue_data_subset_id,
            resource_name='resource_name'
        )
        retrieved_cds_resource_file = CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            catalogue_data_subset_id,
            resource_name
        )
        # Assert file has been created.
        self.assertEqual(
            os.path.basename(cds_resource_file.name),
            os.path.basename(retrieved_cds_resource_file.name)
        )
        CatalogueDataSubsetDataHubService.delete_catalogue_data_subset_resource_file(
            catalogue_data_subset_id,
            resource_name
        )
        cds_resource_file_after_deletion = CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            catalogue_data_subset_id,
            resource_name
        )
        self.assertIsNone(cds_resource_file_after_deletion)

    def test_delete_catalogue_data_subset_directory(self):
        """Deletes the directory for a catalogue
        data subset's resource files.
        """
        catalogue_data_subset_id = 'catalogue_data_subset_id'
        catalogue_data_subset_directory_path = CatalogueDataSubsetDataHubService._get_catalogue_data_subset_directory_path_and_create_if_not_exists(
            catalogue_data_subset_id
        )
        self.assertTrue(os.path.isdir(catalogue_data_subset_directory_path))
        CatalogueDataSubsetDataHubService.delete_catalogue_data_subset_directory(catalogue_data_subset_id)
        self.assertFalse(os.path.isdir(catalogue_data_subset_directory_path))
