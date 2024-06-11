import nh3
import re
import urllib.parse
from django.utils.html import strip_tags


def clean_localid(localid):
    localid = strip_tags(nh3.clean(localid))
    localid = re.sub('[^a-zA-Z0-9 \-\_]+', '', localid)
    return urllib.parse.quote_plus(localid)
