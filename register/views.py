from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .file_upload import handle_uploaded_file

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/register/')
    else:
        form = UploadFileForm()
    return render(request, 'register/index.html', {
        'form': form.as_p()
    })