import json
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.views.generic import View
from lxml import etree
from common.mongodb_models import CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject

from validation.metadata_validation import _create_validation_error_details_dict, validate_acquisition_metadata_xml_file, validate_computation_metadata_xml_file, validate_data_collection_metadata_xml_file, validate_individual_metadata_xml_file, validate_instrument_metadata_xml_file, validate_operation_metadata_xml_file, validate_organisation_metadata_xml_file, validate_platform_metadata_xml_file, validate_process_metadata_xml_file, validate_project_metadata_xml_file
from validation.registration_validation import validate_xml_file_is_unique
from validation.update_validation import validate_xml_file_localid_matches_existing_resource_localid

# Create your views here.
class ValidateXmlMetadataFileFormView(View):
    validate_xml_metadata_file = None
    mongodb_model = None

    def post(self, request, *args, **kwargs):
        xml_file = request.FILES['file']
        validation_results = self.validate_xml_metadata_file(xml_file)
        if 'validate_is_not_registered' in request.POST:
            validation_results['is_new_registration'] = False
            if validate_xml_file_is_unique(self.mongodb_model, xml_file=xml_file):
                validation_results['is_new_registration'] = True
            else:
                validation_results['error'] = _create_validation_error_details_dict(type(BaseException()), 'This XML metadata file has been registered before.', None)
        if 'validate_xml_file_localid_matches_existing_resource_localid' in request.POST:
            validation_results['is_xml_file_localid_matching_with_existing_resource_localid'] = False
            if validate_xml_file_localid_matches_existing_resource_localid(self.mongodb_model, request.POST['resource_id'], xml_file=xml_file):
                validation_results['is_xml_file_localid_matching_with_existing_resource_localid'] = True
            else:
                validation_results['error'] = _create_validation_error_details_dict(type(BaseException()), 'The localID and namespace must be matching with the resource being updated.', None)
        if 'error' not in validation_results:
            return HttpResponse(json.dumps({
                'result': 'valid'
            }), content_type='application/json')
        if validation_results['error']['type'] == etree.DocumentInvalid or validation_results['error']['type'] == etree.XMLSyntaxError:
            return HttpResponse(json.dumps({ 'error': validation_results['error'] }), status=422, content_type='application/json')
        return HttpResponseServerError(json.dumps({ 'error': validation_results['error'] }), content_type='application/json')

class organisation(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_organisation_metadata_xml_file
    mongodb_model = CurrentOrganisation
    
class individual(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_individual_metadata_xml_file
    mongodb_model = CurrentIndividual

class project(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_project_metadata_xml_file
    mongodb_model = CurrentProject

class platform(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_platform_metadata_xml_file
    mongodb_model = CurrentPlatform

class instrument(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_instrument_metadata_xml_file
    mongodb_model = CurrentInstrument

class operation(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_operation_metadata_xml_file
    mongodb_model = CurrentOperation

class acquisition(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_acquisition_metadata_xml_file
    mongodb_model = CurrentAcquisition

class computation(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_computation_metadata_xml_file
    mongodb_model = CurrentComputation

class process(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_process_metadata_xml_file
    mongodb_model = CurrentProcess

class data_collection(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_data_collection_metadata_xml_file
    mongodb_model = CurrentDataCollection