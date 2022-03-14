from django.http import HttpResponseRedirect
from django.shortcuts import render
from register.forms import UploadFileForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/register/')
    else:
        form = UploadFileForm()
    return render(request, 'register/index.html', {
        'form': form
    })