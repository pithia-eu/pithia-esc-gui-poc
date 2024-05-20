import logging
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic import (
    FormView,
    View,
)
from pyexpat import ExpatError
from rdflib.namespace._SKOS import SKOS
from xmlschema import XMLSchemaException

from .forms import *
from .metadata_builder.metadata_structures import *
from .metadata_builder.utils import *

from common import models
from common.decorators import login_session_institution_required
from ontology.utils import get_graph_of_pithia_ontology_component
from resource_management.views import (
    _INDEX_PAGE_TITLE,
    _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE,
    _create_manage_resource_page_title
)
from user_management.services import (
    get_user_id_for_login_session,
    get_institution_id_for_login_session,
)
from validation.file_wrappers import XMLMetadataFile
from validation.services import MetadataFileXSDValidator


logger = logging.getLogger(__name__)


# Create your views here.

@method_decorator(login_session_institution_required, name='dispatch')
class ResourceRegisterWithEditorFormView(FormView):
    success_url = ''
    form_class = None
    template_name = ''

    model = None
    metadata_builder_class = None
    file_upload_registration_url = ''
    resource_management_list_page_breadcrumb_url_name = ''
    resource_management_list_page_breadcrumb_text = ''

    institution_id = None
    owner_id = None

    def process_form(self, form_cleaned_data):
        # Make copy of cleaned data
        processed_form = form_cleaned_data
        processed_form['localid'] = f'{self.model.localid_base}_{processed_form["localid"]}'
        processed_form['namespace'] = processed_form['namespace']
        return processed_form

    def register_xml_file(self, request, xml_file, name):
        self.model.objects.create_from_xml_string(
            xml_file.read(),
            self.institution_id,
            self.owner_id,
        )
        messages.success(request, f'Successfully registered {name}.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in kwargs:
            context['form'] = self.get_form()
        context['success_url'] = self.success_url
        context['localid_base'] = self.model.localid_base
        context['title'] = f'New {self.model.type_readable.title()}'
        context['organisation_short_names'] = {o.metadata_server_url: o.short_name for o in models.Organisation.objects.all()}
        context['localid_validation_url'] = reverse_lazy('validation:new_localid')
        context['resource_management_index_page_breadcrumb_text'] = _INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_text'] = _DATA_COLLECTION_MANAGEMENT_INDEX_PAGE_TITLE
        context['resource_management_category_list_page_breadcrumb_url_name'] = 'resource_management:data_collection_related_metadata_index'
        context['resource_management_list_page_breadcrumb_text'] = self.resource_management_list_page_breadcrumb_text
        context['resource_management_list_page_breadcrumb_url_name'] = self.resource_management_list_page_breadcrumb_url_name
        return context

    def form_valid(self, form):
        try:
            processed_form = self.process_form(form.cleaned_data)
            metadata_builder = self.metadata_builder_class(processed_form)
            xml = metadata_builder.xml
            localid = processed_form['localid']
            name = processed_form['name']
            xml_file = SimpleUploadedFile(f'{localid}.xml', xml.encode('utf-8'))
        except BaseException as err:
            logger.exception('An unexpected error occurred during XML generation.')
            messages.error(self.request, 'An unexpected error occurred during XML generation.')
            return self.render_to_response(self.get_context_data(form=form))

        try:
            MetadataFileXSDValidator.validate(XMLMetadataFile.from_file(xml_file))
        except XMLSchemaException as err:
            logger.exception('Generated XML failed schema validation.')
            form_error_msg = f'''
            This form was unable to be processed into schema-valid XML due to an error.
            Please try submitting the form again, or if the issue persists,
            <a href="{reverse_lazy('support')}" target="_blank">let our support team know</a>.
            <br><br>
            If this functionality is down, the <a href="{self.file_upload_registration_url}">file upload functionality</a>
            may alternatively be used to register your metadata.
            <br><br>
            We apologise for any inconvenience caused.
            <details>
                <summary class="mt-4">
                    <small>Validation feedback</small>
                </summary>
                <p class="mt-2 mb-0">
                    <small style="white-space: pre-wrap;">{escape(err).strip()}</small>
                </p>
            </details>
            '''
            messages.error(self.request, form_error_msg)
            return self.render_to_response(self.get_context_data(form=form))
        except BaseException as err:
            logger.exception('An unexpected error occurred whilst running XSD validation on generated XML.')
            form_error_msg = f'''
            An unexpected error occurred whilst validating the generated XML against the schema.
            Please try submitting the form again, or if the issue persists,
            <a href="{reverse_lazy('support')}" target="_blank">let our support team know</a>.
            <br><br>
            If this functionality is down, the <a href="{self.file_upload_registration_url}">file upload functionality</a>
            may alternatively be used to register your metadata.
            <br><br>
            We apologise for any inconvenience caused.
            '''
            messages.error(self.request, form_error_msg)
            return self.render_to_response(self.get_context_data(form=form))
        
        try:
            xml_file.seek(0)
            self.register_xml_file(self.request, xml_file, name)
        except ExpatError as err:
            logger.exception('Expat error occurred during registration process.')
            messages.error(self.request, f'There was a problem during XML generation. Please report this error to our support team.')
            return self.render_to_response(self.get_context_data(form=form))
        except IntegrityError as err:
            logger.exception('The local ID submitted is already in use.')
            messages.error(self.request, 'The local ID submitted is already in use.')
            return self.render_to_response(self.get_context_data(form=form))
        except BaseException as err:
            logger.exception('An unexpected error occurred during registration.')
            messages.error(self.request, 'An unexpected error occurred during registration.')
            return self.render_to_response(self.get_context_data(form=form))
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'The form submitted was not valid.')
        return super().form_invalid(form)
    
    def dispatch(self, request, *args, **kwargs):
        self.institution_id = get_institution_id_for_login_session(request.session)
        self.owner_id = get_user_id_for_login_session(request.session)
        return super().dispatch(request, *args, **kwargs)

