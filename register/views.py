from pyexpat import ExpatError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import UploadFileForm
from .metadata_upload import convert_and_upload_xml_file

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            try:
                uploaded_file_stats = convert_and_upload_xml_file(files, request.POST)
            except ExpatError as err:
                print("There was an error whilst parsing the XML: {0}".format(err))
                return HttpResponseRedirect(reverse('register:index') + '?error=ExpatError')
            except BaseException as err:
                print("An unexpected error occurred: {0}".format(err))
                return HttpResponseRedirect(reverse('register:index') + '?error=500')

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
            return HttpResponseRedirect(reverse('register:index') + query_string)
        else:
            return HttpResponseRedirect(reverse('register:index'))
    else:
        form = UploadFileForm
    return render(request, 'register/index.html', {
        'title': 'Register Models & Measurements',
        'form': form
    })