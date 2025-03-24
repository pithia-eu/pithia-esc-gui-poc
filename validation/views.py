import json
import logging
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views.decorators.http import (
    require_GET,
    require_POST,
)
from django.views.generic import FormView
from http import HTTPStatus
from openapi_spec_validator import validate_spec_url
from urllib.error import HTTPError

from .file_wrappers import (
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .forms import *
from .services import (
    is_localid_taken,
    validate_instrument_xml_file_update_and_return_errors,
    validate_new_xml_file_registration_and_return_errors,
    validate_xml_file_references_and_return_errors,
    validate_xml_file_update_and_return_errors,
    validate_xml_file_with_xsd_and_return_errors,
)

from common import models
from common.decorators import login_session_institution_required
from common.helpers import clean_localid_or_namespace


logger = logging.getLogger(__name__)

# Create your views here.


class QuickInlineValidationFormView(FormView):
    form_class = QuickInlineMetadataValidationForm
    error_dict = {}
    file_wrapper_class = XMLMetadataFile

    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict.update(validate_xml_file_references_and_return_errors(xml_metadata_file))

    def post(self, request, *args, **kwargs):
        self.error_dict = {}
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('The form submitted was not valid.')
        xml_metadata_file = self.file_wrapper_class(request.POST.get('xml_file_string'), request.POST.get('xml_file_name'))
        self.validate(request, xml_metadata_file)

        if not any(self.error_dict.values()):
            return JsonResponse(self.error_dict, status=HTTPStatus.OK)
        
        return JsonResponse(self.error_dict, status=HTTPStatus.BAD_REQUEST)


class QuickInlineRegistrationValidationFormView(QuickInlineValidationFormView):
    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict['xml_file_registration_errors'] = validate_new_xml_file_registration_and_return_errors(
            xml_metadata_file,
            models.ScientificMetadata
        )
        return super().validate(request, xml_metadata_file)


class QuickInlineUpdateValidationFormView(QuickInlineValidationFormView):
    form_class = QuickInlineMetadataUpdateValidationForm

    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict['xml_file_update_errors'] = validate_xml_file_update_and_return_errors(
            xml_metadata_file,
            models.ScientificMetadata,
            request.POST.get('existing_metadata_id')
        )
        return super().validate(request, xml_metadata_file)


class QuickInlineInstrumentUpdateValidationFormView(QuickInlineValidationFormView):
    file_wrapper_class = InstrumentXMLMetadataFile

    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict['xml_file_update_errors'] = validate_xml_file_update_and_return_errors(
            xml_metadata_file,
            models.Instrument,
            request.POST.get('existing_metadata_id')
        )

        if len(self.error_dict['xml_file_update_errors']) > 0:
            self.error_dict['xml_file_op_mode_errors'] = ['Could not validate operational modes as metadata file did not pass update validation.']
            self.error_dict['xml_file_op_mode_warnings'] = ['Could not validate operational modes as metadata file did not pass update validation.']
            return super().validate(request, xml_metadata_file)
        
        self.error_dict['xml_file_op_mode_errors'] = []
        self.error_dict['xml_file_op_mode_warnings'] = validate_instrument_xml_file_update_and_return_errors(
            xml_metadata_file,
            request.POST.get('existing_metadata_id')
        )

        return super().validate(request, xml_metadata_file)


class InlineXSDValidationFormView(FormView):
    form_class = InlineXSDMetadataValidationForm
    error_dict = {}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('The form submitted was not valid.')
        xml_metadata_file = XMLMetadataFile(request.POST.get('xml_file_string'), '')
        self.error_dict['xml_file_xsd_errors'] = validate_xml_file_with_xsd_and_return_errors(xml_metadata_file)

        if not any(self.error_dict.values()):
            return JsonResponse(self.error_dict, status=HTTPStatus.OK)
        
        return JsonResponse(self.error_dict, status=HTTPStatus.BAD_REQUEST)


@require_GET
@login_session_institution_required
def localid(request):
    form = LocalIDValidationForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest('The submitted form was invalid.')
    
    localid = form.cleaned_data.get('localid')
    localid = clean_localid_or_namespace(localid)
    return JsonResponse(is_localid_taken(localid))


@require_POST
@login_session_institution_required
def api_specification_url(request):
    response_body = {
        'valid': False
    }
    form = ApiSpecificationUrlValidationForm(request.POST)
    if form.is_valid():
        api_specification_url = request.POST['api_specification_url']
        try:
            validate_spec_url(api_specification_url)
            response_body['valid'] = True
        except HTTPError as err:
            logger.exception('The provided API specification URL returned an HTTP Error 404: Not Found.')
            response_body['error'] = 'The URL was not found'
        except BaseException as err:
            logger.exception('The provided API specification URL does not link to a valid OpenAPI specification.')
            response_body['error'] = 'The URL does not link to a valid OpenAPI specification'
            response_body['details'] = str(err)
    else:
        response_body['error'] = 'Please enter a URL'
    return HttpResponse(json.dumps(response_body), content_type='application/json')