class CapabilitiesSelectFormViewMixin(View):
    def get_observed_property_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('observedProperty')
        observed_property_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            observed_property_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in observed_property_dict.items()],
        )

    def get_coordinate_system_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('crs')
        crs_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            crs_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in crs_dict.items()],
        )

    def get_dimensionality_instance_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('dimensionalityInstance')
        dimensionality_instance_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            dimensionality_instance_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in dimensionality_instance_dict.items()],
        )

    def get_dimensionality_timeline_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('dimensionalityTimeline')
        dimensionality_timeline_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            dimensionality_timeline_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in dimensionality_timeline_dict.items()],
        )

    def get_qualifier_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('qualifier')
        qualifier_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            qualifier_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in qualifier_dict.items()],
        )

    def get_unit_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('unit')
        unit_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            unit_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in unit_dict.items()],
        )

    def get_vector_representation_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('component')
        component_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            component_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in component_dict.items()],
        )

class DataLevelSelectFormViewMixin(View):
    def get_data_level_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('dataLevel')
        data_level_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            data_level_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in data_level_dict.items()],
        )

class SrsNameSelectFormViewMixin(View):
    def get_crs_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('crs')
        crs_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            crs_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in crs_dict.items()],
        )

class OrganisationSelectFormViewMixin(View):
    def get_organisation_choices_for_form(self):
        return (
            ('', ''),
            *[(o.metadata_server_url, o.name) for o in models.Organisation.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

class PlatformSelectFormViewMixin(View):
    def get_platform_choices_for_form(self):
        return (
            ('', ''),
            *[(p.metadata_server_url, p.name) for p in models.Platform.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

class QualityAssessmentSelectFormViewMixin(View):
    def get_data_quality_flag_choices_for_form(self):
        g_dqf = get_graph_of_pithia_ontology_component('dataQualityFlag')
        dqf_dict = {}
        for s, p, o in g_dqf.triples((None, SKOS.member, None)):
            o_pref_label = g_dqf.value(o, SKOS.prefLabel)
            dqf_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in dqf_dict.items()],
        )

    def get_metadata_quality_flag_choices_for_form(self):
        g_mqf = get_graph_of_pithia_ontology_component('metadataQualityFlag')
        mqf_dict = {}
        for s, p, o in g_mqf.triples((None, SKOS.member, None)):
            o_pref_label = g_mqf.value(o, SKOS.prefLabel)
            mqf_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *[(key, value) for key, value in mqf_dict.items()],
        )

class RelatedPartiesSelectFormViewMixin(View):
    def get_related_party_choices_for_form(self):
        return (
            ('', ''),
            ('Organisations', list(
                (o.metadata_server_url, o.name) for o in models.Organisation.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
            )),
            ('Individuals', list(
                (o.metadata_server_url, o.name) for o in models.Individual.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
            ))
        )

    def get_related_party_role_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('relatedPartyRole')
        status_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            status_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *((key, value) for key, value in status_dict.items())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_row_content_template'] = render_to_string(
            'register_with_support/components/related_parties_row_content_template.html',
            context=context
        )
        return context


