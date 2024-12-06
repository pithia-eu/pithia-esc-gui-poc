import logging

from .form_to_metadata_mapper_components import (
    BaseMetadataFormFieldsToMetadataMixin,
    CapabilitiesFormFieldsToMetadataMixin,
    CapabilityLinkFormFieldsToMetadataMixin,
    ContactInfoFormFieldsToMetadataMixin,
    DataLevelFormFieldsToMetadataMixin,
    DocumentationFormFieldsToMetadataMixin,
    InputOutputFormFieldsToMetadataMixin,
    LocationFormFieldsToMetadataMixin,
    QualityAssessmentFormFieldsToMetadataMixin,
    RelatedPartyFormFieldsToMetadataMixin,
    SourceFormFieldsToMetadataMixin,
    StandardIdentifierFormFieldsToMetadataMixin,
    TimePeriodFormFieldsToMetadataMixin,
    TypeFormFieldsToMetadataMixin,
)

from datahub_management.services import CatalogueDataSubsetDataHubService
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
        })
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
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
        TimePeriodFormFieldsToMetadataMixin,
        TypeFormFieldsToMetadataMixin,
        RelatedPartyFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    time_period_container_element_name = 'operationTime'

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
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
        InputOutputFormFieldsToMetadataMixin,
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

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        input_descriptions = self._map_input_outputs_to_form('inputDescription')
        initial_values.update({
            'input_descriptions_json': input_descriptions,
        })
        return initial_values
        

class AcquisitionFormFieldsToMetadataMapper(
        CapabilityLinkFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    capabilities_element_key = 'acquisitionCapabilities'


class ComputationCapabilitiesFormFieldsToMetadataMapper(
        CapabilitiesFormFieldsToMetadataMixin,
        DataLevelFormFieldsToMetadataMixin,
        DocumentationFormFieldsToMetadataMixin,
        InputOutputFormFieldsToMetadataMixin,
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
            'software_reference_citation_title': './/%s:softwareReference/%s:Citation/%s:title/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'software_reference_citation_publication_date': './/%s:softwareReference/%s:Citation/%s:date/%s:CI_Date/%s:date/%s:Date' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'software_reference_citation_doi': './/%s:softwareReference/%s:Citation/%s:identifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'software_reference_citation_linkage_url': './/%s:softwareReference/%s:Citation/%s:onlineResource/%s:CI_OnlineResource/%s:linkage/%s:URL' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD),
            'software_reference_other_citation_details': './/%s:softwareReference/%s:Citation/%s:otherCitationDetails/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'version': './/%s:version[not(ancestor::%s:PITHIA_Identifier)]' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX),
        })
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'type': './/%s:type/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'child_computations': './/%s:childComputation/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        processing_inputs = self._map_input_outputs_to_form('processingInput')
        initial_values.update({
            'processing_inputs_json': processing_inputs,
        })
        return initial_values


class ComputationFormFieldsToMetadataMapper(
        CapabilityLinkFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    capabilities_element_key = 'computationCapabilities'


class ProcessFormFieldsToMetadataMapper(
        CapabilitiesFormFieldsToMetadataMixin,
        DataLevelFormFieldsToMetadataMixin,
        DocumentationFormFieldsToMetadataMixin,
        QualityAssessmentFormFieldsToMetadataMixin,
        RelatedPartyFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'acquisitions': './/%s:acquisitionComponent/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'computations': './/%s:computationComponent/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings


class DataCollectionFormFieldsToMetadataMapper(
        DataLevelFormFieldsToMetadataMixin,
        QualityAssessmentFormFieldsToMetadataMixin,
        RelatedPartyFormFieldsToMetadataMixin,
        SourceFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    def _map_sources_to_form(self, online_resource_elements_xpath: str = None):
        return super()._map_sources_to_form('.//%s:collectionResults/%s:source/%s:OnlineResource' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX))

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'process': './/%s:procedure/@%s:href' % (NamespacePrefix.OM, NamespacePrefix.XLINK),
        })      
        return mappings

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_multiple_choice_form_field_to_xml_field_mappings()
        mappings.update({
            'features_of_interest': './/%s:FeatureOfInterest/%s:namedRegion/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'permissions': './/%s:permission/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'projects': './/%s:project/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'sub_collections': './/%s:subCollection/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'types': './/%s:type/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings


class CatalogueFormFieldsToMetadataMapper(BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'catalogue_category': './/%s:catalogueCategory/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK)
        })
        return mappings


class CatalogueEntryFormFieldsToMetadataMapper(
        TimePeriodFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    time_period_container_element_name = 'phenomenonTime'

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'name': './/%s:entryName' % self.DEFAULT_XPATH_NSPREFIX,
            'description': './/%s:entryDescription' % self.DEFAULT_XPATH_NSPREFIX,
            'catalogue_identifier': './/%s:catalogueIdentifier/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings


class CatalogueDataSubsetFormFieldsToMetadataMapper(
        QualityAssessmentFormFieldsToMetadataMixin,
        SourceFormFieldsToMetadataMixin,
        TimePeriodFormFieldsToMetadataMixin,
        BaseMetadataFormFieldsToMetadataMixin):
    time_period_container_element_name = 'resultTime'
    
    def _map_source_to_form(self, online_resource_element):
        source = super()._map_source_to_form(online_resource_element)
        catalogue_data_subset_id = self._get_element_text_or_blank_string(self._get_first_element_from_list(self.xml_string_parsed.xpath('.//%s:identifier/%s:PITHIA_Identifier/%s:localID' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX), namespaces=self.namespaces)))
        source_file_in_datahub = CatalogueDataSubsetDataHubService.get_catalogue_data_subset_file(
            catalogue_data_subset_id,
            source.get('name')
        )
        source.update({
            'isSourceFileInDataHub': source_file_in_datahub is not None,
            'isExistingDataHubFileUsed': source_file_in_datahub is not None,
        })
        return source

    def _map_sources_to_form(self, online_resource_elements_xpath: str = None):
        return super()._map_sources_to_form('.//%s:source/%s:OnlineResource' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX))

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'data_collection': './/%s:dataCollection/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'data_levels': './/%s:dataLevel/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'description': './/%s:dataSubsetDescription' % self.DEFAULT_XPATH_NSPREFIX,
            'entry_identifier': './/%s:entryIdentifier/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'name': './/%s:dataSubsetName' % self.DEFAULT_XPATH_NSPREFIX,
        })
        return mappings


class WorkflowFormFieldsToMetadataMapper(BaseMetadataFormFieldsToMetadataMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'data_collection_1': './/%s:dataCollection/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
            'workflow_details': './/%s:workflowDetails/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK),
        })
        return mappings

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        data_collections = self.xml_string_parsed.xpath('.//%s:dataCollection/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
        data_collection_2_and_others = data_collections[1:]
        initial_values.update({
            'data_collection_2_and_others': data_collection_2_and_others,
        })
        return initial_values