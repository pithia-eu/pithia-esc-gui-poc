from django.test import SimpleTestCase

from .metadata_components import (
    ContactInfoAddressMetadataUpdate,
    ContactInfoMetadataUpdate,
    PithiaIdentifierMetadataUpdate,
)
from .metadata_component_utils import (
    _is_metadata_component_empty,
)
from .utils import (
    IndividualEditor,
    OrganisationEditor,
)

from common.test_xml_files import (
    ORGANISATION_METADATA_XML,
    ORGANISATION_CONTACT_INFO_1_XML,
    ORGANISATION_CONTACT_INFO_2_XML,
    ORGANISATION_MULTIPLE_ADDRESSES_XML,
)


# Create your tests here.
class OrganisationEditorTestCase(SimpleTestCase):
    def test_organisation_editor(self):
        organisation_editor = OrganisationEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Organisation_Test',
            namespace='test',
            version='100',
            creation_date='2022-02-03T12:50:00Z'
        )
        organisation_editor.update_pithia_identifier(pithia_identifier)
        contact_info_address = ContactInfoAddressMetadataUpdate(
            city='London'
        )
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone='123',
            online_resource='https://www.example.com/'
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)

    def test_organisation_editor_with_file(self):
        organisation_editor = OrganisationEditor(xml_string=ORGANISATION_METADATA_XML.read().decode())
        contact_info_address = ContactInfoAddressMetadataUpdate()
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone='',
            online_resource='abc',
            hours_of_service='1:00am-8:00pm',
            contact_instructions='Contact by phone or post'
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)

    def test_organisation_editor_with_custom_contact_info_1(self):
        organisation_editor = OrganisationEditor(xml_string=ORGANISATION_CONTACT_INFO_1_XML.read().decode())
        contact_info_address = ContactInfoAddressMetadataUpdate()
        new_phone_number = '+12345678910'
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone=new_phone_number,
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)

    def test_organisation_editor_with_custom_contact_info_2(self):
        organisation_editor = OrganisationEditor(xml_string=ORGANISATION_CONTACT_INFO_2_XML.read().decode())
        contact_info_address = ContactInfoAddressMetadataUpdate()
        new_phone_number = '+12345678910'
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone=new_phone_number,
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)

    def test_organisation_editor_with_blank_phone_number_1(self):
        organisation_editor = OrganisationEditor(xml_string=ORGANISATION_CONTACT_INFO_2_XML.read().decode())
        contact_info_address = ContactInfoAddressMetadataUpdate()
        new_phone_number = ''
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone=new_phone_number,
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)

    def test_organisation_with_multiple_addresses_fails(self):
        self.assertRaises(Exception, OrganisationEditor, xml_string=ORGANISATION_MULTIPLE_ADDRESSES_XML)

    def test_organisation_editor_with_blank_phone_number_2(self):
        organisation_editor = OrganisationEditor(xml_string=ORGANISATION_CONTACT_INFO_1_XML.read().decode())
        contact_info_address = ContactInfoAddressMetadataUpdate()
        new_phone_number = ''
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone=new_phone_number,
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)

    def test_organisation_with_multiple_addresses_fails(self):
        self.assertRaises(Exception, OrganisationEditor, xml_string=ORGANISATION_MULTIPLE_ADDRESSES_XML)

    def test_organisation_editor_create_minimum_xml(self):
        organisation_editor = OrganisationEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Organisation_Test',
            namespace='test',
            version='10',
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
        )
        organisation_editor.update_pithia_identifier(pithia_identifier)
        organisation_editor.update_name('Organisation test')
        contact_info = ContactInfoMetadataUpdate(
            contact_instructions='Contact by email or phone'
        )
        organisation_editor.update_contact_info(contact_info)
        xml = organisation_editor.to_xml()
        print('xml', xml)


class IndividualEditorTestCase(SimpleTestCase):
    def test_individual_editor(self):
        individual_editor = IndividualEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Individual_Test',
            namespace='test',
            version='95',
            creation_date='2022-02-03T12:50:00Z'
        )
        individual_editor.update_pithia_identifier(pithia_identifier)
        contact_info_address = ContactInfoAddressMetadataUpdate(
            city='Warsaw'
        )
        contact_info = ContactInfoMetadataUpdate(
            address=contact_info_address,
            phone='456',
            online_resource='https://www.example-test.com/'
        )
        individual_editor.update_contact_info(contact_info)
        individual_editor.update_organisation('https://www.example.com/')
        xml = individual_editor.to_xml()
        print('xml', xml)


class UtilsTestCase(SimpleTestCase):
    def test_is_metadata_component_empty(self):
        test_dict = {
                'test': {
                    'test': [{
                        'test': ''
                    }],
                    'test': [
                        '',
                        '',
                        '',
                        0,
                    ]
                }
            }
        result = _is_metadata_component_empty(test_dict)
        self.assertTrue(result)

    def test_is_metadata_component_empty_2(self):
        test_dict = {
            'test': {}
        }
        result = _is_metadata_component_empty(test_dict)
        self.assertTrue(result)

    def test_is_metadata_component_empty_3(self):
        result = _is_metadata_component_empty({})
        self.assertTrue(result)

    def test_is_metadata_component_empty_4(self):
        result = _is_metadata_component_empty([])
        self.assertTrue(result)

    