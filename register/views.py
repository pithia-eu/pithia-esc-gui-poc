import json
import traceback
from lxml import etree
from pyexpat import ExpatError
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from register import validation
from register.exceptions import MetadataFileNotForResourceTypeException, UnregisteredXlinkHrefsException

from .forms import UploadFileForm
from .resource_metadata_upload import convert_and_upload_xml_file

# Create your views here.
def index(request):
    return render(request, 'register/index.html', {
        'title': 'Resource Metadata Registration',
    })

def create_error_response_body(err_class, err_message, err_extra_details):
    return {
        'error': {
            'type': str(err_class),
            'message': err_message,
            'extra_details': err_extra_details
        }
    }

def validate_xml_file_by_resource_type(request, resource_type):
    if request.method != 'POST':
        return Http404
    # Run three validations on XML file
    xml_file = request.FILES['file']
    try:
        # Syntax validation (happens whilst parsing the file)
        xml_file_parsed = validation.parse_xml_file(xml_file)
        # Resource type validation
        is_xml_matching_resource_type = validation.validate_xml_matches_submitted_resource_type(xml_file_parsed, resource_type)
        if not is_xml_matching_resource_type:
            raise MetadataFileNotForResourceTypeException("The metadata file does not match the type of resource being registered.")
        # XML Schema Definition validation
        xml_schema_for_type_file_path = validation.get_xml_schema_file_path_for_resource_type(resource_type)
        schema_validation_result = validation.validate_xml_against_schema(xml_file_parsed, xml_schema_for_type_file_path)
        # Relation validaiton (whether a resource the metadata file
        # is referencing exists in the database or not).
        unregistered_referenced_resource_hrefs, unregistered_referenced_resource_types = validation.get_unregistered_referenced_resources_from_xml(xml_file_parsed)
        if len(unregistered_referenced_resource_hrefs) > 0:
            # "Exception" is handled here to be able to pass more
            # information to the error response body.
            err_class = UnregisteredXlinkHrefsException
            response_body = create_error_response_body(
                err_class,
                'Unregistered resource IRIs: %s.' % ', '.join(unregistered_referenced_resource_hrefs),
                {
                    'unregistered_referenced_resource_types': unregistered_referenced_resource_types
                }
            )
            response_body_json = json.dumps(response_body)
            return HttpResponse(response_body_json, status=422, content_type='application/json')
    except BaseException as err:
        print(traceback.format_exc())
        err_class = type(err)
        response_body = create_error_response_body(err_class, str(err), {})
        response_body_json = json.dumps(response_body)
        if err_class == etree.DocumentInvalid or err_class == etree.XMLSyntaxError:
            return HttpResponse(response_body_json, status=422, content_type='application/json')
        return HttpResponseServerError(response_body_json, content_type='application/json')
    return HttpResponse(json.dumps({
        'result': schema_validation_result
    }), content_type='application/json')

def resource_metadata_upload(request, resource_type):
    # There's probably a DRY-er way of handling
    # 'valid resource upload types'
    valid_resource_types = [
        'organisation',
        'individual',
        'project',
        'platform',
        'operation',
        'instrument',
        'acquisition',
        'computation',
        'process',
        'data-collection',
    ]
    if resource_type not in valid_resource_types:
        raise Http404
    if request.method == 'POST':
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        xml_file = request.FILES['file']
        if form.is_valid():
            # XML should have already been validated
            # when uploading in the front-end.
            try:
                result = convert_and_upload_xml_file(xml_file, resource_type)
                if result == 'Resource type not supported.':
                    messages.error(request, 'The type of resource you are trying to register is not currently supported.')
                    return HttpResponseRedirect(reverse('register:resource_metadata_upload', args=[resource_type]))
            except ExpatError as err:
                print(err)
                messages.error(request, 'An error occurred whilst parsing the XML.')
                return HttpResponseRedirect(reverse('register:resource_metadata_upload', args=[resource_type]))
            except BaseException as err:
                print(err)
                messages.error(request, 'An unexpected error occurred.')
                return HttpResponseRedirect(reverse('register:resource_metadata_upload', args=[resource_type]))

            messages.success(request, f'Successfully registered {xml_file.name}.')
            return HttpResponseRedirect(reverse('register:resource_metadata_upload', args=[resource_type]))
        else:
            messages.error(request, 'The form submitted was not valid.')
            return HttpResponseRedirect(reverse('register:resource_metadata_upload', args=[resource_type]))
    else:
        form = UploadFileForm()
        title = f'Register a {resource_type.capitalize()}'
        if resource_type[0].lower() in 'aeiou':
            title = f'Register an {resource_type.capitalize()}'
        if resource_type.lower() == 'data-collection':
            title = 'Register a Model or Measurement'
    return render(request, 'register/resource_metadata_upload.html', {
        'title': title,
        'resource_type': resource_type,
        'form': form
    })
