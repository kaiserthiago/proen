from django import template
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
import locale

register = template.Library()


@register.simple_tag(name='percentual')
def percentual(total, valor):
    percentual = ((valor / total) * 100)
    return '{:0,.2f}'.format(percentual).replace('.', ',')
