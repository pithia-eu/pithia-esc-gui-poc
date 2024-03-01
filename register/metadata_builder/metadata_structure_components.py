from datetime import datetime
from lxml import etree


class NamespacePrefix:
    GCO = 'gco'
    GMD = 'gmd'
    GML = 'gml'
    OM = 'om'
    PITHIA = None
    XLINK = 'xlink'

class Namespace:
    GCO = 'http://www.isotc211.org/2005/gco'
    GMD = 'http://www.isotc211.org/2005/gmd'
    GML = 'http://www.opengis.net/gml/3.2'
    OM = 'http://www.opengis.net/om/2.0'
    PITHIA = 'https://metadata.pithia.eu/schemas/2.2'
    XLINK = 'http://www.w3.org/1999/xlink'


class BaseMetadataComponent:
    def __init__(self, root_tag, nsmap_extensions={}) -> None:
        self.root = etree.Element(root_tag, nsmap={
            NamespacePrefix.PITHIA: Namespace.PITHIA,
            **nsmap_extensions,
        })

    def append_identifier(self, localid, namespace, version='1', creation_date=datetime.now().isoformat(), last_modification_date=datetime.now().isoformat()):
        # Container elements
        identifier = etree.SubElement(self.root, 'identifier')
        pithia_identifier = etree.SubElement(identifier, 'PITHIA_Identifier')

        # Local ID
        localid_element = etree.SubElement(pithia_identifier, 'localID')
        localid_element.text = localid

        # Namespace
        namespace_element = etree.SubElement(pithia_identifier, 'namespace')
        namespace_element.text = namespace

        # Version
        version_element = etree.SubElement(pithia_identifier, 'version')
        version_element.text = version

        # Creation and last modification date
        creation_date_element = etree.SubElement(pithia_identifier, 'creationDate')
        creation_date_element.text = creation_date
        last_modification_date_element = etree.SubElement(pithia_identifier, 'lastModificationDate')
        last_modification_date_element.text = last_modification_date

    @property
    def xml(self) -> str:
        return etree.tostring(self.root, pretty_print=True).decode()


class NameMetadataComponent(BaseMetadataComponent):
    def append_name(self, name):
        name_element = etree.SubElement(self.root, 'name')
        name_element.text = name


class DescriptionMetadataComponent(BaseMetadataComponent):
    def append_description(self, description):
        description_element = etree.SubElement(self.root, 'description')
        description_element.text = description
    

class CapabilitiesMetadataComponent(BaseMetadataComponent):
    def append_capabilities(self, capabilities):
        # Container element
        capabilities_element = etree.SubElement(self.root, 'capabilities')
        for pc in capabilities:
            # Container element
            process_capability_element = etree.SubElement(capabilities_element, 'processCapability')
            name_element = etree.SubElement(process_capability_element, 'name')
            name_element.text = pc['name']
            observed_property_element_attributes = {
                '{%s}href' % Namespace.XLINK: pc['observed_property']
            }
            observed_property_element = etree.SubElement(process_capability_element, 'observedProperty', **observed_property_element_attributes)
            dimensionality_instance_element_attributes = {
                '{%s}href' % Namespace.XLINK: pc['dimensionality_instance']
            }
            dimensionality_instance_element = etree.SubElement(process_capability_element, 'dimensionalityInstance', **dimensionality_instance_element_attributes)
            dimensionality_timeline_element_attributes = {
                '{%s}href' % Namespace.XLINK: pc['dimensionality_timeline']
            }
            dimensionality_timeline_element = etree.SubElement(process_capability_element, 'dimensionalityTimeline', **dimensionality_timeline_element_attributes)
            units_element_attributes = {
                '{%s}href' % Namespace.XLINK: pc['units']
            }
            units_element = etree.SubElement(process_capability_element, 'units', **units_element_attributes)


class CapabilityLinksMetadataComponent(BaseMetadataComponent):
    capabilities_key = ''
    capabilities_element_name = ''

    def append_capability_links(self, capability_link_dict_list):
        capability_links_element = etree.SubElement(self.root, 'capabilityLinks')
        for cld in capability_link_dict_list:
            capability_link_element = etree.SubElement(capability_links_element, 'capabilityLink')
            platform_element_attributes = {
                '{%s}href' % Namespace.XLINK: cld['platform']
            }
            platform_element = etree.SubElement(capability_link_element, 'platform', **platform_element_attributes)
            standard_identifier_element_attributes = {
                'authority': cld['standard_identifier']['authority'],
            }
            standard_identifier_element = etree.SubElement(capability_link_element, 'standardIdentifier', **standard_identifier_element_attributes)
            standard_identifier_element.text = cld['standard_identifier']['value']
            capabilities_element_attributes = {
                '{%s}href' % Namespace.XLINK: cld[self.capabilities_key],
            }
            capabilities_element = etree.SubElement(capability_link_element, self.capabilities_element_name, **capabilities_element_attributes)


