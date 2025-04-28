from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Alumno, Materia, Inscripcion, MateriaComision, Profesor, RolProfesor, Horario
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def es_alumno(user):
    return hasattr(user, 'alumno')

def es_profesor(user):
    return hasattr(user, 'profesor')

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(request, user)
        messages.success(request, "Te has registrado exitosamente.")
        return redirect('home')
    return render(request, 'sign/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            messages.success(request, "Sesión iniciada correctamente.")
            return redirect('home')
        messages.error(request, "Usuario o contraseña inválidos.")
    return render(request, 'sign/signin.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('home')

@login_required
def perfil(request):
    user = request.user
    perfil_obj = getattr(user, 'alumno', None) or getattr(user, 'profesor', None)
    template = 'alumnos/perfil.html' if es_alumno(user) else 'profesores/perfil.html'

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        perfil_obj.dni = request.POST['dni']
        perfil_obj.telefono = request.POST['telefono']
        perfil_obj.direccion = request.POST['direccion']
        perfil_obj.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("home")

    return render(request, template, {"user": user, "alumno" if es_alumno(user) else "profesor": perfil_obj})

@login_required
def editar_usuario(request):
    form = UserChangeForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect("perfil")
    return render(request, "alumnos/editar_usuario.html", {"form": form})

@login_required
def cambiar_contraseña(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Contraseña actualizada correctamente.")
        return redirect("perfil")
    return render(request, "alumnos/cambiar_contraseña.html", {"form": form})

@login_required
def ingresar_nota(request):
    if request.method == "POST":
        inscripcion = get_object_or_404(Inscripcion, id=request.POST.get("inscripcion_id"))
        inscripcion.nota = int(request.POST.get("nota"))
        inscripcion.save()
        messages.success(request, "Nota ingresada correctamente.")
    return redirect("materias")

@login_required
def profesores(request):
    return render(request, "profesores/profesores.html", {"profesores": Profesor.objects.all()})

@login_required
def detalle_profesor(request, profesor_id):
    profesor = get_object_or_404(Profesor, id=profesor_id)
    comisiones = RolProfesor.objects.filter(profesor=profesor)
    return render(request, "profesores/detalle_profesor.html", {"profesor": profesor, "comisiones": comisiones})

@login_required
def asignar_profesores(request):
    if request.method == "POST":
        profesor = get_object_or_404(Profesor, id=request.POST.get("profesor"))
        comision = get_object_or_404(MateriaComision, id=request.POST.get("comision"))
        rol = request.POST.get("rol_profesor")

        if not RolProfesor.objects.filter(profesor=profesor, materia_comision=comision).exists():
            RolProfesor.objects.create(profesor=profesor, materia_comision=comision, rol=rol)
            messages.success(request, "Profesor asignado correctamente.")
        else:
            messages.warning(request, "El profesor ya está asignado a esta comisión.")
        return redirect("profesores")

    return render(request, "asignar_profesor.html", {
        "profesores": Profesor.objects.all(),
        "comisiones": MateriaComision.objects.all(),
        "roles": RolProfesor.ROL_CHOICES
    })

@login_required
def eliminar_rol_profesor(request, rol_profesor_id):
    get_object_or_404(RolProfesor, id=rol_profesor_id).delete()
    messages.success(request, "Profesor eliminado correctamente.")
    return redirect("profesores")

def materias(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    if hasattr(request.user, 'alumno'):
        alumno = get_object_or_404(Alumno, user=request.user)
        inscripciones = Inscripcion.objects.filter(alumno=alumno)
        materias = Materia.objects.all()

        comisiones_inscritas = [insc.materia_comision.id for insc in inscripciones]
        materias_inscritas = {insc.materia_comision.materia for insc in inscripciones}
        materias_aprobadas = {i.materia_comision.materia for i in inscripciones if i.aprobado}
        materias_no_aprobadas = {i.materia_comision.materia for i in inscripciones if i.nota is not None and i.nota < 4}

        return render(request, "alumnos/materias.html", {
            "materias": materias,
            "comisiones_inscritas": comisiones_inscritas,
            "materias_inscritas": materias_inscritas,
            "materias_aprobadas": materias_aprobadas,
            "materias_no_aprobadas": materias_no_aprobadas
        })

    elif hasattr(request.user, 'profesor'):
        profesor = get_object_or_404(Profesor, user=request.user)
        roles = RolProfesor.objects.filter(profesor=profesor)
        materias = Materia.objects.all()
        materias_asignadas = {rol.materia_comision.materia for rol in roles}

        return render(request, "profesores/materias.html", {
            "materias": materias,
            "materias_asignadas": materias_asignadas
        })

@login_required
def detalle_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)

    if hasattr(request.user, 'alumno'):
        alumno = get_object_or_404(Alumno, user=request.user)
        ya_inscripto = Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=materia).first()

        if ya_inscripto and ya_inscripto.nota is None:
            messages.info(request, "Ya estás inscrito en una comisión de esta materia.")
            return redirect("materias")

        comisiones = materia.materia_comisiones.all()
        return render(request, "alumnos/detalle_materia.html", {
            "materia": materia,
            "comisiones": comisiones
        })

    elif hasattr(request.user, 'profesor'):
        profesor = get_object_or_404(Profesor, user=request.user)
        comisiones = materia.materia_comisiones.filter(rolprofesor__profesor=profesor)
        return render(request, "profesores/detalle_materia.html", {
            "materia": materia,
            "comisiones": comisiones
        })

@login_required
def detalle_comision(request, comision_id):
    comision = get_object_or_404(MateriaComision, id=comision_id)
    inscripciones = Inscripcion.objects.filter(materia_comision=comision)
    alumnos = Alumno.objects.filter(inscripcion__in=inscripciones)
    return render(request, "profesores/detalle_comision.html", {
        "comision": comision,
        "alumnos": alumnos,
        "inscripciones": inscripciones
    })

@login_required
def inscribir_comision(request, comision_id):
    comision = get_object_or_404(MateriaComision, id=comision_id)
    alumno = get_object_or_404(Alumno, user=request.user)

    inscripcion = Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=comision.materia).first()
    if inscripcion:
        if inscripcion.nota is not None and inscripcion.nota < 4:
            inscripcion.delete()
        else:
            messages.info(request, "Ya estás inscrito en una comisión de esta materia.")
            return redirect("materias")

    Inscripcion.objects.create(alumno=alumno, materia_comision=comision)
    messages.success(request, f"Te has inscrito correctamente en {comision.materia.nombre} - {comision.comision.nombre}.")
    return redirect("materias")

@login_required
def desinscribir_materia(request, materia_id):
    alumno = get_object_or_404(Alumno, user=request.user)
    materia = get_object_or_404(Materia, id=materia_id)

    inscripciones = Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=materia)

    if inscripciones.exists():
        inscripciones.delete()
        messages.success(request, f"Te has desinscrito correctamente de todas las comisiones de {materia.nombre}.")
    elif Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=materia, aprobado=True).exists():
        messages.info(request, "Ya has aprobado esta materia.")
    else:
        messages.info(request, "No estás inscrito en ninguna comisión de esta materia.")

    return redirect("materias")

