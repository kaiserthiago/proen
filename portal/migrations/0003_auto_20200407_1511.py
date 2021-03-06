# Generated by Django 2.2.10 on 2020-04-07 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20200407_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='docente_melhorar',
            field=models.TextField(blank=True, null=True, verbose_name='Melhorias na Comunicação do Docente'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='melhoria_ava',
            field=models.TextField(blank=True, null=True, verbose_name='Melhorias no AVA'),
        ),
        migrations.AddField(
            model_name='docente',
            name='estrategia_ponto_negativo',
            field=models.TextField(blank=True, null=True, verbose_name='Estratégias Superar Pontos Negativos'),
        ),
        migrations.AddField(
            model_name='docente',
            name='pontos_positivos_negativos',
            field=models.TextField(blank=True, null=True, verbose_name='Pontos Positivos e Negativos'),
        ),
        migrations.AddField(
            model_name='docente',
            name='sugestao_comissao',
            field=models.TextField(blank=True, null=True, verbose_name='Sugestão à Comissão'),
        ),
        migrations.AddField(
            model_name='tae',
            name='outras_capacitacoes',
            field=models.TextField(blank=True, null=True, verbose_name='Outras Capacitações EaD'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='acesso_internet',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Acesso à Internet'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='auxilio',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='Auxílio'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avaliacao_conteudo',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Avaliação Conteúdo do Professor'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avaliacao_moodle',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Avaliação Moodle'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avaliacao_orientacoes',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Avaliação Orientações do Professor'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='campus',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Campus'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='data_resposta',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data/Hora da Resposta'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='deficiencia',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Deficiência Física'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='nivel_curso',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nível Curso'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='posicao',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Posição'),
        ),
    ]
