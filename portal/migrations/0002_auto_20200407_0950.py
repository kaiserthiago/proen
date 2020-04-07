# Generated by Django 2.2.10 on 2020-04-07 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aluno',
            options={'ordering': ['-data_resposta', 'campus', 'nivel_curso'], 'verbose_name': 'Resposta do Aluno', 'verbose_name_plural': 'Respostas dos Alunos'},
        ),
        migrations.AlterModelOptions(
            name='docente',
            options={'ordering': ['-data_resposta', 'campus'], 'verbose_name': 'Resposta do Docente', 'verbose_name_plural': 'Respostas dos Docentes'},
        ),
        migrations.AlterModelOptions(
            name='tae',
            options={'ordering': ['-data_resposta', 'campus'], 'verbose_name': 'Resposta do TAE', 'verbose_name_plural': 'Respostas dos TAEs'},
        ),
        migrations.AddField(
            model_name='aluno',
            name='conteudo_enviado',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Professores Enviaram Conteúdo ?'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='orientacao_enviada',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Professores Enviaram Orientações?'),
        ),
    ]