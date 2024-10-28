import logging
import os
from django.db import transaction
from pyexpat import ExpatError

from .handle_api import (
    add_doi_metadata_kernel_to_handle,
    create_and_register_handle_for_resource_url,
    delete_handle,
)
from .xml_utils import (
    add_data_subset_data_to_doi_metadata_kernel_dict,
    add_doi_metadata_kernel_to_data_subset,
    add_handle_data_to_doi_metadata_kernel_dict,
    initialise_default_doi_kernel_metadata_dict,
)

from common.models import HandleURLMapping
from utils.url_helpers import create_data_subset_detail_page_url


logger = logging.getLogger(__name__)

def add_handle_to_url_mapping(handle: str, url: str):
    handle_url_mapping = HandleURLMapping(
        id=handle,
        handle_name=handle,
        url=url
    )
    handle_url_mapping.save(using=os.environ['DJANGO_RW_DATABASE_NAME'])

def register_doi_for_catalogue_data_subset(catalogue_data_subset, owner_id):
    handle = None
    handle_api_client = None
    result = {}

    try:
        # Create and register a handle
        data_subset_url = create_data_subset_detail_page_url(catalogue_data_subset.pk)
        handle, handle_api_client, credentials = create_and_register_handle_for_resource_url(data_subset_url)

        # Create a dict storing DOI metadata kernel information.
        # This information in this dict will be added to the
        # Handle to store data that a DOI would normally handle.
        doi_dict = initialise_default_doi_kernel_metadata_dict()

        # Add the handle metadata to the DOI dict
        doi_dict = add_handle_data_to_doi_metadata_kernel_dict(handle, doi_dict)
        add_data_subset_data_to_doi_metadata_kernel_dict(catalogue_data_subset, doi_dict)

        # Add DOI metadata kernel to Handle
        add_doi_metadata_kernel_to_handle(handle, doi_dict, handle_api_client)

        with transaction.atomic(using=os.environ['DJANGO_RW_DATABASE_NAME']):
            # Add DOI metadata kernel to Data Subset
            add_doi_metadata_kernel_to_data_subset(
                catalogue_data_subset.pk,
                doi_dict,
                catalogue_data_subset.xml,
                owner_id
            )
            # Handle to Data Subset URL mapping, to be able to
            # retrieve information from the Handle in case the
            # Data Subset ever gets deleted.
            add_handle_to_url_mapping(handle, data_subset_url)
        result['handle'] = handle
    except ExpatError as err:
        logger.exception('Expat error occurred during DOI registration process.')
        result['error'] = f'An error occurred whilst parsing {catalogue_data_subset.name} during the DOI registration process.'
    except BaseException as err:
        error_msg = 'An unexpected error occurred during DOI registration.'
        logger.exception(error_msg)
        result['error'] = error_msg
        if not handle:
            return result
        try:
            logger.info(f'Attempting to delete handle {handle} due to an error that occurred during DOI registration...')
            delete_handle(handle, handle_api_client)
            logger.info(f'Deleted handle {handle}.')
        except BaseException as err:
            logger.exception(f'Could not delete handle {handle} due to an error.')

    return result