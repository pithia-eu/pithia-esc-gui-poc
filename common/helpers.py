import nh3
import re
import urllib.parse
from django.utils.html import strip_tags


def clean_localid_or_namespace(localid_or_namespace):
    localid_or_namespace = strip_tags(nh3.clean(localid_or_namespace))
    localid_or_namespace = re.sub('[^a-zA-Z0-9\-\_]+', '', localid_or_namespace)
    return urllib.parse.quote_plus(localid_or_namespace)
