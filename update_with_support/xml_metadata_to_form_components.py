import dateutil.parser
from lxml import etree

from metadata_editor.xml_ns_enums import Namespace


class ResourceXmlToFormDataConverter:
    basic_form_field_to_xml_mappings = {
        'localid': './/{%s}localID' % Namespace.PITHIA,
        'namespace': './/{%s}namespace' % Namespace.PITHIA,
        'name': './/{%s}name' % Namespace.PITHIA,
        'description': './/{%s}description' % Namespace.PITHIA,
        'identifier_version': './/{%s}version' % Namespace.PITHIA,
    }

    def __init__(self, xml_string) -> None:
        self.xml_string = xml_string
        self.xml_string_parsed = etree.fromstring(xml_string.encode('utf-8'))

    def map_basic_xml_fields_to_form(self, form_data):
        for field_name, query in self.basic_form_field_to_xml_mappings.items():
            element = self.xml_string_parsed.find(query)
            if element is not None:
                form_data[field_name] = element.text
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
            'phone': './/{%s}voice/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'delivery_point': './/{%s}deliveryPoint/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'city': './/{%s}city/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'administrative_area': './/{%s}administrativeArea/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'postal_code': './/{%s}postalCode/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'country': './/{%s}country/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'email_address': './/{%s}electronicMailAddress/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
            'online_resource': './/{%s}linkage/{%s}URL' % (Namespace.GMD, Namespace.GMD),
            'contact_instructions': './/{%s}contactInstructions/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO),
        })

    def map_complex_xml_fields_to_form(self, form_data):
        form_data = super().map_complex_xml_fields_to_form(form_data)

        hours_of_service_element = self.xml_string_parsed.find('.//{%s}hoursOfService/{%s}CharacterString' % (Namespace.GMD, Namespace.GCO))
        if hours_of_service_element is not None:
            hours_of_service_split = hours_of_service_element.text.split('-')
            hours_of_service_start = hours_of_service_split[0]
            hours_of_service_end = hours_of_service_split[1]
            form_data['hours_of_service_start'] = dateutil.parser.parse(hours_of_service_start).time().strftime('%H:%M')
            form_data['hours_of_service_end'] = dateutil.parser.parse(hours_of_service_end).time().strftime('%H:%M')

        return form_data