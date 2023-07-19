import json
import logging
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import View
from http import HTTPStatus
from lxml import etree
from openapi_spec_validator import validate_spec_url
from urllib.error import HTTPError

from .file_wrappers import (
    AcquisitionCapabilitiesXMLMetadataFile,
    DataSubsetXMLMetadataFile,
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .forms import ApiSpecificationUrlValidationForm
from .helpers import create_validation_summary_error
from .services import validate_xml_file_and_return_summary

from common import models
from common.decorators import login_session_institution_required


logger = logging.getLogger(__name__)

# Create your views here.
@method_decorator(login_session_institution_required, name='dispatch')
class ResourceXmlMetadataFileValidationFormView(View):
    def prepare_xml_metadata_file(self, xml_file):
        return XMLMetadataFile.from_file(xml_file)

    def post(self, request, *args, **kwargs):
        # Extract content from request
        xml_file = request.FILES['file']
        validate_registration = 'validate_is_not_registered' in request.POST
        existing_scientific_metadata_id = request.POST['resource_id'] if 'resource_id' in request.POST else None
        
        # Begin the validation process
        validation_summary = {}
        try:
            # Syntax validation
            prepared_xml_metadata_file = self.prepare_xml_metadata_file(xml_file)
        except etree.XMLSyntaxError as err:
            logger.exception('An exception occurred whilst parsing the XML.')
            validation_summary['error'] = create_validation_summary_error(
                message='Syntax is invalid.',
                details=str(err)
            )
            return JsonResponse(validation_summary, status=HTTPStatus.BAD_REQUEST)

        try:
            validation_summary = validate_xml_file_and_return_summary(
                prepared_xml_metadata_file,
                self.model,
                validate_for_registration=validate_registration,
                metadata_id_to_validate_for_update=existing_scientific_metadata_id
            )
        except BaseException as err:
            logger.exception('An exception occurred during metadata file validation.')
            validation_summary['error'] = create_validation_summary_error(details=str(err))
            return JsonResponse(validation_summary, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        # Process any errors not handled by the try-except block
        if (validation_summary['error'] is None
            and len(validation_summary['warnings']) == 0):
            return JsonResponse({
                'result': 'valid',
            })

        response_body = {}
        if len(validation_summary['warnings']) > 0:
            response_body['warnings'] = validation_summary['warnings']
        if validation_summary['error'] != None:
            response_body['error'] = validation_summary['error']
        return JsonResponse(response_body, status=HTTPStatus.BAD_REQUEST)

class OrganisationXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Organisation
    
class IndividualXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Individual

class ProjectXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Project

class PlatformXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Platform

class OperationXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Operation

class InstrumentXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Instrument

    def prepare_xml_metadata_file(self, xml_file):
        return InstrumentXMLMetadataFile.from_file(xml_file)

class AcquisitionCapabilitiesXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.AcquisitionCapabilities

    def prepare_xml_metadata_file(self, xml_file):
        return AcquisitionCapabilitiesXMLMetadataFile.from_file(xml_file)

class AcquisitionXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Acquisition

class ComputationCapabilitiesXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.ComputationCapabilities

class ComputationXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Computation

class ProcessXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Process

class DataCollectionXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.DataCollection

class CatalogueXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Catalogue

class CatalogueEntryXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.CatalogueEntry

class CatalogueDataSubsetXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.CatalogueDataSubset

    def prepare_xml_metadata_file(self, xml_file):
        return DataSubsetXMLMetadataFile.from_file(xml_file)


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
