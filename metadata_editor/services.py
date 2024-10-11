import copy

from .service_utils import (
    _is_metadata_component_empty,
    BaseMetadataEditor,
    CapabilitiesMetadataEditor,
    CapabilityLinksMetadataEditor,
    ContactInfoMetadataEditor,
    DataLevelMetadataEditor,
    DocumentationMetadataEditor,
    InputOutputTypeMetadataEditor,
    LocationMetadataEditor,
    Namespace,
    NamespacePrefix,
    QualityAssessmentMetadataEditor,
    RelatedPartiesMetadataEditor,
    ShortNameMetadataEditor,
    SourcePropertyTypeEditor,
    StandardIdentifierMetadataEditor,
    StatusMetadataEditor,
    TypeMetadataEditor,
    TypeMultipleMetadataEditor,
    URLMetadataEditor,
    XlinkHrefMetadataEditor,
)
from .editor_dataclasses import (
    CitationPropertyTypeMetadataUpdate,
    InputOutputMetadataUpdate,
    OperationTimeMetadataUpdate,
    SourceMetadataUpdate,
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


class AcquisitionCapabilitiesEditor(
    BaseMetadataEditor,
    CapabilitiesMetadataEditor,
    DataLevelMetadataEditor,
    DocumentationMetadataEditor,
    QualityAssessmentMetadataEditor,
    RelatedPartiesMetadataEditor,
    XlinkHrefMetadataEditor):
    GCO19115_NSPREFIX = 'gco19115'
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('AcquisitionCapabilities', xml_string)

    def setup_namespaces(self):
        super().setup_namespaces()
        self.namespaces.update({
            self.GCO19115_NSPREFIX: Namespace.GCO19115
        })

    def update_first_input_description(self, name: str, description: str):
        input_description_key = 'inputDescription'
        self.metadata_dict.setdefault(input_description_key, [])
        input_descriptions = self.metadata_dict[input_description_key]
        if not input_descriptions:
            input_descriptions.append({})
        input_descriptions[0] = {
            'InputOutput': {
                'name': name,
                'description': {
                    '%s:LE_Source' % NamespacePrefix.MRL: {
                        '%s:description' % NamespacePrefix.MRL: {
                            '%s:CharacterString' % self.GCO19115_NSPREFIX: description
                        }
                    }
                },
            }
        }
        if not description:
            input_descriptions.pop(0)
        self.remove_child_element_if_empty(
            self.metadata_dict,
            input_description_key
        )

    def update_instrument_mode_pair(self, instrument: str, mode: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'instrumentModePair',
            {
                'InstrumentOperationalModePair': {
                    'instrument': self.get_as_xlink_href(instrument),
                    'mode': self.get_as_xlink_href(mode),
                }
            }
        )


class AcquisitionEditor(
    BaseMetadataEditor,
    CapabilityLinksMetadataEditor):
    capabilities_key = 'acquisitionCapabilities'

    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Acquisition', xml_string)


class ComputationCapabilitiesEditor(
        BaseMetadataEditor,
        CapabilitiesMetadataEditor,
        DataLevelMetadataEditor,
        DocumentationMetadataEditor,
        InputOutputTypeMetadataEditor,
        QualityAssessmentMetadataEditor,
        RelatedPartiesMetadataEditor,
        TypeMultipleMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('ComputationCapabilities', xml_string)

    def update_computation_component_version(self, version: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'version',
            version
        )

    def update_child_computations(self, urls: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'childComputation',
            [self.get_as_xlink_href(url) for url in urls if url.strip()]
        )

    def update_processing_inputs(self, update_data: list[InputOutputMetadataUpdate]):
        self._update_input_outputs('processingInput', update_data)

    def update_software_reference(self, update_data: CitationPropertyTypeMetadataUpdate):
        self._update_citation_property_type_element('softwareReference', update_data)


class ComputationEditor(
        BaseMetadataEditor,
        CapabilityLinksMetadataEditor):
    capabilities_key = 'computationCapabilities'

    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Computation', xml_string)


class ProcessEditor(
        BaseMetadataEditor,
        CapabilitiesMetadataEditor,
        DataLevelMetadataEditor,
        DocumentationMetadataEditor,
        QualityAssessmentMetadataEditor,
        RelatedPartiesMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('CompositeProcess', xml_string)

    def update_acquisition_components(self, update_data: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'acquisitionComponent',
            [
                self.get_as_xlink_href(url)
                for url in update_data if url.strip()
            ]
        )

    def update_computation_components(self, update_data: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'computationComponent',
            [
                self.get_as_xlink_href(url)
                for url in update_data if url.strip()
            ]
        )


class DataCollectionEditor(
        BaseMetadataEditor,
        DataLevelMetadataEditor,
        QualityAssessmentMetadataEditor,
        RelatedPartiesMetadataEditor,
        SourcePropertyTypeEditor,
        TypeMultipleMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('DataCollection', xml_string)

    def set_empty_properties(self):
        self.metadata_dict['%s:phenomenonTime' % NamespacePrefix.OM] = {}
        self.metadata_dict['%s:resultTime' % NamespacePrefix.OM] = {}
        self.metadata_dict['%s:observedProperty' % NamespacePrefix.OM] = {}
        self.metadata_dict['%s:result' % NamespacePrefix.OM] = {}

    def update_collection_results(self, update_data: list[SourceMetadataUpdate]):
        collection_results_key = 'collectionResults'
        self.metadata_dict.setdefault(collection_results_key, {})
        collection_results = self.metadata_dict[collection_results_key]
        self.update_sources(collection_results, update_data)
        self.remove_child_element_if_empty(
            self.metadata_dict,
            collection_results_key
        )

    def update_permissions(self, update_data: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'permission',
            [
                self.get_as_xlink_href(ud)
                for ud in update_data if ud.strip()
            ]
        )

    def update_projects(self, update_data: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'project',
            [
                self.get_as_xlink_href(ud)
                for ud in update_data if ud.strip()
            ]
        )

    def update_sub_collections(self, update_data: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'subCollection',
            [
                self.get_as_xlink_href(ud)
                for ud in update_data if ud.strip()
            ]
        )

    def update_procedure(self, process_url: str):
        self.metadata_dict['%s:procedure' % NamespacePrefix.OM] = {}
        if not process_url.strip():
            return
        self.metadata_dict['%s:procedure' % NamespacePrefix.OM] = self.get_as_xlink_href(process_url)
            

    def update_features_of_interest(self, update_data: list[str]):
        # Feature of interest container element
        feature_of_interest_container_key = '%s:featureOfInterest' % NamespacePrefix.OM
        self.metadata_dict[feature_of_interest_container_key] = {}
        feature_of_interest_container_element = self.metadata_dict[feature_of_interest_container_key]
        # Nested feature of interest container element
        nested_feature_of_interest_container_key = 'FeatureOfInterest'
        feature_of_interest_container_element.setdefault(nested_feature_of_interest_container_key, {})
        nested_feature_of_interest_container_element = feature_of_interest_container_element[nested_feature_of_interest_container_key]
        # Named regions
        self.update_child_element_and_remove_if_empty(
            nested_feature_of_interest_container_element,
            'namedRegion',
            [
                self.get_as_xlink_href(ud)
                for ud in update_data if ud.strip()
            ]
        )
        # Clean up
        self.remove_child_element_if_empty(
            feature_of_interest_container_element,
            nested_feature_of_interest_container_key
        )


class CatalogueEditor(
    BaseMetadataEditor,
    XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Catalogue', xml_string)

    def update_catalogue_category(self, catalogue_category_url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'catalogueCategory',
            self.get_as_xlink_href(catalogue_category_url)
        )


class CatalogueEntryEditor(
    BaseMetadataEditor,
    XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('CatalogueEntry', xml_string)

    def update_name(self, name):
        if not name:
            return
        self.metadata_dict['entryName'] = name

    def update_description(self, description):
        self.metadata_dict['entryDescription'] = description

    def update_catalogue_identifier(self, catalogue_url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'catalogueIdentifier',
            self.get_as_xlink_href(catalogue_url)
        )


class WorkflowEditor(
        BaseMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__('Workflow', xml_string)

    def update_data_collections(self, update_data: list[str]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'dataCollection',
            [
                self.get_as_xlink_href(url)
                for url in update_data if url.strip()
            ]
        )

    def update_workflow_details(self, url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'workflowDetails',
            self.get_as_xlink_href(url)
        )