# Generated by Django 5.1.7 on 2025-03-31 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0005_remove_comision_alumnos_inscritos_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='comision',
        ),
        migrations.AddField(
            model_name='materia',
            name='comisiones',
            field=models.ManyToManyField(blank=True, to='gestor.comision'),
        ),
    ]
