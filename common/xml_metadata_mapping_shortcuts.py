from .xml_metadata_mapping_shortcut_mixins import (
    GmdContactInfoMetadataPropertiesMixin,
    PithiaCoreMetadataPropertiesMixin,
    PithiaDescriptionMetadataPropertiesMixin,
    PithiaResourceUrlsMetadataPropertiesMixin,
    PithiaShortNameMetadataPropertiesMixin,
)


class OrganisationXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaDescriptionMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin,
        PithiaShortNameMetadataPropertiesMixin):
    pass


class IndividualXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ProjectXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class PlatformXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class OperationXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class InstrumentXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class AcquisitionCapabilitiesXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class AcquisitionXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ComputationCapabilitiesXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ComputationXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ProcessXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class DataCollectionXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueEntryXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class CatalogueDataSubsetXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class WorkflowXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class PlatformXmlMappingShortcuts(
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass