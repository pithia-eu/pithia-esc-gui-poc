import traceback
from pyexpat import ExpatError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView
from register.register import register_metadata_xml_file

from .forms import UploadFileForm
from register import xml_conversion_checks_and_fixes
from common import mongodb_models
from resource_management.views import _INDEX_PAGE_TITLE


# Create your views here.
def index(request):
    return render(request, 'register/index.html', {
        'title': _INDEX_PAGE_TITLE
    })

class RegisterResourceFormView(FormView):
    resource_mongodb_model = None
    resource_conversion_validate_and_correct_function = None
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    a_or_an = ''
    resource_type = ''
    resource_type_plural = ''
    validation_url = ''
    post_url = ''
    index_page_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.resource_type_plural.title()}'
        context['index_page_title'] = _INDEX_PAGE_TITLE
        context['index_page_url_name'] = self.index_page_url_name
        context['validation_url'] = self.validation_url
        context['post_url'] = self.post_url
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        xml_files = request.FILES.getlist('files')
        if form.is_valid():
            for xml_file in xml_files:
                # XML should have already been validated at
                # the template, and validation could take
                # place again, but takes a long time. Another
                # method which verifies validation took place
                # should be implemented.
                try:
                    registration_results = register_metadata_xml_file(xml_file, self.resource_mongodb_model, self.resource_conversion_validate_and_correct_function)
                    if registration_results == 'This XML metadata file has been registered before.':
                        messages.error(request, f'{xml_file.name} has been registered before.')
                    else:
                        messages.success(request, f'Successfully registered {xml_file.name}.')
                except ExpatError as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, f'An error occurred whilst parsing {xml_file.name}.')
                except BaseException as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An unexpected error occurred.')
                # validation_results = self.validate_resource(xml_file)
                # if 'error' not in validation_results:
                # else:
                #     messages.error(request, 'The file submitted was not valid.')
        else:
            messages.error(request, 'The form submitted was not valid.')
        return super().post(request, *args, **kwargs)

class organisation(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    success_url = reverse_lazy('register:organisation')

    a_or_an = 'an'
    resource_type = 'organisation'
    resource_type_plural = 'organisations'
    validation_url = reverse_lazy('validation:organisation')
    post_url = reverse_lazy('register:organisation')
    index_page_url_name = 'resource_management:organisations'

class individual(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    success_url = reverse_lazy('register:individual')

    a_or_an = 'an'
    resource_type = 'individual'
    resource_type_plural = 'individuals'
    validation_url = reverse_lazy('validation:individual')
    post_url = reverse_lazy('register:individual')
    index_page_url_name = 'resource_management:individuals'

class project(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentProject
    success_url = reverse_lazy('register:project')

    a_or_an = 'a'
    resource_type = 'project'
    resource_type_plural = 'projects'
    validation_url = reverse_lazy('validation:project')
    post_url = reverse_lazy('register:project')
    index_page_url_name = 'resource_management:projects'

class platform(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    success_url = reverse_lazy('register:platform')

    a_or_an = 'a'
    resource_type = 'platform'
    resource_type_plural = 'platforms'
    validation_url = reverse_lazy('validation:platform')
    post_url = reverse_lazy('register:platform')
    index_page_url_name = 'resource_management:platforms'

class instrument(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    success_url = reverse_lazy('register:instrument')

    a_or_an = 'an'
    resource_type = 'instrument'
    resource_type_plural = 'instruments'
    validation_url = reverse_lazy('validation:instrument')
    post_url = reverse_lazy('register:instrument')
    index_page_url_name = 'resource_management:instruments'

class operation(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    success_url = reverse_lazy('register:operation')

    a_or_an = 'an'
    resource_type = 'operation'
    resource_type_plural = 'operations'
    validation_url = reverse_lazy('validation:operation')
    post_url = reverse_lazy('register:operation')
    index_page_url_name = 'resource_management:operations'

class acquisition_capability(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    success_url = reverse_lazy('register:acquisition_capability')

    a_or_an = 'an'
    resource_type = 'acquisition capability'
    resource_type_plural = 'acquisition capabilities'
    validation_url = reverse_lazy('validation:acquisition_capability')
    post_url = reverse_lazy('register:acquisition_capability')
    index_page_url_name = 'resource_management:acquisition_capabilities'

class acquisition(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_acquisition_dictionary
    success_url = reverse_lazy('register:acquisition')

    a_or_an = 'an'
    resource_type = 'acquisition'
    resource_type_plural = 'acquisitions'
    validation_url = reverse_lazy('validation:acquisition')
    post_url = reverse_lazy('register:acquisition')
    index_page_url_name = 'resource_management:acquisitions'

class computation_capability(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    success_url = reverse_lazy('register:computation_capability')

    a_or_an = 'a'
    resource_type = 'computation capability'
    resource_type_plural = 'computation capabilities'
    validation_url = reverse_lazy('validation:computation_capability')
    post_url = reverse_lazy('register:computation_capability')
    index_page_url_name = 'resource_management:computation_capabilities'

class computation(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_computation_dictionary
    success_url = reverse_lazy('register:computation')

    a_or_an = 'a'
    resource_type = 'computation'
    resource_type_plural = 'computations'
    validation_url = reverse_lazy('validation:computation')
    post_url = reverse_lazy('register:computation')
    index_page_url_name = 'resource_management:computations'

class process(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_process_dictionary
    success_url = reverse_lazy('register:process')

    a_or_an = 'a'
    resource_type = 'process'
    resource_type_plural = 'processes'
    validation_url = reverse_lazy('validation:process')
    post_url = reverse_lazy('register:process')
    index_page_url_name = 'resource_management:processes'

class data_collection(RegisterResourceFormView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_data_collection_dictionary
    success_url = reverse_lazy('register:data_collection')

    a_or_an = 'a'
    resource_type = 'data collection'
    resource_type_plural = 'data collections'
    validation_url = reverse_lazy('validation:data_collection')
    post_url = reverse_lazy('register:data_collection')
    index_page_url_name = 'resource_management:data_collections'
