import json
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from django.views.generic import View
from lxml import etree

from validation.metadata_validation import validate_acquisition_metadata_xml_file, validate_computation_metadata_xml_file, validate_data_collection_metadata_xml_file, validate_individual_metadata_xml_file, validate_instrument_metadata_xml_file, validate_operation_metadata_xml_file, validate_organisation_metadata_xml_file, validate_platform_metadata_xml_file, validate_process_metadata_xml_file, validate_project_metadata_xml_file

# Create your views here.
class ValidateXmlMetadataFileFormView(View):
    validate_xml_metadata_file = None

    def post(self, request, *args, **kwargs):
        xml_file = request.FILES['file']
        validation_results = self.validate_xml_metadata_file(xml_file)
        if 'error' not in validation_results:
            return HttpResponse(json.dumps({
                'result': 'valid'
            }), content_type='application/json')
        if validation_results['error']['type'] == etree.DocumentInvalid or validation_results['error']['type'] == etree.XMLSyntaxError:
            return HttpResponse(json.dumps({ 'error': validation_results['error'] }), status=422, content_type='application/json')
        return HttpResponseServerError(json.dumps({ 'error': validation_results['error'] }), content_type='application/json')

class organisation(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_organisation_metadata_xml_file
    
class individual(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_individual_metadata_xml_file

class project(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_project_metadata_xml_file

class platform(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_platform_metadata_xml_file

class instrument(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_instrument_metadata_xml_file

class operation(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_operation_metadata_xml_file

class acquisition(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_acquisition_metadata_xml_file

class computation(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_computation_metadata_xml_file

class process(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_process_metadata_xml_file

class data_collection(ValidateXmlMetadataFileFormView):
    validate_xml_metadata_file = validate_data_collection_metadata_xml_file