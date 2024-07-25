import copy

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
from .editor_dataclasses import OperationTimeMetadataUpdate


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


class OperationEditor(
    BaseMetadataEditor,
    DocumentationMetadataEditor,
    LocationMetadataEditor,
    RelatedPartiesMetadataEditor,
    StatusMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Operation', xml_string)

    def update_platforms(self, update_data):
        platform_key = 'platform'
        self.metadata_dict[platform_key] = [{
            '@%s:href' % NamespacePrefix.XLINK: ud, 
        } for ud in update_data if not _is_metadata_component_empty(ud)]
        self.remove_child_element_if_empty(
            self.metadata_dict,
            platform_key
        )

    def update_child_operations(self, update_data):
        child_operation_key = 'childOperation'
        self.metadata_dict[child_operation_key] = [{
            '@%s:href' % NamespacePrefix.XLINK: ud,
        } for ud in update_data if not _is_metadata_component_empty(ud)]
        self.remove_child_element_if_empty(
            self.metadata_dict,
            child_operation_key
        )

    def _update_time_instant_property_type_element(
        self,
        time_prop_element,
        time_instant_id,
        time_position_value
    ):
        time_instant_key = '%s:TimeInstant' % NamespacePrefix.GML
        time_position_key = '%s:timePosition' % NamespacePrefix.GML
        time_prop_element.setdefault(time_instant_key, {})
        time_instant = time_prop_element[time_instant_key]
        # gml:TimeInstant id attribute
        time_instant['@%s:id' % NamespacePrefix.GML] = time_instant_id
        time_instant.setdefault(time_position_key, {})
        time_position = time_instant[time_position_key]
        # gml:timePosition text
        if time_position_value:
            time_position_value = str(time_position_value)
        time_position['$'] = time_position_value

    def update_operation_time(self, update_data: OperationTimeMetadataUpdate):
        # operationTime container element
        operation_time_key = 'operationTime'
        self.metadata_dict.setdefault(operation_time_key, {})
        operation_time = self.metadata_dict[operation_time_key]
        # gml:TimePeriod container element
        time_period_key = '%s:TimePeriod' % NamespacePrefix.GML
        operation_time.setdefault(time_period_key, {})
        time_period = self.metadata_dict[operation_time_key][time_period_key]
        time_period['@%s:id' % NamespacePrefix.GML] = update_data.time_period_id

        # Check for clashing gml:TimePeriod child elements -
        # gml:beginPosition/endPosition and gml:begin/end cannot
        # both exist in the same gml:TimePeriod element.
        time_period.pop('%s:beginPosition' % NamespacePrefix.GML, None)
        time_period.pop('%s:endPosition' % NamespacePrefix.GML, None)

        # gml:TimePeriod gml:begin container element
        time_period_begin_key = '%s:begin' % NamespacePrefix.GML
        time_period.setdefault(time_period_begin_key, {})
        time_period_begin = time_period[time_period_begin_key]
        self._update_time_instant_property_type_element(
            time_period_begin,
            update_data.time_instant_begin_id,
            update_data.time_instant_begin_position
        )
        self.remove_child_element_if_empty(
            time_period,
            time_period_begin_key
        )

        # gml:TimePeriod gml:end container element
        time_period_end_key = '%s:end' % NamespacePrefix.GML
        time_period.setdefault(time_period_end_key, {})
        time_period_end = time_period[time_period_end_key]
        self._update_time_instant_property_type_element(
            time_period_end,
            update_data.time_instant_end_id,
            update_data.time_instant_end_position
        )
        self.remove_child_element_if_empty(
            time_period,
            time_period_end_key
        )

        time_period_copy = copy.deepcopy(time_period)
        time_period_copy_no_optionals = {
            key: value for key, value in time_period_copy.items()
            if key == time_period_begin_key or key == time_period_end_key
        }
        # Remove "frame" attribute before checking timePeriod
        # element as it affects whether the it is considered
        # "empty" or not. If not added by the user xmlschema
        # adds it in when parsing an existing XML document.
        self.remove_xml_attributes_from_metadata_component(
            time_period_copy_no_optionals,
            disallowed_attrs=['@frame']
        )
        if _is_metadata_component_empty(time_period_copy_no_optionals):
            operation_time.pop(time_period_key)
        self.remove_child_element_if_empty(
            self.metadata_dict,
            operation_time_key
        )


class InstrumentEditor(
    BaseMetadataEditor,
    DocumentationMetadataEditor,
    RelatedPartiesMetadataEditor,
    TypeMetadataEditor,
    URLMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Instrument', xml_string)

    def update_instrument_version(self, version):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'version',
            version
        )

    def update_members(self, update_data):
        members_key = 'member'
        self.metadata_dict[members_key] = [{
            '@%s:href' % NamespacePrefix.XLINK: ud
        } for ud in update_data if ud]
        self.remove_child_element_if_empty(
            self.metadata_dict,
            members_key
        )

    def update_operational_modes(self, update_data):
        operational_modes_key = 'operationalMode'
        self.metadata_dict[operational_modes_key] = [
            {
                'InstrumentOperationalMode': {
                    'id': om.get('id'),
                    'name': om.get('name'),
                    'description': om.get('description'),
                }
            } for om in update_data if not _is_metadata_component_empty(om)
        ]
        self.remove_child_element_if_empty(
            self.metadata_dict,
            operational_modes_key
        )