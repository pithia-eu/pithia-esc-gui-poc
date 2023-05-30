import logging
from bson.objectid import ObjectId
from common import models
from common.helpers import get_interaction_methods_linked_to_data_collection_id
from common.mongodb_models import (
    AcquisitionCapabilityRevision,
    AcquisitionRevision,
    ComputationCapabilityRevision,
    ComputationRevision,
    CurrentAcquisition,
    CurrentAcquisitionCapability,
    CurrentComputation,
    CurrentComputationCapability,
    CurrentDataCollection,
    CurrentDataCollectionInteractionMethod,
    CurrentIndividual,
    CurrentInstrument,
    CurrentOperation,
    CurrentOrganisation,
    CurrentPlatform,
    CurrentProcess,
    CurrentProject,
    DataCollectionRevision,
    IndividualRevision,
    InstrumentRevision,
    OperationRevision,
    OrganisationRevision,
    PlatformRevision,
    ProcessRevision,
    ProjectRevision,
    CurrentCatalogue,
    CatalogueRevision,
    CurrentCatalogueEntry,
    CatalogueEntryRevision,
    CurrentCatalogueDataSubset,
    CatalogueDataSubsetRevision,
)
from django.contrib import messages
from django.shortcuts import (
    render,
    redirect
)
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from handle_management.xml_utils import (
    add_doi_xml_string_to_metadata_xml_string,
    get_doi_xml_string_for_resource_id,
    remove_doi_element_from_metadata_xml_string,
)
from mongodb import client
from pyexpat import ExpatError
from register.register import store_xml_file_as_string_and_map_to_resource_id
from register.xml_conversion_checks_and_fixes import (
    correct_acquisition_capability_set_xml_converted_to_dict,
    correct_acquisition_xml_converted_to_dict,
    correct_computation_capability_set_xml_converted_to_dict,
    correct_computation_xml_converted_to_dict,
    correct_data_collection_xml_converted_to_dict,
    correct_instrument_xml_converted_to_dict,
    correct_process_xml_converted_to_dict
)
from register.xml_metadata_file_conversion import convert_xml_metadata_file_to_dictionary
from register.register_api_specification import register_api_specification
from resource_management.forms import (
    UploadUpdatedDataCollectionFileForm,
    UploadUpdatedFileForm,
    UpdateDataCollectionInteractionMethodsForm
)
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
)
from update.update import (
    update_current_version_of_resource,
    update_data_collection_api_interaction_method_specification_url,
    update_data_collection_api_interaction_method_description
)
from update.version_control import (
    assign_original_xml_file_entry_to_revision_id,
    create_revision_of_current_resource_version,
    create_revision_of_data_collection_api_interaction_method
)


logger = logging.getLogger(__name__)


# Create your views here.
class ResourceUpdateFormView(FormView):
    # Registration variables
    resource_id = ''
    resource_mongodb_model = None
    resource_revision_mongodb_model = None

    # Template variables
    a_or_an = 'a'
    resource_type = ''
    resource_type_plural = ''
    resource_update_page_url_name = ''
    validation_url = ''
    resource_to_update_name = '' # Set in dispatch() function
    resource_management_list_page_breadcrumb_url_name = ''

    # Class variables
    template_name = 'update/file_upload.html'
    form_class = UploadUpdatedFileForm
    success_url = ''
    xml_file_string = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.a_or_an} {self.resource_type.title()}'
        context['form'] = self.form_class
        context['resource_id'] = self.resource_id
        context['resource_to_update_name'] = self.resource_to_update_name
        context['validation_url'] = self.validation_url
        context['post_url'] = reverse_lazy(self.resource_update_page_url_name, args=[self.resource_id])
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = f'Register & Manage {self.resource_type_plural}'
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        xml_file = request.FILES['files']
        if form.is_valid():
            try:
                self.model.objects.update_from_xml_string(self.resource_id, xml_file.read())
                
                # Old code
                if not hasattr(self, 'resource_conversion_validate_and_correct_function'):
                    self.resource_conversion_validate_and_correct_function = None
                with client.start_session() as s:
                    def cb(s):
                        if self.xml_file_string is None:
                            self.xml_file_string = xml_file.read()
                        converted_xml_file = convert_xml_metadata_file_to_dictionary(self.xml_file_string)
                        converted_xml_file = converted_xml_file[(list(converted_xml_file)[0])]
                        pithia_identifier = converted_xml_file['identifier']['PITHIA_Identifier']
                        resource_revision = create_revision_of_current_resource_version(
                            pithia_identifier,
                            self.resource_mongodb_model,
                            self.resource_revision_mongodb_model,
                            session=s
                        )
                        assign_original_xml_file_entry_to_revision_id(
                            self.resource_id,
                            resource_revision['_id'],
                            session=s
                        )
                        update_current_version_of_resource(
                            self.resource_id,
                            self.xml_file_string,
                            self.resource_mongodb_model,
                            self.resource_conversion_validate_and_correct_function,
                            session=s
                        )
                        store_xml_file_as_string_and_map_to_resource_id(
                            self.xml_file_string,
                            self.resource_id,
                            session=s
                        )
                    s.with_transaction(cb)
                messages.success(request, f'Successfully updated {xml_file.name}. It may take a few minutes for the changes to be visible in the metadata\'s details page.')
            except ExpatError as err:
                logger.exception('Could not update a resource as there was an error parsing the update XML.')
                messages.error(request, 'An error occurred whilst parsing the XML.')
            except BaseException as err:
                logger.exception('An unexpected error occurred whilst attempting to update a resource.')
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

