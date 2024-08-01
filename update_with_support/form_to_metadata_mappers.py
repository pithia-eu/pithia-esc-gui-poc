import logging
from .form_to_metadata_mapper_components import (
    BaseMetadataFormFieldsToMetadataMixin,
    CapabilitiesFormFieldsToMetadataMixin,
    CapabilityLinkFormFieldsToMetadataMixin,
    ContactInfoFormFieldsToMetadataMixin,
    DataLevelFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    LocationFormFieldsToMetadataMixin,
    QualityAssessmentFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    StandardIdentifierFormFieldsToMetadataMixin,
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
    StandardIdentifierFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'short_name': './/%s:shortName' % self.DEFAULT_XPATH_NSPREFIX,
            'url': './/%s:URL' % NamespacePrefix.GMD,
            'child_platforms': './/%s:childPlatform/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK)
        })
        return mappings

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        initial_values['standard_identifiers_json'] = self._map_standard_identifiers_to_form(self.xml_string_parsed)
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
    CapabilitiesFormFieldsToMetadataMixin,
    DataLevelFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    QualityAssessmentFormFieldsToMetadataMixin,
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
        

class AcquisitionFormFieldsToMetadataMapper(
    CapabilityLinkFormFieldsToMetadataMixin,
    BaseMetadataFormFieldsToMetadataMixin):
    capabilities_element_key = 'acquisitionCapabilities'


class ComputationCapabilitiesFormFieldsToMetadataMapper(
    CapabilitiesFormFieldsToMetadataMixin,
    DataLevelFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    QualityAssessmentFormFieldsToMetadataMixin,
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
            'software_reference_citation_title': './/%s:documentation/%s:Citation/%s:title/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'software_reference_citation_publication_date': './/%s:documentation/%s:Citation/%s:date/%s:CI_Date/%s:date/%s:Date' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'software_reference_citation_doi': './/%s:documentation/%s:Citation/%s:identifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'software_reference_citation_linkage_url': './/%s:documentation/%s:Citation/%s:onlineResource/%s:CI_OnlineResource/%s:linkage/%s:URL' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD),
            'software_reference_other_citation_details': './/%s:documentation/%s:Citation/%s:otherCitationDetails/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'version': './/%s:version' % self.DEFAULT_XPATH_NSPREFIX,
        })
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'type': './/%s:type/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'child_computations': './/%s:childComputation/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings

    def _map_processing_inputs_to_form(self):
        processing_inputs = []
        processing_input_elements = self.xml_string_parsed.xpath('.//%s:processingInput/%s:InputOutput' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)
        for e in processing_input_elements:
            name = self._get_element_text_or_blank_string(
                self._get_first_element_from_list(
                    e.xpath('.//%s:name' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
                )
            )
            description = self._get_element_text_or_blank_string(
                self._get_first_element_from_list(
                    e.xpath('.//%s:description/%s:LE_Source/%s:description/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.MRL, NamespacePrefix.MRL, self.GCO19115_NSPREFIX), namespaces=self.namespaces)
                )
            )
            processing_inputs.append({
                'name': name,
                'description': description,
            })
        return processing_inputs

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        processing_inputs = self._map_processing_inputs_to_form()
        initial_values.update({
            'processing_inputs_json': processing_inputs,
        })
        return initial_values