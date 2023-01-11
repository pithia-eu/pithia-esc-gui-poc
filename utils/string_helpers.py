import re


# Credit for _split_camel_case() function: https://stackoverflow.com/a/37697078
def _split_camel_case(string):
    return re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', string)).split()