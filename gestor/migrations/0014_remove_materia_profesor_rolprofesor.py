# Generated by Django 5.1.4 on 2025-04-02 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0013_profesor_direccion_profesor_fecha_nacimiento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='profesor',
        ),
        migrations.CreateModel(
            name='RolProfesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(choices=[('Titular', 'Titular'), ('Ayudante', 'Ayudante')], max_length=100)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.materia')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestor.profesor')),
            ],
        ),
    ]
