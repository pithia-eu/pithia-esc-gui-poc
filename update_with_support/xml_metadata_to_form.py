from .xml_metadata_to_form_components import ContactInfoXmlMetadataToFormMixin, ResourceXmlToFormDataConverter

from metadata_editor.xml_ns_enums import Namespace


class OrganisationXmlMetadataToFormConverter(
    ContactInfoXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'short_name': './/{%s}shortName' % Namespace.PITHIA,
        })


class IndividualXmlMetadataToFormConverter(
    ContactInfoXmlMetadataToFormMixin,
    ResourceXmlToFormDataConverter):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'namespace': './/{%s}namespace' % Namespace.PITHIA,
        })