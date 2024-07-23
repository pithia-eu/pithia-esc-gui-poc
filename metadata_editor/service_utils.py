import copy
import json
import xmlschema
import xml.etree.ElementTree as ET
from dataclasses import asdict
from operator import attrgetter

from .editor_dataclasses import (
    ContactInfoMetadataUpdate,
    ContactInfoAddressMetadataUpdate,
    LocationMetadataUpdate,
    PithiaIdentifierMetadataUpdate,
)

from validation.services import MetadataFileXSDValidator


class NamespacePrefix:
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


class BaseMetadataEditor(BaseMetadataComponentEditor):
    def __init__(self, root_element_name, xml_string: str = '') -> None:
        super().__init__()
        self.root_element_name = root_element_name
        namespace_class_attrs = [a for a in vars(NamespacePrefix).keys() if not a.startswith('__')]
        self.namespaces = {getattr(NamespacePrefix, a): getattr(Namespace, a) for a in namespace_class_attrs}
        for prefix, uri in self.namespaces.items():
            ET.register_namespace(prefix, uri)
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


class DocumentationMetadataEditor(
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

    def update_documentation(self, update_data):
        # Set up
        # documentation container element
        documentation_key = 'documentation'
        self.metadata_dict.setdefault(documentation_key, [])
        documentation = self.metadata_dict[documentation_key]
        # Create (if needed) and select the first
        # documentation element.
        if len(documentation) == 0:
            documentation.append({})
        documentation_first = documentation[0]
        # Citation container element
        citation_key = 'Citation'
        documentation_first.setdefault(citation_key, {})
        citation = documentation_first[citation_key]
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
            documentation_first,
            citation_key
        )
        self.pop_child_element_if_empty(
            documentation,
            documentation_first,
            0
        )
        self.remove_child_element_if_empty(
            self.metadata_dict,
            documentation_key
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



class RelatedPartiesMetadataEditor(BaseMetadataComponentEditor):
    responsible_party_info_key = 'ResponsiblePartyInfo'

    def _process_related_party_update_data(self, update_data):
        return [{
            self.responsible_party_info_key: {
                'role': {
                    '@%s:href' % NamespacePrefix.XLINK: ud.get('role'),
                },
                'party': [{
                    '@%s:href' % NamespacePrefix.XLINK: p,
                } for p in ud.get('parties')],
            }
        } for ud in update_data if not _is_metadata_component_empty(ud)]

    def _apply_related_party_update_data(self, related_parties: list, update_data: list):
        for counter, rp in enumerate(related_parties):
            rp_responsible_party_info = rp[self.responsible_party_info_key]
            rp_responsible_party_info.update({
                'role': {
                    '@%s:href' % NamespacePrefix.XLINK: update_data[counter].get('role'),
                },
                'party': [{
                    '@%s:href' % NamespacePrefix.XLINK: p,
                } for p in update_data[counter].get('parties')],
            })

    def _add_empty_related_parties(self, related_parties: list, num_additions: int):
        for _ in range(num_additions):
            related_parties.append({self.responsible_party_info_key: {}})

    def _remove_related_parties(self, related_parties: list, indexes_to_remove: list):
        for i in indexes_to_remove:
            related_parties.pop(i)

    def update_related_parties(self, update_data: list, num_additions: int = 0, deleted_index_sequence: list = [], new: bool = False):
        related_party_key = 'relatedParty'
        # Temp - Update to set as default in next
        # iteration.
        self.metadata_dict.setdefault(related_party_key, [])
        # related_parties_copy = copy.deepcopy(self.metadata_dict[related_party_key])
        # if new:
        #     num_additions = len(update_data)
        # self._add_empty_related_parties(related_parties_copy, num_additions)
        # if not new:
        #     self._remove_related_parties(related_parties_copy, deleted_index_sequence)
        # self._apply_related_party_update_data(related_parties_copy, update_data)
        # self.metadata_dict[related_party_key] = [rp for rp in related_parties_copy if not _is_metadata_component_empty(rp)]
        self.metadata_dict[related_party_key] = self._process_related_party_update_data(update_data)
        self.remove_child_element_if_empty(
            self.metadata_dict,
            related_party_key
        )


class ShortNameMetadataEditor(BaseMetadataComponentEditor):
    def update_short_name(self, short_name):
        self.metadata_dict['shortName'] = short_name


class StandardIdentifierMetadataEditor(BaseMetadataComponentEditor):
    def update_standard_identifiers(self, update_data):
        standard_identifiers_key = 'standardIdentifier'
        self.metadata_dict[standard_identifiers_key] = [{
            '@authority': ud.get('authority'),
            '$': ud.get('value'),
        } for ud in update_data if not _is_metadata_component_empty(ud)]
        self.remove_child_element_if_empty(
            self.metadata_dict,
            standard_identifiers_key
        )


class StatusMetadataEditor(BaseMetadataComponentEditor):
    def update_status(self, status_ontology_url):
        status_key = 'status'
        self.metadata_dict[status_key] = {'@%s:href' % NamespacePrefix.XLINK: status_ontology_url}
        self.remove_child_element_if_empty(
            self.metadata_dict,
            status_key
        )


class TypeMetadataEditor(BaseMetadataComponentEditor):
    def update_type(self, type_ontology_url):
        type_key = 'type'
        self.metadata_dict[type_key] = {'@%s:href' % NamespacePrefix.XLINK: type_ontology_url}
        self.remove_child_element_if_empty(
            self.metadata_dict,
            type_key
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