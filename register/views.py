from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import UploadFileForm
from .metadata_helpers import handle_uploaded_metadata

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            uploaded_file_stats = handle_uploaded_metadata(files)
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
        'title': 'Register Models/Data Collections',
        'form': form
    })