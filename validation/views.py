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
    AcquisitionCapabilitiesMetadataFileMetadataURLReferencesValidator,
    MetadataFileMetadataURLReferencesValidator,
)

from common import models
from common.decorators import login_session_institution_required
from common.helpers import clean_localid_or_namespace
from user_management.services import get_institution_id_for_login_session


logger = logging.getLogger(__name__)

# Create your views here.


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineValidationFormView(FormView):
    form_class = QuickInlineMetadataValidationForm
    error_dict = {}
    file_wrapper_class = XMLMetadataFile
    url_references_validator_class = MetadataFileMetadataURLReferencesValidator

    def generate_url_reference_errors_from_validation_results(self, url_references_validation_results: dict) -> dict:
        metadata_url_reference_errors = list()
        invalid_ontology_url_errors = list()

        if url_references_validation_results.get('incorrectly_structured_urls'):
            metadata_url_reference_errors.append(
                render_to_string(
                    'validation/error_incorrectly_structured_urls.html',
                    context={
                        'incorrectly_structured_urls': url_references_validation_results.get('incorrectly_structured_urls'),
                    }
                )
            )

        if url_references_validation_results.get('unregistered_resource_urls'):
            metadata_url_reference_errors.append(
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

        if url_references_validation_results.get('invalid_ontology_urls'):
            invalid_ontology_url_errors.append(
                render_to_string(
                    'validation/error_invalid_ontology_urls.html',
                    context={
                        'invalid_ontology_urls': url_references_validation_results.get('invalid_ontology_urls'),
                    }
                )
            )
        return {
            'metadata_url_reference_errors': metadata_url_reference_errors,
            'invalid_ontology_url_errors': invalid_ontology_url_errors,
        }

    def validate_url_references_and_get_errors(self, xml_metadata_file: XMLMetadataFile):
        url_references_validation_results = self.url_references_validator_class.validate_and_return_results(xml_metadata_file)
        return self.generate_url_reference_errors_from_validation_results(url_references_validation_results)


    def validate(self, request, xml_metadata_file: XMLMetadataFile):
        url_reference_errors = self.validate_url_references_and_get_errors(xml_metadata_file)
        self.error_dict.update(url_reference_errors)

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

        institution_id = get_institution_id_for_login_session(self.request.session)
        acquisition_capabilities_update_url_and_url_texts = [
            (
                reverse_lazy(f'update:acquisition_capability_set', kwargs={
                    'resource_id': ac.pk,
                }),
                f'Update {ac.name}'
            )
            for ac in op_mode_validation_results.get('acquisition_capabilities_to_update')
            if ac.institution_id == institution_id
        ]
        acquisition_capabilities_detail_url_and_url_texts = [
            (
                reverse_lazy(f'browse:acquisition_capability_set_detail', kwargs={
                    'acquisition_capability_set_id': ac.pk,
                }),
                ac.name
            )
            for ac in op_mode_validation_results.get('acquisition_capabilities_to_update')
            if ac.institution_id != institution_id
        ]
        self.error_dict['op_mode_warnings'].append(
            render_to_string(
                'validation/warning_missing_instrument_operational_modes.html',
                context={
                    'missing_operational_mode_urls': op_mode_validation_results.get('missing_operational_mode_urls'),
                    'acquisition_capabilities_update_url_and_url_texts': acquisition_capabilities_update_url_and_url_texts,
                    'acquisition_capabilities_detail_url_and_url_texts': acquisition_capabilities_detail_url_and_url_texts,
                }
            )
        )

        return super().validate(request, xml_metadata_file)


class QuickInlineAcquisitionCapabilitiesValidationFormViewMixin:
    url_references_validator_class = AcquisitionCapabilitiesMetadataFileMetadataURLReferencesValidator

    def generate_url_reference_errors_from_validation_results(self, url_references_validation_results: dict) -> dict:
        url_reference_errors = super().generate_url_reference_errors_from_validation_results(url_references_validation_results)
        if not url_references_validation_results.get('unregistered_operational_mode_urls'):
            return url_reference_errors
        institution_id = get_institution_id_for_login_session(self.request.session)
        instrument_update_url_and_url_texts = [
            (reverse_lazy('update:instrument', kwargs={'resource_id': instrument.pk}), f'Update {instrument.name}')
            for instrument in url_references_validation_results.get('instruments_to_update')
            if instrument.institution_id == institution_id
        ]
        instrument_detail_url_and_url_texts = [
            (reverse_lazy('browse:instrument_detail', kwargs={'instrument_id': instrument.pk}), instrument.name)
            for instrument in url_references_validation_results.get('instruments_to_update')
            if instrument.institution_id != institution_id
        ]
        url_reference_errors['metadata_url_reference_errors'].append(
            render_to_string(
                'validation/error_unregistered_operational_mode_urls.html',
                context={
                    'unregistered_resource_urls': url_references_validation_results.get('unregistered_operational_mode_urls'),
                    'file_upload_registration_url_and_url_texts': instrument_update_url_and_url_texts,
                    'instrument_detail_url_and_url_texts': instrument_detail_url_and_url_texts,
                }
            )
        )
        return url_reference_errors


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineAcquisitionCapabilitiesRegistrationValidationFormView(
        QuickInlineAcquisitionCapabilitiesValidationFormViewMixin,
        QuickInlineRegistrationValidationFormView):
    file_wrapper_class = AcquisitionCapabilitiesXMLMetadataFile


@method_decorator(login_session_institution_required, name='dispatch')
class QuickInlineAcquisitionCapabilitiesUpdateValidationFormView(
        QuickInlineAcquisitionCapabilitiesValidationFormViewMixin,
        QuickInlineUpdateValidationFormView):
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
        # If XSD errors list stays empty, validation has succeeded.
        self.error_dict.update({
            'xsd_errors': list(),
        })
        xsd_error_unescaped = next(iter(
            MetadataFileXSDValidator.validate_and_return_errors(xml_metadata_file)
        ), None)
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