class ContactInfoMetadataComponent(BaseMetadataComponent):
    def _append_contact_info_address(self, ci_contact_element, delivery_point, city, administrative_area, postal_code, country, eletronic_mail_address):
        # Address container element
        address_element = etree.SubElement(ci_contact_element, 'address')
        ci_address_element = etree.SubElement(address_element, 'CI_Address')
        
        # Delivery point
        delivery_point_element = etree.SubElement(ci_address_element, 'deliveryPoint')
        self._append_gco_character_string_sub_element(delivery_point_element, delivery_point)
        
        # City
        city_element = etree.SubElement(ci_address_element, 'city')
        self._append_gco_character_string_sub_element(city_element, city)
        
        # Administrative area
        administrative_area_element = etree.SubElement(ci_address_element, 'administrativeArea')
        self._append_gco_character_string_sub_element(administrative_area_element, administrative_area)
        
        # Postal code
        postal_code_element = etree.SubElement(ci_address_element, 'postalCode')
        self._append_gco_character_string_sub_element(postal_code_element, postal_code)
        
        # Country
        country_element = etree.SubElement(ci_address_element, 'country')
        self._append_gco_character_string_sub_element(country_element, country)
        
        # Email
        electronic_mail_address_element = etree.SubElement(ci_address_element, 'electronicMailAddress')
        self._append_gco_character_string_sub_element(electronic_mail_address_element, eletronic_mail_address)

    def _append_contact_info_online_resource(self, ci_contact_element, url):
        online_resource_element = etree.SubElement(ci_contact_element, 'onlineResource')
        ci_online_resource_element = etree.SubElement(online_resource_element, 'CI_OnlineResource')
        linkage_element = etree.SubElement(ci_online_resource_element, 'linkage')
        url_element = etree.SubElement(linkage_element, 'URL')
        url_element.text = url

    def _append_contact_info_hours_of_service(self, ci_contact_element, hours_of_service):
        hours_of_service_element = etree.SubElement(ci_contact_element, 'hoursOfService')
        self._append_gco_character_string_sub_element(hours_of_service_element, hours_of_service)

    def _append_contact_info_contact_instructions(self, ci_contact_element, contact_instructions):
        contact_instructions_element = etree.SubElement(ci_contact_element, 'contactInstructions')
        self._append_gco_character_string_sub_element(contact_instructions_element, contact_instructions)

    def append_contact_info(self, contact_info):
        # Container elements
        contact_info_element = etree.SubElement(self.root, 'contactInfo')
        ci_contact_element = etree.SubElement(contact_info_element, 'CI_Contact', xmlns='http://www.isotc211.org/2005/gmd')

        # Phone
        phone_element = etree.SubElement(ci_contact_element, 'phone')
        ci_telephone_element = etree.SubElement(phone_element, 'CI_Telephone')
        voice_element = etree.SubElement(ci_telephone_element, 'voice')
        self._append_gco_character_string_sub_element(voice_element, contact_info['phone'])
        
        # Address
        self._append_contact_info_address(ci_contact_element, *contact_info['address'])

        # Online resource
        self._append_contact_info_online_resource(ci_contact_element, contact_info['online_resource'])

        # Hours of service
        self._append_contact_info_hours_of_service(ci_contact_element, contact_info['hours_of_service'])

        # Contact instructions
        self._append_contact_info_contact_instructions(ci_contact_element, contact_info['contact_instructions'])


class DataLevelMetadataComponent(BaseMetadataComponent):
    def append_data_levels(self, data_levels):
        for dl in data_levels:
            data_level_element_attributes = {
                '{%s}href' % Namespace.XLINK: dl,
            }
            etree.SubElement(self.root, 'dataLevel', **data_level_element_attributes)


class GCOCharacterStringMetadataComponent(BaseMetadataComponent):
    def _append_gco_character_string_sub_element(self, parent_element, text):
        gco_character_string_element = etree.SubElement(parent_element, '{http://www.isotc211.org/2005/gco}CharacterString')
        gco_character_string_element.text = text


