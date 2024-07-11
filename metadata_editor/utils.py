from .metadata_component_utils import (
    BaseMetadataEditor,
    ContactInfoMetadataEditor,
    NamespacePrefix,
)


class OrganisationEditor(
    BaseMetadataEditor,
    ContactInfoMetadataEditor):
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