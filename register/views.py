import logging
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from pyexpat import ExpatError

from common import models, mongodb_models
from handle_management.handle_api import (
    add_doi_metadata_kernel_to_handle,
    create_and_register_handle_for_resource_url,
    delete_handle,
)
from handle_management.utils import (
    add_handle_to_url_mapping,
    add_handle_to_url_mapping_old,
)
from handle_management.xml_utils import (
    add_data_subset_data_to_doi_metadata_kernel_dict,
    add_data_subset_data_to_doi_metadata_kernel_dict_old,
    add_doi_metadata_kernel_to_data_subset,
    add_doi_kernel_metadata_to_xml_and_return_updated_string,
    add_handle_data_to_doi_metadata_kernel_dict,
    initialise_default_doi_kernel_metadata_dict,
    is_doi_element_present_in_xml_file,
)
from mongodb import client
from register import xml_conversion_checks_and_fixes
from register.register import (
    register_metadata_xml_file,
    store_xml_file_as_string_and_map_to_resource_id,
)
from register.register_api_specification import register_api_specification
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title
)
from update.update import update_original_metadata_xml_string
from utils.url_helpers import create_data_subset_detail_page_url
from validation.errors import FileRegisteredBefore

from .forms import (
    UploadDataCollectionFileForm,
    UploadFileForm,
    UploadCatalogueDataSubsetFileForm,
)


logger = logging.getLogger(__name__)


# Create your views here.
class ResourceRegisterFormView(FormView):
    resource_mongodb_model = None
    success_url = ''
    form_class = UploadFileForm
    template_name = 'register/file_upload.html'

    validation_url = ''
    post_url = ''
    resource_management_list_page_breadcrumb_text = ''
    resource_management_list_page_breadcrumb_url_name = ''
    resource_id = None
    new_registration = None
    handle = None
    handle_api_client = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Register {self.model.type_plural_readable.title()}'
        context['validation_url'] = self.validation_url
        context['post_url'] = self.post_url
        context['form'] = self.form_class
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Form validation
        form = UploadFileForm(request.POST, request.FILES)
        xml_files = request.FILES.getlist('files')
        file_registered = False
        if form.is_valid():
            for xml_file in xml_files:
                # XML should have already been validated at
                # the template, and validation could take
                # place again, but takes a long time. Another
                # method which verifies validation took place
                # should be implemented.
                try:
                    self.new_registration = self.model.objects.create_from_xml_string(xml_file.read())

                    # TODO: remove old code
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
                            self.resource_id = registration_results['_id']

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
                    # End of old code
                    
                    file_registered = True
                    messages.success(request, f'Successfully registered {xml_file.name}.')
                except ExpatError as err:
                    logger.exception('Expat error occurred during registration process.')
                    messages.error(request, f'An error occurred whilst parsing {xml_file.name}.')
                except FileRegisteredBefore as err:
                    logger.exception('The XML file submitted for registration has been registered before.')
                    messages.error(request, f'{xml_file.name} has been registered before.')
                except BaseException as err:
                    logger.exception('An unexpected error occurred during metadata registration.')
                    messages.error(request, 'An unexpected error occurred.')
                
                if file_registered == False:
                    return super().post(request, *args, **kwargs)

                try:
                    # POST RESOURCE REGISTRATION
                    # Get the DOI
                    # Update the actual "xml_file" variable by adding the DOI to the XML
                    # Perform an update on the resource
                    # Continue with registration as normal
                    if 'register_doi' in request.POST:
                        is_doi_in_file_already = is_doi_element_present_in_xml_file(xml_file)
                        if is_doi_in_file_already == True:
                            logger.exception('A DOI has already been issued for this metadata file.')
                            messages.error(request, f'A DOI has already been issued for this metadata file.')
                            return super().post(request, *args, **kwargs)
                        # Create a blank DOI dict first
                        doi_dict = initialise_default_doi_kernel_metadata_dict()
                        add_data_subset_data_to_doi_metadata_kernel_dict(self.new_registration, doi_dict)
                        # TODO: remove old code
                        # add_data_subset_data_to_doi_metadata_kernel_dict_old(self.resource_id, doi_dict)
                        # Create and register a handle
                        data_subset_url = create_data_subset_detail_page_url(self.resource_id)
                        handle, handle_api_client, credentials = create_and_register_handle_for_resource_url(data_subset_url, initial_doi_dict_values=doi_dict)
                        self.handle_api_client = handle_api_client
                        self.handle = handle
                        # Add the handle metadata to the DOI dict
                        doi_dict = add_handle_data_to_doi_metadata_kernel_dict(handle, doi_dict)
                        # Add the DOI dict metadata to the handle
                        add_doi_metadata_kernel_to_handle(self.handle, doi_dict, self.handle_api_client)
                        
                        add_doi_metadata_kernel_to_data_subset(self.resource_id, doi_dict, xml_file.read())
                        add_handle_to_url_mapping(handle, data_subset_url)

                        # TODO: remove old code
                        with client.start_session() as s:
                            def cb(s):
                                xml_string_with_doi = add_doi_kernel_metadata_to_xml_and_return_updated_string(
                                    doi_dict,
                                    self.resource_id,
                                    xml_file,
                                    self.resource_mongodb_model,
                                    resource_conversion_validate_and_correct_function=self.resource_conversion_validate_and_correct_function,
                                    session=s
                                )
                                update_original_metadata_xml_string(
                                    xml_string_with_doi,
                                    self.resource_id,
                                    session=s
                                )
                                add_handle_to_url_mapping_old(handle, data_subset_url, session=s)
                            s.with_transaction(cb)
                        # End of old code
                        messages.success(request, f'A DOI with name "{self.handle}" has been registered for this data subset.')
                except ExpatError as err:
                    logger.exception('Expat error occurred during DOI registration process.')
                    messages.error(request, f'An error occurred whilst parsing {xml_file.name} during the DOI registration process.')
                except BaseException as err:
                    logger.exception('An unexpected error occurred during DOI registration.')
                    messages.error(request, 'An unexpected error occurred during DOI registration.')
                    if self.handle != None:
                        try:
                            delete_handle(self.handle, self.handle_api_client)
                            logger.info(f'Deleted handle {self.handle} due to an error that occurred during DOI registration.')
                        except BaseException as err:
                            logger.exception(f'Could not delete handle {self.handle} due to an error.')
                            
        else:
            messages.error(request, 'The form submitted was not valid.')
        return super().post(request, *args, **kwargs)

