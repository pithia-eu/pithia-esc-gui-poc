import dateutil.parser
from lxml import etree

from metadata_editor.xml_ns_enums import Namespace, NamespacePrefix


class ResourceXmlToFormDataConverter:
    PITHIA_NS_PREFIX_FOR_XPATH = 'PITHIA'

    basic_form_field_to_xml_mappings = {
        'localid': './/%s:localID' % PITHIA_NS_PREFIX_FOR_XPATH,
        'namespace': './/%s:namespace' % PITHIA_NS_PREFIX_FOR_XPATH,
        'name': './/%s:name' % PITHIA_NS_PREFIX_FOR_XPATH,
        'description': './/%s:description' % PITHIA_NS_PREFIX_FOR_XPATH,
        'identifier_version': './/%s:version' % PITHIA_NS_PREFIX_FOR_XPATH,
    }

    def __init__(self, xml_string) -> None:
        self.xml_string = xml_string
        self.xml_string_parsed = etree.fromstring(xml_string.encode('utf-8'))
        self.namespaces = {
            NamespacePrefix.GCO: Namespace.GCO,
            NamespacePrefix.GMD: Namespace.GMD,
            NamespacePrefix.GML: Namespace.GML,
            NamespacePrefix.MRL: Namespace.MRL,
            NamespacePrefix.OM: Namespace.OM,
            self.PITHIA_NS_PREFIX_FOR_XPATH: Namespace.PITHIA,
            NamespacePrefix.XLINK: Namespace.XLINK,
            NamespacePrefix.XSI: Namespace.XSI,
        }

    def map_basic_xml_fields_to_form(self, form_data):
        for field_name, query in self.basic_form_field_to_xml_mappings.items():
            element = self.xml_string_parsed.xpath(query, namespaces=self.namespaces)
            if not element:
                continue
            try:
                form_data[field_name] = element[0].text
            except AttributeError:
                form_data[field_name] = element[0]
            except BaseException:
                continue
        return form_data

    def map_complex_xml_fields_to_form(self, form_data):
        return form_data

    def convert(self):
        form_data = {}
        form_data = self.map_basic_xml_fields_to_form(form_data)
        form_data = self.map_complex_xml_fields_to_form(form_data)
        return form_data


