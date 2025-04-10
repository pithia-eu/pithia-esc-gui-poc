import environ
from django.test import (
    TestCase,
    tag
)
from lxml import etree
from pyhandle.handleclient import RESTHandleClient
from pyhandle.clientcredentials import PIDClientCredentials

from .services import (
    HandleClient,
    HandleRegistrationProcessForDataSubset,
)
from .xml_utils import (
    add_doi_xml_string_to_metadata_xml_string,
    get_doi_xml_string_from_metadata_xml_string,
    get_last_source_element,
    get_last_result_time_element,
    is_doi_element_present_in_xml_file,
    remove_doi_element_from_metadata_xml_string,
)

from common.models import (
    DataSubset,
    DataCollection,
    Individual,
    Organisation,
)
from common.test_xml_files import (
    DATA_SUBSET_METADATA_XML,
    DATA_SUBSET_WITH_DOI_METADATA_XML,
    DATA_COLLECTION_METADATA_XML,
    DATA_COLLECTION_2_METADATA_XML,
    DATA_COLLECTION_REFERENCING_INDIVIDUAL_2_METADATA_XML,
    DATA_COLLECTION_WITH_MULTIPLE_POINTS_OF_CONTACT_METADATA_XML,
    DATA_COLLECTION_WITH_NO_RELATED_PARTIES_METADATA_XML,
    DATA_COLLECTION_WITH_PRINCIPAL_INVESTIGATOR_ONLY_METADATA_XML,
    DATA_SUBSET_METADATA_XML,
    DOI_KERNEL_METADATA_XML,
    INDIVIDUAL_METADATA_XML,
    INDIVIDUAL_2_METADATA_XML,
    ORGANISATION_METADATA_XML,
    ORGANISATION_2_METADATA_XML,
)


# For tests where ownership data is required
SAMPLE_USER_ID        = 'johndoe@example.com'
SAMPLE_INSTITUTION_ID = 'John Doe Institution'

env = environ.Env()

# Create your tests here.
@tag('manual')
class PyHandleSetupTestCase(TestCase):
    TEST_HANDLE_NAME_SUFFIX = 'MYTEST-HANDLE'
    HANDLE_VALUE_ORIGINAL = 'https://www.example.com/1'
    HANDLE_VALUE_AFTER = 'https://www.example.com/2'

    def setUp(self) -> None:
        # If HandleClient initialises then
        # connection to Handle API was
        # successful.
        self.handle_client = HandleClient()
        return super().setUp()
    
    def tearDown(self) -> None:
        if ((not hasattr(self, 'handle_name'))
            or self.handle_name is None):
            return super().tearDown()
        self._print_active_handles()
        try:
            print('Tearing down test...')
            print('Attemping to delete handle registered during test...')
            self.handle_client.delete_handle(self.handle_name)
            print('Test tear down complete')
        except Exception as err:
            print('Could not delete handle. Encountered error: ', err)
        self._print_active_handles()
        return super().tearDown()

    def _print_active_handles(self):
        return print('Current active handles: ', self.handle_client.get_registered_handles())
    
    def _create_and_register_handle_for_test(self):
        self.handle_name = self.handle_client._create_handle_name_with_suffix(
            self.TEST_HANDLE_NAME_SUFFIX
        )
        self.handle_client.register_handle(
            self.handle_name,
            self.HANDLE_VALUE_ORIGINAL
        )