class OrganisationUpdateFormView(ResourceUpdateFormView):
    model = models.Organisation
    resource_mongodb_model = CurrentOrganisation
    resource_revision_mongodb_model = OrganisationRevision

    a_or_an = 'an'
    resource_type = 'Organisation'
    resource_type_plural = 'Organisations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    resource_update_page_url_name = 'update:organisation'
    validation_url = reverse_lazy('validation:organisation')
    success_url = reverse_lazy('resource_management:organisations')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['organisation_id']
        return super().dispatch(request, *args, **kwargs)
    

class IndividualUpdateFormView(ResourceUpdateFormView):
    model = models.Individual
    resource_mongodb_model = CurrentIndividual
    resource_revision_mongodb_model = IndividualRevision

    a_or_an = 'an'
    resource_type = 'Individual'
    resource_type_plural = 'Individuals'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_update_page_url_name = 'update:individual'
    validation_url = reverse_lazy('validation:individual')
    success_url = reverse_lazy('resource_management:individuals')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['individual_id']
        return super().dispatch(request, *args, **kwargs)

class ProjectUpdateFormView(ResourceUpdateFormView):
    model = models.Project
    resource_mongodb_model = CurrentProject
    resource_revision_mongodb_model = ProjectRevision

    a_or_an = 'a'
    resource_type = 'Project'
    resource_type_plural = 'Projects'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_update_page_url_name = 'update:project'
    validation_url = reverse_lazy('validation:project')
    success_url = reverse_lazy('resource_management:projects')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['project_id']
        return super().dispatch(request, *args, **kwargs)

class PlatformUpdateFormView(ResourceUpdateFormView):
    model = models.Platform
    resource_mongodb_model = CurrentPlatform
    resource_revision_mongodb_model = PlatformRevision

    a_or_an = 'a'
    resource_type = 'Platform'
    resource_type_plural = 'Platforms'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_update_page_url_name = 'update:platform'
    validation_url = reverse_lazy('validation:platform')
    success_url = reverse_lazy('resource_management:platforms')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['platform_id']
        return super().dispatch(request, *args, **kwargs)

class OperationUpdateFormView(ResourceUpdateFormView):
    model = models.Operation
    resource_mongodb_model = CurrentOperation
    resource_revision_mongodb_model = OperationRevision

    a_or_an = 'an'
    resource_type = 'Operation'
    resource_type_plural = 'Operations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_update_page_url_name = 'update:operation'
    validation_url = reverse_lazy('validation:operation')
    success_url = reverse_lazy('resource_management:operations')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['operation_id']
        return super().dispatch(request, *args, **kwargs)

