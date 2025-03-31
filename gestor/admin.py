from django.contrib import admin
from django.contrib.auth.models import User
from .models import Alumno, Materia, Comision, Inscripcion, Horario, Profesor
from .forms import AlumnoForm
from django.utils.html import format_html

class AlumnoAdmin(admin.ModelAdmin):
    form = AlumnoForm  # Usar el formulario personalizado
    list_display = ('user', 'dni', 'legajo')
    search_fields = ('user__username', 'dni', 'legajo')
    exclude = ('user',)  # Ocultar el campo 'user' en el admin

    def save_model(self, request, obj, form, change):
        if not obj.user:  # Si no hay usuario, lo creamos
            user = User.objects.create_user(
                username=obj.legajo,  
                password=obj.dni,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            obj.user = user  # Asignamos el usuario al alumno
        super().save_model(request, obj, form, change)

admin.site.register(Alumno, AlumnoAdmin)

admin.site.register(Materia)
admin.site.register(Comision)