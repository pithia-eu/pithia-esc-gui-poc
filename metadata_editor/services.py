from lxml import etree

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
    TimePeriodMetadataEditor,
    TypeMetadataEditor,
    TypeMultipleMetadataEditor,
    URLMetadataEditor,
    XlinkHrefMetadataEditor,
)
from .editor_dataclasses import (
    CitationPropertyTypeMetadataUpdate,
    DoiKernelMetadataUpdate,
    InputOutputMetadataUpdate,
    OperationTimeMetadataUpdate,
    PhenomenonTimeMetadataUpdate,
    ResultTimeMetadataUpdate,
    SourceMetadataUpdate,
)

from common import models


class OrganisationEditor(
    BaseMetadataEditor,
    ContactInfoMetadataEditor,
    ShortNameMetadataEditor):
    def __init__(self, xml_string: str ='') -> None:
        super().__init__(models.Organisation.root_element_name, xml_string=xml_string)

    def update_short_name(self, short_name):
        self.metadata_dict['shortName'] = short_name


class IndividualEditor(
    BaseMetadataEditor,
    ContactInfoMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.Individual.root_element_name, xml_string=xml_string)

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
        super().__init__(models.Project.root_element_name, xml_string=xml_string)

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
        super().__init__(models.Platform.root_element_name, xml_string)

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
    StatusMetadataEditor,
    TimePeriodMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.Operation.root_element_name, xml_string)

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

    def update_operation_time(self, update_data: OperationTimeMetadataUpdate):
        operation_time_key = 'operationTime'
        self.update_time_period(update_data, operation_time_key)
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
        super().__init__(models.Instrument.root_element_name, xml_string)

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
    InputOutputTypeMetadataEditor,
    QualityAssessmentMetadataEditor,
    RelatedPartiesMetadataEditor,
    XlinkHrefMetadataEditor):
    GCO19115_NSPREFIX = 'gco19115'
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.AcquisitionCapabilities.root_element_name, xml_string)

    def setup_namespaces(self):
        super().setup_namespaces()
        self.namespaces.update({
            self.GCO19115_NSPREFIX: Namespace.GCO19115
        })

    def update_input_descriptions(self, update_data: list[InputOutputMetadataUpdate]):
        self._update_input_outputs('inputDescription', update_data)

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
        super().__init__(models.Acquisition.root_element_name, xml_string)


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
        super().__init__(models.ComputationCapabilities.root_element_name, xml_string)

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
        super().__init__(models.Computation.root_element_name, xml_string)


class ProcessEditor(
        BaseMetadataEditor,
        CapabilitiesMetadataEditor,
        DataLevelMetadataEditor,
        DocumentationMetadataEditor,
        QualityAssessmentMetadataEditor,
        RelatedPartiesMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.Process.root_element_name, xml_string)

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
        super().__init__(models.DataCollection.root_element_name, xml_string)

    def set_empty_properties(self):
        self.metadata_dict['%s:phenomenonTime' % NamespacePrefix.OM] = {}
        self.metadata_dict['%s:resultTime' % NamespacePrefix.OM] = {}
        self.metadata_dict['%s:observedProperty' % NamespacePrefix.OM] = {}
        self.metadata_dict['%s:result' % NamespacePrefix.OM] = {}

    def update_collection_results(self, update_data: list[SourceMetadataUpdate]):
        collection_results_key = 'collectionResults'
        self.metadata_dict.setdefault(collection_results_key, {})
        collection_results = self.metadata_dict[collection_results_key]
        self._update_sources(collection_results, update_data)
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


class StaticDatasetEntryEditor(
        BaseMetadataEditor,
        TimePeriodMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.StaticDatasetEntry.root_element_name, xml_string)

    def update_name(self, name):
        if not name:
            return
        self.metadata_dict['entryName'] = name

    def update_description(self, description):
        self.metadata_dict['entryDescription'] = description

    def update_static_dataset_identifier(self, static_dataset_url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'staticDatasetIdentifier',
            self.get_as_xlink_href(static_dataset_url)
        )

    def update_static_dataset_category(self, static_dataset_category_url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'category',
            self.get_as_xlink_href(static_dataset_category_url)
        )

    def update_phenomenon_time(self, update_data: PhenomenonTimeMetadataUpdate):
        phenomenon_time_key = 'phenomenonTime'
        self.update_time_period(update_data, phenomenon_time_key)


