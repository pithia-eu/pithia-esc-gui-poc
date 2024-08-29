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

    def _get_elements_with_xpath_query(self, xpath_query: str):
        return self.xml_parsed.xpath(xpath_query, namespaces=self.namespaces)

    def _get_first_element_from_list(self, element_list: list):
        return next(iter(element_list), '')

    def _get_first_element_value_or_blank_string_with_xpath_query(self, xpath_query: str):
        element_list = self._get_elements_with_xpath_query(xpath_query)
        if not len(element_list):
            return ''

        first_element = self._get_first_element_from_list(element_list)
        try:
            return first_element.text
        except AttributeError as err:
            logger.exception(err)
            return first_element
        except Exception as err:
            logger.exception(err)
            return ''


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