@tag('manual')
class PyHandleTestCase(PyHandleSetupTestCase):
    @tag('fast', 'handles', 'connection_to_handle_api')
    def test_connection_to_handle_api(self):
        """handle_client's "client" attribute has a type
        of "RESTHandleClient" and the "credentials" has
        a type of "PIDClientCredentials".
        """
        self.assertIsInstance(self.handle_client.client, RESTHandleClient)
        self.assertIsInstance(self.handle_client.credentials, PIDClientCredentials)

    @tag('fast', 'handles')
    def test_create_handle_name(self):
        """handle_client._create_handle_name() returns a string
        with a format of "{handle_prefix}/{handle_suffix}".
        """
        self.handle_name = self.handle_client._create_handle_name_with_suffix(self.TEST_HANDLE_NAME_SUFFIX)

        self.assertIsInstance(self.handle_name, str)
        self.assertEqual(self.handle_name, f'{self.handle_client.handle_prefix}/{self.TEST_HANDLE_NAME_SUFFIX}')

    @tag('fast', 'handles', 'register_handle')
    def test_register_handle(self):
        """handle_client.register_handle() returns the name
        of the handle that was registered and raises no
        exceptions.
        """
        self.handle_name = self.handle_client._create_handle_name_with_suffix(self.TEST_HANDLE_NAME_SUFFIX)
        register_result = self.handle_client.register_handle(self.handle_name, self.HANDLE_VALUE_ORIGINAL)

        self.assertEqual(register_result, self.handle_name)

    @tag('fast', 'handles', 'get_handle_record')
    def test_get_handle_record(self):
        """handle_client.get_handle_record() returns the
        record for the handle data and raises no exceptions.
        """
        self._create_and_register_handle_for_test()

        handle_record = self.handle_client.get_handle_record(
            self.handle_name
        )
        print('handle_record', handle_record)

        self.assertIsInstance(handle_record, dict)

    @tag('fast', 'handles', 'get_data_subset_detail_page_url_from_handle')
    def test_get_data_subset_detail_page_url_from_handle(self):
        """handle_client.get_data_subset_detail_page_url_from_handle()
        returns the URL assigned to the handle and raises no
        exceptions.
        """
        self._create_and_register_handle_for_test()

        handle_url = self.handle_client.get_data_subset_detail_page_url_from_handle(
            self.handle_name
        )
        print('handle_url', handle_url)

        self.assertEqual(handle_url, self.HANDLE_VALUE_ORIGINAL)
        self.assertIsInstance(handle_url, str)

    @tag('fast', 'handles', 'get_handle_raw')
    def test_get_handle_raw(self):
        """handle_client.get_handle_raw() returns the
        handle without being formatted by the API.
        """
        self._create_and_register_handle_for_test()
        handle_raw = self.handle_client.get_handle_raw(self.handle_name)
        print('handle_raw', handle_raw)

        self.assertIsInstance(handle_raw, dict)

    @tag('fast', 'handles', 'get_time_handle_was_issued_as_string')
    def test_get_time_handle_was_issued_as_string(self):
        """handle_client.get_time_handle_was_issued_as_string()
        returns the time the handle was issued in string format.
        """
        self._create_and_register_handle_for_test()
        issue_time_string = self.handle_client.get_time_handle_was_issued_as_string(
            self.handle_name
        )
        print('issue_time_string', issue_time_string)

        self.assertIsInstance(issue_time_string, str)

    @tag('fast', 'handles', 'get_date_handle_was_issued_as_string')
    def test_get_date_handle_was_issued_as_string(self):
        """handle_client.get_date_handle_was_issued_as_string()
        returns the date the handle was issued.
        """
        self._create_and_register_handle_for_test()
        issue_date_as_string = self.handle_client.get_date_handle_was_issued_as_string(
            self.handle_name
        )
        print('issue_date_as_string', issue_date_as_string)

        self.assertIsInstance(issue_date_as_string, str)

    @tag('fast', 'handles', 'delete_handle')
    def test_delete_handle(self):
        """handle_client.delete_handle() returns the handle
        of the deleted record and raises no exceptions.
        """
        self._create_and_register_handle_for_test()
        delete_result = self.handle_client.delete_handle(self.handle_name)

        self.assertEqual(self.handle_name, delete_result)

        # Set handle_name to None so the test case
        # tearDown() method doesn't try to delete
        # the handle again.
        self.handle_name = None

    @tag('fast', 'handles', 'update_data_subset_detail_page_url_for_handle')
    def test_update_data_subset_detail_page_url_for_handle(self):
        """handle_client.update_data_subset_detail_page_url_for_handle()
        updates the URL assigned to the handle and raises no exceptions.
        """
        self.handle_name = self.handle_client._create_handle_name_with_suffix(
            self.TEST_HANDLE_NAME_SUFFIX
        )
        self.handle_client.register_handle(
            self.handle_name,
            self.HANDLE_VALUE_ORIGINAL
        )
        update_result = self.handle_client.update_data_subset_detail_page_url_for_handle(
            self.handle_name,
            self.HANDLE_VALUE_AFTER
        )
        handle_url = self.handle_client.get_data_subset_detail_page_url_from_handle(
            self.handle_name
        )
        handle_issue_number = self.handle_client.get_handle_issue_number(
            self.handle_name
        )

        self.assertEqual(update_result, self.handle_name)
        self.assertEqual(handle_url, self.HANDLE_VALUE_AFTER)
        self.assertEqual(int(handle_issue_number), 2)

        print('handle_url', handle_url)
        print('handle_issue_number', handle_issue_number)

    @tag('fast', '_get_handles_with_prefix')
    def test_get_handles_with_prefix(self):
        """handle_client._get_handles_with_prefix() returns all
        handles under a given prefix.
        """
        handles = self.handle_client._get_handles_with_prefix(
            self.handle_client.handle_prefix
        )
        print('handles', handles)

    @tag('fast', 'get_registered_handles')
    def test_get_registered_handles(self):
        """handle_client.get_registered_handles() returns all
        registered handles.
        """
        registered_handles = self.handle_client.get_registered_handles()
        print('register_handles', registered_handles)

    @tag('fast', 'add_doi_kernel_metadata_to_handle')
    def test_add_doi_kernel_metadata_to_handle(self):
        """handle_client.add_doi_kernel_metadata_to_handle()
        adds the DOI kernel metadata as an XML string to a
        handle.
        """
        DATA_SUBSET_METADATA_XML.seek(0)
        data_subset = DataSubset.objects.create_from_xml_string(
            DATA_SUBSET_METADATA_XML.read(),
            SAMPLE_INSTITUTION_ID,
            SAMPLE_USER_ID
        )
        self.data_subset_id = data_subset.pk
        self.handle_name = self.handle_client.create_and_register_handle_for_resource(
            self.data_subset_id
        )
        DOI_KERNEL_METADATA_XML.seek(0)
        self.handle_client.add_doi_kernel_metadata_to_handle(
            self.handle_name,
            DOI_KERNEL_METADATA_XML.read().decode()
        )

    @tag('fast', 'create_and_register_handle_for_resource_url')
    def test_create_and_register_handle_for_resource_url(self):
        """handle_client.create_and_register_handle_for_resource_url()
        registers a randomly-generated handle for a URL.
        """
        self.handle_name = self.handle_client.create_and_register_handle_for_resource_url(
            self.HANDLE_VALUE_ORIGINAL
        )
        print('self.handle_name', self.handle_name)


