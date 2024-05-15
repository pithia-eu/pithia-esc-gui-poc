from datetime import datetime
from datetime import timezone
from lxml import etree

from utils.dict_helpers import flatten


class NamespacePrefix:
    GCO = 'gco'
    GCO19115 = 'gco'
    GMD = 'gmd'
    GML = 'gml'
    MRL = 'mrl'
    OM = 'om'
    PITHIA = None
    XLINK = 'xlink'
    XSI = 'xsi'

class Namespace:
    GCO = 'http://www.isotc211.org/2005/gco'
    GCO19115 = 'http://standards.iso.org/iso/19115/-3/gco/1.0'
    GMD = 'http://www.isotc211.org/2005/gmd'
    GML = 'http://www.opengis.net/gml/3.2'
    MRL = 'http://standards.iso.org/iso/19115/-3/mrl/1.0'
    OM = 'http://www.opengis.net/om/2.0'
    PITHIA = 'https://metadata.pithia.eu/schemas/2.2'
    XLINK = 'http://www.w3.org/1999/xlink'
    XSI = 'http://www.w3.org/2001/XMLSchema-instance'


class BaseMetadataComponent:
    def __init__(self, root_tag, nsmap_extensions={}) -> None:
        root_element_attributes = {
            '{%s}schemaLocation' % Namespace.XSI: 'https://metadata.pithia.eu/schemas/2.2 https://metadata.pithia.eu/schemas/2.2/pithia.xsd'
        }
        self.root = etree.Element(
            root_tag, 
            **root_element_attributes,
            nsmap={
                NamespacePrefix.PITHIA: Namespace.PITHIA,
                NamespacePrefix.XSI: Namespace.XSI,
                **nsmap_extensions,
            }
        )

    @property
    def xml(self) -> str:
        etree.indent(self.root, space="    ")
        return etree.tostring(self.root, pretty_print=True).decode()


class IdentifierMetadataComponent(BaseMetadataComponent):
    def append_identifier(self, localid, namespace, version='1', creation_date=datetime.now(timezone.utc).replace(second=0, microsecond=0).isoformat().replace('+00:00', 'Z'), last_modification_date=datetime.now(timezone.utc).replace(second=0, microsecond=0).isoformat().replace('+00:00', 'Z')):
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


class LocationMetadataComponent(BaseMetadataComponent):
    def append_location(self, location_dict):
        if (not any([
            location_dict.get('name_location').get('code'),
            location_dict.get('geometry_location').get('point').get('id'),
            location_dict.get('geometry_location').get('point').get('srs_name'),
            location_dict.get('geometry_location').get('point').get('pos'),
        ])):
            return
        location_wrapper_element = etree.SubElement(self.root, 'location')
        location_element = etree.SubElement(location_wrapper_element, 'Location')
        
        # Geometry location
        if (any([
            location_dict.get('geometry_location').get('point').get('id'),
            location_dict.get('geometry_location').get('point').get('srs_name'),
            location_dict.get('geometry_location').get('point').get('pos'),
        ])):
            geometry_location_element = etree.SubElement(location_element, 'geometryLocation')
            gml_point_element_attributes = {
                '{%s}id' % Namespace.GML: location_dict['geometry_location']['point']['id'],
                'srsName': location_dict['geometry_location']['point']['srs_name'],
            }
            gml_point_element = etree.SubElement(geometry_location_element, '{%s}Point' % Namespace.GML, **gml_point_element_attributes)
            gml_pos_element = etree.SubElement(gml_point_element, '{%s}pos' % Namespace.GML)
            gml_pos_element.text = location_dict['geometry_location']['point']['pos']

        # Name location
        if (any([
            location_dict.get('name_location').get('code'),
        ])):
            name_location_element = etree.SubElement(location_element, 'nameLocation')
            ex_geographic_description_element = etree.SubElement(name_location_element, 'EX_GeographicDescription', xmlns=Namespace.GMD)
            # Geographic identifier
            geographic_identifier_element = etree.SubElement(ex_geographic_description_element, 'geographicIdentifier')
            # MD identifier
            md_identifier_element = etree.SubElement(geographic_identifier_element, 'MD_Identifier')
            # Code
            code_element = etree.SubElement(md_identifier_element, 'code')
            self._append_gco_character_string_sub_element(code_element, location_dict['name_location']['code'])


class NameMetadataComponent(BaseMetadataComponent):
    def append_name(self, name):
        name_element = etree.SubElement(self.root, 'name')
        name_element.text = name


class DescriptionMetadataComponent(BaseMetadataComponent):
    def append_description(self, description=''):
        description_element = etree.SubElement(self.root, 'description')
        description_element.text = description
    

