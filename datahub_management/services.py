import logging
import os
import pathlib
import shutil
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from typing import List

from pithiaesc.settings import BASE_DIR


logger = logging.getLogger(__name__)


class DataHubService:
    @classmethod
    def _get_datahub_directory_path(cls):
        return os.path.join(
            BASE_DIR,
            os.path.normpath(os.environ['DATAHUB_DIRECTORY_PATH'])
        )

    @classmethod
    def _get_file_extension(cls, file_path: str) -> str:
        file_path_and_name, file_extension = os.path.splitext(file_path)
        return file_extension

    @classmethod
    def _store_or_overwrite_file_in_datahub(cls, file_path, file):
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return pathlib.Path(file_path)

    @classmethod
    def _get_file_from_datahub(cls, file_path):
        try:
            # Get the details file by the workflow ID.
            return open(file_path, 'rb')
        except (FileNotFoundError, TypeError) as err:
            logger.exception(f'Could not find a file in DataHub with path: {file_path}.')
        return None

    @classmethod
    def _delete_file_from_datahub(cls, file_path):
        file_to_remove = pathlib.Path(file_path)
        return os.remove(file_to_remove)


class WorkflowDataHubService(DataHubService):
    @classmethod
    def _get_workflow_details_file_path(cls, workflow_id):
        return os.path.join(
            cls._get_datahub_directory_path(),
            'workflows',
            f'{workflow_id}.pdf'
        )

    @classmethod
    def store_or_overwrite_workflow_details_file(cls, file: SimpleUploadedFile, workflow_id: str):
        # Change the name of the workflow details file
        # to the workflow ID and store in DataHub.
        return cls._store_or_overwrite_file_in_datahub(
            cls._get_workflow_details_file_path(workflow_id),
            file
        )
    
    @classmethod
    def get_workflow_details_file(cls, workflow_id: str):
        # Get the details file by the workflow ID.
        return cls._get_file_from_datahub(cls._get_workflow_details_file_path(workflow_id))

    @classmethod
    def delete_workflow_details_file(cls, workflow_id: str):
        return cls._delete_file_from_datahub(cls._get_workflow_details_file_path(workflow_id))


class CatalogueDataSubsetDataHubService(DataHubService):
    @classmethod
    def _get_catalogue_data_subset_directory_path(cls, catalogue_data_subset_id: str):
        return os.path.join(
            cls._get_datahub_directory_path(),
            'catalogues',
            catalogue_data_subset_id
        )

    @classmethod
    def _create_directory_for_catalogue_data_subset(cls, catalogue_data_subset_id: str):
        """Creates a directory for a Catalogue Data
        Subset, based on its ID. An error is raised
        if a file exists at the designated directory 
        path.
        """
        catalogue_data_subset_directory_path = cls._get_catalogue_data_subset_directory_path(
            catalogue_data_subset_id
        )
        pathlib.Path(catalogue_data_subset_directory_path).mkdir(parents=False, exist_ok=True)
        return catalogue_data_subset_directory_path

    @classmethod
    def _get_catalogue_data_subset_resource_file_path_from_name_with_no_extension(
            cls,
            catalogue_data_subset_id: str,
            resource_name_with_no_extension: str):
        """Determines the file extension of a Catalogue
        Data Subset's resource from its name and returns
        a file path to that file, or None if a file is
        not found.
        """
        catalogue_data_subset_directory_path = cls._get_catalogue_data_subset_directory_path(
            catalogue_data_subset_id
        )
        # A list of possible file paths with file
        # extensions which match the resource name
        # without a file extension.
        catalogue_data_subset_resource_file_paths = pathlib.Path(catalogue_data_subset_directory_path).glob(
            f'{slugify(resource_name_with_no_extension)}.*'
        )
        file_path = None
        for cds_resource_file_path in catalogue_data_subset_resource_file_paths:
            file_path = cds_resource_file_path
        return file_path

    @classmethod
    def store_or_overwrite_catalogue_data_subset_resource_file(
            cls,
            file: SimpleUploadedFile,
            new_file_name: str,
            catalogue_data_subset_id: str):
        file_extension = cls._get_file_extension(file.name)
        cls._create_directory_for_catalogue_data_subset(catalogue_data_subset_id)
        return cls._store_or_overwrite_file_in_datahub(
            os.path.join(
                cls._get_catalogue_data_subset_directory_path(catalogue_data_subset_id),
                f'{slugify(new_file_name)}{file_extension}'
            ),
            file
        )

    @classmethod
    def is_catalogue_data_subset_directory_created(cls, catalogue_data_subset_id: str) -> bool:
        return os.path.isdir(
            cls._get_catalogue_data_subset_directory_path(catalogue_data_subset_id)
        )
    
    @classmethod
    def get_catalogue_data_subset_file(cls, catalogue_data_subset_id: str, file_name_with_no_extension: str):
        """Gets a resource file for a Catalogue Data
        Subset based on its name without the file
        extension from DataHub.
        """
        file_name = cls._get_catalogue_data_subset_resource_file_path_from_name_with_no_extension(
            catalogue_data_subset_id,
            file_name_with_no_extension
        )
        return cls._get_file_from_datahub(file_name)

    @classmethod
    def get_files_for_catalogue_data_subset(cls, catalogue_data_subset_id: str) -> List:
        """Returns a list of resource files for a
        Catalogue Data Subset.
        """
        if not cls.is_catalogue_data_subset_directory_created(catalogue_data_subset_id):
            return []
        catalogue_data_subset_directory_path = cls._get_catalogue_data_subset_directory_path(
            catalogue_data_subset_id
        )
        directory_items = os.listdir(catalogue_data_subset_directory_path)
        files = [
            cls._get_file_from_datahub(
                os.path.join(catalogue_data_subset_directory_path, file_name)
            )
            for file_name in directory_items
            if os.path.isfile(
                os.path.join(catalogue_data_subset_directory_path, file_name)
            )
        ]
        return files

    @classmethod
    def delete_catalogue_data_subset_directory(cls, catalogue_data_subset_id: str):
        """Deletes a resource file DataHub directory
        for a Catalogue Data Subset.
        """
        try:
            return shutil.rmtree(cls._get_catalogue_data_subset_directory_path(catalogue_data_subset_id))
        except OSError as err:
            logger.exception(err)