import logging
from .form_to_metadata_mapper_components import (
    ContactInfoFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    LocationFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin,
    TypeFormFieldsToMetadataMixin,
)

from metadata_editor.xml_ns_enums import Namespace, NamespacePrefix


logger = logging.getLogger(__name__)


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
            value = self._get_element_text_or_blank_string(e)
            standard_identifiers.append({
                'authority': e.attrib['authority'],
                'value': value,
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


class InstrumentFormFieldsToMetadataWrapper(
    DocumentationFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    TypeFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'url': './/%s:URL' % NamespacePrefix.GMD,
            'version': './/%s:version[not(ancestor::%s:PITHIA_Identifier)]' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX),
        })
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'members': './/%s:member/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings

    def _map_operational_modes_to_form(self):
        instrument_operational_modes = []
        instrument_operational_mode_elements = self.xml_string_parsed.xpath('.//%s:InstrumentOperationalMode' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        for e in instrument_operational_mode_elements:
            try:
                ids = e.xpath('.//%s:id' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
                id = self._get_first_element_from_list(ids)
                names = e.xpath('.//%s:name' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
                name = self._get_first_element_from_list(names)
                descriptions = e.xpath('.//%s:description' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
                description = self._get_first_element_from_list(descriptions)
                instrument_operational_modes.append({
                    'id': self._get_element_text_or_blank_string(id),
                    'name': self._get_element_text_or_blank_string(name),
                    'description': self._get_element_text_or_blank_string(description),
                })
            except AttributeError as err:
                logger.exception(err)
                continue
        return instrument_operational_modes

    def get_initial_values_from_basic_multiple_choice_mappings(self):
        initial_values = super().get_initial_values_from_basic_multiple_choice_mappings()
        operational_modes = self._map_operational_modes_to_form()
        initial_values['operational_modes_json'] = operational_modes
        return initial_values


class AcquisitionCapabilitiesFormFieldsToMetadataMapper(
    DocumentationFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    GCO19115_NSPREFIX = 'gco19115'
    
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.namespaces.update({
            self.GCO19115_NSPREFIX: Namespace.GCO19115,
        })

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'instrument_mode_pair_instrument': './/%s:instrumentModePair/%s:InstrumentOperationalModePair/%s:instrument/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'instrument_mode_pair_mode': './/%s:instrumentModePair/%s:InstrumentOperationalModePair/%s:mode/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'input_name': './/%s:inputDescription/%s:InputOutput/%s:name' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX),
            'input_description': './/%s:inputDescription/%s:InputOutput/%s:description/%s:LE_Source/%s:description/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.MRL, NamespacePrefix.MRL, self.GCO19115_NSPREFIX),
        })
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'data_levels': './/%s:dataLevel/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'data_quality_flags': './/%s:qualityAssessment/%s:dataQualityFlag/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'metadata_quality_flags': './/%s:qualityAssessment/%s:metadataQualityFlag/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings

    def _map_process_capabilities_to_form(self):
        process_capability_elements = self.xml_string_parsed.xpath('.//%s:capabilities/%s:processCapability' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        process_capabilities = []
        for e in process_capability_elements:
            name_elements = e.xpath('.//%s:name' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
            name = ''
            try:
                name = self._get_element_text_or_blank_string(self._get_first_element_from_list(name_elements))
            except AttributeError:
                pass
            observed_property_elements = e.xpath('.//%s:observedProperty/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            observed_property = self._get_first_element_from_list(observed_property_elements)
            dimensionality_instance_elements = e.xpath('.//%s:dimensionalityInstance/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            dimensionality_instance = self._get_first_element_from_list(dimensionality_instance_elements)
            dimensionality_timeline_elements = e.xpath('.//%s:dimensionalityTimeline/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            dimensionality_timeline = self._get_first_element_from_list(dimensionality_timeline_elements)
            cadence_elements = e.xpath('.//%s:cadence' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
            cadence = ''
            try:
                cadence = self._get_element_text_or_blank_string(self._get_first_element_from_list(cadence_elements))
            except AttributeError:
                pass
            cadence_unit_attributes = e.xpath('.//%s:cadence/@unit' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
            cadence_unit = self._get_first_element_from_list(cadence_unit_attributes)
            vector_representations = e.xpath('.//%s:vectorRepresentation/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            coordinate_system_elements = e.xpath('.//%s:coordinateSystem/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            coordinate_system = self._get_first_element_from_list(coordinate_system_elements)
            units_elements = e.xpath('.//%s:units/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            units = self._get_first_element_from_list(units_elements)
            qualifiers = e.xpath('.//%s:qualifier/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            process_capabilities.append({
                'name': name,
                'observedProperty': observed_property,
                'dimensionalityInstance': dimensionality_instance,
                'dimensionalityTimeline': dimensionality_timeline,
                'cadence': cadence,
                'cadenceUnits': cadence_unit,
                'vectorRepresentation': vector_representations,
                'coordinateSystem': coordinate_system,
                'units': units,
                'qualifier': qualifiers,
            })
        return process_capabilities

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        capabilities = self._map_process_capabilities_to_form()
        initial_values.update({
            'capabilities_json': capabilities
        })
        return initial_values
        