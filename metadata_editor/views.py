import logging
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import FormView

from .forms import *
from .service_utils import BaseMetadataEditor
from .services import (
    IndividualEditor,
    OrganisationEditor,
    ProjectEditor,
    PlatformEditor,
)
from .view_mixins import *

from common import models
from common.decorators import login_session_institution_required
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title
)
from user_management.services import (
    get_user_id_for_login_session,
    get_institution_id_for_login_session,
)


logger = logging.getLogger(__name__)


# Create your views here.

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceEditorFormView(
    FormView,
    OrganisationSelectFormViewMixin,
    ResourceChoicesViewMixin):
    success_url = ''
    form_class = None
    template_name = ''

    model = None
    metadata_editor_class = None
    save_data_local_storage_key = ''
    file_upload_registration_url = ''
    resource_management_list_page_breadcrumb_url_name = ''
    resource_management_list_page_breadcrumb_text = ''
    submit_button_text = 'Validate and Submit'

    institution_id = None
    owner_id = None

    def add_form_data_to_metadata_editor(self, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        metadata_editor.update_name(form_cleaned_data.get('name'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = self.get_form()
        context['success_url'] = self.success_url
        context['metadata_type_readable'] = self.model.type_readable.title()
        context['save_data_local_storage_key'] = self.save_data_local_storage_key
        if 'title' not in context:
            context['title'] = f'{self.model.type_readable.title()} Wizard'
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        context['submit_button_text'] = self.submit_button_text
        return context

    def form_invalid(self, form):
        messages.error(self.request, f'The form submitted was not valid. See the form below for details.')
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['form_metadata_type'] = self.model.type_readable.title()
        return kwargs

class OrganisationEditorFormView(
    ResourceEditorFormView,
    ContactInfoViewMixin):
    form_class = OrganisationEditorForm
    template_name = 'metadata_editor/organisation_editor.html'

    model = models.Organisation
    metadata_editor_class = OrganisationEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'

    def add_form_data_to_metadata_editor(self, metadata_editor: OrganisationEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_short_name(form_cleaned_data.get('short_name'))
        self.update_contact_info_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)


class IndividualEditorFormView(
    ResourceEditorFormView,
    ContactInfoViewMixin):
    form_class = IndividualEditorForm
    template_name = 'metadata_editor/individual_editor.html'

    model = models.Individual
    metadata_editor_class = IndividualEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'

    def add_form_data_to_metadata_editor(self, metadata_editor: IndividualEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_position_name(form_cleaned_data.get('position_name'))
        metadata_editor.update_organisation(form_cleaned_data.get('organisation'))
        self.update_contact_info_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)


class ProjectEditorFormView(
    DocumentationViewMixin,
    RelatedPartiesSelectFormViewMixin,
    RelatedPartiesViewMixin,
    ResourceEditorFormView,
    StatusSelectFormViewMixin):
    form_class = ProjectEditorForm
    template_name = 'metadata_editor/project_editor.html'

    model = models.Project
    metadata_editor_class = ProjectEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Project.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'

    def add_form_data_to_metadata_editor(self, metadata_editor: ProjectEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_short_name(form_cleaned_data.get('short_name'))
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_abstract(form_cleaned_data.get('abstract'))
        metadata_editor.update_status(form_cleaned_data.get('status'))
        metadata_editor.update_url(form_cleaned_data.get('url'))
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_documentation_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['status_choices'] = self.get_status_choices_for_form()
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citation_section_description'] = 'Reference to documentation describing the project.'
        context['related_parties_section_description'] = 'Individual or organisation related to the project.'
        return context

class PlatformEditorFormView(
    DocumentationViewMixin,
    LocationViewMixin,
    PlatformSelectFormViewMixin,
    RelatedPartiesViewMixin,
    RelatedPartiesSelectFormViewMixin,
    SrsNameSelectFormViewMixin,
    StandardIdentifiersFormViewMixin,
    ResourceEditorFormView):
    form_class = PlatformEditorForm
    template_name = 'metadata_editor/platform_editor.html'

    model = models.Platform
    metadata_editor_class = PlatformEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Platform.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'

    def add_form_data_to_metadata_editor(self, metadata_editor: PlatformEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_short_name(form_cleaned_data.get('short_name'))
        metadata_editor.update_child_platforms(form_cleaned_data.get('child_platforms'))
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_url(form_cleaned_data.get('url'))
        metadata_editor.update_type(form_cleaned_data.get('type'))
        metadata_editor.update_standard_identifiers(form_cleaned_data.get('standard_identifiers_json'))
        self.update_location_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_documentation_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)

    def get_type_choices_for_form(self):
        return self.get_choices_from_ontology_category('platformType')

    def get_child_platform_choices_for_form(self):
        return self.get_platform_choices_for_form()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['type_choices'] = self.get_type_choices_for_form()
        kwargs['child_platform_choices'] = self.get_child_platform_choices_for_form()
        kwargs['crs_choices'] = self.get_crs_choices_for_form()
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location_section_description'] = 'Location of the platform. Note, that it is only applicable to static platforms or geo-stationary satellites.'
        context['geo_location_description'] = f'The LAT, LON coordinates of the position of the platform. "{context.get("form").fields.get("geometry_location_point_srs_name").label}" describes the coordinate system.'
        context['citation_section_description'] = 'Reference to documentation describing the platform.'
        context['related_parties_section_description'] = 'Responsibility, identification of, and means of communication with associated person(s) and organisations. A facility owning a platform can be described here.'
        context['standard_identifier_row_content_template'] = render_to_string(
            'metadata_editor/components/platform/platform_standard_identifier_row_content_template.html',
            context=context
        )
        return context


class OperationEditorFormView(
    PlatformSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    SrsNameSelectFormViewMixin,
    ResourceEditorFormView,
    StatusSelectFormViewMixin,
    ResourceChoicesViewMixin):
    form_class = OperationEditorForm
    template_name = 'metadata_editor/operation_editor.html'

    model = models.Operation

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Operation.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'

    def get_child_operation_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Operation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citation_section_description'] = 'Reference to documentation describing the operation.'
        context['related_parties_section_description'] = 'Individual or organisation related to platform operation.'
        context['location_section_description'] = 'Location of the platform operation.'
        context['location_section_example'] = 'A flight line or a ship track for a platform such as an aircraft or a ship respectively.'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['platform_choices'] = self.get_platform_choices_for_form()
        kwargs['child_operation_choices'] = self.get_child_operation_choices_for_form()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['crs_choices'] = self.get_crs_choices_for_form()
        kwargs['status_choices'] = self.get_status_choices_for_form()
        return kwargs


class InstrumentEditorFormView(
    InstrumentTypeSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = InstrumentEditorForm
    template_name = 'metadata_editor/instrument_editor.html'

    model = models.Instrument

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Instrument.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'

    def get_member_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Instrument)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_section_description'] = 'Information regarding organisations and/or individuals related to instrument.'
        context['citation_section_description'] = 'Reference to documentation describing the instrument.'
        context['operational_mode_row_content_template'] = render_to_string(
            'metadata_editor/components/instrument/operational_mode_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instrument_type_choices'] = self.get_instrument_type_choices_for_form()
        kwargs['member_choices'] = self.get_member_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        return kwargs


class AcquisitionCapabilitiesEditorFormView(
    CapabilitiesSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = AcquisitionCapabilitiesEditorForm
    template_name = 'metadata_editor/acquisition_capabilities_editor.html'

    model = models.AcquisitionCapabilities

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.AcquisitionCapabilities.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'

    def get_instrument_choices_with_oms_for_form(self):
        instruments = self.get_resources_with_model_ordered_by_name(models.Instrument)
        return (
            ('', ''),
            *[(instrument.metadata_server_url, instrument.name) for instrument in instruments if instrument.operational_modes],
        )

    def get_instrument_operational_modes_for_form(self):
        instruments = self.get_resources_with_model_ordered_by_name(models.Instrument)
        operational_modes_by_instrument = []
        for instrument in instruments:
            operational_modes = instrument.operational_modes
            if not operational_modes:
                continue
            operational_modes_by_instrument.append((
                instrument.name,
                [(f'{instrument.metadata_server_url}#{om.get("id")}', om.get('name')) for om in operational_modes]
            ))

        return (
            ('', ''),
            *operational_modes_by_instrument,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citation_section_description'] = 'Reference to documentation describing the component.'
        context['related_parties_section_description'] = 'Individual or organisation related to acquisition.'
        context['capabilities_tab_content_template'] = render_to_string(
            'metadata_editor/components/capabilities_tab_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data_level_choices'] = self.get_data_level_choices_for_form()
        kwargs['data_quality_flag_choices'] = self.get_data_quality_flag_choices_for_form()
        kwargs['metadata_quality_flag_choices'] = self.get_metadata_quality_flag_choices_for_form()
        # Capabilities
        kwargs['coordinate_system_choices'] = self.get_coordinate_system_choices_for_form()
        kwargs['dimensionality_instance_choices'] = self.get_dimensionality_instance_choices_for_form()
        kwargs['dimensionality_timeline_choices'] = self.get_dimensionality_timeline_choices_for_form()
        kwargs['observed_property_choices'] = self.get_observed_property_choices_for_form()
        kwargs['qualifier_choices'] = self.get_qualifier_choices_for_form()
        kwargs['unit_choices'] = self.get_unit_choices_for_form()
        kwargs['vector_representation_choices'] = self.get_vector_representation_choices_for_form()
        # Instrument mode pairs
        kwargs['instrument_choices'] = self.get_instrument_choices_with_oms_for_form()
        kwargs['operational_mode_choices'] = self.get_instrument_operational_modes_for_form()
        # Related parties
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        return kwargs


class AcquisitionEditorFormView(
    PlatformSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = AcquisitionEditorForm
    template_name = 'metadata_editor/acquisition_editor.html'

    model = models.Acquisition

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Acquisition.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'

    def get_acquisition_capability_sets_for_form(self):
        return self.get_resource_choices_with_model(models.AcquisitionCapabilities)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['capability_links_tab_pane_content_template'] = render_to_string(
            'metadata_editor/components/capability_links_tab_pane_content_template.html',
            context=context
        )
        context['capability_link_standard_identifier_row_content_template'] = render_to_string(
            'metadata_editor/components/acquisition_and_computation/capability_link_standard_identifier_row_content_template.html',
            context=context
        )
        context['capability_link_time_span_row_content_template'] = render_to_string(
            'metadata_editor/components/acquisition_and_computation/capability_link_time_span_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['capability_set_choices'] = self.get_acquisition_capability_sets_for_form()
        kwargs['platform_choices'] = self.get_platform_choices_for_form()
        return kwargs


class ComputationCapabilitiesEditorFormView(
    CapabilitiesSelectFormViewMixin,
    ComputationTypeSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = ComputationCapabilitiesEditorForm
    template_name = 'metadata_editor/computation_capabilities_editor.html'

    model = models.ComputationCapabilities

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.ComputationCapabilities.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'

    def get_child_computation_choices_for_form(self):
        return self.get_resource_choices_with_model(models.ComputationCapabilities)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_section_description'] = 'Individual or organisation related to Computation.'
        context['citation_section_description'] = 'Reference to documentation describing the component.'
        context['capabilities_tab_content_template'] = render_to_string(
            'metadata_editor/components/capabilities_tab_content_template.html',
            context=context
        )
        context['processing_input_row_content_template'] = render_to_string(
            'metadata_editor/components/computation_capabilities/processing_input_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data_level_choices'] = self.get_data_level_choices_for_form()
        kwargs['data_quality_flag_choices'] = self.get_data_quality_flag_choices_for_form()
        kwargs['metadata_quality_flag_choices'] = self.get_metadata_quality_flag_choices_for_form()
        kwargs['child_computation_choices'] = self.get_child_computation_choices_for_form()
        kwargs['computation_type_choices'] = self.get_computation_type_choices_for_form()
        # Capabilities
        kwargs['coordinate_system_choices'] = self.get_coordinate_system_choices_for_form()
        kwargs['dimensionality_instance_choices'] = self.get_dimensionality_instance_choices_for_form()
        kwargs['dimensionality_timeline_choices'] = self.get_dimensionality_timeline_choices_for_form()
        kwargs['observed_property_choices'] = self.get_observed_property_choices_for_form()
        kwargs['qualifier_choices'] = self.get_qualifier_choices_for_form()
        kwargs['unit_choices'] = self.get_unit_choices_for_form()
        kwargs['vector_representation_choices'] = self.get_vector_representation_choices_for_form()
        # Related parties
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        return kwargs


class ComputationEditorFormView(
    PlatformSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = ComputationEditorForm
    template_name = 'metadata_editor/computation_editor.html'

    model = models.Computation

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Computation.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'

    def get_computation_capability_set_choices_for_form(self):
        return self.get_resource_choices_with_model(models.ComputationCapabilities)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['capability_links_tab_pane_content_template'] = render_to_string(
            'metadata_editor/components/capability_links_tab_pane_content_template.html',
            context=context
        )
        context['capability_link_standard_identifier_row_content_template'] = render_to_string(
            'metadata_editor/components/acquisition_and_computation/capability_link_standard_identifier_row_content_template.html',
            context=context
        )
        context['capability_link_time_span_row_content_template'] = render_to_string(
            'metadata_editor/components/acquisition_and_computation/capability_link_time_span_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['platform_choices'] = self.get_platform_choices_for_form()
        kwargs['capability_set_choices'] = self.get_computation_capability_set_choices_for_form()
        return kwargs


class ProcessEditorFormView(
    CapabilitiesSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = ProcessEditorForm
    template_name = 'metadata_editor/process_editor.html'

    model = models.Process

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Process.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'

    def get_acquisition_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Acquisition)

    def get_computation_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Computation)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_section_description'] = 'Individual or organisation related to composite process.'
        context['citation_section_description'] = 'Reference to documentation describing the component.'
        context['capabilities_tab_content_template'] = render_to_string(
            'metadata_editor/components/capabilities_tab_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Process
        kwargs['acquisition_choices'] = self.get_acquisition_choices_for_form()
        kwargs['computation_choices'] = self.get_computation_choices_for_form()
        # Capabilities
        kwargs['coordinate_system_choices'] = self.get_coordinate_system_choices_for_form()
        kwargs['dimensionality_instance_choices'] = self.get_dimensionality_instance_choices_for_form()
        kwargs['dimensionality_timeline_choices'] = self.get_dimensionality_timeline_choices_for_form()
        kwargs['observed_property_choices'] = self.get_observed_property_choices_for_form()
        kwargs['qualifier_choices'] = self.get_qualifier_choices_for_form()
        kwargs['unit_choices'] = self.get_unit_choices_for_form()
        kwargs['vector_representation_choices'] = self.get_vector_representation_choices_for_form()
        # Data levels
        kwargs['data_level_choices'] = self.get_data_level_choices_for_form()
        kwargs['data_quality_flag_choices'] = self.get_data_quality_flag_choices_for_form()
        # Quality assessment
        kwargs['metadata_quality_flag_choices'] = self.get_metadata_quality_flag_choices_for_form()
        # Related parties
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        return kwargs


class DataCollectionEditorFormView(
    ComputationTypeSelectFormViewMixin,
    DataCollectionSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    InstrumentTypeSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = DataCollectionEditorForm
    template_name = 'metadata_editor/data_collection_editor.html'

    model = models.DataCollection

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.DataCollection.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'

    def register_api_interaction_method(self, request, new_registration):
        try:
            api_specification_url = request.POST.get('api_specification_url', None)
            api_description = request.POST.get('api_description', '')
            if not api_specification_url:
                return
            models.InteractionMethod.api_interaction_methods.create_api_interaction_method(
                api_specification_url,
                api_description,
                new_registration
            )
            messages.success(request, f'<p>Added an API interaction method for {escape(new_registration.name)}.</p><p class="mb-0">It can be viewed and/or updated from the <a href="{reverse_lazy("update:data_collection_interaction_methods", kwargs={"resource_id": new_registration.pk})}">interaction methods page</a> for this data collection.</p>')
        except BaseException as err:
            logger.exception('An unexpected error occurred during API interaction method registration.')
            messages.error(request, 'An unexpected error occurred during API interaction method registration.')
    
    def run_registration_actions(self, request, xml_file, name):
        new_registration = self.register_xml_file(request, xml_file, name)
        self.register_api_interaction_method(request, new_registration)
        return new_registration

    def get_feature_of_interest_choices_for_form(self):
        return self.get_choices_from_ontology_category('featureOfInterest')

    def get_permission_choices_for_form(self):
        return self.get_choices_from_ontology_category('licence')

    def get_type_choices_for_form(self):
        instrument_type_choices = list(self.get_instrument_type_choices_for_form())
        instrument_type_choices.pop(0)
        computation_type_choices = list(self.get_computation_type_choices_for_form())
        computation_type_choices.pop(0)
        return (
            ('', ''),
            ('Instrument Types', instrument_type_choices),
            ('Computation Types', computation_type_choices),
        )

    def get_project_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Project)

    def get_process_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Process)

    def get_service_function_choices_for_form(self):
        return self.get_choices_from_ontology_category('serviceFunction')

    def get_data_format_choices_for_form(self):
        return self.get_choices_from_ontology_category('resultDataFormat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_section_description'] = 'Individual or organisation related to composite process.'
        context['sources_tab_pane_content_template'] = render_to_string(
            'metadata_editor/components/data_collection/sources_tab_pane_content_template.html',
            context=context
        )
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data_level_choices'] = self.get_data_level_choices_for_form()
        kwargs['type_choices'] = self.get_type_choices_for_form()
        kwargs['project_choices'] = self.get_project_choices_for_form()
        kwargs['feature_of_interest_choices'] = self.get_feature_of_interest_choices_for_form()
        kwargs['permission_choices'] = self.get_permission_choices_for_form()
        kwargs['process_choices'] = self.get_process_choices_for_form()
        # Quality assessment
        kwargs['data_quality_flag_choices'] = self.get_data_quality_flag_choices_for_form()
        kwargs['metadata_quality_flag_choices'] = self.get_metadata_quality_flag_choices_for_form()
        # Related parties
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        # Sub collection
        kwargs['sub_collection_choices'] = self.get_data_collection_choices_for_form()
        # Collection results
        kwargs['service_function_choices'] = self.get_service_function_choices_for_form()
        kwargs['data_format_choices'] = self.get_data_format_choices_for_form()
        return kwargs

class WorkflowEditorFormView(
    DataCollectionSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = WorkflowEditorForm
    template_name = 'metadata_editor/workflow_editor.html'

    model = models.Workflow

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Workflow.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data_collection_choices'] = self.get_data_collection_choices_for_form()
        return kwargs
