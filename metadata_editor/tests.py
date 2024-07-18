from django.test import SimpleTestCase

from .editor_dataclasses import (
    ContactInfoAddressMetadataUpdate,
    ContactInfoMetadataUpdate,
    DocumentationMetadataUpdate,
    PithiaIdentifierMetadataUpdate,
)
from .service_utils import (
    _is_metadata_component_empty,
)
from .services import (
    IndividualEditor,
    OrganisationEditor,
    PlatformEditor,
    ProjectEditor,
)

from common.test_xml_files import (
    INDIVIDUAL_METADATA_XML,
    ORGANISATION_METADATA_XML,
    ORGANISATION_CONTACT_INFO_1_XML,
    ORGANISATION_CONTACT_INFO_2_XML,
    ORGANISATION_MULTIPLE_ADDRESSES_XML,
    PLATFORM_WITH_POS_METADATA_XML,
    PROJECT_METADATA_XML,
)


# Test helper function
def reset_test_file(file):
    file.seek(0)

# Create your tests here.
class OrganisationEditorTestCase(SimpleTestCase):
    def test_organisation_editor(self):
        organisation_editor = OrganisationEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Organisation_Test',
            namespace='test',
            version='100',
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
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
        reset_test_file(ORGANISATION_METADATA_XML)
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
        reset_test_file(ORGANISATION_CONTACT_INFO_1_XML)
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
        reset_test_file(ORGANISATION_CONTACT_INFO_2_XML)
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
        reset_test_file(ORGANISATION_CONTACT_INFO_2_XML)
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
        reset_test_file(ORGANISATION_MULTIPLE_ADDRESSES_XML)
        self.assertRaises(Exception, OrganisationEditor, xml_string=ORGANISATION_MULTIPLE_ADDRESSES_XML)

    def test_organisation_editor_with_blank_phone_number_2(self):
        reset_test_file(ORGANISATION_CONTACT_INFO_1_XML)
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
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
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

    def test_individual_editor_with_file(self):
        reset_test_file(INDIVIDUAL_METADATA_XML)
        individual_editor = IndividualEditor(xml_string=INDIVIDUAL_METADATA_XML.read().decode())
        individual_editor.update_position_name('XYZ')
        individual_editor.update_contact_info(ContactInfoMetadataUpdate())
        xml = individual_editor.to_xml()
        print('xml', xml)


class ProjectEditorTestCase(SimpleTestCase):
    def test_project_editor(self):
        project_editor = ProjectEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Project_Test',
            namespace='test',
            version='1',
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
        )
        project_editor.update_pithia_identifier(pithia_identifier)
        project_editor.update_short_name('PT')
        project_editor.update_name('Project test')
        project_editor.update_abstract('test abstract')
        project_editor.update_url('https://www.example.com/')
        documentation_update = DocumentationMetadataUpdate(
            citation_title='hello',
            citation_publication_date='11/07/24',
            citation_doi='doi',
            citation_url='https://www.example.com/',
            other_citation_details=''
        )
        project_editor.update_documentation(documentation_update)
        related_parties = [
            {
                'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
                'parties': [
                    'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test',
                    'https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test_2',
                ],
            },
            {'role': '', 'parties': []},
            {
                'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
                'parties': [
                    'https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test',
                ],
            },
        ]
        project_editor.update_related_parties(related_parties, new=True)
        xml = project_editor.to_xml()
        print('xml', xml)

    def test_project_editor_with_file(self):
        reset_test_file(PROJECT_METADATA_XML)
        project_editor = ProjectEditor(xml_string=PROJECT_METADATA_XML.read().decode())
        documentation_update = DocumentationMetadataUpdate(
            citation_title='hello',
            citation_publication_date='11/07/24'
        )
        project_editor.update_documentation(documentation_update)
        xml = project_editor.to_xml()
        print('xml', xml)


class PlatformEditorTestCase(SimpleTestCase):
    def test_platform_editor_with_file(self):
        reset_test_file(PLATFORM_WITH_POS_METADATA_XML)
        platform_editor = PlatformEditor(xml_string=PLATFORM_WITH_POS_METADATA_XML.read().decode())
        xml = platform_editor.to_xml()
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

    