from .xml_metadata_mapping_shortcut_mixins import (
    GmdContactInfoMetadataPropertiesMixin,
    GmdUrlMetadataPropertiesMixin,
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
    pass


class PlatformXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class OperationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class InstrumentXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class AcquisitionCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class AcquisitionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ComputationCapabilitiesXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ComputationXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class ProcessXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


class DataCollectionXmlMappingShortcuts(
        GmdUrlMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaResourceUrlsMetadataPropertiesMixin):
    pass


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