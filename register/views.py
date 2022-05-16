import json
from lxml import etree
from pyexpat import ExpatError
from pyexpat.errors import XML_ERROR_SYNTAX
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse

from register import validation

from .forms import UploadFileForm
from .metadata_helpers import handle_uploaded_metadata

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
        is_xml_conforming_to_schema = validation.validate_xml_file_by_type(xml_file_parsed, metadata_upload_type)
        # 3: Relation validaiton (whether a component the file metadata
        # is referencing exists in the database or not).
    except etree.XMLSyntaxError as err:
        print(err)
        return HttpResponse(json.dumps({
            'error': str(err)
        }), status=422, content_type='application/json')
    except BaseException as err:
        print(err)
        return HttpResponseServerError(json.dumps({
            'error': str(err)
        }), content_type='application/json')
    return HttpResponse(json.dumps({
        'result': is_xml_conforming_to_schema
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
        'model-or-measurement',
    ]
    if metadata_upload_type not in valid_metadata_upload_types:
        raise Http404
    if request.method == 'POST':
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            # XML Schema validation
            try:
                uploaded_file_stats = handle_uploaded_metadata(files, request.POST)
            except ExpatError as err:
                print('There was an error whilst parsing the XML: {0}'.format(err))
                return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]) + '?error=ExpatError')
            except BaseException as err:
                print('An unexpected error occurred: {0}'.format(err))
                return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]) + '?error=500')

            query_string = '?'
            if uploaded_file_stats['acq_files_uploaded'] > 0:
                query_string += f'acq_files_uploaded={uploaded_file_stats["acq_files_uploaded"]}'
            if uploaded_file_stats['comp_files_uploaded'] > 0:
                query_string += f'comp_files_uploaded={uploaded_file_stats["comp_files_uploaded"]}'
            if uploaded_file_stats['op_files_uploaded'] > 0:
                query_string += f'op_files_uploaded={uploaded_file_stats["op_files_uploaded"]}'
            if uploaded_file_stats['proc_files_uploaded'] > 0:
                query_string += f'proc_files_uploaded={uploaded_file_stats["proc_files_uploaded"]}'
            print(query_string)
            return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]) + query_string)
        else:
            return HttpResponseRedirect(reverse('register:metadata_upload', args=[metadata_upload_type]))
    else:
        form = UploadFileForm()
    return render(request, 'register/metadata_upload.html', {
        'metadata_upload_type': metadata_upload_type,
        'form': form
    })
