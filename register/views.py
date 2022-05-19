from atexit import register
import json
from ntpath import join
import traceback
from lxml import etree
from pyexpat import ExpatError
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from register import validation
from register.exceptions import UnregisteredXlinkHrefsException

from .forms import UploadFileForm
from .metadata_upload import convert_and_upload_xml_file

# Create your views here.
def index(request):
    return render(request, 'register/index.html', {
        'title': 'Register Models & Measurements',
    })

def validate_xml_file_by_type(request, metadata_upload_type):
    if request.method != 'POST':
        return Http404
    # Run three validations on XML file
    xml_file = request.FILES['file']
    try:
        # 1: Syntax validation (happens whilst parsing the file)
        xml_file_parsed = validation.parse_xml_file(xml_file)
        # 2: XML Schema Definition validation
        xml_schema_for_type_file_path = validation.get_xml_schema_file_path_by_type(metadata_upload_type)
        schema_validation_result = validation.validate_xml_against_schema(xml_file_parsed, xml_schema_for_type_file_path)
        # 3: Relation validaiton (whether a component the file metadata
        # is referencing exists in the database or not).
        missing_xlinks = validation.validate_xml_xlinks_by_type(xml_file_parsed, metadata_upload_type)
        if len(missing_xlinks) > 0:
            raise UnregisteredXlinkHrefsException('Unregistered resource IRIs: %s.' % ', '.join(missing_xlinks))
    except BaseException as err:
        print(traceback.format_exc())
        err_class = type(err)
        response_body = json.dumps({
            'errorType': str(err_class),
            'error': str(err)
        })
        if err_class == etree.DocumentInvalid or err_class == etree.XMLSyntaxError or err_class == UnregisteredXlinkHrefsException:
            return HttpResponse(response_body, status=422, content_type='application/json')
        return HttpResponseServerError(response_body, content_type='application/json')
    return HttpResponse(json.dumps({
        'result': schema_validation_result
    }), content_type='application/json')

def metadata_upload(request, metadata_upload_type):
    # There's probably a DRY-er way of handling
    # 'valid metadata upload types'
    valid_metadata_upload_types = [
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
    if metadata_upload_type not in valid_metadata_upload_types:
        raise Http404
    if request.method == 'POST':
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        xml_file = request.FILES['file']
        if form.is_valid():
            # XML should have already been validated
            # when uploading in the front-end.
            try:
                result = convert_and_upload_xml_file(xml_file, metadata_upload_type)
                if result == 'Metadata type not supported.':
                    messages.error(request, 'The metadata file submitted is not currently supported.')
                    return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]))
            except ExpatError as err:
                print(err)
                messages.error(request, 'An error occurred whilst parsing the XML.')
                return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]))
            except BaseException as err:
                print(err)
                messages.error(request, 'An unexpected error occurred.')
                return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]))

            messages.success(request, f'Successfully registered {xml_file.name}.')
            return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]))
        else:
            messages.error(request, 'The form submitted was not valid.')
            return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]))
    else:
        form = UploadFileForm()
    return render(request, 'register/metadata_upload.html', {
        'metadata_upload_type': metadata_upload_type,
        'form': form
    })
