from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_usuario, name='editar_usuario'),
    path('perfil/cambiar-contraseña/', views.cambiar_contraseña, name='password_change'),
    
    path('materias/', views.materias, name='materias'),
    path('materias/<int:materia_id>/', views.detalle_materia, name='detalle_materia'),
    path('inscribir-comision/<int:comision_id>/', views.inscribir_comision, name='inscribir_comision'),
    path('materias/<int:materia_id>/desinscribir/', views.desinscribir_materia, name='desinscribir_materia'),
    path('calificaciones/', views.calificaciones, name='calificaciones'),
    path('detalle-comision/<int:comision_id>/', views.detalle_comision, name='detalle_comision'),
    path('ingresar-nota/', views.ingresar_nota, name='ingresar_nota'),
    
    path('horarios/', views.horarios, name='horarios'),
    
    path('profesores/', views.profesores, name='profesores'),
    path('agregar-profesor/', views.agregar_profesor, name='agregar_profesor'),
    path('profesores/<int:profesor_id>/', views.detalle_profesor, name='detalle_profesor'),
    path('asignar-profesor', views.asignar_profesores, name='asignar_profesor'),
    path('eliminar-rol-profesor/<int:rol_profesor_id>/', views.eliminar_rol_profesor, name='eliminar_rol_profesor'),
    
    path('alumnos/', views.alumnos, name='alumnos'),
    path('agregar-alumno/', views.agregar_alumno, name='agregar_alumno'),

    path('ver_materias', views.ver_materias, name='ver_materias'),
    path('agregar_materia', views.agregar_materia, name='agregar_materia'),
    path('materia/<int:materia_id>', views.ver_materia, name='ver_materia'),
    path('agregar_comision/', views.agregar_comision, name='agregar_comision'),
    path('limpiar-comision/<int:comision_id>/', views.limpiar_comision, name='limpiar_comision'),
        # Agregar a urls.py:
    path('toggle-alumno/<int:alumno_id>/', views.toggle_alumno, name='toggle_alumno'),
    path('toggle-profesor/<int:profesor_id>/', views.toggle_profesor, name='toggle_profesor'),

]
