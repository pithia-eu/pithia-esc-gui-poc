from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.views.generic import View
from rdflib.namespace._SKOS import SKOS

from common import models
from common.helpers import clean_localid_or_namespace
from ontology.utils import get_graph_of_pithia_ontology_component


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
            *[(o.metadata_server_url, f'{o.name} ({clean_localid_or_namespace(o.short_name.lower())})') for o in models.Organisation.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

class PlatformSelectFormViewMixin(View):
    def get_platform_choices_for_form(self):
        return (
            ('', ''),
            *[(p.metadata_server_url, p.name) for p in models.Platform.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

class DataCollectionSelectFormViewMixin(View):
    def get_data_collection_choices_for_form(self):
        return (
            ('', ''),
            *[(data_collection.metadata_server_url, data_collection.name) for data_collection in models.DataCollection.objects.annotate(json_name=KeyTextTransform('name', 'json')).all().order_by(Lower('json_name'))],
        )

class InstrumentTypeSelectFormViewMixin(View):
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

class ComputationTypeSelectFormViewMixin(View):
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