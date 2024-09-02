from .xml_metadata_mapping_shortcut_mixins import (
    GmdContactInfoMetadataPropertiesMixin,
    GmdUrlMetadataPropertiesMixin,
    NamespacePrefix,
    PithiaCapabilitiesMetadataPropertiesMixin,
    PithiaCapabilityLinksMetadataPropertiesMixin,
    PithiaCoreMetadataPropertiesMixin,
    PithiaDescriptionMetadataPropertiesMixin,
    PithiaResourceUrlsMetadataPropertiesMixin,
    PithiaShortNameMetadataPropertiesMixin,
)


class OrganisationXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaDescriptionMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin,
        PithiaShortNameMetadataPropertiesMixin):
    pass


class IndividualXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ProjectXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def sub_projects(self):
        return self._get_elements_with_xpath_query('.//%s:subProject/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class PlatformXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def child_platforms(self):
        return self._get_elements_with_xpath_query('.//%s:childPlatform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class OperationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def platforms(self):
        return self._get_elements_with_xpath_query('.//%s:platform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class InstrumentXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def members(self):
        return self._get_elements_with_xpath_query('.//%s:member/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class AcquisitionCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class AcquisitionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilityLinksMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    capabilities_element_key_xml = 'acquisitionCapabilities'
    capabilities_element_key = 'acquisition_capabilities'


class ComputationCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilitiesMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    @property
    def child_computations(self):
        return self._get_elements_with_xpath_query('.//%s:childComputation/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class ComputationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCapabilityLinksMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    capabilities_element_key_xml = 'computationCapabilities'
    capabilities_element_key = 'computation_capabilities'


class ProcessXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    def acquisition_components(self):
        return self._get_elements_with_xpath_query('.//%s:acquisitionComponent/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
    
    def computation_components(self):
        return self._get_elements_with_xpath_query('.//%s:computationComponent/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class DataCollectionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
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
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueEntryXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueDataSubsetXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class WorkflowXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass