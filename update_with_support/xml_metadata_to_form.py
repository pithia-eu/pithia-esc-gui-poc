from .xml_metadata_to_form_components import (
    ContactInfoXmlMetadataToFormMixin,
    DocumentationXmlMetadataToFormMixin,
    RelatedPartyXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter,
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