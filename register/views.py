from django.http import HttpResponseRedirect
from django.shortcuts import render
from register.forms import UploadFileForm
from .helpers import handle_uploaded_file
import json
import xmltodict
from pymongo import MongoClient

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            with request.FILES['file'] as file:
                xml = file.read()
                dict = xmltodict.parse(xml)
                json_dict = json.dumps(dict)
                json_dict = json_dict.replace('\\n', '')
                json_dict = ' '.join(json_dict.split())
                json_dict = json.loads(json_dict)
                print(json.dumps(json_dict, indent=4, sort_keys=True))

            return HttpResponseRedirect('/register/')
    else:
        form = UploadFileForm()
    return render(request, 'register/index.html', {
        'form': form
    })