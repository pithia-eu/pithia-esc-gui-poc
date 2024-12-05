import copy
import json
import logging
import xmlschema
import xml.etree.ElementTree as ET
from dataclasses import asdict
from operator import attrgetter

from .editor_dataclasses import (
    CapabilityLinkMetadataUpdate,
    CitationPropertyTypeMetadataUpdate,
    ContactInfoMetadataUpdate,
    ContactInfoAddressMetadataUpdate,
    InputOutputMetadataUpdate,
    LocationMetadataUpdate,
    PithiaIdentifierMetadataUpdate,
    ProcessCapabilityMetadataUpdate,
    RelatedPartyMetadataUpdate,
    SourceMetadataUpdate,
    StandardIdentifierMetadataUpdate,
    TimePeriodMetadataUpdate,
    TimeSpanMetadataUpdate,
)

from validation.services import MetadataFileXSDValidator


logger = logging.getLogger(__name__)


class NamespacePrefix:
    DOI = 'doi'
    GCO19115 = 'gco'
    GCO = 'gco'
    GMD = 'gmd'
    GML = 'gml'
    MRL = 'mrl'
    OM = 'om'
    PITHIA = ''
    XLINK = 'xlink'
    XSI = 'xsi'


class Namespace:
    DOI = 'http://www.doi.org/2010/DOISchema'
    GCO19115 = 'http://standards.iso.org/iso/19115/-3/gco/1.0'
    GCO = 'http://www.isotc211.org/2005/gco'
    GMD = 'http://www.isotc211.org/2005/gmd'
    GML = 'http://www.opengis.net/gml/3.2'
    MRL = 'http://standards.iso.org/iso/19115/-3/mrl/1.0'
    OM = 'http://www.opengis.net/om/2.0'
    PITHIA = 'https://metadata.pithia.eu/schemas/2.2'
    XLINK = 'http://www.w3.org/1999/xlink'
    XSI = 'http://www.w3.org/2001/XMLSchema-instance'


def _is_metadata_component_empty(metadata_component, is_falsy: bool = True):
    if isinstance(metadata_component, dict):
        for dict_value in metadata_component.values():
            is_falsy = _is_metadata_component_empty(dict_value, is_falsy=is_falsy) and is_falsy
    elif isinstance(metadata_component, list):
        for item in metadata_component:
            is_falsy = _is_metadata_component_empty(item, is_falsy=is_falsy) and is_falsy
    elif metadata_component:
        is_falsy = False
    return is_falsy


# Key shared XML component editors
class BaseMetadataComponentEditor:
    def __init__(self) -> None:
        self.metadata_dict = {}
        self.setup_namespaces()
        for prefix, uri in self.namespaces.items():
            ET.register_namespace(prefix, uri)

    def setup_namespaces(self):
        namespace_class_attrs = [a for a in vars(NamespacePrefix).keys() if not a.startswith('__')]
        self.namespaces = {getattr(NamespacePrefix, a): getattr(Namespace, a) for a in namespace_class_attrs}

    # Clean up utils
    def remove_child_element_if_empty(self, parent_element: dict, child_element_key: str):
        if not _is_metadata_component_empty(parent_element[child_element_key]):
            return
        parent_element.pop(child_element_key, None)

    def pop_child_element_if_empty(self, parent_element: list, child_element, child_element_index: int):
        if not _is_metadata_component_empty(child_element):
            return
        parent_element.pop(child_element_index)

    def update_child_element_and_remove_if_empty(self, parent_element: dict, child_element_key: str, child_element_value):
        parent_element[child_element_key] = child_element_value
        self.remove_child_element_if_empty(parent_element, child_element_key)

    def update_list_element_and_pop_if_empty(self, element_list: list, element_index: int, new_element_value):
        try:
            element_list[element_index] = new_element_value
        except IndexError:
            element_list.append(new_element_value)
        self.pop_child_element_if_empty(element_list, element_list[element_index], element_index)

    def remove_xml_attributes_from_metadata_component(self, metadata_component: dict, disallowed_attrs: list = []):
        if isinstance(metadata_component, dict):
            for key in disallowed_attrs:
                if key not in metadata_component:
                    continue
                del metadata_component[key]
            for dict_value in metadata_component.values():
                self.remove_xml_attributes_from_metadata_component(dict_value, disallowed_attrs=disallowed_attrs)
        elif isinstance(metadata_component, list):
            for item in metadata_component:
                self.remove_xml_attributes_from_metadata_component(item, disallowed_attrs=disallowed_attrs)

    def remove_xmlschema_attributes_from_metadata_component(self, metadata_component: dict):
        self.remove_xml_attributes_from_metadata_component(
            metadata_component,
            disallowed_attrs=[
                '@owns',
                '@%s:type' % NamespacePrefix.XLINK,
            ]
        )


