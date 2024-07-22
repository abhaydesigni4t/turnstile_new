# custom_filters.py
from django import template
import os

register = template.Library()

@register.filter(name='split_ext')
def split_ext(value):
    return os.path.splitext(value)[0]
