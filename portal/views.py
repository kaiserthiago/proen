import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Sum, Avg, Max, Min
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io
import urllib, base64

# Create your views here.
from tablib import Dataset

from portal.models import Aluno, Tae, Docente, Aluno2, Tae2, Docente2, DocenteReitoria, DificuldadeCasa, GrupoRisco


def home(request):
    return render(request, 'portal/home.html', {})


@login_required
def dashboard(request):
    # PEGA NO GET O CAMPUS SELECIONADO
    if request.GET.get('campus') and not 'btn_limpar' in request.GET:
        qs_campus = request.GET.get('campus')
    else:
        qs_campus = ''

    # LISTA DE CAMPUS SEM REITORIA
    lista_campus_sem_reitoria = [
        'Ariquemes',
        'Cacoal',
        'Colorado do Oeste',
        'Guajará Mirim',
        'Jaru',
        'Ji-Paraná',
        'Porto Velho Calama',
        'Porto Velho Zona Norte',
        'São Miguel do Guaporé',
        'Vilhena',
    ]

    # FUNÇÃO PARA CRIAR A NUVEM DE PALAVRAS
    def word_cloud(text):
        plt.figure(figsize=(20, 5))

        stopwords = set(STOPWORDS)
        stopwords.update(
            ['ava', 'não', 'de', 'ao', 'só', 'ou', 'da', 'na', 'no', 'que', 'um', 'uma', 'em', 'pra', 'para', 'mas',
             'os', 'as', 'eu', 'EAD', 'tem', 'se', 'dos', 'a', 'o', 'como', 'são', 'essa', 'esse'])

        wc = WordCloud(stopwords=stopwords, background_color="white", max_words=1000, max_font_size=400)
        wc = wc.generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")

        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        return image_64

    # DADOS DOS INDICADORES GERAIS
    alunos = Aluno.objects.all()
    docentes = Docente.objects.all()
    taes = Tae.objects.all()
    total_respostas = alunos.count() + docentes.count() + taes.count()

    # DADOS DOS INDICADORES DOS CAMPI
    indicador_alunos_campus = Aluno.objects.all().order_by(
        'campus').values(
        'campus').annotate(
        total=Count('id')).distinct()

    indicador_docentes_campus = Docente.objects.all().order_by(
        'campus').values(
        'campus').annotate(
        total=Count('id')).distinct()

    indicador_taes_campus = Tae.objects.all().order_by(
        'campus').values(
        'campus').annotate(
        total=Count('id')).distinct()

    # DADOS DOS INDICADORES DOS ALUNOS
    indicador_alunos_nivel_curso = Aluno.objects.all().order_by(
        'nivel_curso').values(
        'nivel_curso').annotate(
        total=Count('id')).distinct()

    indicador_alunos_deficiencia = Aluno.objects.all().order_by(
        'deficiencia').values(
        'deficiencia').annotate(
        total=Count('id')).distinct()

    indicador_alunos_transtorno = Aluno.objects.all().order_by(
        'transtorno').values(
        'transtorno').annotate(
        total=Count('id')).distinct()

    # GRÁFICOS ALUNOS POR CAMPUS
    alunos_campus = Aluno.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Count('id')).distinct()

    chart_aluno_campus_label = [obj[0] for obj in alunos_campus]
    chart_aluno_campus_data = [int(obj[1]) for obj in alunos_campus]
    chart_aluno_campus_data.insert(8, 0)

    # GRÁFICOS DOCENTES POR CAMPUS
    docentes_campus = Docente.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Count('id')).distinct()

    chart_docente_campus_label = [obj[0] for obj in docentes_campus]
    chart_docente_campus_data = [int(obj[1]) for obj in docentes_campus]

    # GRÁFICOS TAES POR CAMPUS
    taes_campus = Tae.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Count('id')).distinct()

    chart_tae_campus_label = [obj[0] for obj in taes_campus]
    chart_tae_campus_data = [int(obj[1]) for obj in taes_campus]

    # GRÁFICOS ALUNOS POR NÍVEL DE CURSO
    alunos_nivel_curso = Aluno.objects.all().order_by(
        'nivel_curso').values_list(
        'nivel_curso').annotate(
        total=Count('id')).distinct()

    chart_aluno_nivel_curso_label = [obj[0] for obj in alunos_nivel_curso]
    chart_aluno_nivel_curso_data = [int(obj[1]) for obj in alunos_nivel_curso]

    # GRÁFICO ALUNOS DEFICIÊNCIA
    alunos_deficiencia = Aluno.objects.all().order_by(
        'deficiencia').values_list(
        'deficiencia').annotate(
        total=Count('id')).distinct()

    # GRÁFICO ALUNOS TRANSTORNO
    alunos_transtorno = Aluno.objects.all().order_by(
        'transtorno').values_list(
        'transtorno').annotate(
        total=Count('id')).distinct()

    # GRÁFICO DOCENTES FAZ AR
    docentes_ar = Docente.objects.all().order_by(
        '-promovendo_ar').values_list(
        'promovendo_ar').annotate(
        total=Count('id')).distinct()

    # GRÁFICO ALUNOS POR POSIÇÃO
    if qs_campus:
        alunos_posicao = Aluno.objects.filter(campus=qs_campus).order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()
    else:
        alunos_posicao = Aluno.objects.all().order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()

    # GRÁFICO DOCENTES POR POSIÇÃO
    if qs_campus:
        docentes_posicao = Docente.objects.filter(campus=qs_campus).order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()
    else:
        docentes_posicao = Docente.objects.all().order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()

    # GRÁFICO TAES POR POSIÇÃO
    if qs_campus:
        taes_posicao = Tae.objects.filter(campus=qs_campus).order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()
    else:
        taes_posicao = Tae.objects.all().order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()

    # GRÁFICO DOCENTES POR OPINIÃO
    docentes_opiniao = Docente.objects.all().order_by(
        'opiniao').values_list(
        'opiniao').annotate(
        total=Count('id')).distinct()

    # GRÁFICO TAES POR OPINIÃO
    taes_opiniao = Tae.objects.all().order_by(
        'opiniao').values_list(
        'opiniao').annotate(
        total=Count('id')).distinct()

    # GRÁFICO ALUNOS ACESSO INTERNET ALUNOS
    alunos_acesso_internet = Aluno.objects.all().order_by(
        'acesso_internet').values_list(
        'acesso_internet').annotate(
        total=Count('id')).distinct()

    # GRÁFICO ALUNOS ACESSO INTERNET DOCENTES
    docentes_acesso_internet = Docente.objects.all().order_by(
        'acesso_internet').values_list(
        'acesso_internet').annotate(
        total=Count('id')).distinct()

    # GRÁFICO ALUNOS ACESSO INTERNET TAES
    taes_acesso_internet = Tae.objects.all().order_by(
        'acesso_internet').values_list(
        'acesso_internet').annotate(
        total=Count('id')).distinct()

    # GRÁFICO MÉDIA NOTA MOODLE POR CAMPUS
    alunos_avaliacao_moodle = Aluno.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Avg('avaliacao_moodle')).distinct()

    chart_alunos_avaliacao_moodle_labels = [obj[0] for obj in alunos_avaliacao_moodle]
    chart_alunos_avaliacao_moodle_data = [float(obj[1]) for obj in alunos_avaliacao_moodle]

    # GRÁFICO MÉDIA NOTA ATIVIDADES REMOTAS ALUNOS
    alunos_avaliacao_atividades_remotas = Aluno.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        orientacoes=Avg('avaliacao_orientacoes'),
        conteudo=Avg('avaliacao_conteudo')).distinct()

    chart_alunos_avaliacao_atividades_remotas_label = [obj[0] for obj in alunos_avaliacao_atividades_remotas]
    chart_alunos_avaliacao_atividades_remotas_data_orientacoes = [float(obj[1]) for obj in
                                                                  alunos_avaliacao_atividades_remotas]
    chart_alunos_avaliacao_atividades_remotas_data_conteudo = [float(obj[2]) for obj in
                                                               alunos_avaliacao_atividades_remotas]

    # GRÁFICO MÉDIA NOTA ATIVIDADES REMOTAS DOCENTES
    docentes_avaliacao_atividades_remotas = Docente.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        experiencia=Avg('avaliacao_experiencia')).distinct()

    chart_docentes_avaliacao_atividades_remotas_label = [obj[0] for obj in docentes_avaliacao_atividades_remotas]
    chart_docentes_avaliacao_atividades_remotas_data_experiencia = [float(obj[1]) for obj in
                                                                    docentes_avaliacao_atividades_remotas]

    # GRÁFICO MÉDIA NOTA ATIVIDADES REMOTAS TAES
    taes_avaliacao_atividades_remotas = Tae.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        jornada=Avg('avaliacao_jornada'),
        producao=Avg('avaliacao_producao')).distinct()

    chart_taes_avaliacao_atividades_remotas_label = [obj[0] for obj in taes_avaliacao_atividades_remotas]
    chart_taes_avaliacao_atividades_remotas_data_jornada = [float(obj[1]) for obj in
                                                            taes_avaliacao_atividades_remotas]
    chart_taes_avaliacao_atividades_remotas_data_producao = [float(obj[2]) for obj in
                                                             taes_avaliacao_atividades_remotas]

    chart_campus_label = [obj[0] for obj in alunos_campus]

    chart_campus_reitoria_label = chart_campus_label
    chart_campus_reitoria_label.insert(8, 'Reitoria')

    # GRÁFICO TAES FORMAÇÃO EAD
    taes_formacao_ead = Tae.objects.all().order_by(
        'formacao_ead').values_list(
        'formacao_ead').annotate(
        total=Count('id')).distinct()

    # GRÁFICO DOCENTES COMPETÊNCIAS EAD
    docente_nao_conheco = []
    docente_conheco = []
    docente_sei_usar = []
    docente_conhecimentos_avancados = []
    docente_sei_ensinar = []

    docentes_competencias_ead_competencia_avaliacao = Docente.objects.all().order_by(
        'competencia_avaliacao').values_list(
        'competencia_avaliacao').annotate(
        total=Count('competencia_avaliacao'),
    ).distinct()

    docente_nao_conheco.insert(0, docentes_competencias_ead_competencia_avaliacao[2][1])
    docente_conheco.insert(0, docentes_competencias_ead_competencia_avaliacao[0][1])
    docente_sei_usar.insert(0, docentes_competencias_ead_competencia_avaliacao[1][1])
    docente_conhecimentos_avancados.insert(0, docentes_competencias_ead_competencia_avaliacao[4][1])
    docente_sei_ensinar.insert(0, docentes_competencias_ead_competencia_avaliacao[3][1])

    docentes_competencias_ead_competencia_desenvolvimento = Docente.objects.all().order_by(
        'competencia_desenvolvimento').values_list(
        'competencia_desenvolvimento').annotate(
        total=Count('competencia_desenvolvimento'),
    ).distinct()

    docente_nao_conheco.insert(1, docentes_competencias_ead_competencia_desenvolvimento[2][1])
    docente_conheco.insert(1, docentes_competencias_ead_competencia_desenvolvimento[0][1])
    docente_sei_usar.insert(1, docentes_competencias_ead_competencia_desenvolvimento[1][1])
    docente_conhecimentos_avancados.insert(1, docentes_competencias_ead_competencia_desenvolvimento[4][1])
    docente_sei_ensinar.insert(1, docentes_competencias_ead_competencia_desenvolvimento[3][1])

    docentes_competencias_ead_competencia_design = Docente.objects.all().order_by(
        'competencia_design').values_list(
        'competencia_design').annotate(
        total=Count('competencia_desenvolvimento'),
    ).distinct()

    docente_nao_conheco.insert(2, docentes_competencias_ead_competencia_design[2][1])
    docente_conheco.insert(2, docentes_competencias_ead_competencia_design[0][1])
    docente_sei_usar.insert(2, docentes_competencias_ead_competencia_design[1][1])
    docente_conhecimentos_avancados.insert(2, docentes_competencias_ead_competencia_design[4][1])
    docente_sei_ensinar.insert(2, docentes_competencias_ead_competencia_design[3][1])

    docentes_competencias_ead_competencia_elaboracao = Docente.objects.all().order_by(
        'competencia_elaboracao').values_list(
        'competencia_elaboracao').annotate(
        total=Count('competencia_elaboracao'),
    ).distinct()

    docente_nao_conheco.insert(3, docentes_competencias_ead_competencia_elaboracao[2][1])
    docente_conheco.insert(3, docentes_competencias_ead_competencia_elaboracao[0][1])
    docente_sei_usar.insert(3, docentes_competencias_ead_competencia_elaboracao[1][1])
    docente_conhecimentos_avancados.insert(3, docentes_competencias_ead_competencia_elaboracao[4][1])
    docente_sei_ensinar.insert(3, docentes_competencias_ead_competencia_elaboracao[3][1])

    docentes_competencias_ead_competencia_ensino = Docente.objects.all().order_by(
        'competencia_ensino').values_list(
        'competencia_ensino').annotate(
        total=Count('competencia_ensino'),
    ).distinct()

    docente_nao_conheco.insert(4, docentes_competencias_ead_competencia_ensino[2][1])
    docente_conheco.insert(4, docentes_competencias_ead_competencia_ensino[0][1])
    docente_sei_usar.insert(4, docentes_competencias_ead_competencia_ensino[1][1])
    docente_conhecimentos_avancados.insert(4, docentes_competencias_ead_competencia_ensino[4][1])
    docente_sei_ensinar.insert(4, docentes_competencias_ead_competencia_ensino[3][1])

    docentes_competencias_ead_competencia_plataforma = Docente.objects.all().order_by(
        'competencia_plataforma').values_list(
        'competencia_plataforma').annotate(
        total=Count('competencia_plataforma'),
    ).distinct()

    docente_nao_conheco.insert(5, docentes_competencias_ead_competencia_plataforma[2][1])
    docente_conheco.insert(5, docentes_competencias_ead_competencia_plataforma[0][1])
    docente_sei_usar.insert(5, docentes_competencias_ead_competencia_plataforma[1][1])
    docente_conhecimentos_avancados.insert(5, docentes_competencias_ead_competencia_plataforma[4][1])
    docente_sei_ensinar.insert(5, docentes_competencias_ead_competencia_plataforma[3][1])

    docentes_competencias_ead_competencia_producao = Docente.objects.all().order_by(
        'competencia_producao').values_list(
        'competencia_producao').annotate(
        total=Count('competencia_producao'),
    ).distinct()

    docente_nao_conheco.insert(6, docentes_competencias_ead_competencia_producao[2][1])
    docente_conheco.insert(6, docentes_competencias_ead_competencia_producao[0][1])
    docente_sei_usar.insert(6, docentes_competencias_ead_competencia_producao[1][1])

    try:
        docente_conhecimentos_avancados.insert(6, docentes_competencias_ead_competencia_producao[4][1])
    except:
        docente_conhecimentos_avancados.insert(6, 0)

    docente_sei_ensinar.insert(6, docentes_competencias_ead_competencia_producao[3][1])

    docentes_competencias_ead_competencia_roteiro = Docente.objects.all().order_by(
        'competencia_roteiro').values_list(
        'competencia_roteiro').annotate(
        total=Count('competencia_roteiro'),
    ).distinct()

    docente_nao_conheco.insert(7, docentes_competencias_ead_competencia_roteiro[2][1])
    docente_conheco.insert(7, docentes_competencias_ead_competencia_roteiro[0][1])
    docente_sei_usar.insert(7, docentes_competencias_ead_competencia_roteiro[1][1])
    docente_conhecimentos_avancados.insert(7, docentes_competencias_ead_competencia_roteiro[4][1])
    docente_sei_ensinar.insert(7, docentes_competencias_ead_competencia_roteiro[3][1])

    docentes_competencias_ead_competencia_sala = Docente.objects.all().order_by(
        'competencia_sala').values_list(
        'competencia_sala').annotate(
        total=Count('competencia_sala'),
    ).distinct()

    docente_nao_conheco.insert(8, docentes_competencias_ead_competencia_sala[2][1])
    docente_conheco.insert(8, docentes_competencias_ead_competencia_sala[0][1])
    docente_sei_usar.insert(8, docentes_competencias_ead_competencia_sala[1][1])
    docente_conhecimentos_avancados.insert(8, docentes_competencias_ead_competencia_sala[4][1])
    docente_sei_ensinar.insert(8, docentes_competencias_ead_competencia_sala[3][1])

    docentes_competencias_ead_competencia_simulador = Docente.objects.all().order_by(
        'competencia_simulador').values_list(
        'competencia_simulador').annotate(
        total=Count('competencia_simulador'),
    ).distinct()

    docente_nao_conheco.insert(9, docentes_competencias_ead_competencia_simulador[2][1])
    docente_conheco.insert(9, docentes_competencias_ead_competencia_simulador[0][1])
    docente_sei_usar.insert(9, docentes_competencias_ead_competencia_simulador[1][1])

    try:
        docente_conhecimentos_avancados.insert(9, docentes_competencias_ead_competencia_simulador[4][1])
    except:
        docente_conhecimentos_avancados.insert(9, 0)

    docente_sei_ensinar.insert(9, docentes_competencias_ead_competencia_simulador[3][1])

    docentes_competencias_ead_competencia_rnp = Docente.objects.all().order_by(
        'competencia_rnp').values_list(
        'competencia_rnp').annotate(
        total=Count('competencia_rnp'),
    ).distinct()

    docente_nao_conheco.insert(10, docentes_competencias_ead_competencia_rnp[2][1])
    docente_conheco.insert(10, docentes_competencias_ead_competencia_rnp[0][1])
    docente_sei_usar.insert(10, docentes_competencias_ead_competencia_rnp[1][1])
    docente_conhecimentos_avancados.insert(10, docentes_competencias_ead_competencia_rnp[4][1])
    docente_sei_ensinar.insert(10, docentes_competencias_ead_competencia_rnp[3][1])

    # GRÁFICO TAES COMPETÊNCIAS EAD
    nao_conheco = []
    conheco = []
    sei_usar = []
    conhecimentos_avancados = []
    sei_ensinar = []

    taes_competencias_ead_competencia_avaliacao = Tae.objects.all().order_by(
        'competencia_avaliacao').values_list(
        'competencia_avaliacao').annotate(
        total=Count('competencia_avaliacao'),
    ).distinct()

    nao_conheco.insert(0, taes_competencias_ead_competencia_avaliacao[2][1])
    conheco.insert(0, taes_competencias_ead_competencia_avaliacao[0][1])
    sei_usar.insert(0, taes_competencias_ead_competencia_avaliacao[1][1])
    conhecimentos_avancados.insert(0, taes_competencias_ead_competencia_avaliacao[4][1])
    sei_ensinar.insert(0, taes_competencias_ead_competencia_avaliacao[3][1])

    taes_competencias_ead_competencia_desenvolvimento = Tae.objects.all().order_by(
        'competencia_desenvolvimento').values_list(
        'competencia_desenvolvimento').annotate(
        total=Count('competencia_desenvolvimento'),
    ).distinct()

    nao_conheco.insert(1, taes_competencias_ead_competencia_desenvolvimento[2][1])
    conheco.insert(1, taes_competencias_ead_competencia_desenvolvimento[0][1])
    sei_usar.insert(1, taes_competencias_ead_competencia_desenvolvimento[1][1])
    conhecimentos_avancados.insert(1, taes_competencias_ead_competencia_desenvolvimento[4][1])
    sei_ensinar.insert(1, taes_competencias_ead_competencia_desenvolvimento[3][1])

    taes_competencias_ead_competencia_design = Tae.objects.all().order_by(
        'competencia_design').values_list(
        'competencia_design').annotate(
        total=Count('competencia_desenvolvimento'),
    ).distinct()

    nao_conheco.insert(2, taes_competencias_ead_competencia_design[2][1])
    conheco.insert(2, taes_competencias_ead_competencia_design[0][1])
    sei_usar.insert(2, taes_competencias_ead_competencia_design[1][1])
    conhecimentos_avancados.insert(2, taes_competencias_ead_competencia_design[4][1])
    sei_ensinar.insert(2, taes_competencias_ead_competencia_design[3][1])

    taes_competencias_ead_competencia_elaboracao = Tae.objects.all().order_by(
        'competencia_elaboracao').values_list(
        'competencia_elaboracao').annotate(
        total=Count('competencia_elaboracao'),
    ).distinct()

    nao_conheco.insert(3, taes_competencias_ead_competencia_elaboracao[2][1])
    conheco.insert(3, taes_competencias_ead_competencia_elaboracao[0][1])
    sei_usar.insert(3, taes_competencias_ead_competencia_elaboracao[1][1])
    conhecimentos_avancados.insert(3, taes_competencias_ead_competencia_elaboracao[4][1])
    sei_ensinar.insert(3, taes_competencias_ead_competencia_elaboracao[3][1])

    taes_competencias_ead_competencia_ensino = Tae.objects.all().order_by(
        'competencia_ensino').values_list(
        'competencia_ensino').annotate(
        total=Count('competencia_ensino'),
    ).distinct()

    nao_conheco.insert(4, taes_competencias_ead_competencia_ensino[2][1])
    conheco.insert(4, taes_competencias_ead_competencia_ensino[0][1])
    sei_usar.insert(4, taes_competencias_ead_competencia_ensino[1][1])
    conhecimentos_avancados.insert(4, taes_competencias_ead_competencia_ensino[4][1])
    sei_ensinar.insert(4, taes_competencias_ead_competencia_ensino[3][1])

    taes_competencias_ead_competencia_plataforma = Tae.objects.all().order_by(
        'competencia_plataforma').values_list(
        'competencia_plataforma').annotate(
        total=Count('competencia_plataforma'),
    ).distinct()

    nao_conheco.insert(5, taes_competencias_ead_competencia_plataforma[2][1])
    conheco.insert(5, taes_competencias_ead_competencia_plataforma[0][1])
    sei_usar.insert(5, taes_competencias_ead_competencia_plataforma[1][1])
    conhecimentos_avancados.insert(5, taes_competencias_ead_competencia_plataforma[4][1])
    sei_ensinar.insert(5, taes_competencias_ead_competencia_plataforma[3][1])

    taes_competencias_ead_competencia_producao = Tae.objects.all().order_by(
        'competencia_producao').values_list(
        'competencia_producao').annotate(
        total=Count('competencia_producao'),
    ).distinct()

    nao_conheco.insert(6, taes_competencias_ead_competencia_producao[2][1])
    conheco.insert(6, taes_competencias_ead_competencia_producao[0][1])
    sei_usar.insert(6, taes_competencias_ead_competencia_producao[1][1])

    try:
        conhecimentos_avancados.insert(6, taes_competencias_ead_competencia_producao[4][1])
    except:
        conhecimentos_avancados.insert(6, 0)

    sei_ensinar.insert(6, taes_competencias_ead_competencia_producao[3][1])

    taes_competencias_ead_competencia_roteiro = Tae.objects.all().order_by(
        'competencia_roteiro').values_list(
        'competencia_roteiro').annotate(
        total=Count('competencia_roteiro'),
    ).distinct()

    nao_conheco.insert(7, taes_competencias_ead_competencia_roteiro[2][1])
    conheco.insert(7, taes_competencias_ead_competencia_roteiro[0][1])
    sei_usar.insert(7, taes_competencias_ead_competencia_roteiro[1][1])
    conhecimentos_avancados.insert(7, taes_competencias_ead_competencia_roteiro[4][1])
    sei_ensinar.insert(7, taes_competencias_ead_competencia_roteiro[3][1])

    taes_competencias_ead_competencia_sala = Tae.objects.all().order_by(
        'competencia_sala').values_list(
        'competencia_sala').annotate(
        total=Count('competencia_sala'),
    ).distinct()

    nao_conheco.insert(8, taes_competencias_ead_competencia_sala[2][1])
    conheco.insert(8, taes_competencias_ead_competencia_sala[0][1])
    sei_usar.insert(8, taes_competencias_ead_competencia_sala[1][1])
    conhecimentos_avancados.insert(8, taes_competencias_ead_competencia_sala[4][1])
    sei_ensinar.insert(8, taes_competencias_ead_competencia_sala[3][1])

    taes_competencias_ead_competencia_simulador = Tae.objects.all().order_by(
        'competencia_simulador').values_list(
        'competencia_simulador').annotate(
        total=Count('competencia_simulador'),
    ).distinct()

    nao_conheco.insert(9, taes_competencias_ead_competencia_simulador[2][1])
    conheco.insert(9, taes_competencias_ead_competencia_simulador[0][1])
    sei_usar.insert(9, taes_competencias_ead_competencia_simulador[1][1])

    try:
        conhecimentos_avancados.insert(9, taes_competencias_ead_competencia_simulador[4][1])
    except:
        conhecimentos_avancados.insert(9, 0)

    sei_ensinar.insert(9, taes_competencias_ead_competencia_simulador[3][1])

    taes_competencias_ead_competencia_rnp = Tae.objects.all().order_by(
        'competencia_rnp').values_list(
        'competencia_rnp').annotate(
        total=Count('competencia_rnp'),
    ).distinct()

    nao_conheco.insert(10, taes_competencias_ead_competencia_rnp[2][1])
    conheco.insert(10, taes_competencias_ead_competencia_rnp[0][1])
    sei_usar.insert(10, taes_competencias_ead_competencia_rnp[1][1])
    conhecimentos_avancados.insert(10, taes_competencias_ead_competencia_rnp[4][1])
    sei_ensinar.insert(10, taes_competencias_ead_competencia_rnp[3][1])

    # GRÁFICOS RESPOSTAS POR DATA
    alunos_data_resposta = Aluno.objects.all().order_by(
        'data_resposta__day').values_list(
        'data_resposta__day').annotate(
        total=Count('id')).distinct()

    docentes_data_resposta = Docente.objects.all().order_by(
        'data_resposta__day').values_list(
        'data_resposta__day').annotate(
        total=Count('id')).distinct()

    taes_data_resposta = Tae.objects.all().order_by(
        'data_resposta__day').values_list(
        'data_resposta__day').annotate(
        total=Count('id')).distinct()

    chart_data_resposta_label = [obj[0] for obj in alunos_data_resposta]
    chart_aluno_data_resposta_data = [int(obj[1]) for obj in alunos_data_resposta]
    chart_docente_data_resposta_data = [int(obj[1]) for obj in docentes_data_resposta]
    chart_tae_data_resposta_data = [int(obj[1]) for obj in taes_data_resposta]

    # GRÁFICO ALUNOS FORMA ACESSO INTERNET
    acesso_aluno_nao = []
    acesso_aluno_sim = []

    aluno_acesso_possui_pc = Aluno.objects.all().order_by(
        'possui_pc').values_list(
        'possui_pc').annotate(
        total=Count('possui_pc'),
    ).distinct()

    acesso_aluno_nao.insert(0, aluno_acesso_possui_pc[0][1])
    acesso_aluno_sim.insert(0, aluno_acesso_possui_pc[1][1])

    aluno_acesso_possui_celular = Aluno.objects.all().order_by(
        'possui_celular').values_list(
        'possui_celular').annotate(
        total=Count('possui_celular'),
    ).distinct()

    acesso_aluno_nao.insert(1, aluno_acesso_possui_celular[0][1])
    acesso_aluno_sim.insert(1, aluno_acesso_possui_celular[1][1])

    aluno_acesso_possui_tablet = Aluno.objects.all().order_by(
        'possui_tablet').values_list(
        'possui_tablet').annotate(
        total=Count('possui_tablet'),
    ).distinct()

    acesso_aluno_nao.insert(2, aluno_acesso_possui_tablet[0][1])
    acesso_aluno_sim.insert(2, aluno_acesso_possui_tablet[1][1])

    aluno_acesso_possui_tv = Aluno.objects.all().order_by(
        'possui_tv').values_list(
        'possui_tv').annotate(
        total=Count('possui_tv'),
    ).distinct()

    acesso_aluno_nao.insert(3, aluno_acesso_possui_tv[0][1])
    acesso_aluno_sim.insert(3, aluno_acesso_possui_tv[1][1])

    # GRÁFICO DOCENTES FORMA ACESSO INTERNET
    acesso_docente_nao = []
    acesso_docente_sim = []

    docente_acesso_possui_pc = Docente.objects.all().order_by(
        'possui_pc').values_list(
        'possui_pc').annotate(
        total=Count('possui_pc'),
    ).distinct()

    acesso_docente_nao.insert(0, docente_acesso_possui_pc[0][1])
    acesso_docente_sim.insert(0, docente_acesso_possui_pc[1][1])

    docente_acesso_possui_celular = Docente.objects.all().order_by(
        'possui_celular').values_list(
        'possui_celular').annotate(
        total=Count('possui_celular'),
    ).distinct()

    acesso_docente_nao.insert(1, docente_acesso_possui_celular[0][1])
    acesso_docente_sim.insert(1, docente_acesso_possui_celular[1][1])

    docente_acesso_possui_tablet = Docente.objects.all().order_by(
        'possui_tablet').values_list(
        'possui_tablet').annotate(
        total=Count('possui_tablet'),
    ).distinct()

    acesso_docente_nao.insert(2, docente_acesso_possui_tablet[0][1])
    acesso_docente_sim.insert(2, docente_acesso_possui_tablet[1][1])

    docente_acesso_possui_tv = Docente.objects.all().order_by(
        'possui_tv').values_list(
        'possui_tv').annotate(
        total=Count('possui_tv'),
    ).distinct()

    acesso_docente_nao.insert(3, docente_acesso_possui_tv[0][1])
    acesso_docente_sim.insert(3, docente_acesso_possui_tv[1][1])

    # GRÁFICO TAES FORMA ACESSO INTERNET
    acesso_tae_nao = []
    acesso_tae_sim = []

    tae_acesso_possui_pc = Tae.objects.all().order_by(
        'possui_pc').values_list(
        'possui_pc').annotate(
        total=Count('possui_pc'),
    ).distinct()

    acesso_tae_nao.insert(0, tae_acesso_possui_pc[0][1])
    acesso_tae_sim.insert(0, tae_acesso_possui_pc[1][1])

    tae_acesso_possui_celular = Tae.objects.all().order_by(
        'possui_celular').values_list(
        'possui_celular').annotate(
        total=Count('possui_celular'),
    ).distinct()

    acesso_tae_nao.insert(1, tae_acesso_possui_celular[0][1])
    acesso_tae_sim.insert(1, tae_acesso_possui_celular[1][1])

    tae_acesso_possui_tablet = Tae.objects.all().order_by(
        'possui_tablet').values_list(
        'possui_tablet').annotate(
        total=Count('possui_tablet'),
    ).distinct()

    acesso_tae_nao.insert(2, tae_acesso_possui_tablet[0][1])
    acesso_tae_sim.insert(2, tae_acesso_possui_tablet[1][1])

    tae_acesso_possui_tv = Tae.objects.all().order_by(
        'possui_tv').values_list(
        'possui_tv').annotate(
        total=Count('possui_tv'),
    ).distinct()

    acesso_tae_nao.insert(3, tae_acesso_possui_tv[0][1])
    acesso_tae_sim.insert(3, tae_acesso_possui_tv[1][1])

    # DISCURSIVA ALUNO: MELHORIAS NO AVA
    alunos = Aluno.objects.all()
    alunos_melhoria_ava = ''

    for aluno in alunos:
        if aluno.melhoria_ava != 'None':
            alunos_melhoria_ava += (
                    str(aluno.melhoria_ava).replace("'", '').replace('\n', '').replace('"', '') + ' ')

    wc_alunos_melhorias_ava = word_cloud(alunos_melhoria_ava)

    # DISCURSIVA TAE: MELHORIAS NO AVA
    taes = Tae.objects.all()
    taes_outras_capacitacoes = ''

    for tae in taes:
        if tae.outras_capacitacoes != 'None':
            taes_outras_capacitacoes += (
                    str(tae.outras_capacitacoes).replace("'", '').replace('\n', '').replace('"', '') + ' ')

    wc_taes_outras_capacitacoes = word_cloud(taes_outras_capacitacoes)

    # DISCURSIVA DOCENTES: PONTOS POSITIVOS/NEGATIVOS
    docentes = Docente.objects.all()
    docentes_pontos_positivos_negativos = ''
    docentes_estrategia_ponto_negativo = ''
    docentes_sugestao_comissao = ''

    for docente in docentes:
        if docente.pontos_positivos_negativos != 'None':
            docentes_pontos_positivos_negativos += (
                    str(docente.pontos_positivos_negativos).replace("'", '').replace('\n', '').replace('"', '') + ' ')

        if docente.estrategia_ponto_negativo != 'None':
            docentes_estrategia_ponto_negativo += (
                    str(docente.estrategia_ponto_negativo).replace("'", '').replace('\n', '').replace('"', '') + ' ')

        if docente.sugestao_comissao != 'None':
            docentes_sugestao_comissao += (
                    str(docente.sugestao_comissao).replace("'", '').replace('\n', '').replace('"', '') + ' ')

    wc_docentes_pontos_positivos_negativos = word_cloud(docentes_pontos_positivos_negativos)
    wc_docentes_estrategia_ponto_negativo = word_cloud(docentes_estrategia_ponto_negativo)
    wc_sugestao_comissao = word_cloud(docentes_sugestao_comissao)

    context = {
        'qs_campus': qs_campus,
        'lista_campus_sem_reitoria': lista_campus_sem_reitoria,

        'alunos': alunos,
        'docentes': docentes,
        'taes': taes,
        'total_respostas': total_respostas,

        'indicador_alunos_campus': indicador_alunos_campus,
        'indicador_docentes_campus': indicador_docentes_campus,
        'indicador_taes_campus': indicador_taes_campus,

        'indicador_alunos_nivel_curso': indicador_alunos_nivel_curso,
        'indicador_alunos_deficiencia': indicador_alunos_deficiencia,
        'indicador_alunos_transtorno': indicador_alunos_transtorno,

        'chart_campus_label': json.dumps(chart_campus_label),
        'chart_campus_reitoria_label': json.dumps(chart_campus_reitoria_label),

        'chart_aluno_campus_label': json.dumps(chart_aluno_campus_label),
        'chart_aluno_campus_data': json.dumps(chart_aluno_campus_data),

        'chart_docente_campus_label': json.dumps(chart_docente_campus_label),
        'chart_docente_campus_data': json.dumps(chart_docente_campus_data),

        'chart_tae_campus_label': json.dumps(chart_tae_campus_label),
        'chart_tae_campus_data': json.dumps(chart_tae_campus_data),

        'chart_aluno_nivel_curso_label': json.dumps(chart_aluno_nivel_curso_label),
        'chart_aluno_nivel_curso_data': json.dumps(chart_aluno_nivel_curso_data),
        'alunos_nivel_curso': json.dumps(list(alunos_nivel_curso)),

        'alunos_deficiencia': json.dumps(list(alunos_deficiencia)),
        'alunos_transtorno': json.dumps(list(alunos_transtorno)),

        'alunos_posicao': json.dumps(list(alunos_posicao)),
        'docentes_posicao': json.dumps(list(docentes_posicao)),
        'taes_posicao': json.dumps(list(taes_posicao)),

        'docentes_ar': json.dumps(list(docentes_ar)),

        'docentes_opiniao': json.dumps(list(docentes_opiniao)),
        'taes_opiniao': json.dumps(list(taes_opiniao)),

        'alunos_acesso_internet': json.dumps(list(alunos_acesso_internet)),
        'docentes_acesso_internet': json.dumps(list(docentes_acesso_internet)),
        'taes_acesso_internet': json.dumps(list(taes_acesso_internet)),

        'chart_alunos_avaliacao_moodle_labels': json.dumps(chart_alunos_avaliacao_moodle_labels),
        'chart_alunos_avaliacao_moodle_data': json.dumps(chart_alunos_avaliacao_moodle_data),

        'chart_alunos_avaliacao_atividades_remotas_label': json.dumps(chart_alunos_avaliacao_atividades_remotas_label),
        'chart_alunos_avaliacao_atividades_remotas_data_orientacoes': json.dumps(
            chart_alunos_avaliacao_atividades_remotas_data_orientacoes),
        'chart_alunos_avaliacao_atividades_remotas_data_conteudo': json.dumps(
            chart_alunos_avaliacao_atividades_remotas_data_conteudo),

        'chart_taes_avaliacao_atividades_remotas_label': json.dumps(chart_taes_avaliacao_atividades_remotas_label),
        'chart_taes_avaliacao_atividades_remotas_data_jornada': json.dumps(
            chart_taes_avaliacao_atividades_remotas_data_jornada),
        'chart_taes_avaliacao_atividades_remotas_data_producao': json.dumps(
            chart_taes_avaliacao_atividades_remotas_data_producao),

        'chart_docentes_avaliacao_atividades_remotas_label': json.dumps(
            chart_docentes_avaliacao_atividades_remotas_label),
        'chart_docentes_avaliacao_atividades_remotas_data_experiencia': json.dumps(
            chart_docentes_avaliacao_atividades_remotas_data_experiencia),

        'taes_formacao_ead': json.dumps(list(taes_formacao_ead)),

        'chart_docentes_compentecia_ead_data_nao_conheco': json.dumps(docente_nao_conheco),
        'chart_docentes_compentecia_ead_data_conheco': json.dumps(docente_conheco),
        'chart_docentes_compentecia_ead_data_conheco_sei_usar': json.dumps(docente_sei_usar),
        'chart_docentes_compentecia_ead_data_conhecimentos_avancados': json.dumps(docente_conhecimentos_avancados),
        'chart_docentes_compentecia_ead_data_sei_ensinar': json.dumps(docente_sei_ensinar),

        'chart_taes_compentecia_ead_data_nao_conheco': json.dumps(nao_conheco),
        'chart_taes_compentecia_ead_data_conheco': json.dumps(conheco),
        'chart_taes_compentecia_ead_data_conheco_sei_usar': json.dumps(sei_usar),
        'chart_taes_compentecia_ead_data_conhecimentos_avancados': json.dumps(conhecimentos_avancados),
        'chart_taes_compentecia_ead_data_sei_ensinar': json.dumps(sei_ensinar),

        'chart_data_resposta_label': json.dumps(chart_data_resposta_label),
        'chart_aluno_data_resposta_data': json.dumps(chart_aluno_data_resposta_data),
        'chart_docente_data_resposta_data': json.dumps(chart_docente_data_resposta_data),
        'chart_tae_data_resposta_data': json.dumps(chart_tae_data_resposta_data),

        'chart_alunos_forma_acesso_internet_sim': json.dumps(acesso_aluno_sim),
        'chart_alunos_forma_acesso_internet_nao': json.dumps(acesso_aluno_nao),

        'chart_docentes_forma_acesso_internet_sim': json.dumps(acesso_docente_sim),
        'chart_docentes_forma_acesso_internet_nao': json.dumps(acesso_docente_nao),

        'chart_taes_forma_acesso_internet_sim': json.dumps(acesso_tae_sim),
        'chart_taes_forma_acesso_internet_nao': json.dumps(acesso_tae_nao),

        'alunos_melhoria_ava': (alunos_melhoria_ava),
        'wc_alunos_melhorias_ava': wc_alunos_melhorias_ava,
        'wc_taes_outras_capacitacoes': wc_taes_outras_capacitacoes,
        'wc_docentes_pontos_positivos_negativos': wc_docentes_pontos_positivos_negativos,
        'wc_docentes_estrategia_ponto_negativo': wc_docentes_estrategia_ponto_negativo,
        'wc_sugestao_comissao': wc_sugestao_comissao,

    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def dashboard2(request):
    # PEGA NO GET O CAMPUS SELECIONADO
    if request.GET.get('campus') and not 'btn_limpar' in request.GET:
        qs_campus = request.GET.get('campus')
    else:
        qs_campus = ''

    # LISTA DE CAMPUS SEM REITORIA
    lista_campus_sem_reitoria = [
        'Ariquemes',
        'Cacoal',
        'Colorado do Oeste',
        'Guajará Mirim',
        'Jaru',
        'Ji-Paraná',
        'Porto Velho Calama',
        'Porto Velho Zona Norte',
        'São Miguel do Guaporé',
        'Vilhena',
    ]

    # FUNÇÃO PARA CRIAR A NUVEM DE PALAVRAS
    def word_cloud(text):
        plt.figure(figsize=(20, 5))

        stopwords = set(STOPWORDS)
        stopwords.update(
            ['ava', 'não', 'de', 'ao', 'só', 'ou', 'da', 'na', 'no', 'que', 'um', 'uma', 'em', 'pra', 'para', 'mas',
             'os', 'as', 'eu', 'EAD', 'tem', 'se', 'dos', 'a', 'o', 'como', 'são', 'essa', 'esse'])

        wc = WordCloud(stopwords=stopwords, background_color="white", max_words=1000, max_font_size=400)
        wc = wc.generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")

        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        return image_64

    # DADOS DOS INDICADORES GERAIS
    alunos = Aluno2.objects.all()
    docentes = Docente2.objects.all()
    taes = Tae2.objects.all()
    total_respostas = alunos.count() + docentes.count() + taes.count()

    # DADOS DOS INDICADORES DOS CAMPI
    indicador_alunos_campus = Aluno2.objects.all().order_by(
        'campus').values(
        'campus').annotate(
        total=Count('id')).distinct()

    indicador_docentes_campus = Docente2.objects.all().order_by(
        'campus').values(
        'campus').annotate(
        total=Count('id')).distinct()

    indicador_taes_campus = Tae2.objects.all().order_by(
        'campus').values(
        'campus').annotate(
        total=Count('id')).distinct()

    # DADOS DOS INDICADORES DOS ALUNOS
    indicador_alunos_nivel_curso = Aluno2.objects.all().order_by(
        'nivel_curso').values(
        'nivel_curso').annotate(
        total=Count('id')).distinct()

    indicador_alunos_periodo_letivo_graduacao = Aluno2.objects.filter(
        nivel_curso='Graduação (Bacharel, CST e Licenciatura)').order_by(
        'periodo_letivo').values(
        'periodo_letivo').annotate(
        total=Count('id')).distinct()

    indicador_alunos_periodo_letivo_concomitante = Aluno2.objects.filter(
        nivel_curso='Técnico Concomitante').order_by(
        'periodo_letivo').values(
        'periodo_letivo').annotate(
        total=Count('id')).distinct()

    indicador_alunos_periodo_letivo_integrado = Aluno2.objects.filter(
        nivel_curso='Técnico Integrado').order_by(
        'periodo_letivo').values(
        'periodo_letivo').annotate(
        total=Count('id')).distinct()

    indicador_alunos_periodo_letivo_subsequente = Aluno2.objects.filter(
        nivel_curso='Técnico Subsequente').order_by(
        'periodo_letivo').values(
        'periodo_letivo').annotate(
        total=Count('id')).distinct()

    # GRÁFICOS ALUNOS POR CAMPUS
    alunos_campus = Aluno2.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Count('id')).distinct()

    chart_aluno_campus_label = [obj[0] for obj in alunos_campus]
    chart_aluno_campus_data = [int(obj[1]) for obj in alunos_campus]
    chart_aluno_campus_data.insert(8, 0)

    # GRÁFICOS DOCENTES POR CAMPUS
    docentes_campus = Docente2.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Count('id')).distinct()

    chart_docente_campus_label = [obj[0] for obj in docentes_campus]
    chart_docente_campus_data = [int(obj[1]) for obj in docentes_campus]

    # GRÁFICOS TAES POR CAMPUS
    taes_campus = Tae2.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        total=Count('id')).distinct()

    chart_tae_campus_label = [obj[0] for obj in taes_campus]
    chart_tae_campus_data = [int(obj[1]) for obj in taes_campus]

    # GRÁFICOS ALUNOS POR NÍVEL DE CURSO
    alunos_nivel_curso = Aluno2.objects.all().order_by(
        'nivel_curso').values_list(
        'nivel_curso').annotate(
        total=Count('id')).distinct()

    chart_aluno_nivel_curso_label = [obj[0] for obj in alunos_nivel_curso]
    chart_aluno_nivel_curso_data = [int(obj[1]) for obj in alunos_nivel_curso]


    # GRÁFICO DOCENTES FAZ AR
    docentes_ar = Docente2.objects.all().order_by(
        '-promovendo_ar').values_list(
        'promovendo_ar').annotate(
        total=Count('id')).distinct()

    # GRÁFICO ALUNOS POR POSIÇÃO
    if qs_campus:
        alunos_posicao = Aluno2.objects.filter(campus=qs_campus).order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()
    else:
        alunos_posicao = Aluno2.objects.all().order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()

    # GRÁFICO DOCENTES POR POSIÇÃO
    if qs_campus:
        docentes_posicao = Docente2.objects.filter(campus=qs_campus).order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()
    else:
        docentes_posicao = Docente2.objects.all().order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()

    # GRÁFICO TAES POR POSIÇÃO
    if qs_campus:
        taes_posicao = Tae2.objects.filter(campus=qs_campus).order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()
    else:
        taes_posicao = Tae2.objects.all().order_by(
            'posicao').values_list(
            'posicao').annotate(
            total=Count('id')).distinct()

    # GRÁFICO ALUNOS ACESSO INTERNET ALUNOS
    alunos_acesso_internet = Aluno2.objects.all().order_by(
        'acesso_internet').values_list(
        'acesso_internet').annotate(
        total=Count('id')).distinct()

    # GRÁFICO MÉDIA NOTA ATIVIDADES REMOTAS ALUNOS
    alunos_avaliacao_atividades_remotas = Aluno2.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        orientacoes=Avg('avaliacao_orientacoes'),
        conteudo=Avg('avaliacao_conteudo')).distinct()

    chart_alunos_avaliacao_atividades_remotas_label = [obj[0] for obj in alunos_avaliacao_atividades_remotas]
    chart_alunos_avaliacao_atividades_remotas_data_orientacoes = [float(obj[1]) for obj in
                                                                  alunos_avaliacao_atividades_remotas]
    chart_alunos_avaliacao_atividades_remotas_data_conteudo = [float(obj[2]) for obj in
                                                               alunos_avaliacao_atividades_remotas]

    # GRÁFICO MÉDIA NOTA ATIVIDADES REMOTAS DOCENTES
    docentes_avaliacao_atividades_remotas = Docente.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        experiencia=Avg('avaliacao_experiencia')).distinct()

    chart_docentes_avaliacao_atividades_remotas_label = [obj[0] for obj in docentes_avaliacao_atividades_remotas]
    chart_docentes_avaliacao_atividades_remotas_data_experiencia = [float(obj[1]) for obj in
                                                                    docentes_avaliacao_atividades_remotas]

    # GRÁFICO MÉDIA NOTA ATIVIDADES REMOTAS TAES
    taes_avaliacao_atividades_remotas = Tae.objects.all().order_by(
        'campus').values_list(
        'campus').annotate(
        jornada=Avg('avaliacao_jornada'),
        producao=Avg('avaliacao_producao')).distinct()

    chart_taes_avaliacao_atividades_remotas_label = [obj[0] for obj in taes_avaliacao_atividades_remotas]
    chart_taes_avaliacao_atividades_remotas_data_jornada = [float(obj[1]) for obj in
                                                            taes_avaliacao_atividades_remotas]
    chart_taes_avaliacao_atividades_remotas_data_producao = [float(obj[2]) for obj in
                                                             taes_avaliacao_atividades_remotas]

    chart_campus_label = [obj[0] for obj in alunos_campus]

    chart_campus_reitoria_label = chart_campus_label
    chart_campus_reitoria_label.insert(8, 'Reitoria')

    # GRÁFICOS RESPOSTAS POR DATA
    alunos_data_resposta = Aluno2.objects.all().order_by(
        'data_resposta__day').values_list(
        'data_resposta__day').annotate(
        total=Count('id')).distinct()

    docentes_data_resposta = Docente2.objects.all().order_by(
        'data_resposta__day').values_list(
        'data_resposta__day').annotate(
        total=Count('id')).distinct()

    taes_data_resposta = Tae2.objects.all().order_by(
        'data_resposta__day').values_list(
        'data_resposta__day').annotate(
        total=Count('id')).distinct()

    chart_data_resposta_label = [obj[0] for obj in alunos_data_resposta]
    chart_aluno_data_resposta_data = [int(obj[1]) for obj in alunos_data_resposta]
    chart_docente_data_resposta_data = [int(obj[1]) for obj in docentes_data_resposta]
    chart_tae_data_resposta_data = [int(obj[1]) for obj in taes_data_resposta]

    # GRÁFICO ALUNOS FORMA ACESSO INTERNET
    acesso_aluno_nao = []
    acesso_aluno_sim = []

    aluno_acesso_possui_pc = Aluno2.objects.all().order_by(
        'possui_pc').values_list(
        'possui_pc').annotate(
        total=Count('possui_pc'),
    ).distinct()

    acesso_aluno_nao.insert(0, aluno_acesso_possui_pc[0][1])
    acesso_aluno_sim.insert(0, aluno_acesso_possui_pc[1][1])

    aluno_acesso_possui_celular = Aluno2.objects.all().order_by(
        'possui_celular').values_list(
        'possui_celular').annotate(
        total=Count('possui_celular'),
    ).distinct()

    acesso_aluno_nao.insert(1, aluno_acesso_possui_celular[0][1])
    acesso_aluno_sim.insert(1, aluno_acesso_possui_celular[1][1])

    aluno_acesso_possui_tablet = Aluno2.objects.all().order_by(
        'possui_tablet').values_list(
        'possui_tablet').annotate(
        total=Count('possui_tablet'),
    ).distinct()

    acesso_aluno_nao.insert(2, aluno_acesso_possui_tablet[0][1])
    acesso_aluno_sim.insert(2, aluno_acesso_possui_tablet[1][1])

    aluno_acesso_possui_tv = Aluno2.objects.all().order_by(
        'possui_tv').values_list(
        'possui_tv').annotate(
        total=Count('possui_tv'),
    ).distinct()

    acesso_aluno_nao.insert(3, aluno_acesso_possui_tv[0][1])
    acesso_aluno_sim.insert(3, aluno_acesso_possui_tv[1][1])

    # DISCURSIVA TAES
    taes = Tae2.objects.all()
    taes_sugestao_suspensao = ''
    taes_sugestao_capacitacao = ''

    for tae in taes:
        if tae.sugestao_suspensao != 'None':
            taes_sugestao_suspensao += (
                    str(tae.sugestao_suspensao).replace("'", '').replace('\n', '').replace('"', '') + ' ')

        if tae.sugestao_capacitacao != 'None':
            taes_sugestao_capacitacao += (
                    str(tae.sugestao_capacitacao).replace("'", '').replace('\n', '').replace('"', '') + ' ')

    wc_taes_sugestao_suspensao = word_cloud(taes_sugestao_suspensao)
    wc_taes_sugestao_capacitacao = word_cloud(taes_sugestao_capacitacao)

    # DISCURSIVA DOCENTES
    docentes = Docente2.objects.all()
    docentes_sugestao_suspensao = ''
    docentes_sugestao_capacitacao = ''

    for docente in docentes:
        if docente.sugestao_suspensao != 'None':
            docentes_sugestao_suspensao += (
                    str(docente.sugestao_suspensao).replace("'", '').replace('\n', '').replace('"', '') + ' ')

        if docente.sugestao_capacitacao != 'None':
            docentes_sugestao_capacitacao += (
                    str(docente.sugestao_capacitacao).replace("'", '').replace('\n', '').replace('"', '') + ' ')

    wc_docentes_sugestao_suspensao = word_cloud(docentes_sugestao_suspensao)
    wc_docentes_sugestao_capacitacao = word_cloud(docentes_sugestao_capacitacao)

    context = {
        'qs_campus': qs_campus,
        'lista_campus_sem_reitoria': lista_campus_sem_reitoria,

        'alunos': alunos,
        'docentes': docentes,
        'taes': taes,
        'total_respostas': total_respostas,

        'indicador_alunos_campus': indicador_alunos_campus,
        'indicador_docentes_campus': indicador_docentes_campus,
        'indicador_taes_campus': indicador_taes_campus,

        'indicador_alunos_nivel_curso': indicador_alunos_nivel_curso,
        'indicador_alunos_periodo_letivo_graduacao': indicador_alunos_periodo_letivo_graduacao,
        'indicador_alunos_periodo_letivo_concomitante': indicador_alunos_periodo_letivo_concomitante,
        'indicador_alunos_periodo_letivo_integrado': indicador_alunos_periodo_letivo_integrado,
        'indicador_alunos_periodo_letivo_subsequente': indicador_alunos_periodo_letivo_subsequente,

        'chart_campus_label': json.dumps(chart_campus_label),
        'chart_campus_reitoria_label': json.dumps(chart_campus_reitoria_label),

        'chart_aluno_campus_label': json.dumps(chart_aluno_campus_label),
        'chart_aluno_campus_data': json.dumps(chart_aluno_campus_data),

        'chart_docente_campus_label': json.dumps(chart_docente_campus_label),
        'chart_docente_campus_data': json.dumps(chart_docente_campus_data),

        'chart_tae_campus_label': json.dumps(chart_tae_campus_label),
        'chart_tae_campus_data': json.dumps(chart_tae_campus_data),

        'chart_aluno_nivel_curso_label': json.dumps(chart_aluno_nivel_curso_label),
        'chart_aluno_nivel_curso_data': json.dumps(chart_aluno_nivel_curso_data),
        'alunos_nivel_curso': json.dumps(list(alunos_nivel_curso)),

        'alunos_posicao': json.dumps(list(alunos_posicao)),
        'docentes_posicao': json.dumps(list(docentes_posicao)),
        'taes_posicao': json.dumps(list(taes_posicao)),

        'docentes_ar': json.dumps(list(docentes_ar)),

        'alunos_acesso_internet': json.dumps(list(alunos_acesso_internet)),

        'chart_alunos_avaliacao_atividades_remotas_label': json.dumps(chart_alunos_avaliacao_atividades_remotas_label),
        'chart_alunos_avaliacao_atividades_remotas_data_orientacoes': json.dumps(
            chart_alunos_avaliacao_atividades_remotas_data_orientacoes),
        'chart_alunos_avaliacao_atividades_remotas_data_conteudo': json.dumps(
            chart_alunos_avaliacao_atividades_remotas_data_conteudo),

        'chart_taes_avaliacao_atividades_remotas_label': json.dumps(chart_taes_avaliacao_atividades_remotas_label),
        'chart_taes_avaliacao_atividades_remotas_data_jornada': json.dumps(
            chart_taes_avaliacao_atividades_remotas_data_jornada),
        'chart_taes_avaliacao_atividades_remotas_data_producao': json.dumps(
            chart_taes_avaliacao_atividades_remotas_data_producao),

        'chart_docentes_avaliacao_atividades_remotas_label': json.dumps(
            chart_docentes_avaliacao_atividades_remotas_label),
        'chart_docentes_avaliacao_atividades_remotas_data_experiencia': json.dumps(
            chart_docentes_avaliacao_atividades_remotas_data_experiencia),

        'chart_data_resposta_label': json.dumps(chart_data_resposta_label),
        'chart_aluno_data_resposta_data': json.dumps(chart_aluno_data_resposta_data),
        'chart_docente_data_resposta_data': json.dumps(chart_docente_data_resposta_data),
        'chart_tae_data_resposta_data': json.dumps(chart_tae_data_resposta_data),

        'chart_alunos_forma_acesso_internet_sim': json.dumps(acesso_aluno_sim),
        'chart_alunos_forma_acesso_internet_nao': json.dumps(acesso_aluno_nao),

        'wc_docentes_sugestao_suspensao': wc_docentes_sugestao_suspensao,
        'wc_docentes_sugestao_capacitacao': wc_docentes_sugestao_capacitacao,
        'wc_taes_sugestao_suspensao': wc_taes_sugestao_suspensao,
        'wc_taes_sugestao_capacitacao': wc_taes_sugestao_capacitacao,

    }
    return render(request, 'portal/dashboard2.html', context)


