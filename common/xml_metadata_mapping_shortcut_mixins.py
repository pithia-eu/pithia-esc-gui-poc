import logging
from lxml import etree

from .constants import PITHIA_METADATA_SERVER_HTTPS_URL_BASE
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
            logger.exception(err)
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


class PithiaShortNameMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def short_name(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:shortName' % self.PITHIA_NSPREFIX_XPATH)


class PithiaResourceUrlsMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    def _get_resource_urls_with_type(self, type):
        return list(set(self._get_elements_with_xpath_query(f'.//*[contains(@xlink:href, "{PITHIA_METADATA_SERVER_HTTPS_URL_BASE}/{type}/")]/@xlink:href')))

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


class StandardIdentifiersMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
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


class PithiaCapabilityLinkMetadataPropertiesMixin(StandardIdentifiersMetadataPropertiesMixin):
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
    def non_location_contact_info(self):
        unformatted_nl_contact_info_dict = {
            'administrative_area': self.phone,
            'city': self.phone,
            'contact_instructions': self.phone,
            'country': self.phone,
            'delivery_point': self.phone,
            'email_address': self.phone,
            'online_resource': self.phone,
            'phone': self.phone,
            'postal_code': self.phone,
        }
        return {
            key: value
        for key, value in unformatted_nl_contact_info_dict.items() if value}

    @property
    def contact_info(self):
        unformatted_contact_info_dict = {
            'administrative_area': self.phone,
            'city': self.phone,
            'contact_instructions': self.phone,
            'country': self.phone,
            'delivery_point': self.phone,
            'email_address': self.phone,
            'online_resource': self.phone,
            'phone': self.phone,
            'postal_code': self.phone,
        }
        return {
            key: value
        for key, value in unformatted_contact_info_dict.items() if value}

    @property
    def address(self):
        unformatted_address_dict = {
            'administrative_area': self.phone,
            'city': self.phone,
            'country': self.phone,
            'delivery_point': self.phone,
            'postal_code': self.phone,
        }
        return {
            key: value
        for key, value in unformatted_address_dict.items() if value}


class GmdUrlMetadataPropertiesMixin(BaseMetadataPropertiesShortcutMixin):
    @property
    def gmd_url(self):
        return self._get_first_element_value_or_blank_string_with_xpath_query('.//%s:URL/%s:URL' % (self.PITHIA_NSPREFIX_XPATH, NamespacePrefix.GMD))