class OrganisationRegisterFormView(ResourceRegisterFormView):
    model = models.Organisation
    resource_mongodb_model = mongodb_models.CurrentOrganisation
    success_url = reverse_lazy('register:organisation')

    validation_url = reverse_lazy('validation:organisation')
    post_url = reverse_lazy('register:organisation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')

class IndividualRegisterFormView(ResourceRegisterFormView):
    model = models.Individual
    resource_mongodb_model = mongodb_models.CurrentIndividual
    success_url = reverse_lazy('register:individual')

    validation_url = reverse_lazy('validation:individual')
    post_url = reverse_lazy('register:individual')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')

class ProjectRegisterFormView(ResourceRegisterFormView):
    model = models.Project
    resource_mongodb_model = mongodb_models.CurrentProject
    success_url = reverse_lazy('register:project')

    validation_url = reverse_lazy('validation:project')
    post_url = reverse_lazy('register:project')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('projects')

class PlatformRegisterFormView(ResourceRegisterFormView):
    model = models.Platform
    resource_mongodb_model = mongodb_models.CurrentPlatform
    success_url = reverse_lazy('register:platform')

    validation_url = reverse_lazy('validation:platform')
    post_url = reverse_lazy('register:platform')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('platforms')

class OperationRegisterFormView(ResourceRegisterFormView):
    model = models.Operation
    resource_mongodb_model = mongodb_models.CurrentOperation
    success_url = reverse_lazy('register:operation')

    validation_url = reverse_lazy('validation:operation')
    post_url = reverse_lazy('register:operation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('operations')

class InstrumentRegisterFormView(ResourceRegisterFormView):
    model = models.Instrument
    resource_mongodb_model = mongodb_models.CurrentInstrument
    success_url = reverse_lazy('register:instrument')

    validation_url = reverse_lazy('validation:instrument')
    post_url = reverse_lazy('register:instrument')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('instruments')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_instrument_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class AcquisitionCapabilitiesRegisterFormView(ResourceRegisterFormView):
    model = models.AcquisitionCapabilities
    resource_mongodb_model = mongodb_models.CurrentAcquisitionCapability
    success_url = reverse_lazy('register:acquisition_capability_set')

    validation_url = reverse_lazy('validation:acquisition_capability_set')
    post_url = reverse_lazy('register:acquisition_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisition capabilities')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_acquisition_capability_set_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class AcquisitionRegisterFormView(ResourceRegisterFormView):
    model = models.Acquisition
    resource_mongodb_model = mongodb_models.CurrentAcquisition
    success_url = reverse_lazy('register:acquisition')

    validation_url = reverse_lazy('validation:acquisition')
    post_url = reverse_lazy('register:acquisition')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('acquisitions')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_acquisition_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class ComputationCapabilitiesRegisterFormView(ResourceRegisterFormView):
    model = models.ComputationCapabilities
    resource_mongodb_model = mongodb_models.CurrentComputationCapability
    success_url = reverse_lazy('register:computation_capability_set')

    validation_url = reverse_lazy('validation:computation_capability_set')
    post_url = reverse_lazy('register:computation_capability_set')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computation capabilities')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_computation_capability_set_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class ComputationRegisterFormView(ResourceRegisterFormView):
    model = models.Computation
    resource_mongodb_model = mongodb_models.CurrentComputation
    success_url = reverse_lazy('register:computation')

    validation_url = reverse_lazy('validation:computation')
    post_url = reverse_lazy('register:computation')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('computations')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_computation_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class ProcessRegisterFormView(ResourceRegisterFormView):
    model = models.Process
    resource_mongodb_model = mongodb_models.CurrentProcess
    success_url = reverse_lazy('register:process')

    validation_url = reverse_lazy('validation:process')
    post_url = reverse_lazy('register:process')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('processes')

    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_process_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class DataCollectionRegisterFormView(ResourceRegisterFormView):
    model = models.DataCollection
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
        context['title'] = f'Register a {self.model.type_readable.title()}'
        context['api_specification_validation_url'] = reverse_lazy('validation:api_specification_url')
        return context
        
    def post(self, request, *args, **kwargs):
        self.resource_conversion_validate_and_correct_function = xml_conversion_checks_and_fixes.correct_data_collection_xml_converted_to_dict
        return super().post(request, *args, **kwargs)

class CatalogueRegisterFormView(ResourceRegisterFormView):
    model = models.Catalogue
    resource_mongodb_model = mongodb_models.CurrentCatalogue
    success_url = reverse_lazy('register:catalogue')
    template_name='register/file_upload_catalogue.html'

    validation_url = reverse_lazy('validation:catalogue')
    post_url = reverse_lazy('register:catalogue')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogues')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class CatalogueEntryRegisterFormView(ResourceRegisterFormView):
    model = models.CatalogueEntry
    resource_mongodb_model = mongodb_models.CurrentCatalogueEntry
    success_url = reverse_lazy('register:catalogue_entry')
    template_name='register/file_upload_catalogue.html'

    validation_url = reverse_lazy('validation:catalogue_entry')
    post_url = reverse_lazy('register:catalogue_entry')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogue entries')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context

class CatalogueDataSubsetRegisterFormView(ResourceRegisterFormView):
    model = models.CatalogueDataSubset
    resource_mongodb_model = mongodb_models.CurrentCatalogueDataSubset
    success_url = reverse_lazy('register:catalogue_data_subset')
    template_name='register/file_upload_catalogue_data_subset.html'
    form_class = UploadCatalogueDataSubsetFileForm

    validation_url = reverse_lazy('validation:catalogue_data_subset')
    post_url = reverse_lazy('register:catalogue_data_subset')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('catalogue data subsets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register a Catalogue Data Subset'
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context
