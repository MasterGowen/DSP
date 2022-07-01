# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter
def get_at_index(lst, index):
    return lst[index]
