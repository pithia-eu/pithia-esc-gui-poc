from django.views.generic.edit import FormView
from pyexpat import ExpatError
import traceback
from django.urls import reverse_lazy
from django.contrib import messages
from bson.objectid import ObjectId
from common.helpers import get_interaction_methods_linked_to_data_collection_id, get_revision_ids_for_resource_id
from mongodb import client
from register.register import move_current_version_of_resource_to_revisions, register_metadata_xml_file
from register.register_api_specification import move_current_existing_version_of_api_interaction_method_to_revisions, register_api_specification
from register.xml_conversion_checks_and_fixes import format_acquisition_dictionary, format_computation_dictionary, format_data_collection_dictionary, format_process_dictionary
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from resource_management.forms import UploadUpdatedDataCollectionFileForm, UploadUpdatedFileForm
from common.mongodb_models import AcquisitionRevision, ComputationRevision, CurrentAcquisition, CurrentComputation, CurrentDataCollection, CurrentDataCollectionInteractionMethod, CurrentIndividual, CurrentInstrument, CurrentOperation, CurrentOrganisation, CurrentPlatform, CurrentProcess, CurrentProject, DataCollectionInteractionMethodRevision, DataCollectionRevision, IndividualRevision, InstrumentRevision, OperationRevision, OrganisationRevision, PlatformRevision, ProcessRevision, ProjectRevision
from resource_management.views import _INDEX_PAGE_TITLE


# Create your views here.
class UpdateResourceView(FormView):
    # Registration variables
    resource_id = ''
    resource_mongodb_model = None
    resource_revision_mongodb_model = None
    resource_conversion_validate_and_correct_function = None

    # Template variables
    a_or_an = 'a'
    resource_type = ''
    resource_type_plural = ''
    list_resources_of_type_view_name = ''
    update_resource_type_view_name = ''
    validation_url = ''
    resource_to_update_name = '' # Set in get() function

    # Class variables
    template_name = 'update/file_upload.html'
    form_class = UploadUpdatedFileForm
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.a_or_an} {self.resource_type.title()}'
        context['form'] = self.form_class
        context['resource_id'] = self.resource_id
        context['resource_to_update_name'] = self.resource_to_update_name
        context['validation_url'] = self.validation_url
        context['resource_management_index_page_title'] = _INDEX_PAGE_TITLE
        context['list_resources_of_type_view_page_title'] = f'Manage {self.resource_type_plural}'
        context['list_resources_of_type_view_name'] = self.list_resources_of_type_view_name
        context['post_url'] = reverse_lazy(self.update_resource_type_view_name, args=[self.resource_id])
        context['update_resource_type_view_name'] = self.update_resource_type_view_name
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        xml_file = request.FILES['files']
        if form.is_valid():
            converted_xml_file = None
            try:
                metadata_move_results = None
                api_specification_move_results = None

                converted_xml_file = convert_xml_metadata_file_to_dictionary(xml_file)
                converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
                metadata_move_results = move_current_version_of_resource_to_revisions(converted_xml_file['identifier']['PITHIA_Identifier'], self.resource_mongodb_model, self.resource_revision_mongodb_model)
                if metadata_move_results != None:
                    api_specification_move_results = move_current_existing_version_of_api_interaction_method_to_revisions(metadata_move_results.inserted_id, CurrentDataCollectionInteractionMethod, DataCollectionInteractionMethodRevision)
            except BaseException as err:
                print(err)
                print(traceback.format_exc())
                messages.error(request, 'An unexpected error occurred.')
                return super().post(request, *args, **kwargs)

            try:
                metadata_registration_results = None
                api_specification_registration_results = None

                metadata_registration_results = register_metadata_xml_file(xml_file, self.resource_mongodb_model, self.resource_conversion_validate_and_correct_function)
                if 'interaction_methods' in request.POST:
                    interaction_methods = request.POST.getlist('interaction_methods')
                    if 'api' in interaction_methods:
                        api_specification_url = request.POST['api_specification_url']
                        api_specification_registration_results = register_api_specification(api_specification_url, metadata_registration_results['_id'])
                messages.success(request, f'Successfully updated {xml_file.name}.')
            except ExpatError as err:
                print(err)
                print(traceback.format_exc())
                messages.error(request, 'An error occurred whilst parsing the XML.')
            except BaseException as err:
                print(err)
                print(traceback.format_exc())
                messages.error(request, 'An unexpected error occurred.')
        else:
            messages.error(request, 'The form submitted was not valid.')

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        resource_to_update = self.resource_mongodb_model.find_one({
            '_id': ObjectId(self.resource_id)
        })
        resource_to_update_name = resource_to_update['identifier']['PITHIA_Identifier']['localID']
        if 'name' in resource_to_update:
            resource_to_update_name = resource_to_update['name']
        self.resource_to_update_name = resource_to_update_name
        return super().get(request, *args, **kwargs)

class organisation(UpdateResourceView):
    resource_mongodb_model = CurrentOrganisation
    resource_revision_mongodb_model = OrganisationRevision

    a_or_an = 'an'
    resource_type = 'Organisation'
    resource_type_plural = 'Organisations'
    list_resources_of_type_view_name = 'resource_management:organisations'
    update_resource_type_view_name = 'update:organisation'
    validation_url = reverse_lazy('validation:organisation')
    success_url = reverse_lazy('resource_management:organisations')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)
    

