from django.db import models


# Create your models here.
class Aluno(models.Model):
    data_resposta = models.DateTimeField(verbose_name='Data/Hora da Resposta')
    posicao = models.CharField(verbose_name='Posição', max_length=255)
    campus = models.CharField(verbose_name='Campus', max_length=150)
    nivel_curso = models.CharField(verbose_name='Nível Curso', max_length=150)
    auxilio = models.CharField(verbose_name='Auxílio', max_length=3)
    avaliacao_moodle = models.PositiveIntegerField(verbose_name='Avaliação Moodle')
    avaliacao_conteudo = models.PositiveIntegerField(verbose_name='Avaliação Conteúdo do Professor')
    avaliacao_orientacoes = models.PositiveIntegerField(verbose_name='Avaliação Orientações do Professor')
    acesso_internet = models.CharField(verbose_name='Acesso à Internet', max_length=255)
    deficiencia = models.CharField(verbose_name='Deficiência Física', max_length=150)
    transtorno = models.CharField(verbose_name='Transtorno de Aprendizagem ou Desenvolvimento', max_length=150)
    possui_pc = models.CharField(verbose_name='PC ou Notebook', max_length=3, blank=True, null=True)
    possui_celular = models.CharField(verbose_name='Celular Smartphone', max_length=3, blank=True, null=True)
    possui_tablet = models.CharField(verbose_name='Tablet', max_length=3, blank=True, null=True)
    possui_tv = models.CharField(verbose_name='Smart TV', max_length=3, blank=True, null=True)

    class Meta:
        ordering = ['campus', 'nivel_curso']
        verbose_name = 'Resposta do Aluno'
        verbose_name_plural = 'Respostas dos Alunos'


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
