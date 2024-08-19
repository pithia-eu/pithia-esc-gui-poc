import copy
from itertools import groupby
import re

from utils.dict_helpers import flatten
from utils.string_helpers import split_camel_case


def remove_disallowed_properties_from_property_table_dict(
        property_table_dict,
        disallowed_property_keys=[],
        disallowed_property_key_regexes=[],
        disallowed_property_key_regex_exceptions=[]):
    """Removes any properties that shouldn't be presented in the
    metadata registration property table for any particular reason
    - e.g. the property is displayed in a dedicated format elsewhere
    in the page or the property is only relevant for
    XML/database/JSON support usage.
    """
    property_table_dict_copy = copy.deepcopy(property_table_dict)
    for key in property_table_dict:
        if (not (any(x == key for x in disallowed_property_keys)
            or any(regex for regex in disallowed_property_key_regexes if re.match(regex, key))
            and not any(regex for regex in disallowed_property_key_regex_exceptions if re.match(regex, key)))):
            continue
        property_table_dict_copy.pop(key, None)

    return property_table_dict_copy

def remove_common_disallowed_properties_from_property_table_dict(property_table_dict):
    """Removes properties common to most metadata types
    as they are handled in a dedicated format elsewhere
    in the page, or they are only relevant for
    XML/database/JSON support usage.
    """
    # Selector should only work on top-level
    # attributes which should only be XML namespace
    # attributes.
    # Stored in variable to make purpose clearer.
    namespace_prefix_attribute_selector = '@'
    cleaned_property_table_dict = remove_disallowed_properties_from_property_table_dict(
        property_table_dict,
        disallowed_property_keys=[
            'id',
            'name',
            'description',
        ],
        disallowed_property_key_regexes=[
            re.compile(rf'^{namespace_prefix_attribute_selector}'),
            re.compile(r'^name'),
            re.compile(r'^identifier'),
        ]
    )
    return cleaned_property_table_dict

def _remove_numbering_from_key_section(key_section):
    """Removes numbering from a property if it appears
    that there is only one of that property.
    """
    if not key_section.endswith('(1/1)'):
        return key_section
    return key_section.replace('(1/1)', '')

def _remove_xml_namespace_prefix_from_key_section(key_section):
    """Removes any XML namespace prefixes, which is
    assumed when a key section contains a ":".
    """
    if ':' not in key_section:
        return key_section
    index_of_colon = key_section.index(':')
    return key_section[index_of_colon + 1:]

def _remove_xml_attribute_notation_from_key_section(key_section):
    """Removes the "@" symbol at the start of a
    key section which is assumed to indicate
    an XML attribute.
    """
    if not key_section.startswith('@'):
        return key_section
    return key_section.replace('@', '')

def _reformat_key_contents_for_display(key) -> list:
    key_sections = key.split('.')
    reformatted_key_sections = []

    for key_section in key_sections:
        # Key sections that appear to only be useful for XML/JSON support
        # usage are not included in the reformatted key.
        if key_section.startswith('#') or key_section == '@xlink:href':
            continue

        key_section_reformatted = _remove_numbering_from_key_section(key_section)
        key_section_reformatted = _remove_xml_namespace_prefix_from_key_section(key_section_reformatted)
        key_section_reformatted = _remove_xml_attribute_notation_from_key_section(key_section_reformatted)

        # Append the reformatted key section to a list of
        # other reformatted key sections that will combine
        # to make the whole reformatted key.

        if key_section_reformatted.isupper():
            # If the key section is all upper case, assume that
            # this is a stylistic choice (e.g. it's an acronym
            # like PITHIA or JSON) and do not perform any
            # further reformatting.
            reformatted_key_sections.append(key_section_reformatted)
            continue
        
        if '_' in key_section_reformatted:
            key_section_reformatted = ' '.join(key_section_reformatted.split('_'))

        key_section_reformatted_subsections = split_camel_case(key_section_reformatted)
        key_section_reformatted_subsections_title_case = []
        for subsection in key_section_reformatted_subsections:
            if subsection.isupper():
                key_section_reformatted_subsections_title_case.append(subsection)
                continue
            key_section_reformatted_subsections_title_case.append(subsection.title())
        key_section_reformatted = ' '.join(key_section_reformatted_subsections_title_case)
        reformatted_key_sections.append(key_section_reformatted)

    return reformatted_key_sections

# Credit: https://stackoverflow.com/a/5738933.
def _remove_duplicate_consecutive_key_sections(key_sections: list):
    """Removes duplicate key sections which appear consecutively,
    and may look strange in the key path. E.g. "Feature of Interest,
    Feature of Interest" becomes "Feature of Interest".
    """
    return [key_section for key_section, _group in groupby(key_sections)]

def reformat_and_clean_resource_copy_for_property_table(property_table_dict) -> dict:
    """Reformats the keys of a metadata registration's JSON support dict
    from the default XML format that is passed on from the registration
    XML the JSON support dict was derived from, to a format that is easier
    to read. E.g. "dictionaryKey" becomes "Dictionary Key".
    
    Some HTML may be added to the reformatted key after the initial reformatting
    step to update how it presents in a web page.
    """
    flattened_dict = flatten(property_table_dict)

    flattened_dict_with_reformatted_keys = {}
    for key in flattened_dict:
        reformatted_key_sections = _reformat_key_contents_for_display(key)
        reformatted_key_sections = _remove_duplicate_consecutive_key_sections(reformatted_key_sections)
        last_reformatted_key_section = f'<b>{reformatted_key_sections.pop()}</b>'
        
        reformatted_key_path = ' > '.join(reformatted_key_sections).strip()
        if reformatted_key_path:
            reformatted_key_path = f'<small class="text-muted fst-italic">(from {reformatted_key_path})</small>'
        
        reformatted_key = f'{last_reformatted_key_section} {reformatted_key_path}'.strip()
        if reformatted_key != '':
            flattened_dict_with_reformatted_keys[reformatted_key] = flattened_dict[key]

    return flattened_dict_with_reformatted_keys