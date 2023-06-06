import json
from http import HTTPStatus
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.views.decorators.http import require_POST
from django.views.generic import View
from lxml import etree
from openapi_spec_validator import validate_spec_url
from urllib.error import HTTPError

from .file_wrappers import (
    DataSubsetXMLMetadataFile,
    InstrumentXMLMetadataFile,
    XMLMetadataFile,
)
from .forms import ApiSpecificationUrlValidationForm
# TODO: remove old code
# from .metadata_validation import (
#     ACQUISITION_CAPABILITY_XML_ROOT_TAG_NAME,
#     ACQUISITION_XML_ROOT_TAG_NAME,
#     COMPUTATION_CAPABILITY_XML_ROOT_TAG_NAME,
#     COMPUTATION_XML_ROOT_TAG_NAME,
#     DATA_COLLECTION_XML_ROOT_TAG_NAME,
#     INDIVIDUAL_XML_ROOT_TAG_NAME,
#     INSTRUMENT_XML_ROOT_TAG_NAME,
#     OPERATION_XML_ROOT_TAG_NAME,
#     ORGANISATION_XML_ROOT_TAG_NAME,
#     PLATFORM_XML_ROOT_TAG_NAME,
#     PROCESS_XML_ROOT_TAG_NAME,
#     PROJECT_XML_ROOT_TAG_NAME,
#     CATALOGUE_XML_ROOT_TAG_NAME,
#     CATALOGUE_ENTRY_XML_ROOT_TAG_NAME,
#     CATALOGUE_DATA_SUBSET_XML_ROOT_TAG_NAME,
#     validate_xml_file_and_return_summary,
# )
from .helpers import create_validation_summary_error
from .services import validate_xml_file_and_return_summary

from common import models
# TODO: remove old code
# from common.mongodb_models import (
#     CurrentAcquisition,
#     CurrentAcquisitionCapability,
#     CurrentComputation,
#     CurrentComputationCapability,
#     CurrentDataCollection,
#     CurrentIndividual,
#     CurrentInstrument,
#     CurrentOperation,
#     CurrentOrganisation,
#     CurrentPlatform,
#     CurrentProcess,
#     CurrentProject,
#     CurrentCatalogue,
#     CurrentCatalogueEntry,
#     CurrentCatalogueDataSubset,
# )

import logging

logger = logging.getLogger(__name__)

# Create your views here.
class ResourceXmlMetadataFileValidationFormView(View):
    mongodb_model = None
    expected_root_tag_name = ''

    def prepare_xml_metadata_file(self, xml_file):
        return XMLMetadataFile.from_file(xml_file)

    def post(self, request, *args, **kwargs):
        # Extract content from request
        xml_file = request.FILES['file']
        validate_registration = 'validate_is_not_registered' in request.POST
        # validate_update = 'validate_xml_file_localid_matches_existing_resource_localid' in request.POST
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
        # xml_file = request.FILES['file']
        # check_file_is_unregistered = 'validate_is_not_registered' in request.POST
        # check_xml_file_localid_matches_existing_resource_localid = 'validate_xml_file_localid_matches_existing_resource_localid' in request.POST
        # existing_scientific_metadata_id = ''
        # if 'resource_id' in request.POST:
        #     existing_scientific_metadata_id = request.POST['resource_id']
        # validation_summary = validate_xml_file_and_return_summary(
        #     xml_file,
        #     self.expected_root_tag_name,
        #     self.mongodb_model,
        #     check_file_is_unregistered=check_file_is_unregistered,
        #     check_xml_file_localid_matches_existing_resource_localid=check_xml_file_localid_matches_existing_resource_localid,
        #     existing_scientific_metadata_id=existing_scientific_metadata_id
        # )
        # if validation_summary['error'] is None and len(validation_summary['warnings']) == 0:
        #     return HttpResponse(json.dumps({
        #         'result': 'valid'
        #     }), content_type='application/json')

        # response_body = {}
        # if len(validation_summary['warnings']) > 0:
        #     response_body['warnings'] = validation_summary['warnings']
        # if validation_summary['error'] != None:
        #     response_body['error'] = validation_summary['error']
        # return HttpResponseServerError(
        #     json.dumps(response_body),
        #     content_type='application/json'
        # )

class OrganisationXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Organisation
    # mongodb_model = CurrentOrganisation
    # expected_root_tag_name = ORGANISATION_XML_ROOT_TAG_NAME
    
class IndividualXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Individual
    # mongodb_model = CurrentIndividual
    # expected_root_tag_name = INDIVIDUAL_XML_ROOT_TAG_NAME

class ProjectXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Project
    # mongodb_model = CurrentProject
    # expected_root_tag_name = PROJECT_XML_ROOT_TAG_NAME

class PlatformXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Platform
    # TODO: remove old code
    # mongodb_model = CurrentPlatform
    # expected_root_tag_name = PLATFORM_XML_ROOT_TAG_NAME

class OperationXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Operation
    # TODO: remove old code
    # mongodb_model = CurrentOperation
    # expected_root_tag_name = OPERATION_XML_ROOT_TAG_NAME

class InstrumentXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Instrument
    # TODO: remove old code
    # mongodb_model = CurrentInstrument
    # expected_root_tag_name = INSTRUMENT_XML_ROOT_TAG_NAME

    def prepare_xml_metadata_file(xml_file):
        return InstrumentXMLMetadataFile.from_file(xml_file)

class AcquisitionCapabilitiesXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.AcquisitionCapabilities
    # TODO: remove old code
    # mongodb_model = CurrentAcquisitionCapability
    # expected_root_tag_name = ACQUISITION_CAPABILITY_XML_ROOT_TAG_NAME

class AcquisitionXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Acquisition
    # TODO: remove old code
    # mongodb_model = CurrentAcquisition
    # expected_root_tag_name = ACQUISITION_XML_ROOT_TAG_NAME

class ComputationCapabilitiesXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.ComputationCapabilities
    # TODO: remove old code
    # mongodb_model = CurrentComputationCapability
    # expected_root_tag_name = COMPUTATION_CAPABILITY_XML_ROOT_TAG_NAME

class ComputationXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Computation
    # TODO: remove old code
    # mongodb_model = CurrentComputation
    # expected_root_tag_name = COMPUTATION_XML_ROOT_TAG_NAME

class ProcessXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Process
    # TODO: remove old code
    # mongodb_model = CurrentProcess
    # expected_root_tag_name = PROCESS_XML_ROOT_TAG_NAME

class DataCollectionXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.DataCollection
    # TODO: remove old code
    # mongodb_model = CurrentDataCollection
    # expected_root_tag_name = DATA_COLLECTION_XML_ROOT_TAG_NAME


class CatalogueXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.Catalogue
    # TODO: remove old code
    # mongodb_model = CurrentCatalogue
    # expected_root_tag_name = CATALOGUE_XML_ROOT_TAG_NAME


class CatalogueEntryXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.CatalogueEntry
    # TODO: remove old code
    # mongodb_model = CurrentCatalogueEntry
    # expected_root_tag_name = CATALOGUE_ENTRY_XML_ROOT_TAG_NAME


class CatalogueDataSubsetXmlMetadataFileValidationFormView(ResourceXmlMetadataFileValidationFormView):
    model = models.CatalogueDataSubset
    # TODO: remove old code
    # mongodb_model = CurrentCatalogueDataSubset
    # expected_root_tag_name = CATALOGUE_DATA_SUBSET_XML_ROOT_TAG_NAME

    def prepare_xml_metadata_file(xml_file):
        return DataSubsetXMLMetadataFile.from_file(xml_file)


@require_POST
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
