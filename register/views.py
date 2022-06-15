import traceback
from pyexpat import ExpatError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from validation.validation import validate_acquisition_metadata_xml_file, validate_computation_metadata_xml_file, validate_data_collection_metadata_xml_file, validate_individual_metadata_xml_file, validate_instrument_metadata_xml_file, validate_operation_metadata_xml_file, validate_organisation_metadata_xml_file, validate_platform_metadata_xml_file, validate_process_metadata_xml_file, validate_project_metadata_xml_file

from .forms import UploadFileForm

from register import mongodb_models, preupload_checks

def register_metadata_file_and_redirect(request, mongodb_model, validation, preupload_check_and_fix, redirect_url):
    # Form validation
    form = UploadFileForm(request.POST, request.FILES)
    xml_file = request.FILES['file']
    if form.is_valid():
        # XML should have already been validated at
        # the template, but do it again just to be
        # safe.
        validation_results = validation(xml_file)
        if 'error' not in validation_results:
            try:
                print(validation_results)
                metadata_file_dict = convert_xml_metadata_file_to_dictionary(xml_file)
                if preupload_check_and_fix:
                    preupload_check_and_fix(metadata_file_dict)
                mongodb_model.insert_one(metadata_file_dict)
            except ExpatError as err:
                print(err)
                print(traceback.format_exc())
                messages.error(request, 'An error occurred whilst parsing the XML.')
                return HttpResponseRedirect(redirect_url)
            except BaseException as err:
                print(err)
                print(traceback.format_exc())
                messages.error(request, 'An unexpected error occurred.')
                return HttpResponseRedirect(redirect_url)

            messages.success(request, f'Successfully registered {xml_file.name}.')
            return HttpResponseRedirect(redirect_url)
        messages.error(request, 'Validation failed. Please ensure your files are valid before uploading.')
        return HttpResponseRedirect(redirect_url)
    else:
        messages.error(request, 'The form submitted was not valid.')
        return HttpResponseRedirect(redirect_url)

# Create your views here.
def index(request):
    return render(request, 'register/index.html', {
        'title': 'Resource Metadata Registration'
    })

def organisation(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentOrganisation, validate_organisation_metadata_xml_file, None, reverse('register:organisation'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register an Organisation',
        'breadcrumb_item_active_text': 'Organisation',
        'validation_url': reverse('validation:organisation'),
        'post_url': reverse('register:organisation'),
        'form': UploadFileForm(),
    })

def individual(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentIndividual, validate_individual_metadata_xml_file, None, reverse('register:individual'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register an Individual',
        'breadcrumb_item_active_text': 'Individual',
        'validation_url': reverse('validation:individual'),
        'post_url': reverse('register:individual'),
        'form': UploadFileForm(),
    })

def project(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentProject, validate_project_metadata_xml_file, None, reverse('register:project'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register a Project',
        'breadcrumb_item_active_text': 'Project',
        'validation_url': reverse('validation:project'),
        'post_url': reverse('register:project'),
        'form': UploadFileForm(),
    })

def platform(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentPlatform, validate_platform_metadata_xml_file, None, reverse('register:platform'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register a Platform',
        'breadcrumb_item_active_text': 'Platform',
        'validation_url': reverse('validation:platform'),
        'post_url': reverse('register:platform'),
        'form': UploadFileForm(),
    })

def instrument(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentInstrument, validate_instrument_metadata_xml_file, None, reverse('register:instrument'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register an Instrument',
        'breadcrumb_item_active_text': 'Instrument',
        'validation_url': reverse('validation:instrument'),
        'post_url': reverse('register:instrument'),
        'form': UploadFileForm(),
    })

def operation(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentOperation, validate_operation_metadata_xml_file, None, reverse('register:operation'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register an Operation',
        'breadcrumb_item_active_text': 'Operation',
        'validation_url': reverse('validation:operation'),
        'post_url': reverse('register:operation'),
        'form': UploadFileForm(),
    })

def acquisition(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentAcquisition, validate_acquisition_metadata_xml_file, preupload_checks.format_acquisition_dictionary, reverse('register:acquisition'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register an Acquisition',
        'breadcrumb_item_active_text': 'Acquisition',
        'validation_url': reverse('validation:acquisition'),
        'post_url': reverse('register:acquisition'),
        'form': UploadFileForm(),
    })

def computation(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentComputation, validate_computation_metadata_xml_file, preupload_checks.format_computation_dictionary, reverse('register:computation'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register a Computation',
        'breadcrumb_item_active_text': 'Computation',
        'validation_url': reverse('validation:computation'),
        'post_url': reverse('register:computation'),
        'form': UploadFileForm(),
    })

def process(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentDataCollection, validate_process_metadata_xml_file, preupload_checks.format_process_dictionary, reverse('register:process'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register a Process',
        'breadcrumb_item_active_text': 'Process',
        'validation_url': reverse('validation:process'),
        'post_url': reverse('register:process'),
        'form': UploadFileForm(),
    })

def data_collection(request):
    if request.method == 'POST':
        register_metadata_file_and_redirect(request, mongodb_models.CurrentDataCollection, validate_data_collection_metadata_xml_file, preupload_checks.format_data_collection_dictionary, reverse('register:data_collection'))
    return render(request, 'register/file_upload.html', {
        'title': 'Register a Data Collection',
        'breadcrumb_item_active_text': 'Data Collection',
        'validation_url': reverse('validation:data_collection'),
        'post_url': reverse('register:data_collection'),
        'form': UploadFileForm(),
    })
