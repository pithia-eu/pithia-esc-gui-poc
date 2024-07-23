import dateutil.parser
import logging
from lxml import etree

from metadata_editor.xml_ns_enums import Namespace, NamespacePrefix


logger = logging.getLogger(__name__)


class EditorFormFieldsToMetadataUtilsMixin:
    xml_string_parsed = None
    DEFAULT_XPATH_NSPREFIX = 'PITHIA'
    basic_form_field_to_xml_mappings = {}

    def __init__(self, xml_string) -> None:
        self.xml_string = xml_string
        self.xml_string_parsed = etree.fromstring(xml_string.encode('utf-8'))
        self.namespaces = {
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.MRL: Namespace.MRL,
            NamespacePrefix.OM: Namespace.OM,
            self.DEFAULT_XPATH_NSPREFIX: Namespace.PITHIA,
            NamespacePrefix.XLINK: Namespace.XLINK,
            NamespacePrefix.XSI: Namespace.XSI,
        }

    def _get_first_element_from_list(self, element_list: list):
        return next(iter(element_list), '')

    def get_basic_form_field_to_xml_field_mappings(self):
        return {}

    def get_basic_multiple_choice_form_field_to_xml_field_mappings(self):
        return {}

    def get_initial_values_with_basic_mappings(self):
        basic_mappings = self.get_basic_form_field_to_xml_field_mappings()
        initial_values_from_basic_mappings = {}
        for field_name, query in basic_mappings.items():
            elements_matching_query = self.xml_string_parsed.xpath(query, namespaces=self.namespaces)
            if not elements_matching_query:
                continue
            try:
                initial_values_from_basic_mappings[field_name] = self._get_first_element_from_list(elements_matching_query).text
            except AttributeError as err:
                logger.exception(err)
                initial_values_from_basic_mappings[field_name] = self._get_first_element_from_list(elements_matching_query)
            except BaseException as err:
                logger.exception(err)
                continue
        return initial_values_from_basic_mappings

    def get_initial_values_from_basic_multiple_choice_mappings(self):
        basic_mc_mappings = self.get_basic_multiple_choice_form_field_to_xml_field_mappings()
        initial_values_from_basic_mc_mappings = {}
        for field_name, query in basic_mc_mappings.items():
            elements_matching_query = self.xml_string_parsed.xpath(query, namespaces=self.namespaces)
            if not elements_matching_query:
                continue
            try:
                initial_values_from_basic_mc_mappings[field_name] = [e.text for e in elements_matching_query]
            except AttributeError as err:
                logger.exception(err)
                initial_values_from_basic_mc_mappings[field_name] = elements_matching_query
            except BaseException as err:
                logger.exception(err)
                continue
        return initial_values_from_basic_mc_mappings

    def get_initial_values_with_custom_mappings(self):
        return {}

    def get_initial_form_values(self):
        initial_values = {}
        initial_values_from_basic_mappings = self.get_initial_values_with_basic_mappings()
        initial_values_from_multiple_choice_mappings = self.get_initial_values_from_basic_multiple_choice_mappings()
        initial_values_from_custom_mappings = self.get_initial_values_with_custom_mappings()
        initial_values.update(initial_values_from_basic_mappings)
        initial_values.update(initial_values_from_multiple_choice_mappings)
        initial_values.update(initial_values_from_custom_mappings)
        return initial_values


class BaseMetadataFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'localid': './/%s:localID' % self.DEFAULT_XPATH_NSPREFIX,
            'namespace': './/%s:namespace' % self.DEFAULT_XPATH_NSPREFIX,
            'name': './/%s:name' % self.DEFAULT_XPATH_NSPREFIX,
            'description': './/%s:description' % self.DEFAULT_XPATH_NSPREFIX,
            'identifier_version': './/%s:version' % self.DEFAULT_XPATH_NSPREFIX,
        })
        return mappings


class ContactInfoFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'phone': './/%s:voice/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'delivery_point': './/%s:deliveryPoint/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'city': './/%s:city/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'administrative_area': './/%s:administrativeArea/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'postal_code': './/%s:postalCode/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'country': './/%s:country/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'email_address': './/%s:electronicMailAddress/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
            'online_resource': './/%s:linkage/%s:URL' % (NamespacePrefix.GMD, NamespacePrefix.GMD),
            'contact_instructions': './/%s:contactInstructions/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO),
        })
        return mappings

    def _get_hours_of_service_from_xml(self):
        hours_of_service_elements = self.xml_string_parsed.xpath('.//%s:hoursOfService/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
        if not hours_of_service_elements:
            return {}
        
        hours_of_service_element = self._get_first_element_from_list(hours_of_service_elements)
        try:
            hours_of_service_split = hours_of_service_element.text.split('-')
        except AttributeError as err:
            logger.exception(err)
            return {}

        hours_of_service = {}
        try:
            hours_of_service_start = hours_of_service_split[0]
            hours_of_service['hours_of_service_start'] = dateutil.parser.parse(hours_of_service_start).time().strftime('%H:%M')
        except IndexError as err:
            logger.exception(err)
        
        try:
            hours_of_service_end = hours_of_service_split[1]
            hours_of_service['hours_of_service_end'] = dateutil.parser.parse(hours_of_service_end).time().strftime('%H:%M')
        except IndexError as err:
            logger.exception(err)

        return hours_of_service

    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()

        try:
            hours_of_service = self._get_hours_of_service_from_xml()
            initial_values.update(hours_of_service)
        except BaseException as err:
            logger.exception(err)

        return initial_values


class DocumentationFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'citation_title': './/%s:documentation/%s:Citation/%s:title/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_publication_date': './/%s:documentation/%s:Citation/%s:date/%s:CI_Date/%s:date/%s:Date' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_doi': './/%s:documentation/%s:Citation/%s:identifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_linkage_url': './/%s:documentation/%s:Citation/%s:onlineResource/%s:CI_OnlineResource/%s:linkage/%s:URL' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD),
            'other_citation_details': './/%s:documentation/%s:Citation/%s:otherCitationDetails/%s:CharacterString' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GCO),
        })
        return mappings


class LocationFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self._nested_location_element_xpath = '%s:location/%s:Location' % (self.DEFAULT_XPATH_NSPREFIX, self.DEFAULT_XPATH_NSPREFIX)
        self._geometry_location_element_xpath = '%s:geometryLocation' % (self.DEFAULT_XPATH_NSPREFIX)

    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'location_name': './/%s/%s:nameLocation/%s:EX_GeographicDescription/%s:geographicIdentifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self._nested_location_element_xpath, self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'geometry_location_point_id': './/%s/%s/%s:Point/@%s:id' % (self._nested_location_element_xpath, self._geometry_location_element_xpath, NamespacePrefix.GML, NamespacePrefix.GML),
            'geometry_location_point_srs_name': './/%s/%s/%s:Point/@srsName' % (self._nested_location_element_xpath, self._geometry_location_element_xpath, NamespacePrefix.GML),
        })
        return mappings

    def _get_geometry_location_pos_data_from_xml(self):
        geometry_location_point_pos_elements = self.xml_string_parsed.xpath(
            './/%s/%s/%s:Point/%s:pos' % (self._nested_location_element_xpath, self._geometry_location_element_xpath, NamespacePrefix.GML, NamespacePrefix.GML),
            namespaces=self.namespaces
        )
        if not geometry_location_point_pos_elements:
            return {}

        geometry_location_point_pos_element = self._get_first_element_from_list(geometry_location_point_pos_elements)
        try:
            pos_text = geometry_location_point_pos_element.text
            pos_text_split = pos_text.split()
        except AttributeError as err:
            logger.exception(err)
            return {}

        pos_data = {}
        try:
            pos_data['geometry_location_point_pos_1'] = pos_text_split[0]
        except IndexError as err:
            logger.exception(err)

        try:
            pos_data['geometry_location_point_pos_2'] = pos_text_split[1]
        except IndexError as err:
            logger.exception(err)
        
        return pos_data
    
    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()

        gl_point_pos_data = self._get_geometry_location_pos_data_from_xml()
        initial_values.update(gl_point_pos_data)

        return initial_values


class RelatedPartyFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_initial_values_with_custom_mappings(self):
        initial_values = super().get_initial_values_with_custom_mappings()
        initial_values['related_parties_json'] = []
        responsible_party_info_elements = self.xml_string_parsed.xpath('.//%s:ResponsiblePartyInfo' % self.DEFAULT_XPATH_NSPREFIX, namespaces=self.namespaces)
        for rpi in responsible_party_info_elements:
            roles = rpi.xpath('.//%s:role/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            parties = rpi.xpath('.//%s:party/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK), namespaces=self.namespaces)
            initial_values['related_parties_json'].append({
                'role': self._get_first_element_from_list(roles),
                'parties': parties,
            })
        return initial_values


class TypeFormFieldsToMetadataMixin(EditorFormFieldsToMetadataUtilsMixin):
    def get_basic_form_field_to_xml_field_mappings(self):
        mappings = super().get_basic_form_field_to_xml_field_mappings()
        mappings.update({
            'type': './/%s:type/@%s:href' % (self.DEFAULT_XPATH_NSPREFIX, NamespacePrefix.XLINK)
        })
        return mappings