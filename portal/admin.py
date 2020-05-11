from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from django.template.defaultfilters import date

from portal.models import Aluno, Docente, Tae


@admin.register(Aluno)
class AlunoAdmin(ImportExportModelAdmin):
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
class DocenteAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000

@admin.register(Tae)
class TaeAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000