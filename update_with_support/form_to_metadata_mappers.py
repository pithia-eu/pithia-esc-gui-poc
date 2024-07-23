from .form_to_metadata_mapper_components import (
    ContactInfoFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    LocationFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin,
    TypeFormFieldsToMetadataMixin,
)

from metadata_editor.xml_ns_enums import NamespacePrefix


class OrganisationFormFieldsToMetadataMapper(
    ContactInfoFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'short_name': './/%s:shortName' % self.DEFAULT_XPATH_NSPREFIX,
        })
        return mappings


class IndividualFormFieldsToMetadataMapper(
    ContactInfoFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'namespace': './/%s:namespace' % self.DEFAULT_XPATH_NSPREFIX,
            'position_name': './/%s:positionName' % self.DEFAULT_XPATH_NSPREFIX,
        })
        return mappings


class ProjectFormFieldsToMetadataMapper(
    ContactInfoFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'short_name': './/%s:shortName' % self.DEFAULT_XPATH_NSPREFIX,
            'status': './/%s:status/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'abstract': './/%s:abstract' % self.DEFAULT_XPATH_NSPREFIX,
            'url': './/%s:URL' % NamespacePrefix.GMD,
        })
        return mappings


class PlatformFormFieldsToMetadataMapper(
    DocumentationFormFieldsToMetadataMixin,
    LocationFormFieldsToMetadataMixin,
    TypeFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'short_name': './/%s:shortName' % self.DEFAULT_XPATH_NSPREFIX,
            'url': './/%s:URL' % NamespacePrefix.GMD,
            'child_platforms': './/%s:childPlatform/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK)
        })
        return mappings

    def _map_standard_identifiers_to_form(self):
        standard_identifier_elements = self.xml_string_parsed.xpath('.//%s:standardIdentifier' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        standard_identifiers = []
        for e in standard_identifier_elements:
            standard_identifiers.append({
                'authority': e.attrib['authority'],
                'value': e.text,
            })
        return standard_identifiers

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        initial_values['standard_identifiers_json'] = self._map_standard_identifiers_to_form()
        return initial_values


class OperationFormFieldsToMetadataMapper(
    DocumentationFormFieldsToMetadataMixin,
    LocationFormFieldsToMetadataMixin,
    TypeFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self._gml_id_xpath = '@%s:id' % NamespacePrefix.GML
        self._time_instant_element_xpath = '%s:TimeInstant' % NamespacePrefix.GML
        self._time_position_element_xpath = '%s:timePosition' % NamespacePrefix.GML
        self._time_period_element_xpath = '%s:operationTime/%s:TimePeriod' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GML)

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'time_period_id': './/%s/%s' % (self._time_period_element_xpath, self._gml_id_xpath),
            'time_instant_begin_id': './/%s/%s:begin/%s/%s' % (self._time_period_element_xpath, NamespacePrefix.GML, self._time_instant_element_xpath, self._gml_id_xpath),
            'time_instant_begin_position': './/%s/%s:begin/%s/%s' % (self._time_period_element_xpath, NamespacePrefix.GML, self._time_instant_element_xpath, self._time_position_element_xpath),
            'time_instant_end_id': './/%s/%s:end/%s/%s' % (self._time_period_element_xpath, NamespacePrefix.GML, self._time_instant_element_xpath, self._gml_id_xpath),
            'time_instant_end_position': './/%s/%s:end/%s/%s' % (self._time_period_element_xpath, NamespacePrefix.GML, self._time_instant_element_xpath, self._time_position_element_xpath),
            'status': './/%s:status/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'platforms': './/%s:platform/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'child_operations': './/%s:childOperation/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings