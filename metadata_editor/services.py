from .service_utils import (
    _is_metadata_component_empty,
    BaseMetadataEditor,
    ContactInfoMetadataEditor,
    DocumentationMetadataEditor,
    LocationMetadataEditor,
    NamespacePrefix,
    RelatedPartiesMetadataEditor,
    ShortNameMetadataEditor,
    StandardIdentifierMetadataEditor,
    StatusMetadataEditor,
    TypeMetadataEditor,
    URLMetadataEditor,
)


class OrganisationEditor(
    BaseMetadataEditor,
    ContactInfoMetadataEditor,
    ShortNameMetadataEditor):
    def __init__(self, xml_string: str ='') -> None:
        super().__init__('Organisation', xml_string=xml_string)

    def update_short_name(self, short_name):
        self.metadata_dict['shortName'] = short_name


class IndividualEditor(
    BaseMetadataEditor,
    ContactInfoMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Individual', xml_string=xml_string)

    def update_organisation(self, organisation_url: str):
        organisation_key = 'organisation'
        self.metadata_dict[organisation_key] = {'@%s:href' % NamespacePrefix.XLINK: organisation_url}
        self.remove_child_element_if_empty(
            self.metadata_dict,
            organisation_key
        )

    def update_position_name(self, position_name: str):
        position_name_key = 'positionName'
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            position_name_key,
            position_name
        )


class ProjectEditor(
    BaseMetadataEditor,
    DocumentationMetadataEditor,
    RelatedPartiesMetadataEditor,
    ShortNameMetadataEditor,
    StatusMetadataEditor,
    URLMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Project', xml_string=xml_string)

    def update_abstract(self, abstract):
        abstract_key = 'abstract'
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            abstract_key,
            abstract
        )


class PlatformEditor(
    BaseMetadataEditor,
    DocumentationMetadataEditor,
    LocationMetadataEditor,
    RelatedPartiesMetadataEditor,
    ShortNameMetadataEditor,
    StandardIdentifierMetadataEditor,
    TypeMetadataEditor,
    URLMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Platform', xml_string)

    def update_child_platforms(self, update_data):
        child_platform_key = 'childPlatform'
        self.metadata_dict[child_platform_key] = [{
            '@%s:href' % NamespacePrefix.XLINK: ud,
        } for ud in update_data if not _is_metadata_component_empty(ud)]
        self.remove_child_element_if_empty(
            self.metadata_dict,
            child_platform_key
        )