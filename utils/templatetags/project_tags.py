import random
from django.urls import reverse
from django import template
from typing import Union

register = template.Library()


# Custom template tags
@register.inclusion_tag('breadcrumbs/item.html')
def breadcrumb_item(text, viewname, *args, **kwargs):
    return {
        'text': text,
        'url': reverse(viewname, args=[*args, *kwargs.values()])
    }

@register.inclusion_tag('breadcrumbs/item_active.html')
def breadcrumb_item_active(text):
    return {
        'text': text
    }

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 1, a
    return random.randint(a, b)


# Custom template filters
@register.filter
def get_key_value(dict, key):
    return dict.get(key, '')

@register.filter
def get_key_value_or_blank_string(dict, key):
    try:
        return dict.get(key, '')
    except AttributeError:
        return ''

@register.filter
def get_type(value):
    return type(value).__name__

@register.filter
def wrap_in_list_if_dict(dict_or_list: Union[dict, list]) -> list:
    if isinstance(dict_or_list, list):
        return dict_or_list
    return [dict_or_list]

# Credit for filter implementation: https://stackoverflow.com/a/2507447/10640126
@register.filter(is_safe=True)
def url_target_blank(a_tag_text):
    return a_tag_text.replace('<a ', '<a target="_blank" ')

@register.filter
def choice_values(choices):
    """Returns the values of a ChoiceField's choices"""
    return [c[1] for c in choices]