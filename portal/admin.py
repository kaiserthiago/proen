from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from django.template.defaultfilters import date

from portal.models import Aluno, Docente, Tae, Aluno2, Docente2, Tae2, DocenteReitoria, DificuldadeCasa, GrupoRisco


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


@admin.register(Aluno2)
class Aluno2Admin(ImportExportModelAdmin):
    list_display = (
        'id',
        'campus',
        'nivel_curso',
        'periodo_letivo',
        'auxilio',
        'posicao',
    )

    list_filter = ('campus', 'nivel_curso', 'periodo_letivo', 'auxilio')
    list_per_page = 1000


@admin.register(Docente2)
class Docente2Admin(ImportExportModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000


@admin.register(Tae2)
class Tae2Admin(ImportExportModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000


@admin.register(DocenteReitoria)
class DocenteReitoriaAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'data_resposta',
        'campus',
    )

    list_filter = ('campus',)
    list_per_page = 1000


@admin.register(DificuldadeCasa)
class DificuldadeCasaAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'aluno',
        'docente',
        'docente_reitoria',
        'tae',
        'dificuldade'
    )
    list_filter = ('dificuldade',)
    list_per_page = 1000


@admin.register(GrupoRisco)
class GrupoRiscoAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'aluno',
        'docente',
        'docente_reitoria',
        'tae',
        'grupo'
    )
    list_filter = ('grupo',)
    list_per_page = 1000
