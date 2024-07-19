from .xml_metadata_to_form_components import (
    ContactInfoXmlMetadataToFormMixin,
    DocumentationXmlMetadataToFormMixin,
    LocationXmlMetadataToFormMixin,
    RelatedPartyXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter,
    TypeXmlMetadataToFormMixin,
)

from metadata_editor.xml_ns_enums import NamespacePrefix


class OrganisationXmlMetadataToFormConverter(
    ContactInfoXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'short_name': './/%s:shortName' % self.PITHIA_NS_PREFIX_FOR_XPATH,
        })


class IndividualXmlMetadataToFormConverter(
    ContactInfoXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'namespace': './/%s:namespace' % self.PITHIA_NS_PREFIX_FOR_XPATH,
            'position_name': './/%s:positionName' % self.PITHIA_NS_PREFIX_FOR_XPATH,
        })


class ProjectXmlMetadataToFormConverter(
    ContactInfoXmlMetadataToFormMixin,
    DocumentationXmlMetadataToFormMixin,
    RelatedPartyXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'short_name': './/%s:shortName' % self.PITHIA_NS_PREFIX_FOR_XPATH,
            'status': './/%s:status/@%s:href' % (self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.XLINK),
            'abstract': './/%s:abstract' % self.PITHIA_NS_PREFIX_FOR_XPATH,
            'url': './/%s:URL' % NamespacePrefix.GMD,
        })


class PlatformXmlMetadataToFormConverter(
    DocumentationXmlMetadataToFormMixin,
    LocationXmlMetadataToFormMixin,
    TypeXmlMetadataToFormMixin,
    RelatedPartyXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'short_name': './/%s:shortName' % self.PITHIA_NS_PREFIX_FOR_XPATH,
            'url': './/%s:URL' % NamespacePrefix.GMD,
        })

    def _map_standard_identifiers_to_form(self):
        standard_identifier_elements = self.xml_string_parsed.xpath('.//%s:standardIdentifier' % self.PITHIA_NS_PREFIX_FOR_XPATH, namespaces=self.namespaces)
        standard_identifiers = []
        for e in standard_identifier_elements:
            standard_identifiers.append({
                'authority': e.attrib['authority'],
                'value': e.text,
            })
        return standard_identifiers

    def map_complex_xml_fields_to_form(self, form_data):
        form_data = super().map_complex_xml_fields_to_form(form_data)
        form_data['child_platforms'] = self.xml_string_parsed.xpath('.//%s:childPlatform/@%s:href' % (self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.XLINK), namespaces=self.namespaces)
        form_data['standard_identifiers_json'] = self._map_standard_identifiers_to_form()
        return form_data