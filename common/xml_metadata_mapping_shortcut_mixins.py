import logging
from lxml import etree

from .constants import (
    PITHIA_METADATA_SERVER_HTTPS_URL_BASE,
    PITHIA_METADATA_SERVER_URL_BASE,
    SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE,
)
from .xml_metadata_utils import (
    Namespace,
    NamespacePrefix,
)


logger = logging.getLogger(__name__)


class BaseMetadataPropertiesShortcutMixin:
    PITHIA_NSPREFIX_XPATH = 'pithia'

    def __init__(self, xml) -> None:
        self.xml_parsed = etree.fromstring(xml.encode('utf-8'))
        self.namespaces = {
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.MRL: Namespace.MRL,
            NamespacePrefix.OM: Namespace.OM,
            self.PITHIA_NSPREFIX_XPATH: Namespace.PITHIA,
            NamespacePrefix.XLINK: Namespace.XLINK,
            NamespacePrefix.XSI: Namespace.XSI,
        }

    def _get_elements_with_xpath_query(self, xpath_query: str, parent_element=None):
        if not parent_element:
            parent_element = self.xml_parsed
        return parent_element.xpath(xpath_query, namespaces=self.namespaces)

    def _get_element_value_or_blank_string(self, element):
        try:
            return element.text
        except AttributeError as err:
            # Remove logging as errors are expected here
            # if element does not have text.
            # logger.exception(err)
            return element
        except Exception as err:
            logger.exception(err)
            return ''

    def _get_first_element_from_list(self, element_list: list):
        return next(iter(element_list), '')

    def _get_first_element_value_or_blank_string_with_xpath_query(self, xpath_query: str, parent_element=None):
        element_list = self._get_elements_with_xpath_query(xpath_query, parent_element=parent_element)
        if not len(element_list):
            return ''

        first_element = self._get_first_element_from_list(element_list)
        return self._get_element_value_or_blank_string(first_element)


class PithiaCoreMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def localid(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:localID' % self.PITHIA_NSPREFIX_XPATH)

    @property
    def namespace(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:namespace' % self.PITHIA_NSPREFIX_XPATH)
    
    @property
    def name(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:name' % self.PITHIA_NSPREFIX_XPATH)
    
    @property
    def version(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:version' % self.PITHIA_NSPREFIX_XPATH)


class PithiaDescriptionMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def description(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:description' % self.PITHIA_NSPREFIX_XPATH)


class PithiaOntologyUrlsMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def ontology_urls(self):
        return self._get_elements_with_xpath_query(".//*[contains(@%s:href, '%s')]/@%s:href | .//*[contains(@srsName, '%s')]/@srsName" % (NamespacePrefix.XLINK, SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE, NamespacePrefix.XLINK, SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE))


class PithiaQualityAssessmentMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def data_quality_flags(self):
        return self._get_elements_with_xpath_query('.//%s:dataQualityFlag/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))
        
    @property
    def metadata_quality_flags(self):
        return self._get_elements_with_xpath_query('.//%s:metadataQualityFlag/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))

    @property
    def science_relevance_indicators(self):
        return self._get_elements_with_xpath_query('.//%s:scienceRelevanceIndicator/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK))


class PithiaShortNameMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def short_name(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:shortName' % self.PITHIA_NSPREFIX_XPATH)


class PithiaRelatedPartiesMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    def _get_related_parties_from_metadata(self):
        related_party_elements = self._get_elements_with_xpath_query('.//%s:ResponsiblePartyInfo' % self.PITHIA_NSPREFIX_XPATH)
        related_parties_by_role = {}
        for rp in related_party_elements:
            role = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:role/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=rp)
            if not role:
                continue
            parties = self._get_elements_with_xpath_query('.//%s:party/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=rp)
            if not parties:
                continue
            if role not in related_parties_by_role:
                related_parties_by_role[role] = []
            related_parties_by_role[role] = related_parties_by_role[role] + parties
        return [{
            'role': role,
            'parties': parties,
        } for role, parties in related_parties_by_role.items()]

    @property
    def related_parties(self):
        return self._get_related_parties_from_metadata()


class PithiaResourceUrlsMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    def _get_resource_urls_with_type(self, type):
        return list(set(self._get_elements_with_xpath_query(".//*[contains(@%s:href, '%s/%s/')]/@%s:href" % (NamespacePrefix.XLINK, PITHIA_METADATA_SERVER_HTTPS_URL_BASE, type, NamespacePrefix.XLINK))))

    @property
    def resource_urls(self):
        return list(set(self._get_elements_with_xpath_query(".//*[contains(@%s:href, '%s')]/@%s:href" % (NamespacePrefix.XLINK, PITHIA_METADATA_SERVER_URL_BASE, NamespacePrefix.XLINK))))

    @property
    def organisation_urls(self):
        return self._get_resource_urls_with_type('organisation')

    @property
    def individual_urls(self):
        return self._get_resource_urls_with_type('individual')

    @property
    def project_urls(self):
        return self._get_resource_urls_with_type('project')

    @property
    def platform_urls(self):
        return self._get_resource_urls_with_type('platform')

    @property
    def operation_urls(self):
        return self._get_resource_urls_with_type('operation')

    @property
    def instrument_urls(self):
        return self._get_resource_urls_with_type('instrument')

    @property
    def acquisition_capabilities_urls(self):
        return self._get_resource_urls_with_type('acquisitionCapabilities')

    @property
    def acquisition_urls(self):
        return self._get_resource_urls_with_type('acquisition')

    @property
    def computation_capabilities_urls(self):
        return self._get_resource_urls_with_type('computationCapabilities')

    @property
    def computation_urls(self):
        return self._get_resource_urls_with_type('computation')

    @property
    def process_urls(self):
        return self._get_resource_urls_with_type('process')

    @property
    def data_collection_urls(self):
        return self._get_resource_urls_with_type('collection')

    @property
    def catalogue_urls(self):
        return self._get_elements_with_xpath_query('.//%s:catalogueIdentifier/@xlink:href' % self.PITHIA_NSPREFIX_XPATH)

    @property
    def catalogue_entry_urls(self):
        return self._get_elements_with_xpath_query('.//%s:entryIdentifier/@xlink:href' % self.PITHIA_NSPREFIX_XPATH)


class PithiaStandardIdentifiersMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    def _get_standard_identifiers_from_parent_element(self, parent_element):
        standard_identifier_elements = self._get_elements_with_xpath_query('.//%s:standardIdentifier' % self.PITHIA_NSPREFIX_XPATH, parent_element=parent_element)
        standard_identifiers = []
        for e in standard_identifier_elements:
            value = self._get_element_value_or_blank_string(e)
            standard_identifiers.append({
                'authority': e.get('authority', ''),
                'value': value,
            })
        return standard_identifiers

    @property
    def standard_identifiers(self):
        return self._get_standard_identifiers_from_parent_element(self.xml_parsed)


class PithiaCapabilityLinksMetadataPropertiesMixin(PithiaStandardIdentifiersMetadataPropertiesMixin):
    def _get_time_spans_from_capability_link_element(self, parent_element):
        time_span_elements = self._get_elements_with_xpath_query('.//%s:timeSpan' % self.PITHIA_NSPREFIX_XPATH, parent_element=parent_element)
        time_spans = []
        for time_span_elem in time_span_elements:
            begin_positions = self._get_elements_with_xpath_query('.//%s:beginPosition' % NamespacePrefix.GML, parent_element=time_span_elem)
            begin_position = self._get_element_value_or_blank_string(self._get_first_element_from_list(begin_positions))
            end_positions = self._get_elements_with_xpath_query('.//%s:endPosition/@indeterminatePosition' % NamespacePrefix.GML, parent_element=time_span_elem)
            end_position = self._get_first_element_from_list(end_positions)
            time_spans.append({
                'begin_position': begin_position,
                'end_position': end_position,
            })
        return time_spans

    def _get_capability_links_from_metadata(self):
        capability_link_elements = self._get_elements_with_xpath_query('.//%s:capabilityLink' % self.PITHIA_NSPREFIX_XPATH)
        capability_links = []
        for cap_link_elem in capability_link_elements:
            platforms = self._get_elements_with_xpath_query('.//%s:platform/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=cap_link_elem)
            capabilities = self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:%s/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, self.capabilities_element_key_xml, NamespacePrefix.XLINK), parent_element=cap_link_elem)
            standard_identifiers = self._get_standard_identifiers_from_parent_element(cap_link_elem)
            time_spans = self._get_time_spans_from_capability_link_element(cap_link_elem)
            capability_links.append({
                'platforms': platforms,
                self.capabilities_element_key: capabilities,
                'standard_identifiers': standard_identifiers,
                'time_spans': time_spans,
            })
        return capability_links
    
    @property
    def capability_links(self):
        return self._get_capability_links_from_metadata()


class PithiaCapabilitiesMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    def _get_capabilities_from_metadata(self):
        process_capability_elements = self._get_elements_with_xpath_query('.//%s:capabilities/%s:processCapability' % (self.PITHIA_NSPREFIX_XPATH, self.PITHIA_NSPREFIX_XPATH))
        process_capabilities = []
        for e in process_capability_elements:
            name_elements = self._get_elements_with_xpath_query('.//%s:name' % self.PITHIA_NSPREFIX_XPATH, parent_element=e)
            name = ''
            try:
                name = self._get_element_value_or_blank_string(self._get_first_element_from_list(name_elements))
            except AttributeError:
                pass
            observed_property_elements = self._get_elements_with_xpath_query('.//%s:observedProperty/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            observed_property = self._get_first_element_from_list(observed_property_elements)
            dimensionality_instance_elements = self._get_elements_with_xpath_query('.//%s:dimensionalityInstance/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            dimensionality_instance = self._get_first_element_from_list(dimensionality_instance_elements)
            dimensionality_timeline_elements = self._get_elements_with_xpath_query('.//%s:dimensionalityTimeline/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            dimensionality_timeline = self._get_first_element_from_list(dimensionality_timeline_elements)
            cadence_elements = self._get_elements_with_xpath_query('.//%s:cadence' % self.PITHIA_NSPREFIX_XPATH, parent_element=e)
            cadence = ''
            try:
                cadence = self._get_element_value_or_blank_string(self._get_first_element_from_list(cadence_elements))
                cadence = float(cadence)
                if float.is_integer(cadence):
                    cadence = int(cadence)
                cadence = str(cadence)
            except AttributeError:
                pass
            except ValueError:
                pass
            cadence_unit_attributes = self._get_elements_with_xpath_query('.//%s:cadence/@unit' % self.PITHIA_NSPREFIX_XPATH, parent_element=e)
            cadence_unit = self._get_first_element_from_list(cadence_unit_attributes)
            vector_representations = self._get_elements_with_xpath_query('.//%s:vectorRepresentation/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            coordinate_system_elements = self._get_elements_with_xpath_query('.//%s:coordinateSystem/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            coordinate_system = self._get_first_element_from_list(coordinate_system_elements)
            units_elements = self._get_elements_with_xpath_query('.//%s:units/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            units = self._get_first_element_from_list(units_elements)
            qualifiers = self._get_elements_with_xpath_query('.//%s:qualifier/@%s:href' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.XLINK), parent_element=e)
            process_capabilities.append({
                'name': name,
                'observed_property': observed_property,
                'dimensionality_instance': dimensionality_instance,
                'dimensionality_timeline': dimensionality_timeline,
                'cadence': cadence,
                'cadence_units': cadence_unit,
                'vector_representations': vector_representations,
                'coordinate_system': coordinate_system,
                'units': units,
                'qualifiers': qualifiers,
            })
        return process_capabilities

    @property
    def capabilities(self):
        return self._get_capabilities_from_metadata()


class GmdContactInfoMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def phone(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:voice/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def delivery_point(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:deliveryPoint/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def city(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:city/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def administrative_area(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:administrativeArea/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def postal_code(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:postalCode/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def country(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:country/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def email_address(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:electronicMailAddress/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def online_resource(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:linkage/%s:URL' % (NamespacePrefix.GMD, NamespacePrefix.GMD))

    @property
    def contact_instructions(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:contactInstructions/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def hours_of_service(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:hoursOfService/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO))

    @property
    def address(self):
        unformatted_address_dict = {
            'delivery_point': self.delivery_point,
            'city': self.city,
            'administrative_area': self.administrative_area,
            'postal_code': self.postal_code,
            'country': self.country,
        }
        return {
            key: value
        for key, value in unformatted_address_dict.items() if value and value.strip()}

    @property
    def non_address_contact_info(self):
        unformatted_non_address_contact_info = {
            'phone': self.phone,
            'email_address': self.email_address,
            'online_resource': self.online_resource,
            'contact_instructions': self.contact_instructions,
            'hours_of_service': self.hours_of_service,
        }
        formatted_non_address_contact_info = {
            key: value
            for key, value in unformatted_non_address_contact_info.items()
            if value and value.strip()
        }
        return formatted_non_address_contact_info

    @property
    def contact_info(self):
        contact_info = {}
        contact_info.update(self.address)
        contact_info.update(self.non_address_contact_info)
        return contact_info


class GmdUrlMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def gmd_url(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:URL/%s:URL' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.GMD))