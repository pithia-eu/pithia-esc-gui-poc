from pyexpat import ExpatError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .forms import UploadFileForm
from .resource_metadata_upload import convert_and_upload_xml_file

# Create your views here.
def index(request):
    return render(request, 'register/index.html', {
        'title': 'Resource Metadata Registration',
    })

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
        'validation_url': reverse(f'validation:{resource_type}'),
        'form': form
    })