class CapabilitiesMetadataComponent(BaseMetadataComponent):
    def append_capabilities(self, capabilities):
        if not capabilities:
            return
        # Container element
        capabilities_element = etree.SubElement(self.root, 'capabilities')
        for pc in capabilities:
            # Container element
            process_capability_element = etree.SubElement(capabilities_element, 'processCapability')
            
            # Name
            name_element = etree.SubElement(process_capability_element, 'name')
            name_element.text = pc['name']
            # Observed property
            observed_property_element_attributes = {
                '{%s}href' % Namespace.XLINK: pc['observed_property']
            }
            observed_property_element = etree.SubElement(process_capability_element, 'observedProperty', **observed_property_element_attributes)
            # Dimensionality instance
            if pc['dimensionality_instance']:
                dimensionality_instance_element_attributes = {
                    '{%s}href' % Namespace.XLINK: pc['dimensionality_instance']
                }
                dimensionality_instance_element = etree.SubElement(process_capability_element, 'dimensionalityInstance', **dimensionality_instance_element_attributes)
            # Dimensionality timeline
            if pc['dimensionality_timeline']:
                dimensionality_timeline_element_attributes = {
                    '{%s}href' % Namespace.XLINK: pc['dimensionality_timeline']
                }
                dimensionality_timeline_element = etree.SubElement(process_capability_element, 'dimensionalityTimeline', **dimensionality_timeline_element_attributes)
            # Cadence
            if pc['cadence']:
                cadence_element_attributes = {'unit': pc['cadence_units']}
                cadence_element = etree.SubElement(process_capability_element, 'cadence', **cadence_element_attributes)
                cadence_element.text = pc['cadence']
            # Vector representation
            if pc['vector_representation']:
                for component in pc['vector_representation']:
                    vector_representation_element_attributes = {
                        '{%s}href' % Namespace.XLINK: component,
                    }
                    vector_representation_element = etree.SubElement(process_capability_element, 'vectorRepresentation', **vector_representation_element_attributes)
            # Coordinate system
            if pc['coordinate_system']:
                coordinate_system_element_attributes = {
                    '{%s}href' % Namespace.XLINK: pc['coordinate_system']
                }
                coordinate_system_element = etree.SubElement(process_capability_element, 'coordinateSystem', **coordinate_system_element_attributes)
            # Units
            if pc['units']:
                units_element_attributes = {
                    '{%s}href' % Namespace.XLINK: pc['units']
                }
                units_element = etree.SubElement(process_capability_element, 'units', **units_element_attributes)
            # Qualifier
            if pc['qualifier']:
                for qualifier in pc['qualifier']:
                    qualifier_element_attributes = {
                        '{%s}href' % Namespace.XLINK: qualifier,
                    }
                    qualifier_element = etree.SubElement(process_capability_element, 'qualifier', **qualifier_element_attributes)


class StandardIdentifierComponent(BaseMetadataComponent):
    def append_standard_identifiers(self, parent_element, standard_identifiers):
        for standard_identifier in standard_identifiers:
            if (not any([
                standard_identifier['authority'],
                standard_identifier['value'],
            ])):
                return
            standard_identifier_element_attributes = {
                'authority': standard_identifier['authority']
            }
            standard_identifier_element = etree.SubElement(parent_element, 'standardIdentifier', **standard_identifier_element_attributes)
            standard_identifier_element.text = standard_identifier['value']


class CapabilityLinksMetadataComponent(StandardIdentifierComponent, BaseMetadataComponent):
    capabilities_key = ''
    capabilities_element_name = ''

    def _append_time_spans_to_capability_link(self, time_spans, capability_link_element):
        for ts in time_spans:
            if ts['end_position'] == '':
                continue
            time_span_element = etree.SubElement(capability_link_element, 'timeSpan')
            begin_position_element = etree.SubElement(time_span_element, '{%s}beginPosition' % Namespace.GML)
            begin_position_element.text = ts['begin_position']
            end_position_element_attributes = {
                'indeterminatePosition': ts['end_position'],
            }
            end_position_element = etree.SubElement(time_span_element, '{%s}endPosition' % Namespace.GML, **end_position_element_attributes)

    def append_capability_links(self, capability_link_dict_list):
        capability_links_element = etree.SubElement(self.root, 'capabilityLinks')
        for cld in capability_link_dict_list:
            capability_link_element = etree.SubElement(capability_links_element, 'capabilityLink')
            for p in cld['platforms']:
                platform_element_attributes = {
                    '{%s}href' % Namespace.XLINK: p,
                }
                platform_element = etree.SubElement(capability_link_element, 'platform', **platform_element_attributes)
            self.append_standard_identifiers(capability_link_element, cld['standard_identifiers'])
            if cld[self.capabilities_key]:
                capabilities_element_attributes = {
                    '{%s}href' % Namespace.XLINK: cld[self.capabilities_key],
                }
                capabilities_element = etree.SubElement(capability_link_element, self.capabilities_element_name, **capabilities_element_attributes)
            self._append_time_spans_to_capability_link(cld['time_spans'], capability_link_element)