@tag('manual')
class DoiRegistrationAndReapplicationTestCase(PyHandleSetupTestCase):
    @tag('fast', 'add_doi_xml_string_to_metadata_xml_string')
    def test_add_doi_xml_string_to_metadata_xml_string(self):
        """add_doi_xml_string_to_metadata_xml_string() adds a
        filled out <doi> element to an XML string.
        """
        self._create_and_register_handle_for_test()
        DATA_SUBSET_METADATA_XML.seek(0)
        DOI_KERNEL_METADATA_XML.seek(0)
        updated_xml_string = add_doi_xml_string_to_metadata_xml_string(
            DATA_SUBSET_METADATA_XML.read(),
            DOI_KERNEL_METADATA_XML.read()
        )
        print('updated_xml_string', updated_xml_string)

    @tag('fast', 'get_last_result_time_element')
    def test_get_last_result_time_element(self):
        """Gets the last <resultTime> element in a
        Data Subset XML string, to act as a marker on
        where to insert a new DOI element.
        """
        DATA_SUBSET_METADATA_XML.seek(0)
        xml_string_parsed = etree.fromstring(DATA_SUBSET_METADATA_XML.read())
        last_result_time_element = get_last_result_time_element(xml_string_parsed)
        print('last_result_time_element', last_result_time_element)

    @tag('fast', 'get_last_source_element')
    def test_get_last_source_element(self):
        """Gets the last <source> element in a Data
        Subset XML string, to act as a marker on
        where to insert a new DOI element.
        """
        DATA_SUBSET_METADATA_XML.seek(0)
        xml_string_parsed = etree.fromstring(DATA_SUBSET_METADATA_XML.read())
        last_source_element = get_last_source_element(xml_string_parsed)
        print('last_source_element', last_source_element)

    @tag('fast', 'doi_element_is_not_present_in_xml_file', 'is_doi_element_present_in_xml_file')
    def test_doi_element_is_not_present_in_xml_file(self):
        """is_doi_element_present_in_xml_file() does not find
        a DOI element in the test XML file and returns False.
        """
        DATA_SUBSET_METADATA_XML.seek(0)
        result = is_doi_element_present_in_xml_file(DATA_SUBSET_METADATA_XML)
        print('result', result)
        self.assertEqual(result, False)

    @tag('fast', 'doi_element_is_present_in_xml_file', 'is_doi_element_present_in_xml_file')
    def test_doi_element_is_present_in_xml_file(self):
        """is_doi_element_present_in_xml_file() finds a DOI
        element in the test XML fiel and returns True.
        """
        DATA_SUBSET_WITH_DOI_METADATA_XML.seek(0)
        result = is_doi_element_present_in_xml_file(DATA_SUBSET_WITH_DOI_METADATA_XML)
        print('result', result)
        self.assertEqual(result, True)

    @tag('fast', 'get_doi_xml_string_from_metadata_xml_string')
    def test_get_doi_xml_string_from_metadata_xml_string(self):
        """Returns the first <doi> element from an XML string.
        """
        DATA_SUBSET_WITH_DOI_METADATA_XML.seek(0)
        doi_element_string = get_doi_xml_string_from_metadata_xml_string(
            DATA_SUBSET_WITH_DOI_METADATA_XML.read()
        )
        print('doi_element_string', doi_element_string)

        self.assertIsInstance(doi_element_string, str)
        self.assertEqual(doi_element_string[:4], '<doi')

    @tag('fast', 'remove_doi_element_from_metadata_xml_string')
    def test_remove_doi_element_from_metadata_xml_string(self):
        """Removes all <doi> elements from an XML string.
        """
        DATA_SUBSET_WITH_DOI_METADATA_XML.seek(0)
        xml_string = DATA_SUBSET_WITH_DOI_METADATA_XML.read()
        updated_xml_string = remove_doi_element_from_metadata_xml_string(xml_string)
        print('updated_xml_string', updated_xml_string)
        self.assertIsInstance(updated_xml_string, str)
        self.assertLess(len(updated_xml_string), len(xml_string))

    @tag('fast', 'replace_doi_element_from_metadata_xml_string')
    def test_replace_doi_element_from_metadata_xml_string(self):
        """Removes all <doi> elements from an XML string and
        adds a <doi> element generated from a DOI dict.
        """
        DATA_SUBSET_WITH_DOI_METADATA_XML.seek(0)
        xml_string = DATA_SUBSET_WITH_DOI_METADATA_XML.read()
        xml_string_without_doi_element = remove_doi_element_from_metadata_xml_string(
            xml_string
        )
        self._create_and_register_handle_for_test()
        DOI_KERNEL_METADATA_XML.seek(0)
        updated_xml_string = add_doi_xml_string_to_metadata_xml_string(
            xml_string_without_doi_element,
            DOI_KERNEL_METADATA_XML.read()
        )
        print('updated_xml_string', updated_xml_string)


