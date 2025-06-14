# Generated by Django 5.1.5 on 2025-02-04 17:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('planificadores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre de la sesión (Estudio, Repaso, Descanso, etc.)', max_length=255)),
                ('duracion_minutos', models.PositiveIntegerField(help_text='Duración de la sesión en minutos para ser completada')),
                ('es_obligatoria', models.BooleanField(default=True, help_text='Indica si esta sesión es obligatoria para completar la tarea')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('color', models.CharField(default='#FFFFFF', help_text='Color asociado al estado.', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='TareaTimer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_para_completar', models.PositiveIntegerField(help_text='Número total de sesiones necesarias para completar la tarea')),
                ('cantidad_completadas', models.PositiveIntegerField(default=0, help_text='Número de sesiones completadas actualmente')),
                ('sesiones', models.ManyToManyField(blank=True, help_text='Sesiones asociadas a esta tarea.', to='pomodoro.sesion')),
                ('tarea', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tarea_timer', to='planificadores.tarea')),
            ],
        ),
    ]