class GMLTimePeriodMetadataComponent(BaseMetadataComponent):
    def _append_time_instant_element(self, parent_element, time_instant_id, time_position):
        time_instant_element_attributes = {
            '{%s}id' % Namespace.GML: time_instant_id
        }
        time_instant_element = etree.SubElement(parent_element, '{%s}TimeInstant' % Namespace.GML, **time_instant_element_attributes)
        time_position_element = etree.SubElement(time_instant_element, '{%s}TimePosition' % Namespace.GML)
        time_position_element.text = time_position

    def append_gml_time_period(self, parent_element, time_period_dict):
        # Time period wrapper element
        gml_time_period_element_attributes = {
            '{%s}id' % Namespace.GML: time_period_dict['id'],
        }
        gml_time_period_element = etree.SubElement(parent_element, '{%s}TimePeriod' % Namespace.GML, **gml_time_period_element_attributes)

        # Time period begin
        gml_begin_element = etree.SubElement(gml_time_period_element, '{%s}begin' % Namespace.GML)
        self._append_time_instant_element(gml_begin_element, time_period_dict['begin']['time_instant']['id'], time_period_dict['begin']['time_instant']['time_position'])

        # Time period end
        gml_end_element = etree.SubElement(gml_time_period_element, '{%s}end' % Namespace.GML)
        self._append_time_instant_element(gml_end_element, time_period_dict['begin']['time_instant']['id'], time_period_dict['begin']['time_instant']['time_position'])


class QualityAssessmentMetadataComponent(BaseMetadataComponent):
    def append_quality_assessment(self, quality_assessment_dict):
        quality_assessment_element = etree.SubElement(self.root, 'qualityAssessment')
        for dqf in quality_assessment_dict['data_quality_flags']:
            data_quality_flag_element_attributes = {
                '{%s}href' % Namespace.XLINK: dqf,
            }
            data_quality_flag_element = etree.SubElement(quality_assessment_element, 'dataQualityFlag', **data_quality_flag_element_attributes)
        for mqf in quality_assessment_dict.get('metadata_quality_flags', []):
            metadata_quality_flag_element_attributes = {
                '{%s}href' % Namespace.XLINK: mqf,
            }
            metadata_quality_flag_element = etree.SubElement(quality_assessment_element, 'metadataQualityFlag', **metadata_quality_flag_element_attributes)


class RelatedPartyMetadataComponent(BaseMetadataComponent):
    def append_related_parties(self, related_parties):
        for rp in related_parties:
            related_party_element = etree.SubElement(self.root, 'relatedParty')
            responsible_party_info_element = etree.SubElement(related_party_element, 'ResponsiblePartyInfo')
            role_element_attributes = {
                '{%s}href' % Namespace.XLINK: rp['role']
            }
            role_element = etree.SubElement(responsible_party_info_element, 'role', **role_element_attributes)
            party_element_attributes = {
                '{%s}href' % Namespace.XLINK: rp['party']
            }
            party_element = etree.SubElement(responsible_party_info_element, 'party', **party_element_attributes)


class ShortNameMetadataComponent(BaseMetadataComponent):
    def append_short_name(self, short_name):
        short_name_element = etree.SubElement(self.root, 'shortName')
        short_name_element.text = short_name


class SourceMetadataComponent(BaseMetadataComponent):
    def append_sources(self, parent_element, sources):
        for s in sources:
            # Container elements
            source_element = etree.SubElement(parent_element, 'source')
            online_resource_element = etree.SubElement(source_element, 'OnlineResource')

            # Online resource element properties
            service_function_element_attributes = {
                '{%s}href' % Namespace.XLINK: s['service_function']
            }
            service_function_element = etree.SubElement(online_resource_element, 'serviceFunction', **service_function_element_attributes)
            linkage_element = etree.SubElement(online_resource_element, 'linkage')
            linkage_gmd_url_element = etree.SubElement(linkage_element, '{%s}URL' % Namespace.GMD)
            linkage_gmd_url_element.text = s['linkage']
            name_element = etree.SubElement(online_resource_element, 'name')
            name_element.text = s['name']
            protocol_element = etree.SubElement(online_resource_element, 'protocol')
            protocol_element.text = s['protocol']
            description_element = etree.SubElement(online_resource_element, 'description')
            description_element.text = s['description']
            data_format_element_attributes = {
                '{%s}href' % Namespace.XLINK: s['data_format']
            }
            data_format_element = etree.SubElement(online_resource_element, 'dataFormat', **data_format_element_attributes)


class StatusMetadataComponent(BaseMetadataComponent):
    def append_status(self, status):
        status_element_attributes = {
            '{%s}href' % Namespace.XLINK: status
        }
        status_element = etree.SubElement(self.root, 'status', **status_element_attributes)


class TypeMetadataComponent(BaseMetadataComponent):
    def append_type(self, type):
        type_element_attributes = {
            '{%s}href' % Namespace.XLINK: type,
        }
        type_element = etree.SubElement(self.root, 'type', **type_element_attributes)