@tag('manual')
class PrincipalAgentTestCase(TestCase):
    def _register_xml_file_for_test(self, xml_file, model):
        xml_file.seek(0)
        return model.objects.create_from_xml_string(
            xml_file.read(),
            SAMPLE_INSTITUTION_ID,
            SAMPLE_USER_ID
        )

    @tag('fast', '_get_principal_agent_name_from_data_collection')
    def test_get_principal_agent_name_from_data_collection(self):
        """handle_reg_process._get_principal_agent_name_from_data_collection()
        returns the name of the most relevant organisation listed in the test
        data collection that the data subset is a part of.
        """
        # This organisation is listed as a point of contact which is
        # lower priority than a data provider.
        self._register_xml_file_for_test(ORGANISATION_METADATA_XML, Organisation)
        self._register_xml_file_for_test(INDIVIDUAL_METADATA_XML, Individual)
        # This organisation is listed as a data provider, which has
        # the highest priority.
        self._register_xml_file_for_test(ORGANISATION_2_METADATA_XML, Organisation)
        self._register_xml_file_for_test(
            DATA_COLLECTION_2_METADATA_XML,
            DataCollection
        )
        data_subset = self._register_xml_file_for_test(
            DATA_SUBSET_METADATA_XML,
            DataSubset
        )
        handle_reg_process = HandleRegistrationProcessForDataSubset(
            data_subset,
            SAMPLE_USER_ID
        )
        principal_agent_name = handle_reg_process._get_principal_agent_name_from_data_collection()
        self.assertIsInstance(principal_agent_name, str)
        self.assertEqual(principal_agent_name, 'Organisation Test 2')
        print('principal_agent_name', principal_agent_name)

    @tag('fast', '_get_organisation_responsible_for_data_collection')
    def test_get_organisation_responsible_for_data_collection(self):
        """handle_reg_process._get_organisation_responsible_for_data_collection()
        prioritises the most relevant organisation for the data subset.
        """
        # This organisation has a role of principal investigator for the
        # data subset.
        self._register_xml_file_for_test(ORGANISATION_METADATA_XML, Organisation)
        # This organisation has the role of data provider for the
        # data subset, which is higher priority.
        self._register_xml_file_for_test(ORGANISATION_2_METADATA_XML, Organisation)
        self._register_xml_file_for_test(INDIVIDUAL_2_METADATA_XML, Individual)
        self._register_xml_file_for_test(
            DATA_COLLECTION_REFERENCING_INDIVIDUAL_2_METADATA_XML,
            DataCollection
        )
        data_subset = self._register_xml_file_for_test(
            DATA_SUBSET_METADATA_XML,
            DataSubset
        )
        handle_reg_process = HandleRegistrationProcessForDataSubset(
            data_subset,
            SAMPLE_USER_ID
        )
        principal_agent = handle_reg_process._get_organisation_responsible_for_data_collection()
        principal_agent_name = principal_agent.name
        self.assertIsInstance(principal_agent_name, str)
        self.assertEqual(principal_agent_name, 'Organisation Test 2')
        print('principal_agent_name', principal_agent_name)

    @tag('fast', '_get_organisation_for_related_party')
    def test_get_organisation_for_related_party(self):
        """handle_reg_process._get_organisation_for_related_party()
        gets the first organisation responsible for a role.
        """
        self._register_xml_file_for_test(ORGANISATION_METADATA_XML, Organisation)
        self._register_xml_file_for_test(ORGANISATION_2_METADATA_XML, Organisation)
        self._register_xml_file_for_test(INDIVIDUAL_METADATA_XML, Individual)
        self._register_xml_file_for_test(INDIVIDUAL_2_METADATA_XML, Individual)
        data_collection = self._register_xml_file_for_test(
            DATA_COLLECTION_WITH_MULTIPLE_POINTS_OF_CONTACT_METADATA_XML,
            DataCollection
        )
        data_subset = self._register_xml_file_for_test(
            DATA_SUBSET_METADATA_XML,
            DataSubset
        )
        handle_reg_process = HandleRegistrationProcessForDataSubset(
            data_subset,
            SAMPLE_USER_ID
        )
        principal_agent = handle_reg_process._get_organisation_for_related_party(
            data_collection.properties.related_parties,
            role='https://metadata.pithia.eu/ontology/2.2/relatedPartyRole/PointOfContact'
        )
        self.assertEqual(principal_agent.name, 'Organisation Test')
        print('principal_agent.name', principal_agent.name)

    @tag('fast', '_get_principal_agent_name_from_data_collection')
    def test_principal_agent_is_found_with_less_common_related_party(self):
        """A principal agent is found even if a data provider or
        point of contact is not specified for the data subset.
        """
        self._register_xml_file_for_test(ORGANISATION_METADATA_XML, Organisation)
        self._register_xml_file_for_test(INDIVIDUAL_METADATA_XML, Individual)
        self._register_xml_file_for_test(
            DATA_COLLECTION_WITH_PRINCIPAL_INVESTIGATOR_ONLY_METADATA_XML,
            DataCollection
        )
        data_subset = self._register_xml_file_for_test(
            DATA_SUBSET_METADATA_XML,
            DataSubset
        )
        handle_reg_process = HandleRegistrationProcessForDataSubset(
            data_subset,
            SAMPLE_USER_ID
        )
        principal_agent_name = handle_reg_process._get_principal_agent_name_from_data_collection()
        self.assertEqual(principal_agent_name, 'Organisation Test')
        print('principal_agent_name', principal_agent_name)

    @tag('fast', '_get_principal_agent_name_from_data_collection')
    def test_principal_agent_name_returns_unknown(self):
        """The principal agent name returns 'Unknown' if the
        data subset has no related parties listed.
        """
        self._register_xml_file_for_test(ORGANISATION_METADATA_XML, Organisation)
        self._register_xml_file_for_test(INDIVIDUAL_METADATA_XML, Individual)
        self._register_xml_file_for_test(
            DATA_COLLECTION_WITH_NO_RELATED_PARTIES_METADATA_XML,
            DataCollection
        )
        data_subset = self._register_xml_file_for_test(
            DATA_SUBSET_METADATA_XML,
            DataSubset
        )
        handle_reg_process = HandleRegistrationProcessForDataSubset(
            data_subset,
            SAMPLE_USER_ID
        )
        principal_agent_name = handle_reg_process._get_principal_agent_name_from_data_collection()
        self.assertEqual(principal_agent_name, 'Unknown')
        print('principal_agent_name', principal_agent_name)

    @tag('fast', '_get_principal_agent_name_from_data_collection')
    def test_principal_agent_name_returns_unknown_2(self):
        """The principal agent name returns 'Unknown' if the
        data subset related parties are not registered.
        """
        self._register_xml_file_for_test(
            DATA_COLLECTION_METADATA_XML,
            DataCollection
        )
        data_subset = self._register_xml_file_for_test(
            DATA_SUBSET_METADATA_XML,
            DataSubset
        )
        handle_reg_process = HandleRegistrationProcessForDataSubset(
            data_subset,
            SAMPLE_USER_ID
        )
        principal_agent_name = handle_reg_process._get_principal_agent_name_from_data_collection()
        self.assertEqual(principal_agent_name, 'Unknown')
        print('principal_agent_name', principal_agent_name)


@tag('manual')
class HandleRegistrationProcessForDataSubsetTestCase(PyHandleSetupTestCase):
    def setUp(self) -> None:
        ORGANISATION_METADATA_XML.seek(0)
        Organisation.objects.create_from_xml_string(
            ORGANISATION_METADATA_XML.read(),
            SAMPLE_INSTITUTION_ID,
            SAMPLE_USER_ID
        )
        DATA_COLLECTION_METADATA_XML.seek(0)
        DataCollection.objects.create_from_xml_string(
            DATA_COLLECTION_METADATA_XML.read(),
            SAMPLE_INSTITUTION_ID,
            SAMPLE_USER_ID
        )
        DATA_SUBSET_METADATA_XML.seek(0)
        self.data_subset = DataSubset.objects.create_from_xml_string(
            DATA_SUBSET_METADATA_XML.read(),
            SAMPLE_INSTITUTION_ID,
            SAMPLE_USER_ID
        )
        return super().setUp()

    def test_process_creates_handle(self):
        new_handle_registration_process = HandleRegistrationProcessForDataSubset(
            self.data_subset,
            SAMPLE_USER_ID
        )
        self.handle_name = new_handle_registration_process.run()
        self.assertIsInstance(self.handle_name, str)