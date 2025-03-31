from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('perfil/', views.perfil_alumno, name='perfil_alumno'),
    path('perfil/editar/', views.editar_usuario, name='editar_usuario'),
    path('perfil/cambiar-contraseña/', views.cambiar_contraseña, name='password_change'),
    path('materias/', views.materias, name='materias'),
    path('materias/<int:materia_id>/', views.detalle_materia, name='detalle_materia'),
    
]
