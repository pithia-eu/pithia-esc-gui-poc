import json
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.http import require_POST
from lxml import etree

from validation.validation import validate_acquisition_metadata_xml_file, validate_computation_metadata_xml_file, validate_data_collection_metadata_xml_file, validate_individual_metadata_xml_file, validate_instrument_metadata_xml_file, validate_operation_metadata_xml_file, validate_organisation_metadata_xml_file, validate_platform_metadata_xml_file, validate_process_metadata_xml_file, validate_project_metadata_xml_file

# Create your views here.
def process_validation_results_and_send_httpresponse(request, validation_results):
    if 'error' not in validation_results:
        return HttpResponse(json.dumps({
            'result': 'valid'
        }), content_type='application/json')
    if validation_results['error']['type'] == etree.DocumentInvalid or validation_results['error']['type'] == etree.XMLSyntaxError:
        return HttpResponse(json.dumps({ 'error': validation_results['error'] }), status=422, content_type='application/json')
    return HttpResponseServerError(json.dumps({ 'error': validation_results['error'] }), content_type='application/json')

@require_POST
def organisation(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_organisation_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)
    
@require_POST
def individual(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_individual_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def project(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_project_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def platform(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_platform_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def instrument(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_instrument_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def operation(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_operation_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def acquisition(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_acquisition_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def computation(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_computation_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def process(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_process_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)

@require_POST
def data_collection(request):
    xml_file = request.FILES['file']
    xml_file_validation_results = validate_data_collection_metadata_xml_file(xml_file)
    return process_validation_results_and_send_httpresponse(request, xml_file_validation_results)