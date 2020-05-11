from django.db import models


# Create your models here.
class Aluno(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    nivel_curso = models.CharField(verbose_name='Nível Curso', max_length=150, blank=True, null=True)
    auxilio = models.CharField(verbose_name='Auxílio', max_length=3, blank=True, null=True)
    avaliacao_moodle = models.PositiveIntegerField(verbose_name='Avaliação Moodle', blank=True, null=True)
    avaliacao_conteudo = models.PositiveIntegerField(verbose_name='Avaliação Conteúdo do Professor', blank=True,
                                                     null=True)
    avaliacao_orientacoes = models.PositiveIntegerField(verbose_name='Avaliação Orientações do Professor', blank=True,
                                                        null=True)
    acesso_internet = models.CharField(verbose_name='Acesso à Internet', max_length=255, blank=True, null=True)
    deficiencia = models.CharField(verbose_name='Deficiência Física', max_length=150, blank=True, null=True)
    transtorno = models.CharField(verbose_name='Transtorno de Aprendizagem ou Desenvolvimento', max_length=150)
    possui_pc = models.CharField(verbose_name='PC ou Notebook', max_length=3, blank=True, null=True)
    possui_celular = models.CharField(verbose_name='Celular Smartphone', max_length=3, blank=True, null=True)
    possui_tablet = models.CharField(verbose_name='Tablet', max_length=3, blank=True, null=True)
    possui_tv = models.CharField(verbose_name='Smart TV', max_length=3, blank=True, null=True)
    orientacao_enviada = models.CharField(verbose_name='Professores Enviaram Orientações?', max_length=150, blank=True,
                                          null=True)
    conteudo_enviado = models.CharField(verbose_name='Professores Enviaram Conteúdo ?', max_length=150, blank=True,
                                        null=True)
    melhoria_ava = models.TextField(verbose_name='Melhorias no AVA', blank=True, null=True)
    docente_melhorar = models.TextField(verbose_name='Melhorias na Comunicação do Docente', blank=True, null=True)

    class Meta:
        ordering = ['-data_resposta', 'campus', 'nivel_curso']
        verbose_name = 'Resposta do Aluno'
        verbose_name_plural = '1 - Respostas dos Alunos'


class Docente(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    opiniao = models.CharField(verbose_name='Opinião Atividades Remotas', max_length=50, blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    acesso_internet = models.CharField(verbose_name='Acesso à Internet', max_length=255, blank=True, null=True)
    promovendo_ar = models.CharField(verbose_name='Promovendo Atividades Remotas', max_length=3, blank=True, null=True)
    competencia_avaliacao = models.CharField(verbose_name='Avaliação online', max_length=150, blank=True, null=True)
    competencia_desenvolvimento = models.CharField(verbose_name='Desenvolvimento de Objetos de Aprendizagem',
                                                   max_length=150, blank=True, null=True)
    competencia_design = models.CharField(verbose_name='Design Educacional (Instrucional)', max_length=150, blank=True,
                                          null=True)
    competencia_elaboracao = models.CharField(verbose_name='Elaboração de Projeto Pedagógico de Curso para EAD',
                                              max_length=150, blank=True, null=True)
    competencia_ensino = models.CharField(verbose_name='Ensino Híbrido', max_length=150, blank=True, null=True)
    competencia_plataforma = models.CharField(verbose_name='Plataforma Moodle ', max_length=150, blank=True, null=True)
    competencia_producao = models.CharField(verbose_name='Produção de livro-texto', max_length=150, blank=True,
                                            null=True)
    competencia_roteiro = models.CharField(verbose_name='Roteiro para vídeo aulas', max_length=150, blank=True,
                                           null=True)
    competencia_sala = models.CharField(verbose_name='Sala de aula invertida', max_length=150, blank=True, null=True)
    competencia_simulador = models.CharField(verbose_name='Simuladores e Ambientes de Imersão', max_length=150,
                                             blank=True, null=True)
    competencia_rnp = models.CharField(verbose_name='WebConferência RNP', max_length=150, blank=True, null=True)
    avaliacao_experiencia = models.PositiveIntegerField(verbose_name='Avaliação Experiência', blank=True, null=True)
    possui_pc = models.CharField(verbose_name='PC ou Notebook', max_length=3, blank=True, null=True)
    possui_celular = models.CharField(verbose_name='Celular Smartphone', max_length=3, blank=True, null=True)
    possui_tablet = models.CharField(verbose_name='Tablet', max_length=3, blank=True, null=True)
    possui_tv = models.CharField(verbose_name='Smart TV', max_length=3, blank=True, null=True)
    pontos_positivos_negativos = models.TextField(verbose_name='Pontos Positivos e Negativos', blank=True, null=True)
    estrategia_ponto_negativo = models.TextField(verbose_name='Estratégias Superar Pontos Negativos', blank=True,
                                                 null=True)
    sugestao_comissao = models.TextField(verbose_name='Sugestão à Comissão', blank=True, null=True)

    class Meta:
        ordering = ['-data_resposta', 'campus']
        verbose_name = 'Resposta do Docente'
        verbose_name_plural = '1 - Respostas dos Docentes'


class Tae(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    opiniao = models.CharField(verbose_name='Opinião Atividades Remotas', max_length=50, blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    acesso_internet = models.CharField(verbose_name='Acesso à Internet', max_length=255, blank=True, null=True)
    formacao_ead = models.CharField(verbose_name='Formação em EaD', max_length=3, blank=True, null=True)
    competencia_avaliacao = models.CharField(verbose_name='Avaliação online', max_length=150, blank=True, null=True)
    competencia_desenvolvimento = models.CharField(verbose_name='Desenvolvimento de Objetos de Aprendizagem',
                                                   max_length=150, blank=True, null=True)
    competencia_design = models.CharField(verbose_name='Design Educacional (Instrucional)', max_length=150, blank=True,
                                          null=True)
    competencia_elaboracao = models.CharField(verbose_name='Elaboração de Projeto Pedagógico de Curso para EAD',
                                              max_length=150, blank=True, null=True)
    competencia_ensino = models.CharField(verbose_name='Ensino Híbrido', max_length=150, blank=True, null=True)
    competencia_plataforma = models.CharField(verbose_name='Plataforma Moodle ', max_length=150, blank=True, null=True)
    competencia_producao = models.CharField(verbose_name='Produção de livro-texto', max_length=150, blank=True,
                                            null=True)
    competencia_roteiro = models.CharField(verbose_name='Roteiro para vídeo aulas', max_length=150, blank=True,
                                           null=True)
    competencia_sala = models.CharField(verbose_name='Sala de aula invertida', max_length=150, blank=True, null=True)
    competencia_simulador = models.CharField(verbose_name='Simuladores e Ambientes de Imersão', max_length=150,
                                             blank=True, null=True)
    competencia_rnp = models.CharField(verbose_name='WebConferência RNP', max_length=150, blank=True, null=True)
    avaliacao_jornada = models.PositiveIntegerField(verbose_name='Avaliação Jornada em Casa', blank=True, null=True)
    avaliacao_producao = models.PositiveIntegerField(verbose_name='Avaliação Produção', blank=True, null=True)
    possui_pc = models.CharField(verbose_name='PC ou Notebook', max_length=3, blank=True, null=True)
    possui_celular = models.CharField(verbose_name='Celular Smartphone', max_length=3, blank=True, null=True)
    possui_tablet = models.CharField(verbose_name='Tablet', max_length=3, blank=True, null=True)
    possui_tv = models.CharField(verbose_name='Smart TV', max_length=3, blank=True, null=True)
    outras_capacitacoes = models.TextField(verbose_name='Outras Capacitações EaD', blank=True, null=True)

    class Meta:
        ordering = ['-data_resposta', 'campus']
        verbose_name = 'Resposta do TAE'
        verbose_name_plural = '1 - Respostas dos TAEs'

class Aluno2(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    nivel_curso = models.CharField(verbose_name='Nível Curso', max_length=150, blank=True, null=True)
    periodo_letivo = models.CharField(verbose_name='Período Letivo', max_length=150, blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    acesso_internet = models.CharField(verbose_name='Acesso à Internet', max_length=255, blank=True, null=True)
    possui_pc = models.CharField(verbose_name='PC ou Notebook', max_length=3, blank=True, null=True)
    possui_celular = models.CharField(verbose_name='Celular Smartphone', max_length=3, blank=True, null=True)
    possui_tablet = models.CharField(verbose_name='Tablet', max_length=3, blank=True, null=True)
    possui_tv = models.CharField(verbose_name='Smart TV', max_length=3, blank=True, null=True)
    auxilio = models.CharField(verbose_name='Auxílio', max_length=3, blank=True, null=True)
    avaliacao_conteudo = models.PositiveIntegerField(verbose_name='Avaliação Conteúdo do Professor', blank=True, null=True)
    avaliacao_orientacoes = models.PositiveIntegerField(verbose_name='Avaliação Orientações do Professor', blank=True, null=True)
    avaliacao_comunicacao = models.PositiveIntegerField(verbose_name='Avaliação Comunicação do Professor', blank=True, null=True)
    horas_estudo = models.CharField(verbose_name='Horas de Estudo por Dia', max_length=50, blank=True, null=True)
    avaliacao_ar = models.PositiveIntegerField(verbose_name='Avaliação Atividades Remotas', blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)


    class Meta:
        ordering = ['-data_resposta', 'campus', 'nivel_curso']
        verbose_name = 'Resposta do Aluno 2'
        verbose_name_plural = '2 - Respostas dos Alunos'

class Docente2(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    promovendo_ar = models.CharField(verbose_name='Promovendo Atividades Remotas', max_length=3, blank=True, null=True)
    avaliacao_ar = models.PositiveIntegerField(verbose_name='Avaliação Atividades Remotas', blank=True, null=True)
    avaliacao_comunicao = models.PositiveIntegerField(verbose_name='Avaliação Comunicação com Alunos', blank=True, null=True)
    avaliacao_participacao = models.PositiveIntegerField(verbose_name='Avaliação Participação Alunos', blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)
    sugestao_suspensao = models.TextField(verbose_name='Sugestão Atividades Suspensão', blank=True, null=True)
    sugestao_capacitacao = models.TextField(verbose_name='Sugestão Capacitação', blank=True, null=True)

    class Meta:
        ordering = ['-data_resposta', 'campus']
        verbose_name = 'Resposta do Docente 2'
        verbose_name_plural = '2 - Respostas dos Docentes'

class Tae2(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    setor = models.CharField(verbose_name='Setor Lotação', max_length=50, blank=True, null=True)
    avaliacao_producao = models.CharField(verbose_name='Avaliação Produção', max_length=15, blank=True, null=True)
    avaliacao_rendimento = models.PositiveIntegerField(verbose_name='Avaliação Rendimento', blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)
    sugestao_suspensao = models.TextField(verbose_name='Sugestão Atividades Suspensão', blank=True, null=True)
    sugestao_capacitacao = models.TextField(verbose_name='Sugestão Capacitação', blank=True, null=True)

    class Meta:
        ordering = ['-data_resposta', 'campus']
        verbose_name = 'Resposta do TAE 2'
        verbose_name_plural = '2 - Respostas dos TAEs'

class DocenteReitoria(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta', blank=True, null=True)
    campus = models.CharField(verbose_name='Campus', max_length=150, blank=True, null=True)
    setor = models.CharField(verbose_name='Setor Lotação', max_length=50, blank=True, null=True)
    avaliacao_producao = models.CharField(verbose_name='Avaliação Produção', max_length=15, blank=True, null=True)
    avaliacao_rendimento = models.PositiveIntegerField(verbose_name='Avaliação Rendimento', blank=True, null=True)
    posicao = models.CharField(verbose_name='Posição', max_length=255, blank=True, null=True)
    sugestao_suspensao = models.TextField(verbose_name='Sugestão Atividades Suspensão', blank=True, null=True)
    sugestao_capacitacao = models.TextField(verbose_name='Sugestão Capacitação', blank=True, null=True)

    class Meta:
        ordering = ['-data_resposta', 'campus']
        verbose_name = 'Resposta do Docente na Reitoria 2'
        verbose_name_plural = '2 - Respostas dos Docentes na Reitoria'

class DificuldadeCasa(models.Model):
    aluno = models.ForeignKey(Aluno2, on_delete=models.CASCADE, blank=True, null=True)
    docente = models.ForeignKey(Docente2, on_delete=models.CASCADE, blank=True, null=True)
    docente_reitoria = models.ForeignKey(DocenteReitoria, on_delete=models.CASCADE, blank=True, null=True)
    tae = models.ForeignKey(Tae2, on_delete=models.CASCADE, blank=True, null=True)
    dificuldade = models.CharField(verbose_name='Dificuldade', max_length=100, blank=True, null=True)

class GrupoRisco(models.Model):
    aluno = models.ForeignKey(Aluno2, on_delete=models.CASCADE, blank=True, null=True)
    docente = models.ForeignKey(Docente2, on_delete=models.CASCADE, blank=True, null=True)
    docente_reitoria = models.ForeignKey(DocenteReitoria, on_delete=models.CASCADE, blank=True, null=True)
    tae = models.ForeignKey(Tae2, on_delete=models.CASCADE, blank=True, null=True)
    grupo = models.CharField(verbose_name='Grupo de Risco', max_length=30, blank=True, null=True)
