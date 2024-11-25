import logging
from django.contrib import messages
from django.utils.html import escape

from .services import HandleRegistrationProcessForCatalogueDataSubset
from handle_management.xml_utils import (
    add_doi_xml_string_to_metadata_xml_string,
    get_doi_xml_string_from_metadata_xml_string,
    remove_doi_element_from_metadata_xml_string,
)

from common.models import ScientificMetadata


logger = logging.getLogger(__name__)


# Create your views here.
class HandleRegistrationViewMixin:
    DOI_ALREADY_ISSUED_MESSAGE = 'A new DOI was not issued as a record of a pre-existing DOI was found for this resource.'
    DOI_FOUND_IN_SUBMITTED_FILE_MESSAGE = 'A new DOI was not issued as record of a pre-existing DOI was found in the submitted metadata file.'

    def register_doi_if_requested(self, request, resource: ScientificMetadata, xml_file=None, xml_file_string: str = None):
        if 'register_doi' not in request.POST:
            return None
        if xml_file:
            xml_file.seek(0)
            xml_file_string = xml_file.read()
        elif xml_file_string:
            xml_file_string.encode('utf-8')
        else:
            messages.error(request, 'A DOI was not issued for this registration as an error occurred during the DOI registration process. Please try again later.')
            return None
        doi_kernel_metadata_from_xml_file = get_doi_xml_string_from_metadata_xml_string(xml_file_string)
        doi_kernel_metadata_from_resource = get_doi_xml_string_from_metadata_xml_string(resource.xml)
        if doi_kernel_metadata_from_resource:
            # Do not issue a new DOI if the resource XML contains
            # a record of a previously issued DOI.
            logger.exception(self.DOI_ALREADY_ISSUED_MESSAGE)
            messages.error(request, self.DOI_ALREADY_ISSUED_MESSAGE)
            return None
        elif doi_kernel_metadata_from_xml_file:
            # Do not issue a new DOI if the submitted metadata file
            # XML contains a record of a previously issued DOI.
            logger.exception(self.DOI_FOUND_IN_SUBMITTED_FILE_MESSAGE)
            messages.error(request, self.DOI_FOUND_IN_SUBMITTED_FILE_MESSAGE)
            return None
        
        handle_registration_process = HandleRegistrationProcessForCatalogueDataSubset(
            resource,
            self.owner_id
        )
        handle_name = handle_registration_process.run()
        # No handle name returned indicates that a handle
        # was not created/deleted due to an error.
        if not handle_name:
            messages.error(request, 'A DOI was not issued for this registration as an error occurred during the DOI registration process. Please try again later.')
            return None
        messages.success(request, escape(f'A DOI with name "{handle_name}" has been registered for this data subset. DOI kernel metadata has also been added to the metadata file.'))
        return handle_name


class HandleReapplicationViewMixin:
    def reinsert_pre_existing_doi_kernel_metadata_into_updated_xml_file_if_needed(self, resource, xml_file):
        # Any DOI kernel metadata already stored on a resource
        # in the eSC is considered official, so any DOI passed
        # in the updated submitted XML file is overwritten.
        pre_existing_doi_xml_string = get_doi_xml_string_from_metadata_xml_string(resource.xml)
        xml_file.seek(0)
        xml_file_string = xml_file.read()
        if not pre_existing_doi_xml_string:
            return xml_file_string
        xml_file_string = remove_doi_element_from_metadata_xml_string(xml_file_string)
        xml_file_string = add_doi_xml_string_to_metadata_xml_string(xml_file_string, pre_existing_doi_xml_string)
        return xml_file_string