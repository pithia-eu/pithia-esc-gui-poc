import logging
from django.contrib import messages
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.views.generic import View
from django_countries import countries
from rdflib.namespace._SKOS import SKOS
from unidecode import unidecode
from urllib.parse import quote

from .editor_dataclasses import (
    CitationPropertyTypeMetadataUpdate,
    ContactInfoAddressMetadataUpdate,
    ContactInfoMetadataUpdate,
    LocationMetadataUpdate,
)
from .form_utils import (
    get_hours_of_service_from_form,
    get_phone_field_string_value,
    map_capability_links_to_dataclasses,
    map_process_capabilities_to_dataclasses,
    map_related_parties_to_dataclasses,
)
from .service_utils import BaseMetadataEditor
from .services import (
    AcquisitionEditor,
    PlatformEditor,
    ProjectEditor,
)

from common import models
from common.helpers import clean_localid_or_namespace
from ontology.utils import get_graph_of_pithia_ontology_component

logger = logging.getLogger(__name__)


class CapabilityLinksViewMixin:
    def update_capability_links_with_metadata_editor(self, request, metadata_editor: AcquisitionEditor, form_cleaned_data):
        capability_links = map_capability_links_to_dataclasses(form_cleaned_data)
        metadata_editor.update_capability_links(capability_links)


class CapabilitiesViewMixin:
    def update_capabilities_with_metadata_editor(self, request, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        capabilities_update = map_process_capabilities_to_dataclasses(form_cleaned_data)
        metadata_editor.update_capabilities(capabilities_update)


class ContactInfoViewMixin:
    def update_contact_info_with_metadata_editor(self, request, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        address_update = ContactInfoAddressMetadataUpdate(
            delivery_point=form_cleaned_data.get('delivery_point'),
            city=form_cleaned_data.get('city'),
            administrative_area=form_cleaned_data.get('administrative_area'),
            postal_code=form_cleaned_data.get('postal_code'),
            country=unidecode(form_cleaned_data.get('country')),
            electronic_mail_address=form_cleaned_data.get('email_address')
        )
        contact_info_update = ContactInfoMetadataUpdate(
            phone=get_phone_field_string_value(form_cleaned_data),
            address=address_update,
            online_resource=form_cleaned_data.get('online_resource'),
            hours_of_service=get_hours_of_service_from_form(form_cleaned_data),
            contact_instructions=form_cleaned_data.get('contact_instructions')
        )
        metadata_editor.update_contact_info(contact_info_update)

    def set_initial_country_if_in_country_choices(self, initial):
        initial_country_decoded = initial.get('country')
        countries_decoded = [unidecode(c.name) for c in countries]
        try:
            selected_country_decoded_index = countries_decoded.index(initial_country_decoded)
        except ValueError:
            return
        return initial.update({'country': list(countries)[selected_country_decoded_index]})


class DocumentationViewMixin:
    def update_documentation_with_metadata_editor(self, request, metadata_editor: BaseMetadataEditor, form_cleaned_data):
        try:
            documentation_update = CitationPropertyTypeMetadataUpdate(
                citation_title=form_cleaned_data.get('citation_title'),
                citation_publication_date=form_cleaned_data.get('citation_publication_date'),
                citation_doi=form_cleaned_data.get('citation_doi'),
                citation_url=form_cleaned_data.get('citation_linkage_url'),
                other_citation_details=form_cleaned_data.get('other_citation_details')
            )
            metadata_editor.update_documentation(documentation_update)
        except BaseException as err:
            logger.exception(err)
            messages.error(request, 'Could not add documentation metadata due to an error. Please try again later.')


class LocationViewMixin:
    def update_location_with_metadata_editor(self, request, metadata_editor: PlatformEditor, form_cleaned_data):
        try:
            location_update = LocationMetadataUpdate(
                location_name=form_cleaned_data.get('location_name'),
                geometry_location_point_id=form_cleaned_data.get('geometry_location_point_id'),
                geometry_location_point_srs_name=form_cleaned_data.get('geometry_location_point_srs_name'),
                geometry_location_point_pos_1=form_cleaned_data.get('geometry_location_point_pos_1'),
                geometry_location_point_pos_2=form_cleaned_data.get('geometry_location_point_pos_2'),
            )
            metadata_editor.update_location(location_update)
        except BaseException as err:
            logger.exception(err)
            messages.error(request, 'Could not add location metadata due to an error. Please try again later.')


class RelatedPartiesViewMixin:
    new = False

    def update_related_parties_with_metadata_editor(self, request, metadata_editor: ProjectEditor, form_cleaned_data):
        try:
            metadata_editor.update_related_parties(map_related_parties_to_dataclasses(form_cleaned_data))
        except BaseException as err:
            logger.exception(err)
            messages.error(request, 'Could not add related parties metadata due to an error. Please try again later.')


class OntologyCategoryChoicesViewMixin:
    def get_terms_from_ontology_category(self, ontology_category):
        g = get_graph_of_pithia_ontology_component(ontology_category)
        term_dict = {}
        for s, p, o in g.triples((None, SKOS.member, None)):
            o_pref_label = g.value(o, SKOS.prefLabel)
            term_dict[str(o)] = str(o_pref_label)
        return [(key, value) for key, value in term_dict.items()]

    def get_choices_from_ontology_category(self, ontology_category):
        return (
            ('', ''),
            *self.get_terms_from_ontology_category(ontology_category),
        )

    def get_choices_from_multiple_ontology_categories(self, optgroup_oc_pairs):
        choices_categorised = []
        for optgroup, ontology_category in optgroup_oc_pairs:
            choices_categorised.append(
                (optgroup, list((key, value) for key, value in self.get_terms_from_ontology_category(ontology_category)))
            )
        return (
            ('', ''),
            *choices_categorised
        )


class ResourceChoicesViewMixin:
    def get_resources_with_model_ordered_by_name(self, model):
        return model.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))

    def get_resource_choices_with_model(self, model):
        return (
            ('', ''),
            *[(quote(r.metadata_server_url, safe='/:?=&'), r.name) for r in self.get_resources_with_model_ordered_by_name(model)],
        )

    def get_resource_choices_with_multiple_models(self, optgroup_model_pairs):
        choices_categorised = []
        for optgroup, model in optgroup_model_pairs:
            choices_categorised.append(
                (optgroup, list((r.metadata_server_url, r.name) for r in self.get_resources_with_model_ordered_by_name(model)))
            )
        return (
            ('', ''),
            *choices_categorised
        )


class CapabilitiesSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_observed_property_choices_for_form(self):
        return self.get_choices_from_ontology_category('observedProperty')

    def get_coordinate_system_choices_for_form(self):
        return self.get_choices_from_ontology_category('crs')

    def get_dimensionality_instance_choices_for_form(self):
        return self.get_choices_from_ontology_category('dimensionalityInstance')

    def get_dimensionality_timeline_choices_for_form(self):
        return self.get_choices_from_ontology_category('dimensionalityTimeline')

    def get_qualifier_choices_for_form(self):
        return self.get_choices_from_ontology_category('qualifier')

    def get_unit_choices_for_form(self):
        return self.get_choices_from_ontology_category('unit')

    def get_vector_representation_choices_for_form(self):
        return self.get_choices_from_ontology_category('component')


class DataLevelSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_data_level_choices_for_form(self):
        return self.get_choices_from_ontology_category('dataLevel')


class SrsNameSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_crs_choices_for_form(self):
        return self.get_choices_from_ontology_category('crs')


class OrganisationSelectFormViewMixin(ResourceChoicesViewMixin):
    def get_organisation_choices_for_form(self):
        organisation_choices = [
            (o.metadata_server_url, f'{o.name} ({clean_localid_or_namespace(o.short_name.lower())})')
            for o in self.get_resources_with_model_ordered_by_name(models.Organisation)
        ]
        organisation_choices.append(('pithia', 'PITHIA (pithia)'))
        organisation_choices.sort(key=lambda tup: tup[1].lower() if isinstance(tup[1], str) else tup[1])
        return (
            ('', ''),
            *organisation_choices,
        )


class PlatformSelectFormViewMixin(ResourceChoicesViewMixin):
    def get_platform_choices_for_form(self):
        return self.get_resource_choices_with_model(models.Platform)


class DataCollectionSelectFormViewMixin(ResourceChoicesViewMixin):
    def get_data_collection_choices_for_form(self):
        return self.get_resource_choices_with_model(models.DataCollection)


class InstrumentTypeSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_instrument_type_choices_for_form(self):
        return self.get_choices_from_ontology_category('instrumentType')


class ComputationTypeSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_computation_type_choices_for_form(self):
        return self.get_choices_from_ontology_category('computationType')


class QualityAssessmentSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_data_quality_flag_choices_for_form(self):
        return self.get_choices_from_ontology_category('dataQualityFlag')

    def get_metadata_quality_flag_choices_for_form(self):
        return self.get_choices_from_ontology_category('metadataQualityFlag')


class RelatedPartiesSelectFormViewMixin(
    OntologyCategoryChoicesViewMixin,
    ResourceChoicesViewMixin):
    def get_related_party_choices_for_form(self):
        return self.get_resource_choices_with_multiple_models([
            ('Organisations', models.Organisation),
            ('Individuals', models.Individual),
        ])

    def get_related_party_role_choices_for_form(self):
        return self.get_choices_from_ontology_category('relatedPartyRole')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_parties_row_content_template'] = render_to_string(
            'metadata_editor/components/related_parties_row_content_template.html',
            context=context
        )
        return context


class StandardIdentifiersFormViewMixin(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standard_identifier_row_content_template'] = render_to_string(
            'metadata_editor/components/standard_identifier_row_content_template.html',
            context=context
        )
        return context


class StatusSelectFormViewMixin(OntologyCategoryChoicesViewMixin):
    def get_status_choices_for_form(self):
        return self.get_choices_from_ontology_category('status')