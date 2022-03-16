from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import UploadFileForm
from utils import db
import json
import xmltodict

# Create your views here.
class RegisterView(FormView):
    form_class = UploadFileForm
    template_name = 'register/index.html'
    success_url = '/register/'

    def post(self, request, *args, **kwargs):
        form_class = self.form_class
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            xmls_as_dicts = []
            for f in files:
                observation_collections = db['observation_collections']
                xml = f.read()
                # Convert XML to a dictionary to be able to convert it JSON
                xml_as_dict = xmltodict.parse(xml)
                # Convert the dictionary to JSON
                xml_as_json = json.dumps(xml_as_dict)
                # Some formatting to get rid of '\n' characters and extra
                # whitespace within strings
                xml_as_json = xml_as_json.replace('\\n', '')
                xml_as_json = ' '.join(xml_as_json.split())
                # pymongo takes dictionaries when inserting new documents,
                # so convert the JSON back to a dictionary
                xml_as_dict = json.loads(xml_as_dict)
                # DEBUG: Print out the resulting dictionary
                print(json.dumps(xml_as_dict['ObservationCollection'], indent=2, sort_keys=True))
                # Add the dictionary to the list of dictionaries to be inserted
                # into the database.
                xmls_as_dicts.append(xml_as_dict['ObservationCollection'])
            # Insert the dictionaries into the 'observation_collections' collection
            observation_collections.insert_many(xmls_as_dicts)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register Models/Datasets'
        return context