@login_required
def calificaciones(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    inscripciones = Inscripcion.objects.filter(alumno=alumno)
    return render(request, "alumnos/calificaciones.html", {"inscripciones": inscripciones})

@login_required
def ingresar_nota(request):
    if request.method == "POST":
        inscripcion_id = request.POST.get("inscripcion_id")
        nota = request.POST.get("nota")
        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
        inscripcion.nota = int(nota)
        inscripcion.save()
        messages.success(request, "Nota ingresada correctamente.")
    return redirect("materias")

@login_required
def horarios(request):
    user = request.user

    if hasattr(user, 'alumno'):
        inscripciones = Inscripcion.objects.filter(alumno__user=user, aprobado=False)
        comisiones = [inscripcion.materia_comision for inscripcion in inscripciones]
    elif hasattr(user, 'profesor'):
        roles = RolProfesor.objects.filter(profesor__user=user)
        comisiones = [rol.materia_comision for rol in roles]
    else:
        return redirect("home")

    horarios_por_dia = {
        "Lunes": [], "Martes": [], "Miércoles": [],
        "Jueves": [], "Viernes": [], "Sábado": [], "Domingo": []
    }

    for comision in comisiones:
        for horario in comision.horarios.all():
            horarios_por_dia[horario.dias].append(horario)

    for dia in horarios_por_dia:
        horarios_por_dia[dia].sort(key=lambda h: h.hora_inicio)

    return render(request, "horarios.html", {"horarios": horarios_por_dia})