class InstrumentUpdateFormView(ResourceUpdateFormView):
    model = models.Instrument
    resource_mongodb_model = CurrentInstrument
    resource_revision_mongodb_model = InstrumentRevision

    a_or_an = 'an'
    resource_type = 'Instrument'
    resource_type_plural = 'Instruments'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_update_page_url_name = 'update:instrument'
    validation_url = reverse_lazy('validation:instrument')
    success_url = reverse_lazy('resource_management:instruments')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['instrument_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_instrument_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class AcquisitionCapabilitiesUpdateFormView(ResourceUpdateFormView):
    model = models.AcquisitionCapabilities
    resource_mongodb_model = CurrentAcquisitionCapability
    resource_revision_mongodb_model = AcquisitionCapabilityRevision

    resource_type = 'Acquisition Capabilities'
    resource_type_plural = 'Acquisition Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_update_page_url_name = 'update:acquisition_capability_set'
    validation_url = reverse_lazy('validation:acquisition_capability_set')
    success_url = reverse_lazy('resource_management:acquisition_capability_sets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.resource_type.title()}'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_capability_set_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_acquisition_capability_set_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class AcquisitionUpdateFormView(ResourceUpdateFormView):
    model = models.Acquisition
    resource_mongodb_model = CurrentAcquisition
    resource_revision_mongodb_model = AcquisitionRevision

    a_or_an = 'an'
    resource_type = 'Acquisition'
    resource_type_plural = 'Acquisitions'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_update_page_url_name = 'update:acquisition'
    validation_url = reverse_lazy('validation:acquisition')
    success_url = reverse_lazy('resource_management:acquisitions')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['acquisition_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_acquisition_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class ComputationCapabilitiesUpdateFormView(ResourceUpdateFormView):
    model = models.ComputationCapabilities
    resource_mongodb_model = CurrentComputationCapability
    resource_revision_mongodb_model = ComputationCapabilityRevision

    resource_type = 'Computation Capabilities'
    resource_type_plural = 'Computation Capabilities'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_update_page_url_name = 'update:computation_capability_set'
    validation_url = reverse_lazy('validation:computation_capability_set')
    success_url = reverse_lazy('resource_management:computation_capability_sets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update {self.resource_type.title()}'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_capability_set_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_computation_capability_set_xml_converted_to_dict
        return super().post(request, *args, **kwargs)
        
class ComputationUpdateFormView(ResourceUpdateFormView):
    model = models.Computation
    resource_mongodb_model = CurrentComputation
    resource_revision_mongodb_model = ComputationRevision

    a_or_an = 'a'
    resource_type = 'Computation'
    resource_type_plural = 'Computations'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_update_page_url_name = 'update:computation'
    validation_url = reverse_lazy('validation:computation')
    success_url = reverse_lazy('resource_management:computations')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['computation_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_computation_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class ProcessUpdateFormView(ResourceUpdateFormView):
    model = models.Process
    resource_mongodb_model = CurrentProcess
    resource_revision_mongodb_model = ProcessRevision

    a_or_an = 'a'
    resource_type = 'Process'
    resource_type_plural = 'Processes'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_update_page_url_name = 'update:process'
    validation_url = reverse_lazy('validation:process')
    success_url = reverse_lazy('resource_management:processes')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['process_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_process_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class DataCollectionUpdateFormView(ResourceUpdateFormView):
    model = models.DataCollection
    resource_mongodb_model = CurrentDataCollection
    resource_revision_mongodb_model = DataCollectionRevision
    template_name = 'update/file_upload_data_collection.html'
    form_class = UploadUpdatedDataCollectionFileForm

    a_or_an = 'a'
    resource_type = 'Data Collection'
    resource_type_plural = 'Data Collections'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'
    resource_update_page_url_name = 'update:data_collection'
    validation_url = reverse_lazy('validation:data_collection')
    success_url = reverse_lazy('resource_management:data_collections')

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['data_collection_id']
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = correct_data_collection_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

def data_collection_interaction_methods(request, data_collection_id):
    data_collection = CurrentDataCollection.find_one({
        '_id': ObjectId(data_collection_id)
    })
    if request.method == 'POST':
        form = UpdateDataCollectionInteractionMethodsForm(request.POST)
        if form.is_valid():
            data_collection_localid = data_collection['identifier']['PITHIA_Identifier']['localID']
            try:
                with client.start_session() as s:
                    def cb(s):
                        create_revision_of_data_collection_api_interaction_method(
                            data_collection_localid,
                            session=s
                        )
                        if 'api_selected' not in request.POST:
                            CurrentDataCollectionInteractionMethod.delete_one({
                                'data_collection_localid': data_collection_localid,
                                'interaction_method': 'api',
                            }, session=s)
                            return redirect('update:data_collection_interaction_methods', data_collection_id=data_collection_id)
                        api_specification_url = request.POST['api_specification_url']
                        api_description = ''
                        if 'api_description' in request.POST:
                            api_description = request.POST['api_description']
                        existing_api_interaction_method = CurrentDataCollectionInteractionMethod.find_one({
                            'data_collection_localid': data_collection_localid
                        })
                        if existing_api_interaction_method is None:
                            register_api_specification(
                                api_specification_url,
                                data_collection_localid,
                                api_description,
                                session=s
                            )
                        else:
                            update_data_collection_api_interaction_method_specification_url(
                                data_collection_localid,
                                api_specification_url,
                                session=s
                            )
                            update_data_collection_api_interaction_method_description(
                                data_collection_localid,
                                api_description,
                                session=s
                            )
                    s.with_transaction(cb)
                messages.success(request, f'Successfully updated interaction methods for {data_collection["name"]}.')
            except BaseException as err:
                logger.exception('An unexpected error occurred whilst trying to update a Data Collection interaction method.')
                messages.error(request, 'An unexpected error occurred.')
            return redirect('update:data_collection_interaction_methods', data_collection_id=data_collection_id)
    form = UpdateDataCollectionInteractionMethodsForm()
    interaction_methods = get_interaction_methods_linked_to_data_collection_id(data_collection_id)
    if len(interaction_methods) > 0:
        form_data = {}
        for im in interaction_methods:
            if im['interaction_method'] == 'api':
                form_data['api_selected'] = True
                form_data['api_specification_url'] = im['interaction_url']
                form_data['api_description'] = im['interaction_method_description']
        form = UpdateDataCollectionInteractionMethodsForm(initial=form_data)
    return render(request, 'update/interaction_methods.html', {
        'data_collection': data_collection,
        'data_collection_id': str(data_collection['_id']),
        'form': form,
        'api_specification_validation_url': reverse_lazy('validation:api_specification_url'),
        'title': 'Update Interaction Methods',
        'resource_management_index_page_breadcrumb_text': _INDEX_PAGE_TITLE,
        'resource_management_category_list_page_breadcrumb_url_name': 'resource_management:data_collection_related_metadata_index',
        'resource_management_category_list_page_breadcrumb_text': _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
        'resource_management_list_page_breadcrumb_url_name': 'resource_management:data_collections',
        'resource_management_list_page_breadcrumb_text': 'Register & Manage Data Collections'
    })

class CatalogueUpdateFormView(ResourceUpdateFormView):
    model = models.Catalogue
    resource_mongodb_model = CurrentCatalogue
    resource_revision_mongodb_model = CatalogueRevision

    a_or_an = 'a'
    resource_type = 'Catalogue'
    resource_type_plural = 'Catalogues'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    resource_update_page_url_name = 'update:catalogue'
    validation_url = reverse_lazy('validation:catalogue')
    success_url = reverse_lazy('resource_management:catalogues')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_id']
        return super().dispatch(request, *args, **kwargs)

class CatalogueEntryUpdateFormView(ResourceUpdateFormView):
    model = models.CatalogueEntry
    resource_mongodb_model = CurrentCatalogueEntry
    resource_revision_mongodb_model = CatalogueEntryRevision

    a_or_an = 'a'
    resource_type = 'Catalogue Entry'
    resource_type_plural = 'Catalogue Entries'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    resource_update_page_url_name = 'update:catalogue_entry'
    validation_url = reverse_lazy('validation:catalogue_entry')
    success_url = reverse_lazy('resource_management:catalogue_entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_entry_id']
        return super().dispatch(request, *args, **kwargs)

class CatalogueDataSubsetUpdateFormView(ResourceUpdateFormView):
    model = models.CatalogueDataSubset
    resource_mongodb_model = CurrentCatalogueDataSubset
    resource_revision_mongodb_model = CatalogueDataSubsetRevision

    a_or_an = 'a'
    resource_type = 'Catalogue Data Subset'
    resource_type_plural = 'Catalogue Data Subsets'
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    resource_update_page_url_name = 'update:catalogue_data_subset'
    validation_url = reverse_lazy('validation:catalogue_data_subset')
    success_url = reverse_lazy('resource_management:catalogue_data_subsets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

    def dispatch(self, request, *args, **kwargs):
        self.resource_id = self.kwargs['catalogue_data_subset_id']
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        xml_file = request.FILES['files']
        if form.is_valid():
            # The DOI stored in the e-Science Centre will always be considered the
            # "right" version, so we need to replace any DOI that may have been
            # passed in the updated XML file.
            resource_doi_xml_string = get_doi_xml_string_for_resource_id(self.resource_id)
            self.xml_file_string = xml_file.read()
            if resource_doi_xml_string is None:
                return super().post(request, *args, **kwargs)
            self.xml_file_string = remove_doi_element_from_metadata_xml_string(self.xml_file_string)
            self.xml_file_string = add_doi_xml_string_to_metadata_xml_string(self.xml_file_string, resource_doi_xml_string)
        return super().post(request, *args, **kwargs)