class StandardIdentifiersFormViewMixin(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standard_identifier_row_content_template'] = render_to_string(
            'register_with_support/components/standard_identifier_row_content_template.html',
            context=context
        )
        return context

class StatusSelectFormViewMixin(View):
    def get_status_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('status')
        status_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            status_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *((key, value) for key, value in status_dict.items())
        )
    


class OrganisationRegisterWithEditorFormView(ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:organisation_with_editor')
    form_class = OrganisationEditorForm
    template_name = 'register_with_support/organisation_editor.html'

    model = models.Organisation
    metadata_builder_class = OrganisationMetadata
    file_upload_registration_url = reverse_lazy('register:organisation')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('organisations')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:organisations'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['namespace'] = 'pithia'

        # Hours of service
        hours_of_service = process_hours_of_service_in_form(form_cleaned_data)
        processed_form['hours_of_service'] = hours_of_service
        
        # Contact info
        processed_form['contact_info'] = process_contact_info_in_form(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'namespace': 'pithia'}
        return kwargs

class IndividualRegisterWithEditorFormView(OrganisationSelectFormViewMixin, ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:individual_with_editor')
    form_class = IndividualEditorForm
    template_name = 'register_with_support/individual_editor.html'

    model = models.Individual
    metadata_builder_class = IndividualMetadata
    file_upload_registration_url = reverse_lazy('register:individual')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title('individuals')
    resource_management_list_page_breadcrumb_url_name = 'resource_management:individuals'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        # Hours of service
        hours_of_service = process_hours_of_service_in_form(form_cleaned_data)
        processed_form['hours_of_service'] = hours_of_service
        
        # Contact info
        processed_form['contact_info'] = process_contact_info_in_form(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        return kwargs

class ProjectRegisterWithEditorFormView(
    OrganisationSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceRegisterWithEditorFormView,
    StatusSelectFormViewMixin):
    success_url = reverse_lazy('register:project_with_editor')
    form_class = ProjectEditorForm
    template_name = 'register_with_support/project_editor.html'

    model = models.Project
    metadata_builder_class = ProjectMetadata
    file_upload_registration_url = reverse_lazy('register:project')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Project.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:projects'

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        # processed_form['keyword_dict_list'] = process_project_keywords(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['status_choices'] = self.get_status_choices_for_form()
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['keywords_row_content_template'] = render_to_string(
        #     'register_with_support/components/project/keywords_row_content.html',
        #     context=context
        # )
        context['citation_section_description'] = 'Reference to documentation describing the project.'
        context['related_parties_section_description'] = 'Individual or organisation related to the project.'
        return context

class PlatformRegisterWithoutFormView(
    OrganisationSelectFormViewMixin,
    PlatformSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    SrsNameSelectFormViewMixin,
    StandardIdentifiersFormViewMixin,
    ResourceRegisterWithEditorFormView):
    success_url = reverse_lazy('register:platform_with_editor')
    form_class = PlatformEditorForm
    template_name = 'register_with_support/platform_editor.html'

    model = models.Platform
    metadata_builder_class = PlatformMetadata
    file_upload_registration_url = reverse_lazy('register:platform')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Platform.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:platforms'

    def get_type_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('platformType')
        type_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            type_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *((key, value) for key, value in type_dict.items())
        )

    def get_child_platform_choices_for_form(self):
        return self.get_platform_choices_for_form()

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['location'] = process_location(form_cleaned_data)
        processed_form['standard_identifiers'] = form_cleaned_data['standard_identifiers_json']

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
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
            'register_with_support/components/platform/platform_standard_identifier_row_content_template.html',
            context=context
        )
        return context


class OperationRegisterWithoutFormView(
    OrganisationSelectFormViewMixin,
    PlatformSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    SrsNameSelectFormViewMixin,
    ResourceRegisterWithEditorFormView,
    StatusSelectFormViewMixin
):
    success_url = reverse_lazy('register:operation_with_editor')
    form_class = OperationEditorForm
    template_name = 'register_with_support/operation_editor.html'

    model = models.Operation
    metadata_builder_class = OperationMetadata
    file_upload_registration_url = reverse_lazy('register:operation')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Operation.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:operations'

    def get_child_operation_choices_for_form(self):
        return (
            ('', ''),
            *[(operation.metadata_server_url, operation.name) for operation in Operation.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['location'] = process_location(form_cleaned_data)
        processed_form['operation_time'] = process_operation_time(form_cleaned_data)

        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citation_section_description'] = 'Reference to documentation describing the operation.'
        context['related_parties_section_description'] = 'Individual or organisation related to platform operation.'
        context['location_section_description'] = 'Location of the platform operation.'
        context['location_section_example'] = 'A flight line or a ship track for a platform such as an aircraft or a ship respectively.'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['platform_choices'] = self.get_platform_choices_for_form()
        kwargs['child_operation_choices'] = self.get_child_operation_choices_for_form()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['crs_choices'] = self.get_crs_choices_for_form()
        kwargs['status_choices'] = self.get_status_choices_for_form()
        return kwargs


class InstrumentRegisterWithoutFormView(
    OrganisationSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceRegisterWithEditorFormView,
):
    success_url = reverse_lazy('register:instrument_with_editor')
    form_class = InstrumentEditorForm
    template_name = 'register_with_support/instrument_editor.html'

    model = models.Instrument
    metadata_builder_class = InstrumentMetadata
    file_upload_registration_url = reverse_lazy('register:instrument')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Instrument.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:instruments'

    def get_instrument_type_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('instrumentType')
        type_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            type_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *((key, value) for key, value in type_dict.items())
        )

    def get_member_choices_for_form(self):
        return (
            ('', ''),
            *[(instrument.metadata_server_url, instrument.name) for instrument in Instrument.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['operational_modes'] = process_operational_modes(form_cleaned_data)

        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_section_description'] = 'Information regarding organisations and/or individuals related to instrument.'
        context['citation_section_description'] = 'Reference to documentation describing the instrument.'
        context['operational_mode_row_content_template'] = render_to_string(
            'register_with_support/components/instrument/operational_mode_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['instrument_type_choices'] = self.get_instrument_type_choices_for_form()
        kwargs['member_choices'] = self.get_member_choices_for_form()
        kwargs['related_party_choices'] = self.get_related_party_choices_for_form()
        kwargs['related_party_role_choices'] = self.get_related_party_role_choices_for_form()
        return kwargs


class AcquisitionCapabilitiesRegisterWithoutFormView(
    CapabilitiesSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    OrganisationSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceRegisterWithEditorFormView
):
    success_url = reverse_lazy('register:acquisition_capability_set_with_editor')
    form_class = AcquisitionCapabilitiesEditorForm
    template_name = 'register_with_support/acquisition_capabilities_editor.html'

    model = models.AcquisitionCapabilities
    metadata_builder_class = AcquisitionCapabilitiesMetadata
    file_upload_registration_url = reverse_lazy('register:acquisition_capability_set')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.AcquisitionCapabilities.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisition_capability_sets'

    def get_instrument_choices_with_oms_for_form(self):
        instruments = Instrument.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
        return (
            ('', ''),
            *[(instrument.metadata_server_url, instrument.name) for instrument in instruments if instrument.operational_modes],
        )

    def get_instrument_operational_modes_for_form(self):
        instruments = Instrument.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
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

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['capabilities'] = process_capabilities(form_cleaned_data)
        processed_form['instrument_mode_pair'] = process_instrument_mode_pair(form_cleaned_data)
        processed_form['quality_assessment'] = process_quality_assessment(form_cleaned_data)

        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['citation_section_description'] = 'Reference to documentation describing the component.'
        context['related_parties_section_description'] = 'Individual or organisation related to acquisition.'
        context['capabilities_tab_content_template'] = render_to_string(
            'register_with_support/components/capabilities_tab_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
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


class AcquisitionRegisterWithoutFormView(
    OrganisationSelectFormViewMixin,
    PlatformSelectFormViewMixin,
    ResourceRegisterWithEditorFormView
):
    success_url = reverse_lazy('register:acquisition_with_editor')
    form_class = AcquisitionEditorForm
    template_name = 'register_with_support/acquisition_editor.html'

    model = models.Acquisition
    metadata_builder_class = AcquisitionMetadata
    file_upload_registration_url = reverse_lazy('register:acquisition')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Acquisition.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:acquisitions'

    def get_acquisition_capability_sets_for_form(self):
        acquisition_capability_sets = AcquisitionCapabilities.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
        return (
            ('', ''),
            *[(acs.metadata_server_url, acs.name) for acs in acquisition_capability_sets],
        )

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['capability_links'] = process_acquisition_capability_links(form_cleaned_data)

        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['capability_links_tab_pane_content_template'] = render_to_string(
            'register_with_support/components/capability_links_tab_pane_content_template.html',
            context=context
        )
        context['capability_link_standard_identifier_row_content_template'] = render_to_string(
            'register_with_support/components/acquisition_and_computation/capability_link_standard_identifier_row_content_template.html',
            context=context
        )
        context['capability_link_time_span_row_content_template'] = render_to_string(
            'register_with_support/components/acquisition_and_computation/capability_link_time_span_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['acquisition_capability_set_choices'] = self.get_acquisition_capability_sets_for_form()
        kwargs['platform_choices'] = self.get_platform_choices_for_form()
        return kwargs


class ComputationCapabilitiesRegisterWithoutFormView(
    CapabilitiesSelectFormViewMixin,
    DataLevelSelectFormViewMixin,
    OrganisationSelectFormViewMixin,
    QualityAssessmentSelectFormViewMixin,
    RelatedPartiesSelectFormViewMixin,
    ResourceRegisterWithEditorFormView
):
    success_url = reverse_lazy('register:computation_capability_set_with_editor')
    form_class = ComputationCapabilitiesEditorForm
    template_name = 'register_with_support/computation_capabilities_editor.html'

    model = models.ComputationCapabilities
    metadata_builder_class = ComputationCapabilitiesMetadata
    file_upload_registration_url = reverse_lazy('register:computation_capability_set')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.ComputationCapabilities.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computation_capability_sets'

    def get_child_computation_choices_for_form(self):
        computation_capability_sets = ComputationCapabilities.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
        return (
            ('', ''),
            *[(ccs.metadata_server_url, ccs.name) for ccs in computation_capability_sets],
        )

    def get_computation_type_choices_for_form(self):
        g = get_graph_of_pithia_ontology_component('computationType')
        type_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            type_dict[str(o)] = str(o_pref_label)
        return (
            ('', ''),
            *((key, value) for key, value in type_dict.items())
        )

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)
        
        processed_form['documentation'] = process_documentation(form_cleaned_data)
        processed_form['related_parties'] = process_related_parties(form_cleaned_data)
        processed_form['capabilities'] = process_capabilities(form_cleaned_data)
        processed_form['quality_assessment'] = process_quality_assessment(form_cleaned_data)
        processed_form['processing_inputs'] = process_processing_inputs(form_cleaned_data)
        processed_form['processing_output'] = process_processing_output(form_cleaned_data)
        processed_form['software_reference'] = process_software_reference(form_cleaned_data)
        
        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_section_description'] = 'Individual or organisation related to Computation.'
        context['citation_section_description'] = 'Reference to documentation describing the component.'
        context['capabilities_tab_content_template'] = render_to_string(
            'register_with_support/components/capabilities_tab_content_template.html',
            context=context
        )
        context['processing_input_row_content_template'] = render_to_string(
            'register_with_support/components/computation_capabilities/processing_input_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
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


class ComputationRegisterWithoutFormView(
    OrganisationSelectFormViewMixin,
    PlatformSelectFormViewMixin,
    ResourceRegisterWithEditorFormView
):
    success_url = reverse_lazy('register:computation_with_editor')
    form_class = ComputationEditorForm
    template_name = 'register_with_support/computation_editor.html'

    model = models.Computation
    metadata_builder_class = ComputationMetadata
    file_upload_registration_url = reverse_lazy('register:computation')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Computation.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:computations'

    def get_computation_capability_set_choices_for_form(self):
        computation_capability_sets = ComputationCapabilities.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))
        return (
            ('', ''),
            *[(ccs.metadata_server_url, ccs.name) for ccs in computation_capability_sets],
        )

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['capability_links'] = process_acquisition_capability_links(form_cleaned_data)

        return processed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['capability_links_tab_pane_content_template'] = render_to_string(
            'register_with_support/components/capability_links_tab_pane_content_template.html',
            context=context
        )
        context['capability_link_standard_identifier_row_content_template'] = render_to_string(
            'register_with_support/components/acquisition_and_computation/capability_link_standard_identifier_row_content_template.html',
            context=context
        )
        context['capability_link_time_span_row_content_template'] = render_to_string(
            'register_with_support/components/acquisition_and_computation/capability_link_time_span_row_content_template.html',
            context=context
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['platform_choices'] = self.get_platform_choices_for_form()
        kwargs['computation_capability_set_choices'] = self.get_computation_capability_set_choices_for_form()
        return kwargs


class WorkflowRegisterWithoutFormView(
    OrganisationSelectFormViewMixin,
    ResourceRegisterWithEditorFormView
):
    success_url = reverse_lazy('register:workflow_with_editor')
    form_class = WorkflowEditorForm
    template_name = 'register_with_support/workflow_editor.html'

    model = models.Workflow
    metadata_builder_class = WorkflowMetadata
    file_upload_registration_url = reverse_lazy('register:workflow')

    resource_management_list_page_breadcrumb_text = _create_manage_resource_page_title(models.Workflow.type_plural_readable)
    resource_management_list_page_breadcrumb_url_name = 'resource_management:workflows'

    def get_data_collection_choices_for_form(self):
        return (
            ('', ''),
            *[(data_collection.metadata_server_url, data_collection.name) for data_collection in DataCollection.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

    def process_form(self, form_cleaned_data):
        processed_form = super().process_form(form_cleaned_data)

        processed_form['data_collections'] = process_workflow_data_collections(form_cleaned_data)

        return processed_form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation_choices'] = self.get_organisation_choices_for_form()
        kwargs['data_collection_choices'] = self.get_data_collection_choices_for_form()
        return kwargs
