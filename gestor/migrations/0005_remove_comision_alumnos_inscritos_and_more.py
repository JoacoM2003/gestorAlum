# Generated by Django 5.1.7 on 2025-03-31 04:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0004_alter_comision_cupos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comision',
            name='alumnos_inscritos',
        ),
        migrations.RemoveField(
            model_name='comision',
            name='cupos',
        ),
        migrations.RemoveField(
            model_name='comision',
            name='horario',
        ),
        migrations.RemoveField(
            model_name='comision',
            name='materia',
        ),
        migrations.RemoveField(
            model_name='comision',
            name='profesor',
        ),
        migrations.RemoveField(
            model_name='inscripcion',
            name='comision',
        ),
        migrations.AddField(
            model_name='inscripcion',
            name='materia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestor.materia'),
        ),
        migrations.AddField(
            model_name='materia',
            name='comision',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestor.comision'),
        ),
        migrations.AddField(
            model_name='materia',
            name='profesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestor.profesor'),
        ),
    ]
