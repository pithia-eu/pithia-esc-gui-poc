import random
from django.urls import reverse
from django import template

register = template.Library()

@register.filter
def get_key_value(dict, key):
    return dict.get(key, '')

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

@register.filter
def get_type(value):
    return type(value).__name__

# Credit for filter implementation: https://stackoverflow.com/a/2507447/10640126
@register.filter(is_safe=True)
def url_target_blank(a_tag_text):
    return a_tag_text.replace('<a ', '<a target="_blank" ')

@register.filter
def choice_values(choices):
    """Returns the values of a ChoiceField's choices"""
    return [c[1] for c in choices]

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 1, a
    return random.randint(a, b)