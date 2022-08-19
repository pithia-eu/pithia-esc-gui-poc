from django.shortcuts import render
from pyexpat import ExpatError
import traceback
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponseRedirect
from django.contrib import messages
from bson.objectid import ObjectId
from register.register import move_current_version_of_resource_to_revisions, register_metadata_xml_file
from register.xml_conversion_checks_and_fixes import format_acquisition_dictionary, format_computation_dictionary, format_data_collection_dictionary, format_process_dictionary
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from resource_management.forms import UploadUpdatedFileForm
from search.helpers import remove_underscore_from_id_attribute, get_view_helper_variables_by_url_namespace
from common.mongodb_models import AcquisitionRevision, ComputationRevision, CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject, DataCollectionRevision, IndividualRevision, InstrumentRevision, OperationRevision, OrganisationRevision, PlatformRevision, ProcessRevision, ProjectRevision
from validation.validation import validate_acquisition_metadata_xml_file, validate_computation_metadata_xml_file, validate_data_collection_metadata_xml_file, validate_individual_metadata_xml_file, validate_instrument_metadata_xml_file, validate_operation_metadata_xml_file, validate_organisation_metadata_xml_file, validate_platform_metadata_xml_file, validate_process_metadata_xml_file, validate_project_metadata_xml_file

# Create your views here.
def update(request, resource_id, resource_mongodb_model, resource_revision_mongodb_model, resource_validation_function, resource_conversion_validate_and_correct_function, list_resource_type_view_name, update_resource_type_view_name, validation_url, resource_type, resource_type_plural):
    url_namespace = request.resolver_match.namespace
    if request.method == 'POST':
        # Form validation
        form = UploadUpdatedFileForm(request.POST, request.FILES)
        xml_file = request.FILES['file']
        if form.is_valid():
            # XML should have already been validated at
            # the template, but do it again just to be
            # safe.
            validation_results = resource_validation_function(xml_file)
            # TODO: Change to checking validation results before deploying to production
            if True:
                try:
                    converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
                    converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
                    move_current_version_of_resource_to_revisions(converted_xml_file['identifier']['pithia:Identifier'], resource_mongodb_model, resource_revision_mongodb_model)
                    register_metadata_xml_file(xml_file, resource_mongodb_model, resource_conversion_validate_and_correct_function)
                except ExpatError as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An error occurred whilst parsing the XML.')
                except BaseException as err:
                    print(err)
                    print(traceback.format_exc())
                    messages.error(request, 'An unexpected error occurred.')
        return HttpResponseRedirect(reverse(list_resource_type_view_name))
    resource_to_update = resource_mongodb_model.find_one({
        '_id': ObjectId(resource_id)
    })
    resource_to_update_name = resource_to_update['identifier']['pithia:Identifier']['localID']
    if 'name' in resource_to_update:
        resource_to_update_name = resource_to_update['name']
    a_or_an = 'a'
    if resource_type.lower().startswith(('a', 'e', 'i',  'o', 'u' )):
        a_or_an = 'an'
    return render(request, 'resource_management/update.html', {
        'title': f'Update {a_or_an} {resource_type.title()}',
        'breadcrumb_item_list_resources_of_type_text': f'Manage {resource_type_plural}',
        'url_namespace': url_namespace,
        'form': UploadUpdatedFileForm(),
        'resource_id': resource_id,
        'resource_to_update_name': resource_to_update_name,
        'validation_url': validation_url,
        'list_resource_type_view_name': list_resource_type_view_name,
        'update_resource_type_view_name': update_resource_type_view_name,
    })

@require_http_methods(["GET", "POST"])
def organisation(request, organisation_id):
    return update(request, organisation_id, CurrentOrganisation, OrganisationRevision, validate_organisation_metadata_xml_file, None, 'resource_management:list_organisations', 'resource_management:update_organisation', 'validate:organisation', 'Organisation', 'Organisations')

@require_http_methods(["GET", "POST"])
def individual(request, individual_id):
    return update(request, individual_id, CurrentIndividual, IndividualRevision, validate_individual_metadata_xml_file, None, 'resource_management:list_individuals', 'resource_management:update_individual', 'validate:individual', 'Individual', 'Individuals')

@require_http_methods(["GET", "POST"])
def project(request, project_id):
    return update(request, project_id, CurrentProject, ProjectRevision, validate_project_metadata_xml_file, None, 'resource_management:list_projects', 'resource_management:update_project', 'validate:project', 'Project', 'Projects')

@require_http_methods(["GET", "POST"])
def platform(request, platform_id):
    return update(request, platform_id, CurrentPlatform, PlatformRevision, validate_platform_metadata_xml_file, None, 'resource_management:list_platforms', 'resource_management:update_platform', 'validate:platform', 'Platform', 'Platforms')

@require_http_methods(["GET", "POST"])
def instrument(request, instrument_id):
    return update(request, instrument_id, CurrentInstrument, InstrumentRevision, validate_instrument_metadata_xml_file, None, 'resource_management:list_instruments', 'resource_management:update_instrument', 'validate:instrument', 'Instrument', 'Instruments')

@require_http_methods(["GET", "POST"])
def operation(request, operation_id):
    return update(request, operation_id, CurrentOperation, OperationRevision, validate_operation_metadata_xml_file, None, 'resource_management:list_operations', 'resource_management:update_operation', 'validate:operation', 'Operation', 'Operations')

@require_http_methods(["GET", "POST"])
def acquisition(request, acquisition_id):
    return update(request, acquisition_id, CurrentAcquisition, AcquisitionRevision, validate_acquisition_metadata_xml_file, format_acquisition_dictionary, 'resource_management:list_acquisitions', 'resource_management:update_acquisition', 'validate:acquisition', 'Acquisition', 'Acquisitions')

@require_http_methods(["GET", "POST"])
def computation(request, computation_id):
    return update(request, computation_id, CurrentComputation, ComputationRevision, validate_computation_metadata_xml_file, format_computation_dictionary, 'resource_management:list_computations', 'resource_management:update_computation', 'validate:computation', 'Computation', 'Computations')

@require_http_methods(["GET", "POST"])
def process(request, process_id):
    return update(request, process_id, CurrentProcess, ProcessRevision, validate_process_metadata_xml_file, format_process_dictionary, 'resource_management:list_processes', 'resource_management:update_process', 'validate:process', 'Process', 'Processes')

@require_http_methods(["GET", "POST"])
def data_collection(request, data_collection_id):
    return update(request, data_collection_id, CurrentDataCollection, DataCollectionRevision, validate_data_collection_metadata_xml_file, format_data_collection_dictionary, 'resource_management:list_data_collections', 'resource_management:update_data_collection', 'validate:data_collection', 'Data Collection', 'Data Collections')