class BaseMetadataEditor(BaseMetadataComponentEditor):
    def __init__(self, root_element_name, xml_string: str = '') -> None:
        super().__init__()
        self.root_element_name = root_element_name
        self.schema = MetadataFileXSDValidator._instantiate_pithia_schema()
        if not xml_string:
            return
        self._load_from_xml_string(xml_string)

    def _load_from_xml_string(self, xml_string: str):
        metadata_json_unformatted = xmlschema.to_json(
            xml_string.encode('utf-8'),
            schema=self.schema
        )
        metadata_dict_unformatted = json.loads(metadata_json_unformatted)
        # Convert to dict twice so all elements
        # use prefixes instead of the "xmlns"
        # attribute.
        metadata_etree_formatted = xmlschema.to_etree(
            metadata_dict_unformatted,
            schema=self.schema,
            path=self.root_element_name,
            namespaces=self.namespaces
        )
        metadata_json_formatted = xmlschema.to_json(
            ET.tostring(metadata_etree_formatted, encoding='utf-8'),
            schema=self.schema
        )
        self.metadata_dict = json.loads(metadata_json_formatted)
        self.remove_xmlschema_attributes_from_metadata_component(self.metadata_dict)

    def _metadata_dict_to_xml(self, component_dict: dict, path: str):
        xml = xmlschema.to_etree(
            component_dict,
            schema=self.schema,
            path=path,
            namespaces=self.namespaces,
            unordered=True)
        for elem in xml.iter():
            if 'owns' in elem.attrib:
                del elem.attrib['owns']
            if '{%s}type' % Namespace.XLINK in elem.attrib:
                del elem.attrib['{%s}type' % Namespace.XLINK]
        ET.indent(xml, space='    ')
        xml_string = ET.tostring(xml, xml_declaration=True, encoding='utf-8').decode()
        return xml_string

    def to_xml(self):
        return self._metadata_dict_to_xml(self.metadata_dict, self.root_element_name)

    def update_pithia_identifier(self, update_data: PithiaIdentifierMetadataUpdate):
        if not any(asdict(update_data).values()):
            return
        # Initialise identifier and PITHIA_Identifier
        # if not there already.
        self.metadata_dict.setdefault('identifier', {'PITHIA_Identifier': {}})
        pithia_identifier = self.metadata_dict['identifier']['PITHIA_Identifier']
        localid, namespace, creation_date, \
        last_modification_date, version = attrgetter(
            'localid',
            'namespace',
            'creation_date',
            'last_modification_date',
            'version')(update_data)
        if localid:
            pithia_identifier['localID'] = localid
        if namespace:
            pithia_identifier['namespace'] = namespace
        if creation_date:
            pithia_identifier['creationDate'] = creation_date
        if last_modification_date:
            pithia_identifier['lastModificationDate'] = last_modification_date
        if version:
            pithia_identifier['version'] = version

    def update_name(self, name):
        if not name:
            return
        self.metadata_dict['name'] = name

    def update_description(self, description):
        self.metadata_dict['description'] = description


class GCOCharacterStringMetadataEditor:
    def get_as_gco_character_string(self, value):
        return {'%s:CharacterString' % NamespacePrefix.GCO: value}


class XlinkHrefMetadataEditor:
    def get_as_xlink_href(self, url):
        return {'@%s:href' % NamespacePrefix.XLINK: url}


