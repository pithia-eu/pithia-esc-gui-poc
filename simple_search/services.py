from lxml import etree

from common.models import DataCollection

def find_data_collections_for_simple_search(query):
    data_collections = DataCollection.objects.all().values('id', 'xml')
    data_collections_with_match = []
    for dc in data_collections:
        parsed_xml = etree.fromstring(dc['xml'].encode())
        if parsed_xml.xpath(f'.//*[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), translate("{query}", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"))]'):
            # If partial case-insensitive text match found.
            # Credit: https://stackoverflow.com/a/36427554
            data_collections_with_match.append(dc)
    
    return data_collections_with_match

def find_data_collections_for_case_sensitive_simple_search(query):
    # https://stackoverflow.com/a/14300008
    pass
    