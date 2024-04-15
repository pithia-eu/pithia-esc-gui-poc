from lxml import etree

from .metadata_structure_components import *

from common.models import (
    Acquisition,
    AcquisitionCapabilities,
    Catalogue,
    CatalogueDataSubset,
    CatalogueEntry,
    Computation,
    ComputationCapabilities,
    DataCollection,
    Individual,
    Instrument,
    Operation,
    Organisation,
    Platform,
    Process,
    Project,
    Workflow,
)


class OrganisationMetadata(ContactInfoMetadataComponent, DescriptionMetadataComponent, GCOCharacterStringMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent, ShortNameMetadataComponent):
    def __init__(self, properties: dict) -> None:
        super().__init__(Organisation.root_element_name, nsmap_extensions={
            NamespacePrefix.GCO: Namespace.GCO,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_contact_info(properties['contact_info'])
        self.append_short_name(properties['short_name'])
        self.append_description(properties['description'])


class IndividualMetadata(ContactInfoMetadataComponent, DescriptionMetadataComponent, GCOCharacterStringMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Individual.root_element_name, nsmap_extensions={
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_contact_info(properties['contact_info'])
        self.append_organisation(properties['organisation'])

    def append_position_name(self, position_name):
        position_name_element = etree.SubElement(self.root, 'positionName')
        position_name_element.text = position_name

    def append_organisation(self, organisation_url):
        organisation_element_attributes = {
            '{%s}href' % Namespace.XLINK: organisation_url,
        }
        etree.SubElement(self.root, 'organisation', **organisation_element_attributes)


class ProjectMetadata(DescriptionMetadataComponent, GCOCharacterStringMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent, RelatedPartyMetadataComponent, ShortNameMetadataComponent, StatusMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Project.root_element_name, nsmap_extensions={
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_short_name(properties['short_name'])
        self.append_abstract(properties['abstract'])
        self.append_description(properties['description'])
        self.append_url(properties['url'])
        self.append_documentation(properties['documentation'])
        self.append_keywords(properties['keyword_dict_list'])
        self.append_related_parties(properties['related_parties'])
        self.append_status(properties['status'])

    def append_abstract(self, abstract):
        abstract_element = etree.SubElement(self.root, 'abstract')
        abstract_element.text = abstract

    def append_url(self, url):
        if not url:
            return
        url_element = etree.SubElement(self.root, 'URL')
        gmd_url_element = etree.SubElement(url_element, '{%s}URL' % Namespace.GMD)
        gmd_url_element.text = url

    def append_documentation(self, documentation):
        # Since CI_DateTypeCode 
        # If no title, date, identifier, other citation details, online resource
        if (not any([
            documentation.get('citation_title'),
            documentation.get('citation_date'),
            documentation.get('other_citation_details'),
            documentation.get('doi'),
            documentation.get('ci_linkage_url'),
        ])):
            return

        # Container elements
        documentation_element = etree.SubElement(self.root, 'documentation')
        citation_element = etree.SubElement(documentation_element, 'Citation')

        # GMD title - required
        gmd_title_element = etree.SubElement(citation_element, '{%s}title' % Namespace.GMD)
        self._append_gco_character_string_sub_element(gmd_title_element, documentation['citation_title'])

        # Date
        date_element = etree.SubElement(citation_element, 'date', xmlns=Namespace.GMD)
        ci_date_element = etree.SubElement(date_element, 'CI_Date')
        ci_date_date_element = etree.SubElement(ci_date_element, 'date')
        gco_date_element = etree.SubElement(ci_date_date_element, '{%s}Date' % Namespace.GCO)
        # Citation date - required, if container elements are included.
        gco_date_element.text = documentation['citation_date']
        ci_date_date_type_element = etree.SubElement(ci_date_element, 'dateType')
        # Assume <CI_DateTypeCode> will be the same for every XML file.
        # Citation date - code list and code list value need to be present
        # but can be left blank.
        ci_date_type_code_element = etree.SubElement(ci_date_date_type_element, 'CI_DateTypeCode', codeList=documentation['ci_date_type_code_code_list'], codeListValue=documentation['ci_date_type_code_code_list_value'])
        # Date type code is normally 'Publication date'.
        ci_date_type_code_element.text = documentation['ci_date_type_code']

        # Identifier (DOI)
        if documentation.get('doi'):
            identifier_element = etree.SubElement(citation_element, 'identifier', xmlns=Namespace.GMD)
            md_identifier_element = etree.SubElement(identifier_element, 'MD_Identifier')
            code_element = etree.SubElement(md_identifier_element, 'code')
            self._append_gco_character_string_sub_element(code_element, documentation['doi'])

        # GMD other citation details
        if documentation.get('other_citation_details'):
            gmd_other_citation_details_element = etree.SubElement(citation_element, '{%s}otherCitationDetails' % Namespace.GMD)
            self._append_gco_character_string_sub_element(gmd_other_citation_details_element, documentation['other_citation_details'])

        # Online Resource
        if documentation.get('ci_linkage_url'):
            online_resource_element = etree.SubElement(citation_element, 'onlineResource')
            ci_online_resource_element = etree.SubElement(online_resource_element, 'CI_OnlineResource', xmlns=Namespace.GMD)
            linkage_element = etree.SubElement(ci_online_resource_element, 'linkage')
            url_element = etree.SubElement(linkage_element, 'URL')
            url_element.text = documentation['ci_linkage_url']

    def append_keywords(self, keyword_dict_list):
        for keyword_dict in keyword_dict_list:
            keywords_element = etree.SubElement(self.root, 'keywords')
            md_keywords_element = etree.SubElement(keywords_element, 'MD_Keywords', xmlns=Namespace.GMD)
            for keyword in keyword_dict['keywords']:
                keyword_element = etree.SubElement(md_keywords_element, 'keyword')
                self._append_gco_character_string_sub_element(keyword_element, keyword)
            type_element = etree.SubElement(md_keywords_element, 'type')
            md_keyword_type_code_element = etree.SubElement(type_element, 'MD_KeywordTypeCode', codeList=keyword_dict['type']['code_list'], codeListValue=keyword_dict['type']['code_list_value'])


class PlatformMetadata(DescriptionMetadataComponent, GCOCharacterStringMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent, RelatedPartyMetadataComponent, ShortNameMetadataComponent, StandardIdentifierComponent, TypeMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Platform.root_element_name, nsmap_extensions={
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_short_name(properties['short_name'])
        self.append_standard_identifiers(self.root, properties['standard_identifiers'])
        self.append_url(properties['url'])
        self.append_description(properties['description'])
        self.append_type(properties['type'])
        self.append_location(properties['location'])
        self.append_related_parties(properties['related_parties'])
        self.append_child_platforms(properties['child_platforms'])

    def append_url(self, url):
        # Container element
        url_element = etree.SubElement(self.root, 'URL')
        # GMD URL
        gmd_url_element = etree.SubElement(url_element, '{%s}URL' % Namespace.GMD)
        gmd_url_element.text = url

    def append_location(self, location_dict):
        location_wrapper_element = etree.SubElement(self.root, 'location')
        location_element = etree.SubElement(location_wrapper_element, 'Location')
        
        # Geometry location
        geometry_location_element = etree.SubElement(location_element, 'geometryLocation')
        gml_point_element_attributes = {
            '{%s}id' % Namespace.GML: location_dict['geometry_location']['point']['id'],
            'srsName': location_dict['geometry_location']['point']['srs_name'],
        }
        gml_point_element = etree.SubElement(geometry_location_element, '{%s}Point' % Namespace.GML, **gml_point_element_attributes)
        gml_pos_element = etree.SubElement(gml_point_element, '{%s}pos' % Namespace.GML)
        gml_pos_element.text = location_dict['geometry_location']['point']['pos']

        # Name location
        name_location_element = etree.SubElement(location_element, 'nameLocation')
        ex_geographic_description_element = etree.SubElement(name_location_element, 'EX_GeographicDescription', xmlns=Namespace.GMD)
        # Geographic identifier
        geographic_identifier_element = etree.SubElement(ex_geographic_description_element, 'geographicIdentifier')
        # MD identifier
        md_identifier_element = etree.SubElement(geographic_identifier_element, 'MD_Identifier')
        # Code
        code_element = etree.SubElement(md_identifier_element, 'code')
        self._append_gco_character_string_sub_element(code_element, location_dict['name_location']['code'])

    def append_child_platforms(self, child_platforms):
        for cp in child_platforms:
            child_platform_element_attributes = {
                '{%s}href' % Namespace.XLINK: cp,
            }
            etree.SubElement(self.root, 'childPlatform', **child_platform_element_attributes)


class OperationMetadata(DescriptionMetadataComponent, NameMetadataComponent, GMLTimePeriodMetadataComponent, IdentifierMetadataComponent, RelatedPartyMetadataComponent, StatusMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Operation.root_element_name, nsmap_extensions={
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_name(properties['description'])
        self.append_operation_time(properties['operation_time'])
        self.append_status(properties['status'])
        self.append_related_parties(properties['related_parties'])
        self.append_platform(properties['platform'])

    def append_operation_time(self, operation_time_dict):
        # Operation time wrapper element
        operation_time_element = etree.SubElement(self.root, 'operationTime')

        self.append_gml_time_period(operation_time_element, operation_time_dict['time_period'])

    def append_platform(self, platform):
        platform_element_attributes = {
            '{%s}href' % Namespace.XLINK: platform,
        }
        etree.SubElement(self.root, 'platform', **platform_element_attributes)


class InstrumentMetadata(DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent, RelatedPartyMetadataComponent, TypeMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Instrument.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_type(properties['type'])
        self.append_operational_modes(properties['operational_modes'])
        self.append_related_parties(properties['related_parties'])

    def append_operational_modes(self, operational_mode_dict_list):
        for operational_mode_dict in operational_mode_dict_list:
            # Container elements
            operational_mode_element = etree.SubElement(self.root, 'operationalMode')
            instrument_operational_mode_element = etree.SubElement(operational_mode_element, 'InstrumentOperationalMode')
            # ID
            id_element = etree.SubElement(instrument_operational_mode_element, 'id')
            id_element.text = operational_mode_dict['id']
            # Name
            name_element = etree.SubElement(instrument_operational_mode_element, 'name')
            id_element.text = operational_mode_dict['name']
            # Description
            description_element = etree.SubElement(instrument_operational_mode_element, 'name')
            id_element.text = operational_mode_dict['description']


class AcquisitionCapabilitiesMetadata(CapabilitiesMetadataComponent, DataLevelMetadataComponent, DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent, QualityAssessmentMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(AcquisitionCapabilities.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_capabilities(properties['capabilities'])
        self.append_data_levels(properties['data_levels'])
        self.append_instrument_mode_pair(properties['instrument_mode_pair'])
        self.append_quality_assessment(properties['quality_assessment'])

    def append_instrument_mode_pair(self, instrument_mode_pairs):
        # Container elements
        instrument_mode_pair_element = etree.SubElement(self.root, 'instrumentModePair')
        instrument_operational_mode_pair_element = etree.SubElement(instrument_mode_pair_element, 'instrumentOperationalModePair')
        instrument_element_attributes = {
            '{%s}href' % Namespace.XLINK: 'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test',
        }
        instrument_element = etree.SubElement(instrument_operational_mode_pair_element, 'instrument', **instrument_element_attributes)
        mode_element_attributes = {
            '{%s}href' % Namespace.XLINK: 'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test#instrumentoperationalmode1',
        }
        mode_element = etree.SubElement(instrument_operational_mode_pair_element, 'mode', **mode_element_attributes)


class AcquisitionMetadata(CapabilityLinksMetadataComponent, DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent):
    capabilities_key = 'acquisition_capabilities'
    capabilities_element_name = 'acquisitionCapabilities'

    def __init__(self, properties) -> None:
        super().__init__(Acquisition.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_capability_links(properties['capability_links'])


class ComputationCapabilitiesMetadata(CapabilitiesMetadataComponent, DataLevelMetadataComponent, DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent, TypeMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(ComputationCapabilities.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_capabilities(properties['capabilities'])
        self.append_data_levels(properties['data_levels'])
        self.append_type(properties['type'])
        self.append_unused_elements()

    def append_unused_elements(self):
        etree.SubElement(self.root, 'version')
        etree.SubElement(self.root, 'softwareReference')
        etree.SubElement(self.root, 'processingInput')
        etree.SubElement(self.root, 'algorithm')


class ComputationMetadata(CapabilityLinksMetadataComponent, DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent):
    capabilities_key = 'computation_capabilities'
    capabilities_element_name = 'computationCapabilities'

    def __init__(self, properties) -> None:
        super().__init__(Computation.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_capability_links(properties['capability_links'])


class ProcessMetadata(DataLevelMetadataComponent, DescriptionMetadataComponent, NameMetadataComponent, IdentifierMetadataComponent, QualityAssessmentMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Process.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_data_levels(properties['data_levels'])
        self.append_quality_assessment(properties['quality_assessment'])
        self.append_acquisition_component(properties['acquisition'])
        self.append_computation_component(properties['computation'])

    def append_acquisition_component(self, acquisition):
        acquisition_element_attributes = {
            '{%s}href' % Namespace.XLINK: acquisition,
        }
        etree.SubElement(self.root, 'acquisitionComponent', **acquisition_element_attributes)

    def append_computation_component(self, computation):
        computation_element_attributes = {
            '{%s}href' % Namespace.XLINK: computation,
        }
        etree.SubElement(self.root, 'computationComponent', **computation_element_attributes)


class DataCollectionMetadata(DataLevelMetadataComponent, DescriptionMetadataComponent, NameMetadataComponent, IdentifierMetadataComponent, QualityAssessmentMetadataComponent, RelatedPartyMetadataComponent, SourceMetadataComponent, TypeMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(DataCollection.root_element_name, nsmap_extensions={
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.OM: Namespace.OM,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_unused_phenomenon_time()
        self.append_unused_result_time()
        self.append_process(properties['process'])
        self.append_unused_observed_property()
        self.append_features_of_interest(properties['features_of_interest'])
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_type(properties['type'])
        self.append_project(properties['project'])
        self.append_related_parties(properties['related_parties'])
        self.append_collection_results(properties['collection_results'])
        self.append_data_levels(properties['data_levels'])
        self.append_quality_assessment(properties['quality_assessment'])
        self.append_permissions(properties['permissions'])

    def append_features_of_interest(self, named_regions):
        # Container elements
        om_feature_of_interest_element = etree.SubElement(self.root, '{%s}featureOfInterest' % Namespace.OM)
        feature_of_interest_element = etree.SubElement(om_feature_of_interest_element, 'FeatureOfInterest')

        # Named regions
        for nr in named_regions:
            nr_element_attributes = {
                '{%s}href' % Namespace.XLINK: nr,
            }
            nr_element = etree.SubElement(feature_of_interest_element, 'namedRegion', **nr_element_attributes)

    def append_project(self, project):
        project_element_attributes = {
            '{%s}href' % Namespace.XLINK: project,
        }
        etree.SubElement(self.root, 'project', **project_element_attributes)

    def append_process(self, process):
        om_procedure_element_attributes = {
            '{%s}procedure' % Namespace.OM: process,
        }
        etree.SubElement(self.root, '{%s}procedure' % Namespace.OM, **om_procedure_element_attributes)

    def append_collection_results(self, sources):
        # Container element
        collection_results_element = etree.SubElement(self.root, 'collectionResults')

        self.append_sources(collection_results_element, sources)


    def append_permissions(self, permissions):
        for p in permissions:
            permission_element_attributes = {
                '{%s}href' % Namespace.XLINK: p,
            }
            etree.SubElement(self.root, 'permission', **permission_element_attributes)

    def append_unused_phenomenon_time(self):
        etree.SubElement(self.root, '{%s}phenomenonTime' % Namespace.OM)

    def append_unused_result_time(self):
        etree.SubElement(self.root, '{%s}resultTime' % Namespace.OM)

    def append_unused_observed_property(self):
        etree.SubElement(self.root, '{%s}observedProperty' % Namespace.OM)


class CatalogueMetadata(DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Catalogue.root_element_name, nsmap_extensions={
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_catalogue_category(properties['catalogue_category'])

    def append_catalogue_category(self, catalogue_category):
        catalogue_category_element_attributes = {
            '{%s}href' % Namespace.XLINK: catalogue_category,
        }
        etree.SubElement(self.root, 'catalogueCategory', **catalogue_category_element_attributes)


class CatalogueEntryMetadata(GMLTimePeriodMetadataComponent, IdentifierMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(CatalogueEntry.root_element_name, nsmap_extensions={
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_entry_name(properties['entry_name'])
        self.append_entry_description(properties['entry_description'])
        self.append_phenomenon_time(properties['phenomenon_time'])

    def append_entry_name(self, entry_name):
        entry_name_element = etree.SubElement(self.root, 'entryName')
        entry_name_element.text = entry_name

    def append_entry_description(self, entry_description):
        entry_description_element = etree.SubElement(self.root, 'entryDescription')
        entry_description_element.text = entry_description

    def append_catalogue_identifier(self, catalogue):
        catalogue_identifier_element_attributes = {
            '{%s}href' % Namespace.XLINK: catalogue,
        }
        catalogue_identifier_element = etree.SubElement(self.root, 'catalogueIdentifier', **catalogue_identifier_element_attributes)

    def append_phenomenon_time(self, phenomenon_time_dict):
        phenomenon_time_element = etree.SubElement(self.root, 'phenomenonTime')
        self.append_gml_time_period(phenomenon_time_element, phenomenon_time_dict['time_period'])


class CatalogueDataSubsetMetadata(DataLevelMetadataComponent, GMLTimePeriodMetadataComponent, IdentifierMetadataComponent, QualityAssessmentMetadataComponent, SourceMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(CatalogueDataSubset.root_element_name, nsmap_extensions={
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.XLINK: Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_data_subset_name(properties['data_subset_name'])
        self.append_data_subset_description(properties['data_subset_description'])
        self.append_data_collection(properties['data_collection'])
        self.append_result_time(properties['result_time']['time_period'])
        self.append_sources(self.root, properties['sources'])
        self.append_data_levels(properties['data_levels'])
        self.append_quality_assessment(properties['quality_assessment'])

    def append_entry_identifier(self, catalogue_entry):
        entry_identifier_element_attributes = {
            '{%s}href' % Namespace.XLINK: catalogue_entry,
        }
        entry_identifier_element = etree.SubElement(self.root, 'entryIdentifier', **entry_identifier_element_attributes)

    def append_data_subset_name(self, data_subset_name):
        data_subset_name_element = etree.SubElement(self.root, 'dataSubsetName')
        data_subset_name_element.text = data_subset_name

    def append_data_subset_description(self, data_subset_description):
        data_subset_description_element = etree.SubElement(self.root, 'dataSubsetDescription')
        data_subset_description_element.text = data_subset_description

    def append_data_collection(self, data_collection):
        data_collection_element_attributes = {
            '{%s}href' % Namespace.XLINK: data_collection,
        }
        data_collection_element = etree.SubElement(self.root, 'dataCollection', **data_collection_element_attributes)

    def append_result_time(self, time_period_dict):
        # Container element
        result_time_element = etree.SubElement(self.root, 'resultTime')

        self.append_gml_time_period(result_time_element, time_period_dict)


class WorkflowMetadata(DescriptionMetadataComponent, IdentifierMetadataComponent, NameMetadataComponent):
    def __init__(self, properties) -> None:
        super().__init__(Workflow.root_element_name, nsmap_extensions={
            'xlink': Namespace.XLINK,
        })
        self.append_identifier(properties['localid'], properties['namespace'])
        self.append_name(properties['name'])
        self.append_description(properties['description'])
        self.append_data_collections(properties['data_collections'])
        self.append_workflow_details(properties['workflow_details'])

    def append_data_collections(self, data_collections):
        data_collection_1_element_attributes = {
            '{%s}href' % Namespace.XLINK: data_collections[0],
        }
        etree.SubElement(self.root, 'dataCollection', **data_collection_1_element_attributes)
        data_collection_2_element_attributes = {
            '{%s}href' % Namespace.XLINK: data_collections[1],
        }
        etree.SubElement(self.root, 'dataCollection', **data_collection_2_element_attributes)

    def append_workflow_details(self, workflow_details_url):
        workflow_details_element_attributes = {
            '{%s}href' % Namespace.XLINK: workflow_details_url,
        }
        etree.SubElement(self.root, 'workflowDetails', **workflow_details_element_attributes)