class ContactInfoMetadataComponent(BaseMetadataComponent):
    def _append_contact_info_address(self, ci_contact_element, address):
        # Address container element
        address_element = etree.SubElement(ci_contact_element, 'address')
        ci_address_element = etree.SubElement(address_element, 'CI_Address')
        
        # Delivery point
        if len(address['delivery_point']) > 0:
            delivery_point_element = etree.SubElement(ci_address_element, 'deliveryPoint')
            self._append_gco_character_string_sub_element(delivery_point_element, address['delivery_point'])
        
        # City
        if len(address['city']) > 0:
            city_element = etree.SubElement(ci_address_element, 'city')
            self._append_gco_character_string_sub_element(city_element, address['city'])
        
        # Administrative area
        if len(address['administrative_area']) > 0:
            administrative_area_element = etree.SubElement(ci_address_element, 'administrativeArea')
            self._append_gco_character_string_sub_element(administrative_area_element, address['administrative_area'])
        
        # Postal code
        if len(address['postal_code']) > 0:
            postal_code_element = etree.SubElement(ci_address_element, 'postalCode')
            self._append_gco_character_string_sub_element(postal_code_element, address['postal_code'])
        
        # Country
        if len(address['country']) > 0:
            country_element = etree.SubElement(ci_address_element, 'country')
            self._append_gco_character_string_sub_element(country_element, address['country'])
        
        # Email
        if len(address['electronic_mail_address']) > 0:
            electronic_mail_address_element = etree.SubElement(ci_address_element, 'electronicMailAddress')
            self._append_gco_character_string_sub_element(electronic_mail_address_element, address['electronic_mail_address'])

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
        if not any(flatten(contact_info).values()):
            return

        # Container elements
        contact_info_element = etree.SubElement(self.root, 'contactInfo')
        ci_contact_element = etree.SubElement(contact_info_element, 'CI_Contact', xmlns='http://www.isotc211.org/2005/gmd')

        # Phone
        if len(contact_info['phone']) > 0:
            phone_element = etree.SubElement(ci_contact_element, 'phone')
            ci_telephone_element = etree.SubElement(phone_element, 'CI_Telephone')
            voice_element = etree.SubElement(ci_telephone_element, 'voice')
            self._append_gco_character_string_sub_element(voice_element, contact_info['phone'])
        
        # Address
        if any(contact_info['address'].values()):
            self._append_contact_info_address(ci_contact_element, contact_info['address'])

        # Online resource
        if len(contact_info['online_resource']) > 0:
            self._append_contact_info_online_resource(ci_contact_element, contact_info['online_resource'])

        # Hours of service
        if len(contact_info['hours_of_service']) > 0:
            self._append_contact_info_hours_of_service(ci_contact_element, contact_info['hours_of_service'])

        # Contact instructions
        if len(contact_info['contact_instructions']) > 0:
            self._append_contact_info_contact_instructions(ci_contact_element, contact_info['contact_instructions'])


class DataLevelMetadataComponent(BaseMetadataComponent):
    def append_data_levels(self, data_levels):
        for dl in data_levels:
            data_level_element_attributes = {
                '{%s}href' % Namespace.XLINK: dl,
            }
            etree.SubElement(self.root, 'dataLevel', **data_level_element_attributes)


class DocumentationMetadataComponent(BaseMetadataComponent):
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
        time_position_element = etree.SubElement(time_instant_element, '{%s}timePosition' % Namespace.GML)
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
        self._append_time_instant_element(gml_end_element, time_period_dict['end']['time_instant']['id'], time_period_dict['end']['time_instant']['time_position'])


class QualityAssessmentMetadataComponent(BaseMetadataComponent):
    def append_quality_assessment(self, quality_assessment_dict):
        if not quality_assessment_dict.get('data_quality_flags'):
            return
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
            for party in rp['parties']:
                party_element_attributes = {
                    '{%s}href' % Namespace.XLINK: party
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
        if not status:
            return
        status_element_attributes = {
            '{%s}href' % Namespace.XLINK: status
        }
        status_element = etree.SubElement(self.root, 'status', **status_element_attributes)


class TypeMetadataComponent(BaseMetadataComponent):
    def append_type(self, type):
        if not type:
            return
        type_element_attributes = {
            '{%s}href' % Namespace.XLINK: type,
        }
        type_element = etree.SubElement(self.root, 'type', **type_element_attributes)