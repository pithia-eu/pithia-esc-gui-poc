import logging
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import FormView

from .editor_dataclasses import (
    CitationPropertyTypeMetadataUpdate,
    OperationTimeMetadataUpdate,
    PhenomenonTimeMetadataUpdate,
    ResultTimeMetadataUpdate,
    StandardIdentifierMetadataUpdate,
)
from .forms import *
from .form_utils import (
    map_catalogue_data_subset_sources_to_dataclasses,
    map_input_descriptions_to_dataclasses,
    map_processing_inputs_to_dataclasses,
    map_sources_to_dataclasses,
)
from .service_utils import BaseMetadataEditor
from .services import (
    AcquisitionCapabilitiesEditor,
    AcquisitionEditor,
    CatalogueEditor,
    CatalogueDataSubsetEditor,
    CatalogueEntryEditor,
    ComputationCapabilitiesEditor,
    ComputationEditor,
    DataCollectionEditor,
    IndividualEditor,
    InstrumentEditor,
    OperationEditor,
    OrganisationEditor,
    PlatformEditor,
    ProcessEditor,
    ProjectEditor,
    WorkflowEditor,
)
from .view_mixins import *

from common import models
from common.decorators import login_session_institution_required
from datahub_management.view_mixins import (
    CatalogueDataSubsetDataHubViewMixin,
    WorkflowDataHubViewMixin,
)
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE,
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
        metadata_editor.update_standard_identifiers(metadata_editor.metadata_dict, [StandardIdentifierMetadataUpdate(**si) for si in form_cleaned_data.get('standard_identifiers_json')])
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
    DocumentationViewMixin,
    LocationViewMixin,
    PlatformSelectFormViewMixin,
    RelatedPartiesViewMixin,
    RelatedPartiesSelectFormViewMixin,
    SrsNameSelectFormViewMixin,
    ResourceEditorFormView,
    StatusSelectFormViewMixin,
    ResourceChoicesViewMixin):
    form_class = OperationEditorForm
    template_name = 'metadata_editor/operation_editor.html'

    model = models.Operation
    metadata_editor_class = OperationEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Operation.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'

    def add_form_data_to_metadata_editor(self, metadata_editor: OperationEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_status(form_cleaned_data.get('status'))
        metadata_editor.update_platforms(form_cleaned_data.get('platforms'))
        metadata_editor.update_child_operations(form_cleaned_data.get('child_operations'))
        operation_time_update = OperationTimeMetadataUpdate(
            time_period_id=form_cleaned_data.get('time_period_id'),
            time_instant_begin_id=form_cleaned_data.get('time_instant_begin_id'),
            time_instant_begin_position=form_cleaned_data.get('time_instant_begin_position'),
            time_instant_end_id=form_cleaned_data.get('time_instant_end_id'),
            time_instant_end_position=form_cleaned_data.get('time_instant_end_position')
        )
        metadata_editor.update_operation_time(operation_time_update)
        self.update_location_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_documentation_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
    
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
    DocumentationViewMixin,
    InstrumentTypeSelectFormViewMixin,
    RelatedPartiesViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = InstrumentEditorForm
    template_name = 'metadata_editor/instrument_editor.html'

    model = models.Instrument
    metadata_editor_class = InstrumentEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Instrument.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'

    def add_form_data_to_metadata_editor(self, metadata_editor: InstrumentEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_type(form_cleaned_data.get('type'))
        metadata_editor.update_instrument_version(form_cleaned_data.get('version'))
        metadata_editor.update_url(form_cleaned_data.get('url'))
        metadata_editor.update_members(form_cleaned_data.get('members'))
        metadata_editor.update_operational_modes(form_cleaned_data.get('operational_modes_json'))
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_documentation_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)

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
    CapabilitiesViewMixin,
    CapabilitiesSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    DocumentationViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    RelatedPartiesViewMixin,
    ResourceEditorFormView):
    form_class = AcquisitionCapabilitiesEditorForm
    template_name = 'metadata_editor/acquisition_capabilities_editor.html'

    model = models.AcquisitionCapabilities
    metadata_editor_class = AcquisitionCapabilitiesEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.AcquisitionCapabilities.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'

    def add_form_data_to_metadata_editor(self, metadata_editor: AcquisitionCapabilitiesEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_quality_assessment(
            form_cleaned_data.get('data_quality_flags'),
            form_cleaned_data.get('metadata_quality_flags')
        )
        metadata_editor.update_data_levels(form_cleaned_data.get('data_levels'))
        metadata_editor.update_input_descriptions(map_input_descriptions_to_dataclasses(form_cleaned_data))
        metadata_editor.update_instrument_mode_pair(
            form_cleaned_data.get('instrument_mode_pair_instrument'),
            form_cleaned_data.get('instrument_mode_pair_mode')
        )
        self.update_capabilities_with_metadata_editor(
            self.request,
            metadata_editor,
            form_cleaned_data
        )
        self.update_documentation_with_metadata_editor(
            self.request,
            metadata_editor,
            form_cleaned_data
        )
        self.update_related_parties_with_metadata_editor(
            self.request,
            metadata_editor,
            form_cleaned_data
        )

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
        context['input_description_row_content_template'] = render_to_string(
            'metadata_editor/components/acquisition_capabilities/input_description_row_content_template.html',
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
    CapabilityLinksViewMixin,
    PlatformSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = AcquisitionEditorForm
    template_name = 'metadata_editor/acquisition_editor.html'

    model = models.Acquisition
    metadata_editor_class = AcquisitionEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Acquisition.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'

    def add_form_data_to_metadata_editor(self, metadata_editor: AcquisitionEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        self.update_capability_links_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
    
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
    CapabilitiesViewMixin,
    CapabilitiesSelectFormViewMixin,
    ComputationTypeSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    DocumentationViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = ComputationCapabilitiesEditorForm
    template_name = 'metadata_editor/computation_capabilities_editor.html'

    model = models.ComputationCapabilities
    metadata_editor_class = ComputationCapabilitiesEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.ComputationCapabilities.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'

    def add_form_data_to_metadata_editor(self, metadata_editor: ComputationCapabilitiesEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_computation_component_version(form_cleaned_data.get('version'))
        metadata_editor.update_child_computations(form_cleaned_data.get('child_computations'))
        metadata_editor.update_types(form_cleaned_data.get('type'))
        metadata_editor.update_quality_assessment(
            form_cleaned_data.get('data_quality_flags'),
            form_cleaned_data.get('metadata_quality_flags')
        )
        metadata_editor.update_data_levels(form_cleaned_data.get('data_levels'))
        metadata_editor.update_processing_inputs(map_processing_inputs_to_dataclasses(form_cleaned_data))
        software_reference_update = CitationPropertyTypeMetadataUpdate(
            citation_title=form_cleaned_data.get('software_reference_citation_title'),
            citation_publication_date=form_cleaned_data.get('software_reference_citation_publication_date'),
            citation_doi=form_cleaned_data.get('software_reference_citation_doi'),
            citation_url=form_cleaned_data.get('software_reference_citation_linkage_url'),
            other_citation_details=form_cleaned_data.get('software_reference_other_citation_details')
        )
        metadata_editor.update_software_reference(software_reference_update)
        self.update_documentation_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_capabilities_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)


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
    CapabilityLinksViewMixin,
    PlatformSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = ComputationEditorForm
    template_name = 'metadata_editor/computation_editor.html'

    model = models.Computation
    metadata_editor_class = ComputationEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Computation.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'

    def add_form_data_to_metadata_editor(self, metadata_editor: ComputationEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        self.update_capability_links_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)

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
    CapabilitiesViewMixin,
    DataLevelSelectFormViewMixin,
    DocumentationViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = ProcessEditorForm
    template_name = 'metadata_editor/process_editor.html'

    model = models.Process
    metadata_editor_class = ProcessEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Process.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:processes'

    def add_form_data_to_metadata_editor(self, metadata_editor: ProcessEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_acquisition_components(form_cleaned_data.get('acquisitions'))
        metadata_editor.update_computation_components(form_cleaned_data.get('computations'))
        metadata_editor.update_quality_assessment(
            form_cleaned_data.get('data_quality_flags'),
            form_cleaned_data.get('metadata_quality_flags')
        )
        metadata_editor.update_data_levels(form_cleaned_data.get('data_levels'))
        self.update_documentation_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)
        self.update_capabilities_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)

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
        RelatedPartiesViewMixin,
        ResourceEditorFormView):
    form_class = DataCollectionEditorForm
    template_name = 'metadata_editor/data_collection_editor.html'

    model = models.DataCollection
    metadata_editor_class = DataCollectionEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.DataCollection.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:data_collections'

    def add_form_data_to_metadata_editor(self, metadata_editor: DataCollectionEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.set_empty_properties()
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_types(form_cleaned_data.get('types'))
        metadata_editor.update_features_of_interest(form_cleaned_data.get('features_of_interest'))
        metadata_editor.update_permissions(form_cleaned_data.get('permissions'))
        metadata_editor.update_projects(form_cleaned_data.get('projects'))
        metadata_editor.update_procedure(form_cleaned_data.get('process'))
        metadata_editor.update_sub_collections(form_cleaned_data.get('sub_collections'))
        metadata_editor.update_data_levels(form_cleaned_data.get('data_levels'))
        metadata_editor.update_quality_assessment(
            form_cleaned_data.get('data_quality_flags'),
            form_cleaned_data.get('metadata_quality_flags')
        )
        metadata_editor.update_collection_results(map_sources_to_dataclasses(form_cleaned_data))
        self.update_related_parties_with_metadata_editor(self.request, metadata_editor, form_cleaned_data)

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
        annotation_type_choices = list(self.get_choices_from_ontology_category('annotationType'))
        instrument_type_choices = list(self.get_instrument_type_choices_for_form())
        instrument_type_choices.pop(0)
        computation_type_choices = list(self.get_computation_type_choices_for_form())
        computation_type_choices.pop(0)
        return (
            ('', ''),
            ('Annotation Types', annotation_type_choices),
            ('Computation Types', computation_type_choices),
            ('Instrument Types', instrument_type_choices),
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
            'metadata_editor/components/sources_tab_pane_content_template.html',
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


class CatalogueRelatedEditorFormViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_management_category_list_page_breadcrumb_text'] = _CATALOGUE_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:catalogue_related_metadata_index'
        return context


class CatalogueEditorFormView(
    CatalogueRelatedEditorFormViewMixin,
    OntologyCategoryChoicesViewMixin,
    ResourceEditorFormView):
    form_class = CatalogueEditorForm
    template_name = 'metadata_editor/catalogue_editor.html'

    model = models.Catalogue
    metadata_editor_class = CatalogueEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Catalogue.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogues'

    def get_catalogue_category_choices_for_form(self):
        return self.get_choices_from_ontology_category('catalogueCategory')

    def add_form_data_to_metadata_editor(self, metadata_editor: CatalogueEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_catalogue_category(form_cleaned_data.get('catalogue_category'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['catalogue_category_choices'] = self.get_catalogue_category_choices_for_form()
        return kwargs


class CatalogueEntryEditorFormView(
    CatalogueRelatedEditorFormViewMixin,
    ResourceEditorFormView):
    form_class = CatalogueEntryEditorForm
    template_name = 'metadata_editor/catalogue_entry_editor.html'

    model = models.CatalogueEntry
    metadata_editor_class = CatalogueEntryEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.CatalogueEntry.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_entries'

    def add_form_data_to_metadata_editor(self, metadata_editor: CatalogueEntryEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_catalogue_identifier(form_cleaned_data.get('catalogue_identifier'))
        phenomenon_time_update = PhenomenonTimeMetadataUpdate(
            time_period_id=form_cleaned_data.get('time_period_id'),
            time_instant_begin_id=form_cleaned_data.get('time_instant_begin_id'),
            time_instant_begin_position=form_cleaned_data.get('time_instant_begin_position').replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
            time_instant_end_id=form_cleaned_data.get('time_instant_end_id'),
            time_instant_end_position=form_cleaned_data.get('time_instant_end_position').replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        )
        metadata_editor.update_phenomenon_time(phenomenon_time_update)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['catalogue_choices'] = self.get_resource_choices_with_model(models.Catalogue)
        return kwargs


class CatalogueDataSubsetEditorFormView(
    CatalogueDataSubsetDataHubViewMixin,
    CatalogueRelatedEditorFormViewMixin,
    DataCollectionSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    ResourceEditorFormView):
    form_class = CatalogueDataSubsetForm
    template_name = 'metadata_editor/catalogue_data_subset_editor.html'

    model = models.CatalogueDataSubset
    metadata_editor_class = CatalogueDataSubsetEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.CatalogueDataSubset.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:catalogue_data_subsets'
    
    def get_sources_tab_pane_content_template_path(self):
        return 'metadata_editor/components/catalogue_data_subset/sources_tab_pane_content_template.html'

    def get_sources_tab_pane_content_template(self, context):
        return render_to_string(
            self.get_sources_tab_pane_content_template_path(),
            context=context
        )

    def add_form_data_to_metadata_editor(self, metadata_editor: CatalogueDataSubsetEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        metadata_editor.update_entry_identifier(form_cleaned_data.get('entry_identifier'))
        metadata_editor.update_data_collection(form_cleaned_data.get('data_collection'))
        result_time_update = ResultTimeMetadataUpdate(
            time_period_id=form_cleaned_data.get('time_period_id'),
            time_instant_begin_id=form_cleaned_data.get('time_instant_begin_id'),
            time_instant_begin_position=form_cleaned_data.get('time_instant_begin_position').replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
            time_instant_end_id=form_cleaned_data.get('time_instant_end_id'),
            time_instant_end_position=form_cleaned_data.get('time_instant_end_position').replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        )
        metadata_editor.update_result_time(result_time_update)
        metadata_editor.update_data_levels([form_cleaned_data.get('data_levels')])
        metadata_editor.update_quality_assessment(
            form_cleaned_data.get('data_quality_flags'),
            form_cleaned_data.get('metadata_quality_flags'),
            is_max_occurs_unbounded=False
        )
        self.valid_sources = metadata_editor.update_sources(
            map_catalogue_data_subset_sources_to_dataclasses(
                form_cleaned_data,
                is_file_uploaded_for_each_online_resource=form_cleaned_data.get('is_file_uploaded_for_each_online_resource')
            )
        )

    def get_catalogue_entry_choices_for_form(self):
        catalogue_entries = self.get_resources_with_model_ordered_by_name(models.CatalogueEntry)
        UNKNOWN_KEY = 'ZZZ'
        entries_by_catalogue = {
            UNKNOWN_KEY: {
                'name': UNKNOWN_KEY,
                'entries': [],
            }
        }
        # Sort catalogue entries by catalogue ID
        for entry in catalogue_entries:
            catalogue_id = entry.properties.catalogue_identifier.split('/')[-1]
            if not catalogue_id:
                entries_by_catalogue[UNKNOWN_KEY]['entries'].append(entry)
                continue
            if catalogue_id not in entries_by_catalogue:
                entries_by_catalogue[catalogue_id] = {
                    'name': catalogue_id,
                    'entries': [],
                }
            entries_by_catalogue[catalogue_id]['entries'].append(entry)
        # Map each catalogue ID to a name
        for catalogue_id, optgroup_data in entries_by_catalogue.items():
            try:
                catalogue = models.Catalogue.objects.get(pk=catalogue_id)
                optgroup_data.update({
                    'name': catalogue.name,
                })
            except models.Catalogue.DoesNotExist:
                pass
        # Sort catalogues by name
        entries_by_catalogue = dict(sorted(entries_by_catalogue.items(), key=lambda item: item[1]['name']))
        # Create optgroups and options for select
        choices_categorised = []
        for catalogue_id, optgroup_data in entries_by_catalogue.items():
            optgroup_name = optgroup_data.get('name')
            if optgroup_name == UNKNOWN_KEY:
                optgroup_name = 'Unknown'
            choices_categorised.append(
                (
                    optgroup_name,
                    list(
                        (entry.metadata_server_url, entry.name)
                        for entry in optgroup_data.get('entries')
                    )
                )
            )
        return (
            ('', ''),
            *choices_categorised,
        )

    def get_service_function_choices_for_form(self):
        return self.get_choices_from_ontology_category('serviceFunction')

    def get_data_format_choices_for_form(self):
        return self.get_choices_from_ontology_category('resultDataFormat')

    def check_source_names(self, form):
        source_names = [source.get('name', '') for source in form.cleaned_data.get('sources_json')]
        source_names_normalised = set(source_name.lower().strip() for source_name in source_names)
        return len(source_names) == len(source_names_normalised)

    def form_valid(self, form):
        self.source_files = self.request.FILES
        is_each_source_name_unique = True
        try:
            is_each_source_name_unique = self.check_source_names(form)
        except Exception as err:
            logger.exception(err)
            messages.error(self.request, 'An unexpected error occurred.')
            return self.form_invalid(form)

        if not is_each_source_name_unique:
            form.add_error('sources_json', 'Online resource names must be unique.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sources_tab_pane_content_template_path'] = self.get_sources_tab_pane_content_template_path()
        context['sources_tab_pane_content_template'] = self.get_sources_tab_pane_content_template(context)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data_collection_choices'] = self.get_data_collection_choices_for_form()
        kwargs['catalogue_entry_choices'] = self.get_catalogue_entry_choices_for_form()
        kwargs['data_level_choices'] = self.get_data_level_choices_for_form()
        kwargs['data_quality_flag_choices'] = self.get_data_quality_flag_choices_for_form()
        kwargs['metadata_quality_flag_choices'] = self.get_metadata_quality_flag_choices_for_form()
        # Sources
        kwargs['service_function_choices'] = self.get_service_function_choices_for_form()
        kwargs['data_format_choices'] = self.get_data_format_choices_for_form()
        return kwargs


class WorkflowEditorFormView(
    DataCollectionSelectFormViewMixin,
    ResourceEditorFormView,
    WorkflowDataHubViewMixin):
    form_class = WorkflowEditorForm
    template_name = 'metadata_editor/workflow_editor.html'

    model = models.Workflow
    metadata_editor_class = WorkflowEditor

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Workflow.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'

    def add_form_data_to_metadata_editor(self, metadata_editor: WorkflowEditor, form_cleaned_data):
        super().add_form_data_to_metadata_editor(metadata_editor, form_cleaned_data)
        metadata_editor.update_description(form_cleaned_data.get('description'))
        data_collections = [form_cleaned_data.get('data_collection_1')] + form_cleaned_data.get('data_collection_2_and_others')
        metadata_editor.update_data_collections(data_collections)
        if self.workflow_details_file_source == 'existing':
            return
        elif self.workflow_details_file_source == 'file_upload':
            metadata_editor.update_workflow_details('TEMP_WORKFLOW_DETAILS_URL')
            return
        metadata_editor.update_workflow_details(form_cleaned_data.get('workflow_details'))
    
    def get_index_of_workflow_details_file_source_choice(self, choice_value: str):
        try:
            return [
                choice[0]
                for choice in self.form_class().fields.get('workflow_details_file_source').choices
            ].index(choice_value)
        except ValueError:
            logger.exception(f'Workflow details source choice, "{choice_value}" does not exist!')
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workflow_details_file_source_file_upload_choice_index'] = self.get_index_of_workflow_details_file_source_choice('file_upload')
        context['workflow_details_file_source_external_choice_index'] = self.get_index_of_workflow_details_file_source_choice('external')
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data_collection_choices'] = self.get_data_collection_choices_for_form()
        return kwargs
