from .xml_metadata_mapping_shortcut_mixins import (
    GmdContactInfoMetadataPropertiesMixin,
    PithiaCoreMetadataPropertiesMixin,
    PithiaDescriptionMetadataPropertiesMixin,
    PithiaShortNameMetadataPropertiesMixin,
)


class OrganisationXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin,
        PithiaDescriptionMetadataPropertiesMixin,
        PithiaShortNameMetadataPropertiesMixin):
    pass


class IndividualXmlMappingShortcuts(
        GmdContactInfoMetadataPropertiesMixin,
        PithiaCoreMetadataPropertiesMixin):
    pass