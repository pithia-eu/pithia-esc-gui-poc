import json
import logging
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
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
    AcquisitionCapabilitiesXMLMetadataFile,
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .forms import *
from .helpers import create_register_url_from_resource_type_from_resource_url
from .services import (
    InstrumentMetadataFileValidator,
    MetadataFileRegistrationValidator,
    MetadataFileUpdateValidator,
    MetadataFileXSDValidator,
)
from .url_validation_services import (
    MetadataFileMetadataURLReferencesValidator,
)

from common import models
from common.decorators import login_session_institution_required
from common.helpers import clean_localid_or_namespace


logger = logging.getLogger(__name__)

# Create your views here.


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineValidationFormView(FormView):
    form_class = QuickInlineMetadataValidationForm
    error_dict = {}
    file_wrapper_class = XMLMetadataFile

    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        url_references_validation_results = MetadataFileMetadataURLReferencesValidator.validate_and_return_results(xml_metadata_file)
        self.error_dict.update({
            'incorrectly_structured_url_errors': list(),
            'unregistered_resource_url_errors': list(),
            'unregistered_operational_mode_url_errors': list(),
            'invalid_ontology_url_errors': list(),
        })

        if url_references_validation_results.get('incorrectly_structured_urls'):
            self.error_dict['incorrectly_structured_url_errors'].append(
                render_to_string(
                    'validation/error_incorrectly_structured_urls.html',
                    context={
                        'incorrectly_structured_urls': url_references_validation_results.get('incorrectly_structured_urls'),
                    }
                )
            )
        if url_references_validation_results.get('unregistered_resource_urls'):
            self.error_dict['unregistered_resource_url_errors'].append(
                render_to_string(
                    'validation/error_unregistered_resource_urls.html',
                    context={
                        'unregistered_resource_urls': url_references_validation_results.get('unregistered_resource_urls'),
                        'file_upload_registration_url_and_url_texts': list(map(
                            create_register_url_from_resource_type_from_resource_url,
                            url_references_validation_results.get('types_in_unregistered_resource_urls'),
                        )),
                    }
                )
            )
        if url_references_validation_results.get('unregistered_operational_mode_urls'):
            self.error_dict['unregistered_operational_mode_url_errors'].append(
                render_to_string(
                    'validation/error_unregistered_operational_mode_urls.html',
                    context={
                        'unregistered_resource_urls': url_references_validation_results.get('unregistered_operational_mode_urls'),
                        'file_upload_registration_url_and_url_texts': list(map(
                            create_register_url_from_resource_type_from_resource_url,
                            url_references_validation_results.get('types_in_unregistered_operational_mode_urls'),
                        )),
                    }
                )
            )
        if url_references_validation_results.get('invalid_ontology_urls'):
            self.error_dict['invalid_ontology_url_errors'].append(
                render_to_string(
                    'validation/error_invalid_ontology_urls.html',
                    context={
                        'invalid_ontology_urls': url_references_validation_results.get('invalid_ontology_urls'),
                    }
                )
            )

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


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineRegistrationValidationFormView(QuickInlineValidationFormView):
    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict.update({
            'registration_conflicts': MetadataFileRegistrationValidator.validate_and_return_errors(
                xml_metadata_file,
                models.ScientificMetadata
            )
        })
        return super().validate(request, xml_metadata_file)


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineUpdateValidationFormView(QuickInlineValidationFormView):
    form_class = QuickInlineMetadataUpdateValidationForm

    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict.update({
            'update_conflicts': MetadataFileUpdateValidator.validate_and_return_errors(
                xml_metadata_file,
                models.ScientificMetadata,
                request.POST.get('existing_metadata_id')
            )
        })
        return super().validate(request, xml_metadata_file)


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineInstrumentUpdateValidationFormView(QuickInlineValidationFormView):
    file_wrapper_class = InstrumentXMLMetadataFile

    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        self.error_dict.update({
            'update_conflicts': MetadataFileUpdateValidator.validate_and_return_errors(
                xml_metadata_file,
                models.Instrument,
                request.POST.get('existing_metadata_id')
            )
        })

        if len(self.error_dict.get('update_conflicts', [])) > 0:
            # Don't continue with instrument operational mode
            # validation if update validation was not successful.
            self.error_dict.update({
                'op_mode_conflicts': ['Could not validate operational modes as metadata file did not pass update validation.'],
                'op_mode_warnings': ['Could not validate operational modes as metadata file did not pass update validation.'],
            })
            return super().validate(request, xml_metadata_file)
        
        self.error_dict.update({
            'op_mode_conflicts': [],
            'op_mode_warnings': [],
        })
        op_mode_validation_results = InstrumentMetadataFileValidator.validate_and_return_results(
            xml_metadata_file,
            request.POST.get('existing_metadata_id')
        )
        if len(op_mode_validation_results.get('acquisition_capabilities_to_update')) == 0:
            return super().validate(request, xml_metadata_file)

        self.error_dict['op_mode_warnings'].append(
            render_to_string(
                'validation/warning_missing_instrument_operational_modes.html',
                context={
                    'missing_operational_mode_urls': op_mode_validation_results.get('missing_operational_mode_urls'),
                    'acquisition_capabilities_update_url_and_url_texts': [
                        (
                            reverse_lazy(f'update:acquisition_capability_set', kwargs={
                                'resource_id': ac.pk,
                            }),
                            f'Update {ac.name}'
                        )
                        for ac in op_mode_validation_results.get('acquisition_capabilities_to_update')
                    ],
                }
            )
        )

        return super().validate(request, xml_metadata_file)


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineAcquisitionCapabilitiesRegistrationValidationFormView(QuickInlineRegistrationValidationFormView):
    file_wrapper_class = AcquisitionCapabilitiesXMLMetadataFile


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineAcquisitionCapabilitiesUpdateValidationFormView(QuickInlineUpdateValidationFormView):
    file_wrapper_class = AcquisitionCapabilitiesXMLMetadataFile


