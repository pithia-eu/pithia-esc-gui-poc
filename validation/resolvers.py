import requests
from lxml import etree

class PrefixResolver(etree.Resolver):
    def __init__(self, prefix):
        self.prefix = prefix.lower()

    def resolve(self, url, pubid, context):
        if url.lower().startswith(self.prefix):
            response = requests.get(url, allow_redirects=True)
            return self.resolve_string(response.text, context)
    