class CapabilitiesMetadataEditor(
    BaseMetadataComponentEditor,
    XlinkHrefMetadataEditor):
    def update_capabilities(self, update_data: list[ProcessCapabilityMetadataUpdate]):
        capabilities_key = 'capabilities'
        self.metadata_dict[capabilities_key] = {}
        capabilities = self.metadata_dict[capabilities_key]
        process_capabilities_key = 'processCapability'
        process_capabilities = []
        try:
            for ud in update_data:
                name = ud.name
                observed_property = ud.observed_property
                if not name or not observed_property:
                    continue
                process_capability = {}
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'name',
                    name
                )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'observedProperty',
                    self.get_as_xlink_href(observed_property)
                )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'dimensionalityInstance',
                    self.get_as_xlink_href(ud.dimensionality_instance)
                )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'dimensionalityTimeline',
                    self.get_as_xlink_href(ud.dimensionality_timeline)
                )
                cadence = ud.cadence
                cadence_unit = ud.cadence_unit
                if cadence and cadence_unit:
                    self.update_child_element_and_remove_if_empty(
                        process_capability,
                        'cadence',
                        {
                            '$': cadence,
                            '@unit': cadence_unit,
                        }
                    )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'vectorRepresentation',
                    [self.get_as_xlink_href(url) for url in ud.vector_representation if url]
                )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'coordinateSystem',
                    self.get_as_xlink_href(ud.coordinate_system)
                )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'units',
                    self.get_as_xlink_href(ud.units)
                )
                self.update_child_element_and_remove_if_empty(
                    process_capability,
                    'qualifier',
                    [self.get_as_xlink_href(url) for url in ud.qualifier if url]
                )
                process_capabilities.append(process_capability)
            capabilities[process_capabilities_key] = process_capabilities
        except BaseException as err:
            logger.exception(err)
        self.remove_child_element_if_empty(
            self.metadata_dict,
            capabilities_key
        )


class StandardIdentifierMetadataEditor(BaseMetadataComponentEditor):
    def update_standard_identifiers(self, parent_element, update_data: list[StandardIdentifierMetadataUpdate]):
        standard_identifiers_key = 'standardIdentifier'
        parent_element[standard_identifiers_key] = [{
            '@authority': ud.authority,
            '$': ud.value,
        } for ud in update_data if not _is_metadata_component_empty(asdict(ud))]
        self.remove_child_element_if_empty(
            parent_element,
            standard_identifiers_key
        )


class CapabilityLinksMetadataEditor(
        StandardIdentifierMetadataEditor,
        BaseMetadataComponentEditor,
        XlinkHrefMetadataEditor):
    def _update_time_spans(self, parent_element, time_spans: list[TimeSpanMetadataUpdate]):
        time_spans_key = 'timeSpan'
        parent_element[time_spans_key] = [{
            '%s:beginPosition' % NamespacePrefix.GML: ts.begin_position,
            '%s:endPosition' % NamespacePrefix.GML: {
                '@indeterminatePosition': ts.end_position,
            },
        } for ts in time_spans if not _is_metadata_component_empty(asdict(ts))]
        self.remove_child_element_if_empty(
            parent_element,
            time_spans_key
        )

    def update_capability_links(self, update_data: list[CapabilityLinkMetadataUpdate]):
        capability_links_container_key = 'capabilityLinks'
        self.metadata_dict.setdefault(capability_links_container_key, {})
        capability_links_container_element = self.metadata_dict[capability_links_container_key]
        capability_links_key = 'capabilityLink'
        capability_links = []
        for ud in update_data:
            capabilities = ud.capabilities
            if not capabilities:
                continue
            capability_link = {}
            # acquisitionCapabilities or computationCapabilities
            if isinstance(capabilities, list):
                capabilities = capabilities[0]
            capability_link[self.capabilities_key] = self.get_as_xlink_href(capabilities)
            # Platforms
            platforms = ud.platforms
            platforms_key = 'platform'
            capability_link[platforms_key] = [
                self.get_as_xlink_href(url)
            for url in platforms if url.strip()]
            self.remove_child_element_if_empty(
                capability_link,
                platforms_key
            )
            # Standard identifiers
            standard_identifiers = ud.standard_identifiers
            self.update_standard_identifiers(capability_link, standard_identifiers)
            # Time spans
            time_spans = ud.time_spans
            self._update_time_spans(capability_link, time_spans)
            capability_links.append(capability_link)
        capability_links_container_element[capability_links_key] = capability_links
        self.remove_child_element_if_empty(
            self.metadata_dict,
            capability_links_container_key
        )


