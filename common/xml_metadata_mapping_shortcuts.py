from .xml_metadata_mapping_shortcut_mixins import (
    GmdContactInfoMetadataPropertiesMixin,
    GmdUrlMetadataPropertiesMixin,
    GmlTimePeriodMetadataPropertiesMixin,
    NamespacePrefix,
    PithiaCapabilitiesMetadataPropertiesMixin,
    PithiaCapabilityLinksMetadataPropertiesMixin,
    PithiaCoreMetadataPropertiesMixin,
    PithiaDescriptionMetadataPropertiesMixin,
    PithiaDoiMetadataPropertiesMixin,
    PithiaDocumentationMetadataPropertiesMixin,
    PithiaFeaturesOfInterestMetadataPropertiesMixin,
    PithiaInputOutputMetadataPropertiesMixin,
    PithiaObservedPropertiesMetadataPropertiesMixin,
    PithiaOnlineResourceMetadataPropertiesMixin,
    PithiaOntologyUrlsMetadataPropertiesMixin,
    PithiaQualityAssessmentMetadataPropertiesMixin,
    PithiaRelatedPartiesMetadataPropertiesMixin,
    PithiaResourceUrlsMetadataPropertiesMixin,
    PithiaShortNameMetadataPropertiesMixin,
    PithiaStandardIdentifiersMetadataPropertiesMixin,
    PithiaStatusMetadataPropertiesMixin,
    PithiaTypeMetadataPropertiesMixin,
    PithiaTypesMetadataPropertiesMixin,
)


class ScientificMetadataXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class OrganisationXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        GmdUrlMetadataPropertiesMixin,
        PithiaDescriptionMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaShortNameMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    pass


class IndividualXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        GmdUrlMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def position_name(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:positionName' % self.PITHIA_NSPREFIX_XPATH)
    
    @property
    def organisation(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:organisation/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class ProjectXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaStatusMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def keywords(self):
        keyword_elements = self._get_elements_with_xpath_query('.//%s:keyword/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))
        keywords = []
        for kw_elem in keyword_elements:
            keyword = self._get_element_value_or_blank_string(kw_elem)
            if not keyword:
                continue
            keywords.append(keyword)
        return list(set(keywords))

    @property
    def sub_projects(self):
        return self._get_elements_with_xpath_query('.//%s:subProject/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class PlatformXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaStandardIdentifiersMetadataPropertiesMixin,
        PithiaTypeMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def location(self):
        gml_point = self._get_first_element_from_list(self._get_elements_with_xpath_query('.//%s:geometryLocation' % (self.PITHIA_NSPREFIX_XPATH)))
        if not gml_point:
            return None
        nl_identifier = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:nameLocation/%s:EX_GeographicDescription/%s:geographicIdentifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO))
        return {
            'name': nl_identifier,
            'point': {
                'id': self._get_first_element_value_or_blank_string_with_xpath_query('.//@%s:id' % NamespacePrefix.GML, parent_element=gml_point),
                'srs_name': self._get_first_element_value_or_blank_string_with_xpath_query('.//@srsName', parent_element=gml_point),
                'pos': self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:pos' % NamespacePrefix.GML, parent_element=gml_point),
            },
        }

    @property
    def child_platforms(self):
        return self._get_elements_with_xpath_query('.//%s:childPlatform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class OperationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        GmlTimePeriodMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaStatusMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def operation_time(self):
        operation_time_element = self._get_first_element_from_list(self._get_elements_with_xpath_query('.//%s:operationTime' % self.PITHIA_NSPREFIX_XPATH))
        return self._gml_time_period(operation_time_element)

    @property
    def platforms(self):
        return self._get_elements_with_xpath_query('.//%s:platform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class InstrumentXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaTypeMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def instrument_version(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('/%s:Instrument/%s:version' % (self.PITHIA_NSPREFIX_XPATH, self.PITHIA_NSPREFIX_XPATH))

    @property
    def members(self):
        return self._get_elements_with_xpath_query('.//%s:member/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))

    @property
    def operational_modes(self):
        operational_mode_elements = self._get_elements_with_xpath_query('.//%s:InstrumentOperationalMode' % self.PITHIA_NSPREFIX_XPATH)
        operational_modes = []
        for om in operational_mode_elements:
            om_id = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:id' % self.PITHIA_NSPREFIX_XPATH, parent_element=om)
            om_name = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:name' % self.PITHIA_NSPREFIX_XPATH, parent_element=om)
            om_description = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:description' % self.PITHIA_NSPREFIX_XPATH, parent_element=om)
            operational_modes.append({
                'id': om_id,
                'name': om_name,
                'description': om_description,
            })
        return operational_modes


class AcquisitionCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilitiesMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaInputOutputMetadataPropertiesMixin,
        PithiaObservedPropertiesMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def instrument_mode_pair(self):
        instrument_mode_pair_element = self._get_first_element_from_list(self._get_elements_with_xpath_query('.//%s:InstrumentOperationalModePair' % self.PITHIA_NSPREFIX_XPATH))
        instrument = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:instrument/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=instrument_mode_pair_element)
        mode = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:mode/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=instrument_mode_pair_element)
        if not instrument:
            return {}
        if not mode:
            return {}
        return {
            'instrument': instrument,
            'mode': mode,
        }

    @property
    def input_descriptions(self):
        return self._get_input_outputs('inputDescription')

    @property
    def output_descriptions(self):
        return self._get_input_outputs('outputDescription')


class AcquisitionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilityLinksMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    capabilities_element_key_xml = 'acquisitionCapabilities'
    capabilities_element_key = 'acquisition_capabilities'


class ComputationCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilitiesMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaInputOutputMetadataPropertiesMixin,
        PithiaObservedPropertiesMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaTypesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def computation_version(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('/%s:ComputationCapabilities/%s:version' % (self.PITHIA_NSPREFIX_XPATH, self.PITHIA_NSPREFIX_XPATH))

    @property
    def child_computations(self):
        return self._get_elements_with_xpath_query('.//%s:childComputation/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))

    @property
    def processing_inputs(self):
        return self._get_input_outputs('processingInput')

    @property
    def processing_outputs(self):
        return self._get_input_outputs('processingOutput')


class ComputationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilityLinksMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    capabilities_element_key_xml = 'computationCapabilities'
    capabilities_element_key = 'computation_capabilities'


class ProcessXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilitiesMetadataPropertiesMixin,
        PithiaDocumentationMetadataPropertiesMixin,
        PithiaObservedPropertiesMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    def acquisition_components(self):
        return self._get_elements_with_xpath_query('.//%s:acquisitionComponent/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    def computation_components(self):
        return self._get_elements_with_xpath_query('.//%s:computationComponent/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class DataCollectionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaFeaturesOfInterestMetadataPropertiesMixin,
        PithiaOnlineResourceMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaTypesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def procedure(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:procedure/@%s:href' % (NamespacePrefix.OM, NamespacePrefix.XLINK))
    
    @property
    def projects(self):
        return self._get_elements_with_xpath_query('.//%s:project/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    @property
    def sub_collections(self):
        return self._get_elements_with_xpath_query('.//%s:subCollection/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    @property
    def online_resources(self):
        collection_results_element = self._get_first_element_from_list(self._get_elements_with_xpath_query('.//%s:collectionResults' % self.PITHIA_NSPREFIX_XPATH))
        return self._get_online_resources(collection_results_element)

    @property
    def permissions(self):
        return self._get_elements_with_xpath_query('.//%s:permission/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class StaticDatasetEntryXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        GmlTimePeriodMetadataPropertiesMixin,
        PithiaFeaturesOfInterestMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def static_dataset_category(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:category/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))

    @property
    def phenomenon_time(self):
        phenomenon_time_element = self._get_first_element_from_list(self._get_elements_with_xpath_query('.//%s:phenomenonTime' % self.PITHIA_NSPREFIX_XPATH))
        return self._gml_time_period(phenomenon_time_element)


class DataSubsetXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        GmlTimePeriodMetadataPropertiesMixin,
        PithiaDoiMetadataPropertiesMixin,
        PithiaFeaturesOfInterestMetadataPropertiesMixin,
        PithiaOnlineResourceMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def result_times(self):
        result_time_elements = self._get_elements_with_xpath_query('.//%s:resultTime' % self.PITHIA_NSPREFIX_XPATH)
        if not result_time_elements:
            return []
        return [
            self._gml_time_period(result_time_element)
            for result_time_element in result_time_elements
            if result_time_element is not None
        ]
    
    @property
    def online_resources(self):
        return self._get_online_resources()


class WorkflowXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        ScientificMetadataXmlMappingShortcuts):
    @property
    def workflow_details_url(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:workflowDetails/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class DoiKernelMetadataMappingShortcuts(PithiaDoiMetadataPropertiesMixin):
    @property
    def properties(self):
        return self.doi_kernel_metadata