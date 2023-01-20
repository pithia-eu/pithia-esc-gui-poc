import traceback
from pyexpat import ExpatError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView
from register.register import (
    register_metadata_xml_file,
    store_xml_file_as_string_and_map_to_resource_id,
)
from register.register_api_specification import register_api_specification

from .forms import UploadDataCollectionFileForm, UploadFileForm
from register import xml_conversion_checks_and_fixes
from common import mongodb_models
from resource_management.views import _INDEX_PAGE_TITLE, _create_manage_resource_page_title
from validation.errors import FileRegisteredBefore
from mongodb import client


# Create your views here.
class ResourceRegisterFormView(FormView):
    resource_mongodb_model = None
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    resource_type_plural = ''
    validation_url = ''
    post_url = ''
    resource_management_list_page_breadcrumb_text = ''
    resource_management_list_page_breadcrumb_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.resource_type_plural.title()}'
        context['validation_url'] = self.validation_url
        context['post_url'] = self.post_url
        context['form'] = self.form_class
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
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
                    if not hasattr(self, 'resource_conversion_validate_and_correct_function'):
                        self.resource_conversion_validate_and_correct_function = None
                    with client.start_session() as s:
                        def cb(s):
                            registration_results = register_metadata_xml_file(
                                xml_file,
                                self.resource_mongodb_model,
                                self.resource_conversion_validate_and_correct_function,
                                session=s
                            )
                            store_xml_file_as_string_and_map_to_resource_id(
                                xml_file,
                                registration_results['_id'],
                                session=s
                            )
                            if 'api_selected' in request.POST:
                                api_specification_url = request.POST['api_specification_url']
                                api_description = ''
                                if 'api_description' in request.POST:
                                    api_description = request.POST['api_description']
                                register_api_specification(
                                    api_specification_url,
                                    registration_results['identifier']['PITHIA_Identifier']['localID'],
                                    api_description=api_description,
                                    session=s
                                )
                        s.with_transaction(cb)
                    messages.success(request, f'Successfully registered {xml_file.name}.')
                except ExpatError as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, f'An error occurred whilst parsing {xml_file.name}.')
                except FileRegisteredBefore as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, f'{xml_file.name} has been registered before.')
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

class OrganisationRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    success_url = reverse_lazy('register:organisation')

    resource_type_plural = 'organisations'
    validation_url = reverse_lazy('validation:organisation')
    post_url = reverse_lazy('register:organisation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')

class IndividualRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentIndividual
    success_url = reverse_lazy('register:individual')

    resource_type_plural = 'individuals'
    validation_url = reverse_lazy('validation:individual')
    post_url = reverse_lazy('register:individual')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')

class ProjectRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentProject
    success_url = reverse_lazy('register:project')

    resource_type_plural = 'projects'
    validation_url = reverse_lazy('validation:project')
    post_url = reverse_lazy('register:project')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('projects')

class PlatformRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentPlatform
    success_url = reverse_lazy('register:platform')

    resource_type_plural = 'platforms'
    validation_url = reverse_lazy('validation:platform')
    post_url = reverse_lazy('register:platform')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('platforms')

class InstrumentRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentInstrument
    success_url = reverse_lazy('register:instrument')

    resource_type_plural = 'instruments'
    validation_url = reverse_lazy('validation:instrument')
    post_url = reverse_lazy('register:instrument')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('instruments')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_instrument_dictionary
        return super().post(request, *args, **kwargs)

class OperationRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentOperation
    success_url = reverse_lazy('register:operation')

    resource_type_plural = 'operations'
    validation_url = reverse_lazy('validation:operation')
    post_url = reverse_lazy('register:operation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('operations')

class AcquisitionCapabilitiesRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    success_url = reverse_lazy('register:acquisition_capability_set')

    resource_type_plural = 'acquisition capabilities'
    validation_url = reverse_lazy('validation:acquisition_capability_set')
    post_url = reverse_lazy('register:acquisition_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisition capabilities')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_acquisition_capability_set_dictionary
        return super().post(request, *args, **kwargs)

class AcquisitionRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    success_url = reverse_lazy('register:acquisition')

    resource_type_plural = 'acquisitions'
    validation_url = reverse_lazy('validation:acquisition')
    post_url = reverse_lazy('register:acquisition')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisitions')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_acquisition_dictionary
        return super().post(request, *args, **kwargs)

class ComputationCapabilitiesRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    success_url = reverse_lazy('register:computation_capability_set')

    resource_type_plural = 'computation capabilities'
    validation_url = reverse_lazy('validation:computation_capability_set')
    post_url = reverse_lazy('register:computation_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computation capabilities')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_computation_capability_set_dictionary
        return super().post(request, *args, **kwargs)

class ComputationRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentComputation
    success_url = reverse_lazy('register:computation')

    resource_type_plural = 'computations'
    validation_url = reverse_lazy('validation:computation')
    post_url = reverse_lazy('register:computation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computations')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_computation_dictionary
        return super().post(request, *args, **kwargs)

class ProcessRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentProcess
    success_url = reverse_lazy('register:process')

    resource_type_plural = 'processes'
    validation_url = reverse_lazy('validation:process')
    post_url = reverse_lazy('register:process')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('processes')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_process_dictionary
        return super().post(request, *args, **kwargs)

class DataCollectionRegisterFormView(ResourceRegisterFormView):
    resource_mongodb_model = mongodb_models.CurrentDataCollection
    success_url = reverse_lazy('register:data_collection')
    template_name = 'register/file_upload_data_collection.html'
    form_class = UploadDataCollectionFileForm

    validation_url = reverse_lazy('validation:data_collection')
    post_url = reverse_lazy('register:data_collection')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('data collections')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register a Data Collection'
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.format_data_collection_dictionary
        return super().post(request, *args, **kwargs)