@permission_required('is_superuser')
def import_form(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        # VERIFICA O ARQUIVO A PARTIR DA LINHA 1
        for n in imported_data[0:]:
            if str(n[1]) == 'Aluno':
                try:
                    aluno = get_object_or_404(Aluno, data_resposta=n[0], campus=n[50])
                except:
                    aluno = None

                if not aluno:
                    aluno = Aluno()

                    aluno.data_resposta = str(n[0])
                    aluno.campus = str(n[50])
                    aluno.acesso_internet = str(n[51])
                    aluno.possui_pc = str(n[52])
                    aluno.possui_celular = str(n[53])
                    aluno.possui_tablet = str(n[54])
                    aluno.possui_tv = str(n[55])
                    aluno.nivel_curso = str(n[56])
                    aluno.deficiencia = str(n[57])
                    aluno.transtorno = str(n[58])
                    aluno.orientacao_enviada = str(n[59])
                    aluno.avaliacao_orientacoes = int(n[60])
                    aluno.conteudo_enviada = str(n[61])
                    aluno.avaliacao_conteudo = int(n[62])
                    aluno.avaliacao_moodle = int(n[64])
                    aluno.melhoria_ava = str(n[65])
                    aluno.docente_melhorar = str(n[66])
                    aluno.auxilio = str(n[67])
                    aluno.posicao = str(n[68])

                    aluno.save()

            if str(n[1]) == 'TAE':
                try:
                    tae = get_object_or_404(Tae, data_resposta=n[0])
                except:
                    tae = None

                if not tae:
                    tae = Tae()

                    tae.data_resposta = str(n[0])
                    tae.campus = str(n[2])
                    tae.acesso_internet = str(n[3])
                    tae.possui_pc = str(n[4])
                    tae.possui_celular = str(n[5])
                    tae.possui_tablet = str(n[6])
                    tae.possui_tv = str(n[7])
                    tae.formacao_ead = str(n[8])
                    tae.competencia_avaliacao = str(n[9])
                    tae.competencia_desenvolvimento = str(n[10])
                    tae.competencia_design = str(n[11])
                    tae.competencia_elaboracao = str(n[12])
                    tae.competencia_ensino = str(n[13])
                    tae.competencia_plataforma = str(n[14])
                    tae.competencia_producao = str(n[15])
                    tae.competencia_roteiro = str(n[16])
                    tae.competencia_sala = str(n[17])
                    tae.competencia_simulador = str(n[18])
                    tae.competencia_rnp = str(n[19])
                    tae.outras_capacitacoes = str(n[20])
                    tae.avaliacao_jornada = int(n[21])
                    tae.avaliacao_producao = int(n[22])
                    tae.opiniao = str(n[23])
                    tae.posicao = str(n[24])

                    tae.save()

            if str(n[1]) == 'Professor':
                try:
                    docente = get_object_or_404(Docente, data_resposta=n[0])
                except:
                    docente = None

                if not docente:
                    docente = Docente()

                    docente.data_resposta = str(n[0])
                    docente.campus = str(n[25])
                    docente.acesso_internet = str(n[26])
                    docente.possui_pc = str(n[27])
                    docente.possui_celular = str(n[28])
                    docente.possui_tablet = str(n[29])
                    docente.possui_tv = str(n[30])
                    docente.promovendo_ar = str(n[31])
                    docente.competencia_avaliacao = str(n[33])
                    docente.competencia_desenvolvimento = str(n[34])
                    docente.competencia_design = str(n[35])
                    docente.competencia_elaboracao = str(n[36])
                    docente.competencia_ensino = str(n[37])
                    docente.competencia_plataforma = str(n[38])
                    docente.competencia_producao = str(n[39])
                    docente.competencia_roteiro = str(n[40])
                    docente.competencia_sala = str(n[41])
                    docente.competencia_simulador = str(n[42])
                    docente.competencia_rnp = str(n[43])
                    docente.avaliacao_experiencia = int(n[44])
                    docente.pontos_positivos_negativos = str(n[45])
                    docente.estrategia_ponto_negativo = str(n[46])
                    docente.sugestao_comissao = str(n[47])
                    docente.opiniao = str(n[48])
                    docente.posicao = str(n[49])

                    docente.save()

        messages.success(request, 'Dados importados')
    context = {
    }

    return render(request, 'portal/import_form.html', context)

@permission_required('is_superuser')
def import_form2(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        # VERIFICA O ARQUIVO A PARTIR DA LINHA 1
        for n in imported_data[0:]:
            if str(n[1]) == 'Aluno':
                try:
                    aluno = get_object_or_404(Aluno2, data_resposta=n[0], campus=n[6])
                except:
                    aluno = None

                if not aluno:
                    aluno = Aluno2()

                    aluno.data_resposta = str(n[0])
                    aluno.nivel_curso = str(n[2])

                    if str(n[2]) == 'Graduação (Bacharel, CST e Licenciatura)':
                        aluno.periodo_letivo = str(n[3])
                    elif str(n[2]) == 'Técnico Concomitante':
                        aluno.periodo_letivo = str(n[5])
                    elif str(n[2]) == 'Técnico Integrado':
                        aluno.periodo_letivo = str(n[4])
                    elif str(n[2]) == 'Técnico Subsequente':
                        aluno.periodo_letivo = str(n[5])
                    else:
                        aluno.periodo_letivo = ''

                    aluno.campus = str(n[6])
                    aluno.acesso_internet = str(n[7])
                    aluno.possui_pc = str(n[8])
                    aluno.possui_celular = str(n[9])
                    aluno.possui_tablet = str(n[10])
                    aluno.possui_tv = str(n[11])
                    aluno.auxilio = str(n[12])
                    aluno.avaliacao_conteudo = int(n[13])
                    aluno.avaliacao_orientacoes = int(n[14])
                    aluno.avaliacao_comunicacao = int(n[15])
                    aluno.horas_estudo = str(n[17])
                    aluno.avaliacao_ar = int(n[18])
                    aluno.posicao = str(n[20])

                    aluno.save()

                    # CADASTRAR TODAS AS DIFICULDADES
                    dificuldade = str(n[16])
                    lista_dificuldade = dificuldade.split(',')

                    for item in lista_dificuldade:
                        aluno_dificuldade = DificuldadeCasa()

                        aluno_dificuldade.aluno = aluno
                        aluno_dificuldade.dificuldade = item

                        aluno_dificuldade.save()

                    # CADASRAR TODOS OS GRUPOS DE RISCO
                    grupo = str(n[19])
                    lista_grupo = grupo.split(',')

                    for item in lista_grupo:
                        aluno_grupo = GrupoRisco()

                        aluno_grupo.aluno = aluno
                        aluno_grupo.grupo = item

                        aluno_grupo.save()

            if str(n[1]) == 'TAE':
                try:
                    tae = get_object_or_404(Tae2, data_resposta=n[0], campus=n[31])
                except:
                    tae = None

                if not tae:
                    tae = Tae2()

                    tae.data_resposta = str(n[0])
                    tae.campus = str(n[31])
                    tae.setor = str(n[32])
                    tae.avaliacao_producao = str(n[33])
                    tae.avaliacao_rendimento = int(n[34])
                    tae.posicao = str(n[37])
                    tae.sugestao_suspensao = str(n[38])
                    tae.sugestao_capacitacao = str(n[39])

                    tae.save()

                    # CADASTRAR TODAS AS DIFICULDADES
                    dificuldade = str(n[35])
                    lista_dificuldade = dificuldade.split(',')

                    for item in lista_dificuldade:
                        tae_dificuldade = DificuldadeCasa()

                        tae_dificuldade.tae = tae
                        tae_dificuldade.dificuldade = item

                        tae_dificuldade.save()

                        # CADASRAR TODOS OS GRUPOS DE RISCO
                        grupo = str(n[36])
                        lista_grupo = grupo.split(',')

                        for item in lista_grupo:
                            tae_grupo = GrupoRisco()

                            tae_grupo.tae = tae
                            tae_grupo.grupo = item

                            tae_grupo.save()

            if str(n[1]) == 'Docente':
                try:
                    docente = get_object_or_404(Docente2, data_resposta=n[0], campus=n[21])
                except:
                    docente = None

                if not docente:
                    docente = Docente2()

                    docente.data_resposta = str(n[0])
                    docente.campus = str(n[21])
                    docente.promovendo_ar = str(n[22])
                    docente.avaliacao_ar = int(n[23])
                    docente.avaliacao_comunicao = int(n[24])
                    docente.avaliacao_participacao = int(n[25])
                    docente.posicao = str(n[28])
                    docente.sugestao_suspensao = str(n[29])
                    docente.sugestao_capacitacao = str(n[30])

                    docente.save()

                    # CADASTRAR TODAS AS DIFICULDADES
                    dificuldade = str(n[26])
                    lista_dificuldade = dificuldade.split(',')

                    for item in lista_dificuldade:
                        docente_dificuldade = DificuldadeCasa()

                        docente_dificuldade.docente = docente
                        docente_dificuldade.dificuldade = item

                        docente_dificuldade.save()

                        # CADASRAR TODOS OS GRUPOS DE RISCO
                        grupo = str(n[27])
                        lista_grupo = grupo.split(',')

                        for item in lista_grupo:
                            docente_grupo = GrupoRisco()

                            docente_grupo.docente = docente
                            docente_grupo.grupo = item

                            docente_grupo.save()

            if str(n[1]) == 'Docente em exercício na Reitoria':
                try:
                    docente_reitoria = get_object_or_404(DocenteReitoria, data_resposta=n[0], campus=n[31])
                except:
                    docente_reitoria = None

                if not docente_reitoria:
                    docente_reitoria = DocenteReitoria()

                    docente_reitoria.data_resposta = str(n[0])
                    docente_reitoria.campus = str(n[31])
                    docente_reitoria.setor = str(n[32])
                    docente_reitoria.avaliacao_producao = str(n[33])
                    docente_reitoria.avaliacao_rendimento = int(n[34])
                    docente_reitoria.posicao = str(n[37])
                    docente_reitoria.sugestao_suspensao = str(n[38])
                    docente_reitoria.sugestao_capacitacao = str(n[39])

                    docente_reitoria.save()

                    # CADASTRAR TODAS AS DIFICULDADES
                    dificuldade = str(n[35])
                    lista_dificuldade = dificuldade.split(',')

                    for item in lista_dificuldade:
                        docente_reitoria_dificuldade = DificuldadeCasa()

                        docente_reitoria_dificuldade.docente_reitoria = docente_reitoria
                        docente_reitoria_dificuldade.dificuldade = item

                        docente_reitoria_dificuldade.save()

                        # CADASRAR TODOS OS GRUPOS DE RISCO
                        grupo = str(n[36])
                        lista_grupo = grupo.split(',')

                        for item in lista_grupo:
                            docente_reitoria_grupo = GrupoRisco()

                            docente_reitoria_grupo.docente_reitoria = docente_reitoria
                            docente_reitoria_grupo.grupo = item

                            docente_reitoria_grupo.save()

        messages.success(request, 'Dados importados')
    context = {
    }

    return render(request, 'portal/import_form.html', context)