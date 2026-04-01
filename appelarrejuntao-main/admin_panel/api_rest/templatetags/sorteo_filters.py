from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Template filter: {{ my_dict|dict_get:key }}"""
    return d.get(key)
