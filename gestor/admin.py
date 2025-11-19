# gestor/admin.py

from django.contrib import admin
from .models import Alumno, Profesor, Materia, Comision, MateriaComision, RolProfesor, Horario, Inscripcion

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('legajo', 'user', 'dni', 'activo', 'fecha_inscripcion')
    list_filter = ('activo', 'fecha_inscripcion')
    search_fields = ('legajo', 'dni', 'user__first_name', 'user__last_name')

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('legajo', 'user', 'dni', 'activo')
    list_filter = ('activo',)
    search_fields = ('legajo', 'dni', 'user__first_name', 'user__last_name')

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'año', 'creditos')
    list_filter = ('año',)
    search_fields = ('codigo', 'nombre')

@admin.register(Comision)
class ComisionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(MateriaComision)
class MateriaComisionAdmin(admin.ModelAdmin):
    list_display = ('materia', 'comision', 'cupo_maximo', 'cantidad_inscriptos')
    list_filter = ('materia', 'comision')
    search_fields = ('materia__nombre', 'comision__nombre')
    # ELIMINAR: filter_horizontal = ('horarios',)  # Ya no existe este campo

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('materia_comision', 'dia', 'hora_inicio', 'hora_fin')
    list_filter = ('dia', 'materia_comision__materia')
    search_fields = ('materia_comision__materia__nombre', 'materia_comision__comision__nombre')

@admin.register(RolProfesor)
class RolProfesorAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'materia_comision', 'rol')
    list_filter = ('rol',)
    search_fields = ('profesor__user__first_name', 'profesor__user__last_name')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia_comision', 'año_cursada', 'nota', 'aprobado', 'fecha_inscripcion')
    list_filter = ('aprobado', 'año_cursada', 'fecha_inscripcion')
    search_fields = ('alumno__legajo', 'alumno__user__first_name', 'alumno__user__last_name')