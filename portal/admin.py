from django.contrib import admin

# Register your models here.
from django.template.defaultfilters import date

from portal.models import Aluno, Docente, Tae


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'campus',
        'nivel_curso',
        'auxilio', 'posicao',
        'avaliacao_conteudo',
        'avaliacao_orientacoes',
        'avaliacao_moodle',
        'acesso_internet',
        'deficiencia',
        'transtorno'
    )

    list_filter = ('campus', 'nivel_curso', 'auxilio')
    list_per_page = 1000

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000

@admin.register(Tae)
class TaeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000