class individual(UpdateResourceView):
    resource_mongodb_model = CurrentIndividual
    resource_revision_mongodb_model = IndividualRevision

    a_or_an = 'an'
    resource_type = 'Individual'
    resource_type_plural = 'Individuals'
    list_resources_of_type_view_name = 'resource_management:individuals'
    update_resource_type_view_name = 'update:individual'
    validation_url = reverse_lazy('validation:individual')
    success_url = reverse_lazy('resource_management:individuals')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class project(UpdateResourceView):
    resource_mongodb_model = CurrentProject
    resource_revision_mongodb_model = ProjectRevision

    a_or_an = 'a'
    resource_type = 'Project'
    resource_type_plural = 'Projects'
    list_resources_of_type_view_name = 'resource_management:projects'
    update_resource_type_view_name = 'update:project'
    validation_url = reverse_lazy('validation:project')
    success_url = reverse_lazy('resource_management:projects')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class platform(UpdateResourceView):
    resource_mongodb_model = CurrentPlatform
    resource_revision_mongodb_model = PlatformRevision

    a_or_an = 'a'
    resource_type = 'Platform'
    resource_type_plural = 'Platforms'
    list_resources_of_type_view_name = 'resource_management:platforms'
    update_resource_type_view_name = 'update:platform'
    validation_url = reverse_lazy('validation:platform')
    success_url = reverse_lazy('resource_management:platforms')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class instrument(UpdateResourceView):
    resource_mongodb_model = CurrentInstrument
    resource_revision_mongodb_model = InstrumentRevision

    a_or_an = 'an'
    resource_type = 'Instrument'
    resource_type_plural = 'Instruments'
    list_resources_of_type_view_name = 'resource_management:instruments'
    update_resource_type_view_name = 'update:instrument'
    validation_url = reverse_lazy('validation:instrument')
    success_url = reverse_lazy('resource_management:instruments')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

class operation(UpdateResourceView):
    resource_mongodb_model = CurrentOperation
    resource_revision_mongodb_model = OperationRevision

    a_or_an = 'an'
    resource_type = 'Operation'
    resource_type_plural = 'Operations'
    list_resources_of_type_view_name = 'resource_management:operations'
    update_resource_type_view_name = 'update:operation'
    validation_url = reverse_lazy('validation:operation')
    success_url = reverse_lazy('resource_management:operations')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class acquisition(UpdateResourceView):
    resource_mongodb_model = CurrentAcquisition
    resource_revision_mongodb_model = AcquisitionRevision
    resource_conversion_validate_and_correct_function = format_acquisition_dictionary

    a_or_an = 'an'
    resource_type = 'Acquisition'
    resource_type_plural = 'Acquisitions'
    list_resources_of_type_view_name = 'resource_management:acquisitions'
    update_resource_type_view_name = 'update:acquisition'
    validation_url = reverse_lazy('validation:acquisition')
    success_url = reverse_lazy('resource_management:acquisitions')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

class computation(UpdateResourceView):
    resource_mongodb_model = CurrentComputation
    resource_revision_mongodb_model = ComputationRevision
    resource_conversion_validate_and_correct_function = format_computation_dictionary

    a_or_an = 'a'
    resource_type = 'Computation'
    resource_type_plural = 'Computations'
    list_resources_of_type_view_name = 'resource_management:computations'
    update_resource_type_view_name = 'update:computation'
    validation_url = reverse_lazy('validation:computation')
    success_url = reverse_lazy('resource_management:computations')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

class process(UpdateResourceView):
    resource_mongodb_model = CurrentProcess
    resource_revision_mongodb_model = ProcessRevision
    resource_conversion_validate_and_correct_function = format_process_dictionary

    a_or_an = 'a'
    resource_type = 'Process'
    resource_type_plural = 'Processes'
    list_resources_of_type_view_name = 'resource_management:processes'
    update_resource_type_view_name = 'update:process'
    validation_url = reverse_lazy('validation:process')
    success_url = reverse_lazy('resource_management:processes')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

class data_collection(UpdateResourceView):
    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    resource_conversion_validate_and_correct_function = format_data_collection_dictionary
    template_name = 'update/file_upload_data_collection.html'
    form_class = UploadUpdatedDataCollectionFileForm

    a_or_an = 'a'
    resource_type = 'Data Collection'
    resource_type_plural = 'Data Collections'
    list_resources_of_type_view_name = 'resource_management:data_collections'
    update_resource_type_view_name = 'update:data_collection'
    validation_url = reverse_lazy('validation:data_collection')
    success_url = reverse_lazy('resource_management:data_collections')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        interaction_methods = get_interaction_methods_linked_to_data_collection_id(self.resource_id)
        if len(interaction_methods) > 0:
            form_data = {}
            form_data['interaction_methods'] = []   
            for im in interaction_methods:
                if im['interaction_method'] == 'api':
                    form_data['interaction_methods'].append('api')
                    form_data['api_specification_url'] = im['interaction_url']
            context['form'] = self.form_class(initial=form_data)
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)