class CitationPropertyTypeMetadataEditor(
        BaseMetadataComponentEditor,
        GCOCharacterStringMetadataEditor):
    def _update_publication_date_in_first_citation(self, citation, citation_publication_date):
        # A citation can have multiple dates
        citation_date_key = '%s:date' % NamespacePrefix.GMD
        citation.setdefault(citation_date_key, [])
        citation_dates = citation[citation_date_key]
        if len(citation_dates) == 0:
            citation_dates.append({})
        # CI_Date container element
        ci_date_key = '%s:CI_Date' % NamespacePrefix.GMD
        # The in-between tag text for elements with attributes
        # is set using '$' as a key.
        ci_date_type_code = {
            '@codeList': '',
            '@codeListValue': '',
            '$': '',
        }
        self.update_list_element_and_pop_if_empty(
            citation_dates,
            0,
            {
                ci_date_key: {
                    '%s:date' % NamespacePrefix.GMD: {
                        '%s:Date' % NamespacePrefix.GCO: citation_publication_date
                    },
                    '%s:dateType' % NamespacePrefix.GMD: {
                        '%s:CI_DateTypeCode' % NamespacePrefix.GMD: ci_date_type_code
                    }
                }
            }
        )
        ci_date_type_code['$'] = 'Publication Date'
        # Clean up
        self.remove_child_element_if_empty(
            citation,
            citation_date_key
        )

    def _update_identifier_in_first_citation(self, citation, value):
        citation_identifier_key = '%s:identifier' % NamespacePrefix.GMD
        citation.setdefault(citation_identifier_key, [])
        citation_identifiers = citation[citation_identifier_key]
        self.update_list_element_and_pop_if_empty(
            citation_identifiers,
            0,
            {
                '%s:MD_Identifier' % NamespacePrefix.GMD: {
                    '%s:code' % NamespacePrefix.GMD: self.get_as_gco_character_string(value)
                }
            }
        )
        # Clean up
        self.remove_child_element_if_empty(citation, citation_identifier_key)

    def _update_online_resource_in_first_citation(self, citation, value):
        citation_online_resource_key = 'onlineResource'
        citation.setdefault(citation_online_resource_key, [])
        citation_online_resources = citation[citation_online_resource_key]
        if len(citation_online_resources) == 0:
            citation_online_resources.append({})
        citation_online_resource_first = citation_online_resources[0]
        ci_online_resource_key = '%s:CI_OnlineResource' % NamespacePrefix.GMD
        citation_online_resource_first.setdefault(ci_online_resource_key, {})
        ci_online_resource = citation_online_resource_first[ci_online_resource_key]
        linkage_key = '%s:linkage' % NamespacePrefix.GMD
        self.update_child_element_and_remove_if_empty(
            ci_online_resource,
            linkage_key,
            {
                '%s:URL' % NamespacePrefix.GMD: value
            }
        )
        self.pop_child_element_if_empty(
            citation_online_resources,
            citation_online_resource_first,
            0
        )
        # Clean up
        self.remove_child_element_if_empty(citation, citation_online_resource_key)

    def _update_other_details_in_first_citation(self, citation, value):
        citation_other_details_key = '%s:otherCitationDetails' % NamespacePrefix.GMD
        self.update_child_element_and_remove_if_empty(
            citation,
            citation_other_details_key,
            self.get_as_gco_character_string(value)
        )

    def _update_citation_property_type_element(self, element_key, update_data: CitationPropertyTypeMetadataUpdate):
        # Set up container element
        self.metadata_dict.setdefault(element_key, [])
        citation_prop_type_elements = self.metadata_dict[element_key]
        # Create (if needed) and select the first
        # documentation element.
        if not citation_prop_type_elements:
            citation_prop_type_elements.append({})
        cpt_elem_first = citation_prop_type_elements[0]
        # Citation container element
        citation_key = 'Citation'
        cpt_elem_first.setdefault(citation_key, {})
        citation = cpt_elem_first[citation_key]
        # Citation properties
        citation_title, citation_publication_date, \
        citation_doi, citation_url, other_citation_details = attrgetter(
            'citation_title',
            'citation_publication_date',
            'citation_doi',
            'citation_url',
            'other_citation_details'
        )(update_data)
        # Citation title
        citation_title_key = '%s:title' % NamespacePrefix.GMD
        self.update_child_element_and_remove_if_empty(
            citation,
            citation_title_key,
            self.get_as_gco_character_string(citation_title)
        )
        # Citation date
        self._update_publication_date_in_first_citation(citation, citation_publication_date)
        # Citation identifier
        self._update_identifier_in_first_citation(citation, citation_doi)
        # Citation online resource
        self._update_online_resource_in_first_citation(citation, citation_url)
        # Citation other details
        self._update_other_details_in_first_citation(citation, other_citation_details)
        # Clean up
        self.remove_child_element_if_empty(
            cpt_elem_first,
            citation_key
        )
        self.pop_child_element_if_empty(
            citation_prop_type_elements,
            cpt_elem_first,
            0
        )
        self.remove_child_element_if_empty(
            self.metadata_dict,
            element_key
        )


