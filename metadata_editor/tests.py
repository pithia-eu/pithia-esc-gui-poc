from django.test import SimpleTestCase
from lxml import etree

from .editor_dataclasses import (
    ContactInfoAddressMetadataUpdate,
    ContactInfoMetadataUpdate,
    DocumentationMetadataUpdate,
    LocationMetadataUpdate,
    OperationTimeMetadataUpdate,
    PithiaIdentifierMetadataUpdate,
)
from .service_utils import (
    _is_metadata_component_empty,
)
from .services import (
    IndividualEditor,
    InstrumentEditor,
    OperationEditor,
    OrganisationEditor,
    PlatformEditor,
    ProjectEditor,
)

from common.test_xml_files import (
    INDIVIDUAL_METADATA_XML,
    OPERATION_METADATA_XML,
    OPERATION_METADATA_WITH_TIME_INTERVAL_XML,
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


class OperationEditorTestCase(SimpleTestCase):
    def test_operation_editor(self):
        """Test that properties supported by the operation
        editor can be updated.
        """
        operation_editor = OperationEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Operation_Test',
            namespace='test',
            version='1',
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
        )
        operation_editor.update_pithia_identifier(pithia_identifier)
        operation_editor.update_name('Operation test')
        operation_editor.update_description('Operation test description')
        operation_editor.update_status('https://metadata.pithia.eu/ontology/2.2/status/OnGoing')
        operation_editor.update_platforms([
            'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test',
            'https://metadata.pithia.eu/resources/2.2/platform/test/Platform_Test_2',
        ])
        operation_editor.update_child_operations([
            'https://metadata.pithia.eu/resources/2.2/operation/test/Operation_Test',
            'https://metadata.pithia.eu/resources/2.2/operation/test/Operation_Test_2',
        ])
        operation_time = OperationTimeMetadataUpdate(
            time_period_id='tpi_id',
            time_instant_begin_id='tib_id',
            time_instant_begin_position='tib_p',
            time_instant_end_id='tie_id',
            time_instant_end_position='tie_p'
        )
        operation_editor.update_operation_time(operation_time)
        location = LocationMetadataUpdate(
            location_name='location name',
            geometry_location_point_id='glp_id',
            geometry_location_point_pos_1=float('1.23456'),
            geometry_location_point_pos_2=float('2.34567'),
            geometry_location_point_srs_name='glp_srsname',
        )
        operation_editor.update_location(location)
        operation_editor.update_related_parties([
            {
                'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact',
                'parties': ['https://metadata.pithia.eu/resources/2.2/individual/test/Individual_Test']
            },
            {'role': '', 'parties': []},
            {
                'role': 'https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/DataProvider',
                'parties': ['https://metadata.pithia.eu/resources/2.2/organisation/test/Organisation_Test']
            },
        ])
        documentation = DocumentationMetadataUpdate(
            citation_title='Citation title',
            citation_publication_date='23/07/24',
            citation_doi='doi:10.1234/4321',
            citation_url='https://www.example.com/',
            other_citation_details='Other citation details'
        )
        operation_editor.update_documentation(documentation)
        xml = operation_editor.to_xml()
        print('xml', xml)

    def test_operation_editor_empty_op_time(self):
        """Test that passing an empty operation time object
        does not add an <operationTime> element to the
        resulting XML.
        """
        operation_editor = OperationEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Operation_Test',
            namespace='test',
            version='1',
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
        )
        operation_editor.update_pithia_identifier(pithia_identifier)
        operation_editor.update_name('Operation test')
        operation_time = OperationTimeMetadataUpdate(
            time_period_id='',
            time_instant_begin_id='',
            time_instant_begin_position='',
            time_instant_end_id='',
            time_instant_end_position=''
        )
        operation_editor.update_operation_time(operation_time)
        xml = operation_editor.to_xml()
        print('xml', xml)
        parsed_xml = etree.fromstring(xml.encode('utf-8'))
        op_time_element = parsed_xml.find('.//{https://metadata.pithia.eu/schemas/2.2}operationTime')
        self.assertIsNone(op_time_element)

    def test_operation_editor_with_file(self):
        """Test that the operation editor parses in a valid XML
        string and is able to reconstruct it without any changes.
        """
        reset_test_file(OPERATION_METADATA_XML)
        operation_editor = OperationEditor(xml_string=OPERATION_METADATA_XML.read().decode())
        xml = operation_editor.to_xml()
        print('xml', xml)

    def test_optional_operation_time_data_is_not_overwritten(self):
        """Optional <operationTime> elements (in this case,
        <gml:timeInterval>) are kept even when updating
        <gml:begin> and <gml:end> elements."""
        reset_test_file(OPERATION_METADATA_WITH_TIME_INTERVAL_XML)
        operation_editor = OperationEditor(xml_string=OPERATION_METADATA_WITH_TIME_INTERVAL_XML.read().decode())
        operation_time = OperationTimeMetadataUpdate(
            time_period_id='tpi_id',
            time_instant_begin_id='tib_id',
            time_instant_begin_position='tib_p',
            time_instant_end_id='tie_id',
            time_instant_end_position='tie_p'
        )
        operation_editor.update_operation_time(operation_time)
        xml = operation_editor.to_xml()
        print('xml', xml)
        parsed_xml = etree.fromstring(xml.encode('utf-8'))
        time_interval_element = parsed_xml.find('.//{http://www.opengis.net/gml/3.2}timeInterval')
        self.assertIsNotNone(time_interval_element)

    def test_operation_editor_removes_operation_time_from_xml(self):
        """The <operationTime> element is removed from the xml
        when wiped, even with the optional <timeInterval> element
        present.
        """
        reset_test_file(OPERATION_METADATA_WITH_TIME_INTERVAL_XML)
        operation_editor = OperationEditor(xml_string=OPERATION_METADATA_WITH_TIME_INTERVAL_XML.read().decode())
        operation_time = OperationTimeMetadataUpdate(
            time_period_id='',
            time_instant_begin_id='',
            time_instant_begin_position='',
            time_instant_end_id='',
            time_instant_end_position=''
        )
        operation_editor.update_operation_time(operation_time)
        xml = operation_editor.to_xml()
        print('xml', xml)
        parsed_xml = etree.fromstring(xml.encode('utf-8'))
        op_time_element = parsed_xml.find('.//{https://metadata.pithia.eu/schemas/2.2}operationTime')
        self.assertIsNone(op_time_element)


class InstrumentEditorTestCase(SimpleTestCase):
    def test_instrument_editor(self):
        instrument_editor = InstrumentEditor()
        pithia_identifier = PithiaIdentifierMetadataUpdate(
            localid='Instrument_Test',
            namespace='test',
            version='1',
            creation_date='2022-02-03T12:50:00Z',
            last_modification_date='2022-02-03T12:50:00Z'
        )
        instrument_editor.update_pithia_identifier(pithia_identifier)
        instrument_editor.update_name('Instrument test')
        instrument_editor.update_description('Instrument test description')
        instrument_editor.update_type('https://metadata.pithia.eu/ontology/2.2/instrumentType/VerticalSounder')
        instrument_editor.update_instrument_version('52')
        instrument_editor.update_members([
            'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_1',
            'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_2',
            'https://metadata.pithia.eu/resources/2.2/instrument/test/Instrument_Test_3',
        ])
        instrument_editor.update_operational_modes([
            {
                'id': 'opm1',
                'name': 'opm1 name',
                'description': 'opm1 description',
            },
            {
                'id': 'opm2',
                'name': 'opm2 name',
                'description': 'opm2 description',
            },
        ])
        xml = instrument_editor.to_xml()
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

    