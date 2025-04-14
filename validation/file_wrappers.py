from lxml import etree
from pathlib import Path

from common.constants import (
    PITHIA_METADATA_SERVER_URL_BASE_NO_VERSION,
    PITHIA_METADATA_SERVER_URL_BASE,
    SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE_NO_VERSION,
    SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE,
)
from common.xml_metadata_utils import (
    Namespace,
    NamespacePrefix,
)

class XMLMetadataFile:
    """
    A wrapper class around an XML Metadata File
    being submitted for validation. Facilitates
    accessing certain properties and hides
    complexity behind functions.
    """
    def __init__(self, xml_file_string, xml_file_name) -> None:
        self._xml_file_name = xml_file_name
        self._xml_file_contents = xml_file_string
        self._parsed_xml = self._parse_xml_string(self._xml_file_contents)

    @classmethod
    def from_file(cls, xml_file):
        xml_file.seek(0)
        return cls(xml_file.read(), xml_file.name)

    def _parse_xml_file(self, xml_file):
        return etree.parse(xml_file)

    def _parse_xml_string(self, xml_string: str):
        try:
            return etree.fromstring(xml_string)
        except ValueError:
            return etree.fromstring(xml_string.encode('utf-8'))

    @property
    def contents(self):
        return self._xml_file_contents

    # Scientific Metadata properties
    @property
    def localid(self):
        # There should be only one <localID> tag in the tree
        return self._parsed_xml.find('.//{%s}localID' % Namespace.PITHIA).text

    @property
    def namespace(self):
        return self._parsed_xml.find('.//{%s}namespace' % Namespace.PITHIA).text
    
    @property
    def ontology_urls(self):
        return self._parsed_xml.xpath(
            f"//*[contains(@xlink:href, '{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE}')]/@*[local-name()='href' and namespace-uri()='{Namespace.XLINK}']",
            namespaces={NamespacePrefix.XLINK: Namespace.XLINK}
        )
    
    @property
    def metadata_urls(self):
        return self._parsed_xml.xpath(
            f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and not(contains(@xlink:href, '#'))]/@*[local-name()='href' and namespace-uri()='{Namespace.XLINK}']",
            namespaces={NamespacePrefix.XLINK: Namespace.XLINK}
        )
    
    @property
    def potential_ontology_urls(self):
        return self._parsed_xml.xpath(
            f"//*[contains(@xlink:href, '{SPACE_PHYSICS_ONTOLOGY_SERVER_URL_BASE_NO_VERSION}')]/@*[local-name()='href' and namespace-uri()='{Namespace.XLINK}']",
            namespaces={NamespacePrefix.XLINK: Namespace.XLINK}
        )
    
    @property
    def potential_metadata_urls(self):
        return self._parsed_xml.xpath(
            f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE_NO_VERSION}') and not(contains(@xlink:href, '#'))]/@*[local-name()='href' and namespace-uri()='{Namespace.XLINK}']",
            namespaces={NamespacePrefix.XLINK: Namespace.XLINK}
        )

    # Helper properties
    @property
    def file_name_no_extension(self):
        return Path(self._xml_file_name).stem
    
    @property
    def schema_url(self):
        urls_with_xsi_ns = self._parsed_xml.xpath("//@*[local-name()='schemaLocation' and namespace-uri()='http://www.w3.org/2001/XMLSchema-instance']")
        urls_with_xsi_ns = urls_with_xsi_ns[0].split()
        schema_url = urls_with_xsi_ns[0]
        if len(urls_with_xsi_ns) > 1:
            schema_url = urls_with_xsi_ns[1]
        return schema_url

    @property
    def root_element_name(self):
        # Get the root tag text without the namespace
        root_localname = etree.QName(self._parsed_xml).localname
        return root_localname

class DataSubsetXMLMetadataFile(XMLMetadataFile):
    def __init__(self, xml_file_string, xml_file_name) -> None:
        xml_file_string = self._xml_string_with_spoofed_doi(xml_file_string)
        super().__init__(xml_file_string, xml_file_name)

    def _xml_string_with_spoofed_doi(self, xml_string):
        parsed_xml_string = self._parse_xml_string(xml_string)
        valid_doi_name = '10.000/000'
        doi_name_element = parsed_xml_string.find('.//{%s}referentDoiName' % Namespace.PITHIA)
        doi_registration_agency_name_element = parsed_xml_string.find('.//{%s}registrationAgencyDoiName' % Namespace.PITHIA)
        if doi_name_element is not None:
            doi_name_element.text = valid_doi_name
        if doi_registration_agency_name_element is not None:
            doi_registration_agency_name_element.text = valid_doi_name
        contents_with_spoofed_doi = etree.tostring(parsed_xml_string).decode()
        try:
            contents_with_spoofed_doi = contents_with_spoofed_doi.decode()
        except (UnicodeDecodeError, AttributeError):
            pass
        return contents_with_spoofed_doi

class InstrumentXMLMetadataFile(XMLMetadataFile):
    @property
    def operational_mode_ids(self):
        # Operational mode IDs are the only values enclosed in <id></id> tags
        return [
            om_element.text
            for om_element in self._parsed_xml.findall('.//{%s}id' % Namespace.PITHIA)
        ]
    
class AcquisitionCapabilitiesXMLMetadataFile(XMLMetadataFile):
    @property
    def operational_mode_urls(self):
        return self._parsed_xml.xpath(
            f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE}') and contains(@xlink:href, '#')]/@*[local-name()='href' and namespace-uri()='{Namespace.XLINK}']",
            namespaces={NamespacePrefix.XLINK: Namespace.XLINK}
        )
    
    @property
    def potential_operational_mode_urls(self):
        return self._parsed_xml.xpath(
            f"//*[contains(@xlink:href, '{PITHIA_METADATA_SERVER_URL_BASE_NO_VERSION}') and contains(@xlink:href, '#')]/@*[local-name()='href' and namespace-uri()='{Namespace.XLINK}']",
            namespaces={NamespacePrefix.XLINK: Namespace.XLINK}
        )