# Shared XML component editors
class ContactInfoMetadataEditor(
    BaseMetadataComponentEditor,
    GCOCharacterStringMetadataEditor):
    def update_address_in_contact_info(self, ci_contact: dict, update_data: ContactInfoAddressMetadataUpdate):
        address_key = '%s:address' % NamespacePrefix.GMD
        ci_address_key = '%s:CI_Address' % NamespacePrefix.GMD
        ci_contact.setdefault(address_key, {ci_address_key: {}})
        ci_address = ci_contact[address_key][ci_address_key]
        delivery_point, city, administrative_area, \
        postal_code, country, electronic_mail_address = attrgetter(
            'delivery_point',
            'city',
            'administrative_area',
            'postal_code',
            'country',
            'electronic_mail_address')(update_data)
        # deliveryPoint can occur more than once.
        delivery_point_key = '%s:deliveryPoint' % NamespacePrefix.GMD
        ci_address.setdefault(delivery_point_key, [])
        self.update_list_element_and_pop_if_empty(
            ci_address[delivery_point_key],
            0,
            self.get_as_gco_character_string(delivery_point)
        )
        self.remove_child_element_if_empty(ci_address, delivery_point_key)

        self.update_child_element_and_remove_if_empty(
            ci_address,
            '%s:deliveryPoint' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(delivery_point)
        )
        self.update_child_element_and_remove_if_empty(
            ci_address,
            '%s:city' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(city)
        )
        self.update_child_element_and_remove_if_empty(
            ci_address,
            '%s:administrativeArea' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(administrative_area)
        )
        self.update_child_element_and_remove_if_empty(
            ci_address,
            '%s:postalCode' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(postal_code)
        )
        self.update_child_element_and_remove_if_empty(
            ci_address,
            '%s:country' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(country)
        )
        # electronicMailAddress can occur more than once.
        electronic_mail_address_key = '%s:electronicMailAddress' % NamespacePrefix.GMD
        ci_address.setdefault(electronic_mail_address_key, [])
        self.update_list_element_and_pop_if_empty(
            ci_address[electronic_mail_address_key],
            0,
            self.get_as_gco_character_string(electronic_mail_address)
        )
        self.remove_child_element_if_empty(ci_address, electronic_mail_address_key)

        # Clean up
        self.remove_child_element_if_empty(ci_contact, address_key)

    def update_phone_voice_in_contact_info(self, ci_contact: dict, value: str):
        phone_key = '%s:phone' % NamespacePrefix.GMD
        # phone container element
        ci_contact.setdefault(phone_key, {})
        phone = ci_contact[phone_key]
        # CI_Contact container element
        ci_telephone_key = '%s:CI_Telephone' % NamespacePrefix.GMD
        phone.setdefault(ci_telephone_key, {})
        ci_telephone = phone[ci_telephone_key]
        # CI_Contact - voice
        voice_key = '%s:voice' % NamespacePrefix.GMD
        ci_telephone.setdefault(voice_key, [])
        self.update_list_element_and_pop_if_empty(
            ci_telephone[voice_key],
            0,
            self.get_as_gco_character_string(value)
        )
        
        # Clean up
        self.remove_child_element_if_empty(ci_telephone, voice_key)
        self.remove_child_element_if_empty(phone, ci_telephone_key)
        self.remove_child_element_if_empty(ci_contact, phone_key)

    def update_online_resource_url_in_contact_info(self, ci_contact: dict, value: str):
        online_resource_key = '%s:onlineResource' % NamespacePrefix.GMD
        # onlineResource container element
        ci_contact.setdefault(
            online_resource_key,
            {
                '%s:CI_OnlineResource' % NamespacePrefix.GMD: {}
            }
        )
        online_resource = ci_contact['%s:onlineResource' % NamespacePrefix.GMD]
        # CI_OnlineResource container element
        online_resource.setdefault(
            '%s:CI_OnlineResource' % NamespacePrefix.GMD, {}
        )
        ci_online_resource = online_resource['%s:CI_OnlineResource' % NamespacePrefix.GMD]
        # Set both linkage > URL as linkage should only contain
        # one URL element.
        linkage_key = '%s:linkage' % NamespacePrefix.GMD
        self.update_child_element_and_remove_if_empty(
            ci_online_resource,
            linkage_key,
            {
                '%s:URL' % NamespacePrefix.GMD: value,
            }
        )

        # Clean up
        self.remove_child_element_if_empty(ci_contact, online_resource_key)

    def update_hours_of_service_in_contact_info(self, ci_contact: dict, value):
        self.update_child_element_and_remove_if_empty(
            ci_contact,
            '%s:hoursOfService' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(value),
        )

    def update_contact_instructions_in_contact_info(self, ci_contact: dict, value: str):
        self.update_child_element_and_remove_if_empty(
            ci_contact,
            '%s:contactInstructions' % NamespacePrefix.GMD,
            self.get_as_gco_character_string(value),
        )

    def update_contact_info(self, update_data: ContactInfoMetadataUpdate):
        # contactInfo container element
        contact_info_key = 'contactInfo'
        self.metadata_dict.setdefault(contact_info_key, [])
        contact_info = self.metadata_dict[contact_info_key]
        # CI_Contact container element
        ci_contact_key = '%s:CI_Contact' % NamespacePrefix.GMD
        # If no existing contactInfo elements, add an
        # empty one.
        if len(contact_info) == 0:
            contact_info.append({ci_contact_key: {}})
        contact_info_first = contact_info[0]
        ci_contact = contact_info_first[ci_contact_key]
        phone, address, online_resource, \
        hours_of_service, contact_instructions = attrgetter(
            'phone',
            'address',
            'online_resource',
            'hours_of_service',
            'contact_instructions')(update_data)
        self.update_address_in_contact_info(ci_contact, address)
        self.update_phone_voice_in_contact_info(ci_contact, phone)
        self.update_online_resource_url_in_contact_info(ci_contact, online_resource)
        self.update_hours_of_service_in_contact_info(ci_contact, hours_of_service)
        self.update_contact_instructions_in_contact_info(ci_contact, contact_instructions)
        
        # Clean up
        self.remove_child_element_if_empty(contact_info_first, ci_contact_key)
        self.pop_child_element_if_empty(
            self.metadata_dict[contact_info_key],
            contact_info_first,
            0
        )
        self.remove_child_element_if_empty(self.metadata_dict, contact_info_key)