class ContactInfoXmlMetadataToFormMixin:
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
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

    def map_complex_xml_fields_to_form(self, form_data):
        form_data = super().map_complex_xml_fields_to_form(form_data)

        hours_of_service_elements = self.xml_string_parsed.xpath('.//%s:hoursOfService/%s:CharacterString' % (NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
        if hours_of_service_elements:
            hours_of_service_element = hours_of_service_elements[0]
            hours_of_service_split = hours_of_service_element.text.split('-')
            hours_of_service_start = hours_of_service_split[0]
            hours_of_service_end = hours_of_service_split[1]
            form_data['hours_of_service_start'] = dateutil.parser.parse(hours_of_service_start).time().strftime('%H:%M')
            form_data['hours_of_service_end'] = dateutil.parser.parse(hours_of_service_end).time().strftime('%H:%M')

        return form_data


class DocumentationXmlMetadataToFormMixin:
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'citation_title': './/%s:documentation/%s:Citation/%s:title/%s:CharacterString' % (self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_publication_date': './/%s:documentation/%s:Citation/%s:date/%s:CI_Date/%s:date/%s:Date' % (self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_doi': './/%s:documentation/%s:Citation/%s:identifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO),
            'citation_linkage_url': './/%s:documentation/%s:Citation/%s:onlineResource/%s:CI_OnlineResource/%s:linkage/%s:URL' % (self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD),
            'other_citation_details': './/%s:documentation/%s:Citation/%s:otherCitationDetails/%s:CharacterString' % (self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.GMD, NamespacePrefix.GCO),
        })


class LocationXmlMetadataToFormMixin:
    def _get_name_location(self, nested_location_element):
        name_location_character_string_elements = nested_location_element.xpath('.//%s:nameLocation/%s:EX_GeographicDescription/%s:geographicIdentifier/%s:MD_Identifier/%s:code/%s:CharacterString' % (self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GMD, NamespacePrefix.GCO), namespaces=self.namespaces)
        if not name_location_character_string_elements:
            return ''
        return name_location_character_string_elements[0].text

    def _get_geometry_location_data(self, nested_location_element):
        geometry_location_elements = nested_location_element.xpath('.//%s:geometryLocation' % (self.PITHIA_NS_PREFIX_FOR_XPATH), namespaces=self.namespaces)
        geometry_location_data = {
            'geometry_location_point_id': '',
            'geometry_location_point_srs_name': '',
            'geometry_location_point_pos_1': '',
            'geometry_location_point_pos_2': '',
        }
        if not geometry_location_elements:
            return geometry_location_data
        geometry_location_element = geometry_location_elements[0]
        geometry_location_data['geometry_location_point_id'] = next(iter(geometry_location_element.xpath('.//%s:Point/@%s:id' % (NamespacePrefix.GML, NamespacePrefix.GML), namespaces=self.namespaces)), '')
        geometry_location_data['geometry_location_point_srs_name'] = next(iter(geometry_location_element.xpath('.//%s:Point/@srsName' % (NamespacePrefix.GML), namespaces=self.namespaces)), '')
        geometry_location_point_pos_elements = geometry_location_element.xpath('.//%s:Point/%s:pos' % (NamespacePrefix.GML, NamespacePrefix.GML), namespaces=self.namespaces)
        if geometry_location_point_pos_elements:
            pos_text = geometry_location_point_pos_elements[0].text
            pos_text_split = pos_text.split(' ')
            geometry_location_data['geometry_location_point_pos_1'] = pos_text_split[0]
            geometry_location_data['geometry_location_point_pos_2'] = pos_text_split[1]
        return geometry_location_data
    
    def map_complex_xml_fields_to_form(self, form_data):
        form_data = super().map_complex_xml_fields_to_form(form_data)
        nested_location_elements = self.xml_string_parsed.xpath('.//%s:location/%s:Location' % (self.PITHIA_NS_PREFIX_FOR_XPATH, self.PITHIA_NS_PREFIX_FOR_XPATH), namespaces=self.namespaces)
        if not nested_location_elements:
            return form_data
        nested_location_element = nested_location_elements[0]
        name_location = self._get_name_location(nested_location_element)
        if name_location:
            form_data['location_name'] = name_location
        geometry_location_data = self._get_geometry_location_data(nested_location_element)
        for key, value in geometry_location_data.items():
            if not value:
                continue
            form_data[key] = value

        return form_data


class RelatedPartyXmlMetadataToFormMixin:
    def map_complex_xml_fields_to_form(self, form_data):
        form_data = super().map_complex_xml_fields_to_form(form_data)
        form_data['related_parties_json'] = []
        responsible_party_info_elements = self.xml_string_parsed.xpath('.//%s:ResponsiblePartyInfo' % self.PITHIA_NS_PREFIX_FOR_XPATH, namespaces=self.namespaces)
        for rpi in responsible_party_info_elements:
            roles = rpi.xpath('.//%s:role/@%s:href' % (self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.XLINK), namespaces=self.namespaces)
            parties = rpi.xpath('.//%s:party/@%s:href' % (self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.XLINK), namespaces=self.namespaces)
            form_data['related_parties_json'].append({
                'role': roles[0],
                'parties': parties,
            })
        return form_data


class TypeXmlMetadataToFormMixin:
    def __init__(self, xml_string) -> None:
        super().__init__(xml_string)
        self.basic_form_field_to_xml_mappings.update({
            'type': './/%s:type/@%s:href' % (self.PITHIA_NS_PREFIX_FOR_XPATH, NamespacePrefix.XLINK)
        })