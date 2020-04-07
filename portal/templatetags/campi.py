from django import template
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
import locale

register = template.Library()

@register.simple_tag(name='campi')
def campi(tipo, valor, i):
    lista_aluno = [
        1079,
        947,
        1368,
        701,
        551,
        1125,
        1511,
        1489,
        0,
        1079,
    ]

    lista_docente = [
        83,
        76,
        101,
        56,
        38,
        77,
        141,
        55,
        0,
        4,
        75
    ]

    lista_tae = [
        62,
        55,
        83,
        21,
        16,
        54,
        74,
        47,
        106,
        1,
        48
    ]

    percentual = 0

    if tipo == 'Aluno':
        try:
            percentual = (valor / lista_aluno[i]) * 100
        except:
            percentual = 0

    elif tipo == 'Docente':
        try:
            percentual = (valor / lista_docente[i]) * 100
        except:
            percentual = 0

    elif tipo == 'TAE':
        try:
            percentual = (valor / lista_tae[i]) * 100
        except:
            percentual = 0

    return '{:0,.2f}'.format(percentual).replace('.', ',')