class DataLevelMetadataEditor(BaseMetadataComponentEditor):
    def update_data_levels(self, data_level_urls: list):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'dataLevel',
            [{
                '@%s:href' % NamespacePrefix.XLINK: url
            } for url in data_level_urls if url.strip()]
        )


class DocumentationMetadataEditor(CitationPropertyTypeMetadataEditor):
    def update_documentation(self, update_data: CitationPropertyTypeMetadataUpdate):
        self._update_citation_property_type_element('documentation', update_data)


class InputOutputTypeMetadataEditor(BaseMetadataComponentEditor):
    GCO19115_NSPREFIX = 'gco19115'

    def setup_namespaces(self):
        super().setup_namespaces()
        self.namespaces.update({
            self.GCO19115_NSPREFIX: Namespace.GCO19115
        })

    def _update_input_outputs(self, container_element_key, update_data: list[InputOutputMetadataUpdate]):
        self.metadata_dict.setdefault(container_element_key, [])
        input_output_container_elements = self.metadata_dict[container_element_key]
        if not input_output_container_elements:
            input_output_container_elements.append({})
        input_outputs = [
            {
                'InputOutput': {
                    'name': ud.name,
                    'description': {
                        '%s:LE_Source' % NamespacePrefix.MRL: {
                            '%s:description' % NamespacePrefix.MRL: {
                                '%s:CharacterString' % self.GCO19115_NSPREFIX: ud.description
                            }
                        }
                    },
                }
            } for ud in update_data if not _is_metadata_component_empty(asdict(ud) and ud.description)
        ]
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            container_element_key,
            input_outputs
        )


