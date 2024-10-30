import logging
from lxml import etree
from lxml.etree import (
    Element,
    ElementTree,
)
from pyhandle.handleexceptions import *

from metadata_editor.service_utils import Namespace


logger = logging.getLogger(__name__)


def _create_lxml_utf8_parser():
    return etree.XMLParser(remove_blank_text=True, encoding='utf-8')


def get_doi_xml_string_from_metadata_xml_string(xml_string):
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    parser = _create_lxml_utf8_parser()
    root = etree.fromstring(xml_string, parser)
    doi_element = root.find('.//{%s}doi' % Namespace.PITHIA)
    if doi_element is None:
        return None
    doi_element_string = etree.tostring(doi_element, pretty_print=True)
    doi_element_string = doi_element_string.decode('utf-8')
    return doi_element_string


def is_doi_element_present_in_xml_file(xml_file) -> bool:
    xml_file.seek(0)
    doi_element_in_xml_file_string = get_doi_xml_string_from_metadata_xml_string(
        xml_file.read()
    )
    return doi_element_in_xml_file_string != None


def get_last_result_time_element(data_subset_xml_string_parsed: ElementTree) -> Element:
    result_time_elements_found = data_subset_xml_string_parsed.findall('.//{%s}resultTime' % Namespace.PITHIA)
    if len(result_time_elements_found) == 0:
        return None
    return result_time_elements_found[-1]


def get_last_source_element(data_subset_xml_string_parsed: ElementTree) -> Element:
    source_elements_found = data_subset_xml_string_parsed.findall('.//{%s}source' % Namespace.PITHIA)
    if len(source_elements_found) == 0:
        return None
    return source_elements_found[-1]


def add_doi_xml_string_to_metadata_xml_string(metadata_xml_string: str, doi_xml_string: str) -> str:
    if isinstance(metadata_xml_string, str):
        metadata_xml_string = metadata_xml_string.encode('utf-8')
    if isinstance(doi_xml_string, str):
        doi_xml_string = doi_xml_string.encode('utf-8')
    # Use lxml to append a new filled in doi element
    parser = _create_lxml_utf8_parser()
    root = etree.fromstring(metadata_xml_string, parser)
    doi_xml_string_parsed = etree.fromstring(doi_xml_string)
    element_to_insert_after = get_last_source_element(root)
    if element_to_insert_after is None:
        element_to_insert_after = get_last_result_time_element(root)
    parent_of_element_to_insert_after = element_to_insert_after.getparent()
    parent_of_element_to_insert_after.insert(parent_of_element_to_insert_after.index(element_to_insert_after) + 1, doi_xml_string_parsed)
    etree.indent(root, space='    ')
    updated_xml_string = etree.tostring(root, pretty_print=True)
    updated_xml_string = updated_xml_string.decode('utf-8')
    return updated_xml_string


def remove_doi_element_from_metadata_xml_string(xml_string):
    if isinstance(xml_string, str):
        xml_string = xml_string.encode('utf-8')
    parser = _create_lxml_utf8_parser()
    root = etree.fromstring(xml_string, parser)
    for doi in root.findall('.//{%s}doi' % Namespace.PITHIA):
        doi.getparent().remove(doi)
    updated_xml_string = etree.tostring(root, pretty_print=True)
    updated_xml_string = updated_xml_string.decode('utf-8')
    return updated_xml_string