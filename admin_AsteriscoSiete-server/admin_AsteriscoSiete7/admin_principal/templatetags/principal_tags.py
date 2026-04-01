# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter
def module(num, val):
    return num % val == 0