class LocationMetadataEditor(BaseMetadataComponentEditor, GCOCharacterStringMetadataEditor):
    def _update_geometry_location(
        self,
        nested_location: dict,
        point_id: str,
        point_srs_name_url: str,
        point_pos_1: float,
        point_pos_2: float):
        geometry_location_key = 'geometryLocation'
        pos = [point_pos_1, point_pos_2]
        if point_pos_1 is None or point_pos_2 is None:
            pos = []
        self.update_child_element_and_remove_if_empty(
            nested_location,
            geometry_location_key,
            {
                '%s:Point' % NamespacePrefix.GML: {
                    '@%s:id' % NamespacePrefix.GML: point_id,
                    '@srsName': point_srs_name_url,
                    '%s:pos' % NamespacePrefix.GML: pos
                }
            }
        )

    def _update_name_location(self, nested_location: dict, value: str):
        self.update_child_element_and_remove_if_empty(
            nested_location,
            'nameLocation',
            {
                '%s:EX_GeographicDescription' % NamespacePrefix.GMD: {
                    '%s:geographicIdentifier' % NamespacePrefix.GMD: {
                        '%s:MD_Identifier' % NamespacePrefix.GMD: {
                            '%s:code' % NamespacePrefix.GMD: self.get_as_gco_character_string(value)
                        }
                    }
                }
            }
        )

    def update_location(self, update_data: LocationMetadataUpdate):
        location_key = 'location'
        nested_location_key = 'Location'
        self.metadata_dict.setdefault(location_key, {nested_location_key: {}})
        nested_location = self.metadata_dict[location_key][nested_location_key]
        self._update_geometry_location(
            nested_location,
            update_data.geometry_location_point_id,
            update_data.geometry_location_point_srs_name,
            update_data.geometry_location_point_pos_1,
            update_data.geometry_location_point_pos_2,
        )
        self._update_name_location(nested_location, update_data.location_name)
        self.remove_child_element_if_empty(
            self.metadata_dict,
            location_key
        )


class QualityAssessmentMetadataEditor(BaseMetadataComponentEditor):
    data_quality_flag_key = 'dataQualityFlag'

    def update_quality_assessment(
            self,
            data_quality_flag_urls: list,
            metadata_quality_flag_urls: list = [],
            is_max_occurs_unbounded: bool = True):
        quality_assessment_key = 'qualityAssessment'
        if is_max_occurs_unbounded:
            self.metadata_dict.setdefault(quality_assessment_key, [])
            quality_assessments = self.metadata_dict[quality_assessment_key]
            if not quality_assessments:
                quality_assessments.append({})
            quality_assessment = quality_assessments[0]
        else:
            self.metadata_dict.setdefault(quality_assessment_key, {})
            quality_assessment = self.metadata_dict[quality_assessment_key]
        # Data/Metadata quality flags
        self._update_data_quality_flags(quality_assessment, data_quality_flag_urls)
        self._update_metadata_quality_flags(quality_assessment, metadata_quality_flag_urls)
        # Remove <qualityAssessment> if there are no data quality
        # flags.
        quality_assessment_copy = copy.deepcopy(quality_assessment)
        quality_assessment_copy_no_optionals = {
            key: value for key, value in quality_assessment_copy.items()
            if key == self.data_quality_flag_key
        }
        if _is_metadata_component_empty(quality_assessment_copy_no_optionals):
            self.metadata_dict.pop(quality_assessment_key)
        

    def _update_data_quality_flags(self, parent_element, update_data):
        self.update_child_element_and_remove_if_empty(
            parent_element,
            self.data_quality_flag_key,
            [
                {
                    '@%s:href' % NamespacePrefix.XLINK: url,
                } for url in update_data if url.strip()
            ]
        )

    def _update_metadata_quality_flags(self, parent_element, update_data):
        self.update_child_element_and_remove_if_empty(
            parent_element,
            'metadataQualityFlag',
            [
                {
                    '@%s:href' % NamespacePrefix.XLINK: url,
                } for url in update_data if url.strip()
            ]
        )


class RelatedPartiesMetadataEditor(BaseMetadataComponentEditor):
    def update_related_parties(self, update_data: list[RelatedPartyMetadataUpdate]):
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            'relatedParty',
            [{
                'ResponsiblePartyInfo': {
                    'role': {
                        '@%s:href' % NamespacePrefix.XLINK: ud.role,
                    },
                    'party': [{
                        '@%s:href' % NamespacePrefix.XLINK: p,
                    } for p in ud.parties],
                }
            } for ud in update_data if not _is_metadata_component_empty(asdict(ud))]
        )


