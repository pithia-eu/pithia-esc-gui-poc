import traceback
from pyexpat import ExpatError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView
from register.register import register_metadata_xml_file

from validation.validation import validate_acquisition_metadata_xml_file, validate_computation_metadata_xml_file, validate_data_collection_metadata_xml_file, validate_individual_metadata_xml_file, validate_instrument_metadata_xml_file, validate_operation_metadata_xml_file, validate_organisation_metadata_xml_file, validate_platform_metadata_xml_file, validate_process_metadata_xml_file, validate_project_metadata_xml_file
from .forms import UploadFileForm
from register import xml_conversion_checks_and_fixes
from common import mongodb_models

# Create your views here.
def index(request):
    return render(request, 'register/index.html', {
        'title': 'Resource Metadata Registration'
    })

class RegisterResourceFormView(FormView):
    resource_mongodb_model = None
    validate_resource = None
    resource_conversion_validate_and_correct_function = None
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    a_or_an = ''
    resource_type = ''
    validation_url = ''
    post_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.a_or_an} {self.resource_type.title()}'
        context['validation_url'] = self.validation_url
        context['post_url'] = self.post_url
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        xml_file = request.FILES['file']
        if form.is_valid():
            # XML should have already been validated at
            # the template, but do it again just to be
            # safe.
            validation_results = self.validate_resource(xml_file)
            if 'error' not in validation_results:
                try:
                    registration_results = register_metadata_xml_file(xml_file, self.resource_mongodb_model, self.resource_conversion_validate_and_correct_function)
                    if registration_results == 'This XML metadata file has been registered before.':
                        messages.error(request, registration_results)
                except ExpatError as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An error occurred whilst parsing the XML.')
                except BaseException as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An unexpected error occurred.')

                messages.success(request, f'Successfully registered {xml_file.name}.')
            else:
                messages.error(request, 'The file submitted was not valid.')
        else:
            messages.error(request, 'The form submitted was not valid.')
        return super().post(request, *args, **kwargs)

class organisation(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    validate_resource = validate_organisation_metadata_xml_file
    success_url = reverse_lazy('register:organisation')

    a_or_an = 'an'
    resource_type = 'organisation'
    validation_url = reverse_lazy('validation:organisation')
    post_url = reverse_lazy('register:organisation')

class individual(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    validate_resource = validate_individual_metadata_xml_file
    success_url = reverse_lazy('register:individual')

    a_or_an = 'an'
    resource_type = 'individual'
    validation_url = reverse_lazy('validation:individual')
    post_url = reverse_lazy('register:individual')

class project(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentProject
    validate_resource = validate_project_metadata_xml_file
    success_url = reverse_lazy('register:project')

    a_or_an = 'a'
    resource_type = 'project'
    validation_url = reverse_lazy('validation:project')
    post_url = reverse_lazy('register:project')

class platform(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    validate_resource = validate_platform_metadata_xml_file
    success_url = reverse_lazy('register:platform')

    a_or_an = 'a'
    resource_type = 'platform'
    validation_url = reverse_lazy('validation:platform')
    post_url = reverse_lazy('register:platform')

class instrument(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    validate_resource = validate_instrument_metadata_xml_file
    success_url = reverse_lazy('register:instrument')

    a_or_an = 'an'
    resource_type = 'instrument'
    validation_url = reverse_lazy('validation:instrument')
    post_url = reverse_lazy('register:instrument')

class operation(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    validate_resource = validate_operation_metadata_xml_file
    success_url = reverse_lazy('register:operation')

    a_or_an = 'an'
    resource_type = 'operation'
    validation_url = reverse_lazy('validation:operation')
    post_url = reverse_lazy('register:operation')

class acquisition(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    validate_resource = validate_acquisition_metadata_xml_file
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_acquisition_dictionary
    success_url = reverse_lazy('register:acquisition')

    a_or_an = 'an'
    resource_type = 'acquisition'
    validation_url = reverse_lazy('validation:acquisition')
    post_url = reverse_lazy('register:acquisition')

class computation(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    validate_resource = validate_computation_metadata_xml_file
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_computation_dictionary
    success_url = reverse_lazy('register:computation')

    a_or_an = 'a'
    resource_type = 'computation'
    validation_url = reverse_lazy('validation:computation')
    post_url = reverse_lazy('register:computation')

class process(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    validate_resource = validate_process_metadata_xml_file
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_process_dictionary
    success_url = reverse_lazy('register:process')

    a_or_an = 'a'
    resource_type = 'process'
    validation_url = reverse_lazy('validation:process')
    post_url = reverse_lazy('register:process')

class data_collection(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    validate_resource = validate_data_collection_metadata_xml_file
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_data_collection_dictionary
    success_url = reverse_lazy('register:data_collection')

    a_or_an = 'a'
    resource_type = 'data collection'
    validation_url = reverse_lazy('validation:data_collection')
    post_url = reverse_lazy('register:data_collection')
