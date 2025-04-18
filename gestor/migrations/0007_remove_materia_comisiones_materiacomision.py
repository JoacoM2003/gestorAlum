# Generated by Django 5.1.7 on 2025-03-31 05:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0006_remove_materia_comision_materia_comisiones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='comisiones',
        ),
        migrations.CreateModel(
            name='MateriaComision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cupo_maximo', models.PositiveIntegerField(default=30)),
                ('comision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comision_materias', to='gestor.comision')),
                ('horario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestor.horario')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materia_comisiones', to='gestor.materia')),
            ],
        ),
    ]