class ShortNameMetadataEditor(BaseMetadataComponentEditor):
    def update_short_name(self, short_name):
        self.metadata_dict['shortName'] = short_name


class SourcePropertyTypeEditor(
    BaseMetadataComponentEditor,
    XlinkHrefMetadataEditor):
    def _update_sources(self, parent_element: dict, sources: list[SourceMetadataUpdate]):
        sources_key = 'source'
        parent_element[sources_key] = []
        source_elements = parent_element[sources_key]
        valid_sources = []
        for s in sources:
            service_functions, linkage, name, \
            protocol, description, data_formats = attrgetter(
                'service_functions',
                'linkage',
                'name',
                'protocol',
                'description',
                'data_formats')(s)
            is_any_required_property_empty = (
                not linkage
                or not name
                or not protocol
            )
            if is_any_required_property_empty:
                continue
            valid_sources.append(s)
            online_resource = {}
            self.update_child_element_and_remove_if_empty(
                online_resource,
                'serviceFunction',
                [
                    self.get_as_xlink_href(service_function)
                    for service_function in service_functions
                    if service_function.strip()
                ]
            )
            self.update_child_element_and_remove_if_empty(
                online_resource,
                'linkage',
                {
                    '%s:URL' % NamespacePrefix.GMD: linkage,
                }
            )
            self.update_child_element_and_remove_if_empty(
                online_resource,
                'name',
                name
            )
            self.update_child_element_and_remove_if_empty(
                online_resource,
                'protocol',
                protocol
            )
            self.update_child_element_and_remove_if_empty(
                online_resource,
                'description',
                description
            )
            self.update_child_element_and_remove_if_empty(
                online_resource,
                'dataFormat',
                [
                    self.get_as_xlink_href(data_format)
                    for data_format in data_formats
                    if data_format.strip()
                ]
            )
            source_elements.append({
                'OnlineResource': online_resource
            })
        self.remove_child_element_if_empty(
            parent_element,
            sources_key
        )
        return valid_sources


class StatusMetadataEditor(BaseMetadataComponentEditor):
    def update_status(self, status_ontology_url):
        status_key = 'status'
        self.metadata_dict[status_key] = {'@%s:href' % NamespacePrefix.XLINK: status_ontology_url}
        self.remove_child_element_if_empty(
            self.metadata_dict,
            status_key
        )


class TimePeriodMetadataEditor(BaseMetadataComponentEditor):
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

    def update_time_period(self, update_data: TimePeriodMetadataUpdate, time_period_container_element_key: str):
        # Time period container element
        self.metadata_dict.setdefault(time_period_container_element_key, {})
        time_period_container_element = self.metadata_dict[time_period_container_element_key]
        # gml:TimePeriod container element
        time_period_key = '%s:TimePeriod' % NamespacePrefix.GML
        time_period_container_element.setdefault(time_period_key, {})
        time_period = self.metadata_dict[time_period_container_element_key][time_period_key]
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
            time_period_container_element.pop(time_period_key)


class TypeMetadataEditor(BaseMetadataComponentEditor):
    def update_type(self, type_ontology_url):
        type_key = 'type'
        self.metadata_dict[type_key] = {'@%s:href' % NamespacePrefix.XLINK: type_ontology_url}
        self.remove_child_element_if_empty(
            self.metadata_dict,
            type_key
        )


class TypeMultipleMetadataEditor(
    BaseMetadataComponentEditor,
    XlinkHrefMetadataEditor):
    def update_types(self, type_ontology_urls):
        types_key = 'type'
        self.update_child_element_and_remove_if_empty(
            self.metadata_dict,
            types_key,
            [
                self.get_as_xlink_href(url)
                for url in type_ontology_urls if url.strip()
            ]
        )


class URLMetadataEditor(BaseMetadataComponentEditor):
    def update_url(self, url):
        url_key = 'URL'
        self.metadata_dict.setdefault(url_key, [])
        urls = self.metadata_dict[url_key]
        if len(urls) == 0:
            urls.append({})
        gmd_url_key = '%s:URL' % NamespacePrefix.GMD
        self.update_list_element_and_pop_if_empty(
            urls,
            0,
            {gmd_url_key: url}
        )
        self.remove_child_element_if_empty(
            self.metadata_dict,
            url_key
        )