class DataSubsetEditor(
    BaseMetadataEditor,
    DataLevelMetadataEditor,
    QualityAssessmentMetadataEditor,
    SourcePropertyTypeEditor,
    TimePeriodMetadataEditor,
    XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.DataSubset.root_element_name, xml_string)

    def update_name(self, name):
        if not name:
            return
        self.metadata_dict['dataSubsetName'] = name

    def update_description(self, description):
        self.metadata_dict['dataSubsetDescription'] = description

    def update_entry_identifier(self, entry_url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'entryIdentifier',
            self.get_as_xlink_href(entry_url)
        )

    def update_data_collection(self, data_collection_url: str):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'dataCollection',
            self.get_as_xlink_href(data_collection_url)
        )

    def update_phenomenon_time(self, update_data: PhenomenonTimeMetadataUpdate):
        phenomenon_time_key = 'phenomenonTime'
        self.update_time_period(update_data, phenomenon_time_key)

    def update_result_time(self, update_data: ResultTimeMetadataUpdate):
        result_time_key = 'resultTime'
        self.update_time_period(update_data, result_time_key)

    def update_result_times(self, update_data: list[ResultTimeMetadataUpdate]):
        result_time_key = 'resultTime'
        self.update_time_periods(update_data, result_time_key)

    def update_sources(self, update_data: list[SourceMetadataUpdate]):
        return self._update_sources(self.metadata_dict, update_data)

    def update_doi_kernel_metadata(self, update_data: DoiKernelMetadataUpdate):
        self.metadata_dict['doi'] = {
            '%s:referentDoiName' % NamespacePrefix.DOI: update_data.referent_doi_name,
            '%s:primaryReferentType' % NamespacePrefix.DOI: update_data.primary_referent_type,
            '%s:registrationAgencyDoiName' % NamespacePrefix.DOI: update_data.registration_agency_doi_name,
            # Already stored in the handle, can just retrieve it.
            '%s:issueDate' % NamespacePrefix.DOI: update_data.doi_issue_date,
            # issueNumber - Added manually to the handle, then incremented manually as well,
            # each time the handle is updated.
            '%s:issueNumber' % NamespacePrefix.DOI: update_data.doi_issue_number,
            '%s:referentCreation' % NamespacePrefix.DOI: {
                '%s:name' % NamespacePrefix.DOI: {
                    '@primaryLanguage': update_data.rc_name_primary_language,
                    '%s:value' % NamespacePrefix.DOI: update_data.rc_name_value,
                    '%s:type' % NamespacePrefix.DOI: update_data.rc_name_type,
                },
                '%s:identifier' % NamespacePrefix.DOI: {
                    '%s:nonUriValue' % NamespacePrefix.DOI: update_data.rc_identifier_non_uri_value,
                    '%s:uri' % NamespacePrefix.DOI: {
                        '@returnType': update_data.rc_identifier_uri_return_type,
                        '$': update_data.rc_identifier_uri_value,
                    },
                    '%s:type' % NamespacePrefix.DOI: update_data.rc_identifier_type,
                },
                '%s:structuralType' % NamespacePrefix.DOI: update_data.rc_structural_type,
                '%s:mode' % NamespacePrefix.DOI: update_data.rc_mode,
                '%s:character' % NamespacePrefix.DOI: update_data.rc_character,
                '%s:type' % NamespacePrefix.DOI: update_data.rc_type,
                '%s:principalAgent' % NamespacePrefix.DOI: {
                    '%s:name' % NamespacePrefix.DOI: {
                        '%s:value' % NamespacePrefix.DOI: update_data.rc_principal_agent_name_value,
                        '%s:type' % NamespacePrefix.DOI: update_data.rc_principal_agent_name_type,
                    },
                },
            },
        }


class WorkflowEditor(
        BaseMetadataEditor,
        XlinkHrefMetadataEditor):
    def __init__(self, xml_string: str = '') -> None:
        super().__init__(models.Workflow.root_element_name, xml_string)

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


class SimpleMetadataEditor:
    def __init__(self, xml_string: str) -> None:
        self.xml_string = xml_string
        try:
            self.xml_string_parsed = etree.fromstring(self.xml_string.encode('utf-8'))
        except AttributeError:
            self.xml_string_parsed = etree.fromstring(self.xml_string)
        self.PITHIA_NS_PREFIX = 'PITHIA'
        self.namespaces = {
            self.PITHIA_NS_PREFIX: Namespace.PITHIA,
            NamespacePrefix.GMD: Namespace.GMD,
        }

    def to_xml(self):
        return etree.tostring(self.xml_string_parsed, pretty_print=True).decode()


class SimpleDataSubsetEditor(SimpleMetadataEditor):
    def update_online_resource_url(self, online_resource_name: str, online_resource_url: str):
        corresponding_linkage_elements = self.xml_string_parsed.xpath(
            './/%s:source/%s:OnlineResource[%s:name[contains(text(), "%s")]]/%s:linkage/%s:URL'
            % (
                self.PITHIA_NS_PREFIX,
                self.PITHIA_NS_PREFIX,
                self.PITHIA_NS_PREFIX,
                online_resource_name,
                self.PITHIA_NS_PREFIX,
                NamespacePrefix.GMD,
            ),
            namespaces=self.namespaces
        )
        corresponding_linkage_element = next(iter(corresponding_linkage_elements), None)
        if corresponding_linkage_element is None:
            return
        corresponding_linkage_element.text = online_resource_url

    def update_referent_doi_name_if_exists(self, referent_doi_name: str):
        doi_kernel_metadata_element = self.xml_string_parsed.find('{%s}doi' % Namespace.PITHIA)
        if doi_kernel_metadata_element is None:
            return
        referent_doi_name_element = doi_kernel_metadata_element.find('{%s}referentDoiName' % Namespace.DOI)
        referent_doi_name_element.text = referent_doi_name


class SimpleWorkflowEditor(SimpleMetadataEditor):
    def update_workflow_details_url(self, workflow_details_url: str):
        workflow_details_element = self.xml_string_parsed.find('{%s}workflowDetails' % Namespace.PITHIA)
        workflow_details_element.set('{%s}href' % Namespace.XLINK, workflow_details_url)