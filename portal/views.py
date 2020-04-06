import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Sum, Avg, Max, Min
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import date

# Create your views here.
from django.template.defaultfilters import lower
from tablib import Dataset

from portal.models import Aluno, Tae, Docente

@login_required
def dashboard(request):
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

    # GRÁFICO ALUNOS POR POSIÇÃO
    alunos_posicao = Aluno.objects.all().order_by(
        'posicao').values_list(
        'posicao').annotate(
        total=Count('id')).distinct()

    # GRÁFICO DOCENTES POR POSIÇÃO
    docentes_posicao = Docente.objects.all().order_by(
        'posicao').values_list(
        'posicao').annotate(
        total=Count('id')).distinct()

    # GRÁFICO TAES POR POSIÇÃO
    taes_posicao = Tae.objects.all().order_by(
        'posicao').values_list(
        'posicao').annotate(
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
    # preparacao_sulfato = PreparacaoSulfato.objects.filter(empresa=request.user.userprofile.empresa,
    #                                                       data__year=date.today().year).order_by(
    #     'data').values_list(
    #     'data').annotate(
    #     total=Sum('quantidade'))
    #
    # chart_sulfato_label = [str(obj[0].strftime('%d/%m/%y')) for obj in preparacao_sulfato]
    # chart_sulfato_data = [float(obj[1]) for obj in preparacao_sulfato]
    #
    # utilizacal_cal = UtilizacaoCal.objects.filter(empresa=request.user.userprofile.empresa,
    #                                               data__year=date.today().year).order_by(
    #     'data').values_list(
    #     'data').annotate(
    #     total=Sum('quantidade'))
    #
    # chart_cal_label = [str(obj[0].strftime('%d/%m/%y')) for obj in utilizacal_cal]
    # chart_cal_data = [float(obj[1]) for obj in utilizacal_cal]
    #
    # # ANÁLISE BRUTA
    # dados_analise_bruta = AnaliseBruta.objects.filter(empresa=request.user.userprofile.empresa,
    #                                                   data__year=date.today().year).order_by('data').values_list(
    #     'data', 'turbidez', 'alcalinidade', 'gas_carbonico', 'ph').annotate(Count('id'))
    #
    # chart_analise_bruta_label = [str(obj[0].strftime('%d/%m/%y')) for obj in dados_analise_bruta]
    # chart_analise_bruta_dados_turbidez = [float(obj[1]) for obj in dados_analise_bruta]
    # chart_analise_bruta_dados_alcalinidade = [float(obj[2]) for obj in dados_analise_bruta]
    # chart_analise_bruta_dados_gas_carbonico = [float(obj[3]) for obj in dados_analise_bruta]
    # chart_analise_bruta_dados_ph = [float(obj[4]) for obj in dados_analise_bruta]

    context = {
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

        'alunos_posicao': json.dumps(list(alunos_posicao)),
        'docentes_posicao': json.dumps(list(docentes_posicao)),
        'taes_posicao': json.dumps(list(taes_posicao)),

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

        # 'chart_lavagem_data_consumo': json.dumps(chart_lavagem_data_consumo),
        # 'chart_lavagem_data_tempo': json.dumps(chart_lavagem_data_tempo),
        #
        # 'chart_sulfato_label': json.dumps(chart_sulfato_label),
        # 'chart_sulfato_data': json.dumps(chart_sulfato_data),
        #
        # 'chart_cal_label': json.dumps(chart_cal_label),
        # 'chart_cal_data': json.dumps(chart_cal_data),
        #
        # 'chart_analise_bruta_label': json.dumps(chart_analise_bruta_label),
        # 'chart_analise_bruta_dados_turbidez': chart_analise_bruta_dados_turbidez,
        # 'chart_analise_bruta_dados_alcalinidade': chart_analise_bruta_dados_alcalinidade,
        # 'chart_analise_bruta_dados_gas_carbonico': chart_analise_bruta_dados_gas_carbonico,
        # 'chart_analise_bruta_dados_ph': chart_analise_bruta_dados_ph
    }
    return render(request, 'portal/dashboard.html', context)

@permission_required('is_superuser')
def import_form(request):
    # try:
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read())

        # VERIFICA O ARQUIVO A PARTIR DA LINHA 2
        for n in imported_data[0:]:
            if str(n[2]) == 'Aluno':
                try:
                    aluno = get_object_or_404(Aluno, data_resposta=n[0])
                except:
                    aluno = None

                if not aluno:
                    aluno = Aluno()

                    aluno.data_resposta = str(n[0])
                    aluno.posicao = str(n[59])
                    aluno.campus = str(n[40])
                    aluno.nivel_curso = str(n[46])
                    aluno.avaliacao_moodle = int(n[54])
                    aluno.avaliacao_conteudo = int(n[52])
                    aluno.avaliacao_orientacoes = int(n[50])
                    aluno.acesso_internet = str(n[41])
                    aluno.deficiencia = str(n[47])
                    aluno.transtorno = str(n[48])
                    aluno.auxilio = str(n[57])

                    aluno.save()

            if str(n[2]) == 'TAE':
                try:
                    tae = get_object_or_404(Tae, data_resposta=n[0])
                except:
                    tae = None

                if not tae:
                    tae = Tae()

                    tae.data_resposta = str(n[0])
                    tae.opiniao = str(n[24])
                    tae.posicao = str(n[25])
                    tae.campus = str(n[3])
                    tae.acesso_internet = str(n[4])
                    tae.formacao_ead = str(n[9])
                    tae.competencia_avaliacao = str(n[10])
                    tae.competencia_desenvolvimento = str(n[11])
                    tae.competencia_design = str(n[12])
                    tae.competencia_elaboracao = str(n[13])
                    tae.competencia_ensino = str(n[14])
                    tae.competencia_plataforma = str(n[15])
                    tae.competencia_producao = str(n[16])
                    tae.competencia_roteiro = str(n[17])
                    tae.competencia_sala = str(n[18])
                    tae.competencia_simulador = str(n[19])
                    tae.competencia_rnp = str(n[20])
                    tae.avaliacao_jornada = int(n[22])
                    tae.avaliacao_producao = int(n[23])

                    tae.save()

            if str(n[2]) == 'Professor':
                try:
                    docente = get_object_or_404(Docente, data_resposta=n[0])
                except:
                    docente = None

                if not docente:
                    docente = Docente()

                    docente.data_resposta = str(n[0])
                    docente.opiniao = str(n[38])
                    docente.posicao = str(n[39])
                    docente.campus = str(n[26])
                    docente.acesso_internet = str(n[27])
                    docente.promovendo_ar = str(n[32])
                    docente.competencia_avaliacao = str(n[60])
                    docente.competencia_desenvolvimento = str(n[61])
                    docente.competencia_design = str(n[62])
                    docente.competencia_elaboracao = str(n[63])
                    docente.competencia_ensino = str(n[64])
                    docente.competencia_plataforma = str(n[65])
                    docente.competencia_producao = str(n[66])
                    docente.competencia_roteiro = str(n[67])
                    docente.competencia_sala = str(n[68])
                    docente.competencia_simulador = str(n[69])
                    docente.competencia_rnp = str(n[70])
                    docente.avaliacao_experiencia = int(n[34])

                    docente.save()

        messages.success(request, 'Dados importados')
    context = {
    }

    return render(request, 'portal/import_form.html', context)

# except:
#     return HttpResponse('Deu erro')
