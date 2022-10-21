import json
from django.http import HttpResponse, HttpResponseServerError
from django.views.generic import View
from lxml import etree
from common.mongodb_models import CurrentAcquisition, CurrentAcquisitionCapability, CurrentComputation, CurrentComputationCapability, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject

from validation.metadata_validation import ACQUISITION_CAPABILITY_XML_ROOT_TAG_NAME, ACQUISITION_XML_ROOT_TAG_NAME, COMPUTATION_CAPABILITY_XML_ROOT_TAG_NAME, COMPUTATION_XML_ROOT_TAG_NAME, DATA_COLLECTION_XML_ROOT_TAG_NAME, INDIVIDUAL_XML_ROOT_TAG_NAME, INSTRUMENT_XML_ROOT_TAG_NAME, OPERATION_XML_ROOT_TAG_NAME, ORGANISATION_XML_ROOT_TAG_NAME, PLATFORM_XML_ROOT_TAG_NAME, PROCESS_XML_ROOT_TAG_NAME, PROJECT_XML_ROOT_TAG_NAME, validate_xml_metadata_file

# Create your views here.
class ValidateXmlMetadataFileFormView(View):
    mongodb_model = None
    expected_root_tag_name = ''

    def post(self, request, *args, **kwargs):
        xml_file = request.FILES['file']
        check_file_is_unregistered = 'validate_is_not_registered' in request.POST
        check_xml_file_localid_matches_existing_resource_localid = 'validate_xml_file_localid_matches_existing_resource_localid' in request.POST
        existing_resource_id = ''
        if 'resource_id' in request.POST:
            existing_resource_id = request.POST['resource_id']
        validation_results = validate_xml_metadata_file(xml_file, self.expected_root_tag_name, mongodb_model=self.mongodb_model, check_file_is_unregistered=check_file_is_unregistered, check_xml_file_localid_matches_existing_resource_localid=check_xml_file_localid_matches_existing_resource_localid, existing_resource_id=existing_resource_id)
        if 'error' not in validation_results:
            return HttpResponse(json.dumps({
                'result': 'valid'
            }), content_type='application/json')
        if validation_results['error']['type'] == etree.DocumentInvalid or validation_results['error']['type'] == etree.XMLSyntaxError:
            return HttpResponse(json.dumps({ 'error': validation_results['error'] }), status=422, content_type='application/json')
        return HttpResponseServerError(json.dumps({ 'error': validation_results['error'] }), content_type='application/json')

class organisation(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentOrganisation
    expected_root_tag_name = ORGANISATION_XML_ROOT_TAG_NAME
    
class individual(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentIndividual
    expected_root_tag_name = INDIVIDUAL_XML_ROOT_TAG_NAME

class project(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentProject
    expected_root_tag_name = PROJECT_XML_ROOT_TAG_NAME

class platform(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentPlatform
    expected_root_tag_name = PLATFORM_XML_ROOT_TAG_NAME

class instrument(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentInstrument
    expected_root_tag_name = INSTRUMENT_XML_ROOT_TAG_NAME

class operation(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentOperation
    expected_root_tag_name = OPERATION_XML_ROOT_TAG_NAME

class acquisition_capability(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentAcquisitionCapability
    expected_root_tag_name = ACQUISITION_CAPABILITY_XML_ROOT_TAG_NAME

class acquisition(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentAcquisition
    expected_root_tag_name = ACQUISITION_XML_ROOT_TAG_NAME

class computation_capability(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentComputationCapability
    expected_root_tag_name = COMPUTATION_CAPABILITY_XML_ROOT_TAG_NAME

class computation(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentComputation
    expected_root_tag_name = COMPUTATION_XML_ROOT_TAG_NAME

class process(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentProcess
    expected_root_tag_name = PROCESS_XML_ROOT_TAG_NAME

class data_collection(ValidateXmlMetadataFileFormView):
    mongodb_model = CurrentDataCollection
    expected_root_tag_name = DATA_COLLECTION_XML_ROOT_TAG_NAME