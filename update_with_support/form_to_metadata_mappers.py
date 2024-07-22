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