@method_decorator(login_session_institution_required, name='dispatch')
class InlineXSDValidationFormView(FormView):
    form_class = InlineXSDMetadataValidationForm
    error_dict = {}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('The form submitted was not valid.')
        xml_metadata_file = XMLMetadataFile(request.POST.get('xml_file_string'), '')
        self.error_dict.update({
            'xsd_errors': list(),
        })
        xsd_error_unescaped = next(iter(MetadataFileXSDValidator.validate_and_return_errors(xml_metadata_file)), None)
        if not xsd_error_unescaped:
            return JsonResponse(self.error_dict, status=HTTPStatus.OK)

        self.error_dict.update({
            'xsd_errors': [render_to_string(
                'validation/error_xsd_validation_failed.html',
                context={
                    'error': xsd_error_unescaped,
                }
            )],
        })
        
        return JsonResponse(self.error_dict, status=HTTPStatus.BAD_REQUEST)


@require_GET
@login_session_institution_required
def localid(request):
    form = LocalIDValidationForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest('The submitted form was invalid.')
    
    localid = form.cleaned_data.get('localid')
    localid = clean_localid_or_namespace(localid)
    return JsonResponse(MetadataFileRegistrationValidator.check_if_localid_is_already_in_use_and_return_suggestion_if_taken(
        localid
    ))


@require_POST
@login_session_institution_required
def api_specification_url(request):
    response_body = {
        'valid': False
    }
    
    form = ApiSpecificationUrlValidationForm(request.POST)
    if not form.is_valid():
        # Stop further processing if the API specification
        # URL is not valid.
        response_body.update({
            'error': 'Please enter a URL',
        })
        return HttpResponse(json.dumps(response_body), content_type='application/json')

    api_specification_url = request.POST['api_specification_url']
    try:
        validate_spec_url(api_specification_url)
        response_body['valid'] = True
    except HTTPError as err:
        logger.exception('The provided API specification URL returned an HTTP Error 404: Not Found.')
        response_body.update({
            'error': 'The URL was not found',
        })
    except BaseException as err:
        logger.exception('The provided API specification URL does not link to a valid OpenAPI specification.')
        response_body.update({
            'error': 'The URL does not link to a valid OpenAPI specification',
            'details': str(err),
        })
    return HttpResponse(json.dumps(response_body), content_type='application/json')
