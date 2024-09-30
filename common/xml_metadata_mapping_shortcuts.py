from .xml_metadata_mapping_shortcut_mixins import (
    GmdContactInfoMetadataPropertiesMixin,
    GmdUrlMetadataPropertiesMixin,
    NamespacePrefix,
    PithiaCapabilitiesMetadataPropertiesMixin,
    PithiaCapabilityLinksMetadataPropertiesMixin,
    PithiaCoreMetadataPropertiesMixin,
    PithiaDescriptionMetadataPropertiesMixin,
    PithiaOntologyUrlsMetadataPropertiesMixin,
    PithiaQualityAssessmentMetadataPropertiesMixin,
    PithiaRelatedPartiesMetadataPropertiesMixin,
    PithiaResourceUrlsMetadataPropertiesMixin,
    PithiaShortNameMetadataPropertiesMixin,
)


class OrganisationXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaDescriptionMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin,
        PithiaShortNameMetadataPropertiesMixin):
    pass


class IndividualXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def position_name(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:positionName' % self.PITHIA_NSPREFIX_XPATH)
    
    @property
    def organisation(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:organisation/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class ProjectXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
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
    def status(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:status/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))

    @property
    def sub_projects(self):
        return self._get_elements_with_xpath_query('.//%s:subProject/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class PlatformXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def child_platforms(self):
        return self._get_elements_with_xpath_query('.//%s:childPlatform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class OperationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def platforms(self):
        return self._get_elements_with_xpath_query('.//%s:platform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class InstrumentXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
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
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
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


class AcquisitionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilityLinksMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    capabilities_element_key_xml = 'acquisitionCapabilities'
    capabilities_element_key = 'acquisition_capabilities'


class ComputationCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilitiesMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def computation_version(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('/%s:ComputationCapabilities/%s:version' % (self.PITHIA_NSPREFIX_XPATH, self.PITHIA_NSPREFIX_XPATH))

    @property
    def child_computations(self):
        return self._get_elements_with_xpath_query('.//%s:childComputation/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class ComputationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilityLinksMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    capabilities_element_key_xml = 'computationCapabilities'
    capabilities_element_key = 'computation_capabilities'


class ProcessXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    def acquisition_components(self):
        return self._get_elements_with_xpath_query('.//%s:acquisitionComponent/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    def computation_components(self):
        return self._get_elements_with_xpath_query('.//%s:computationComponent/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class DataCollectionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def features_of_interest(self):
        return self._get_elements_with_xpath_query('.//%s:namedRegion/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    @property
    def procedure(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:procedure/@%s:href' % (NamespacePrefix.OM, NamespacePrefix.XLINK))
    
    @property
    def projects(self):
        return self._get_elements_with_xpath_query('.//%s:project/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    @property
    def sub_collections(self):
        return self._get_elements_with_xpath_query('.//%s:subCollection/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class CatalogueXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueEntryXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueDataSubsetXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaQualityAssessmentMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class WorkflowXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaOntologyUrlsMetadataPropertiesMixin,
        PithiaRelatedPartiesMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass