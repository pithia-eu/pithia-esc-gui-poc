import logging
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


class WorkflowDetailsUrlValidationViewMixin:
    def check_workflow_details_url(self, workflow_details_url):
        try:
            validator = URLValidator()
            validator(workflow_details_url)
            parsed_url = urlparse(workflow_details_url)
            if not parsed_url.hostname == 'esc.pithia.eu':
                return None
        except ValidationError as err:
            logger.exception(err)
            return 'The workflow details file URL provided in the metadata file is invalid.'
        except Exception as err:
            logger.exception(err)
            return 'An unexpected error occurred during registration.'
        return 'Please use the provided workflow details file input to register the details file with this workflow.'