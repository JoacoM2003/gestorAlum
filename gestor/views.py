from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Alumno, Materia, Inscripcion, MateriaComision, Profesor
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registered")
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    else:
        return render(request, 'sign/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'sign/signin.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('signin')

@login_required
def signout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')

@login_required
def perfil(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    if hasattr(request.user, 'alumno'):
        alumno = Alumno.objects.get(user=request.user)  # Obtener el Alumno asociado al usuario

        if request.method == "POST":
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.email = request.POST['email']
            request.user.save()

            alumno.dni = request.POST['dni']
            alumno.telefono = request.POST['telefono']
            alumno.direccion = request.POST['direccion']
            alumno.save()

            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("home")
        return render(request, "alumnos/perfil.html", {"user": request.user, "alumno": alumno})
    
    elif hasattr(request.user, 'profesor'):
        profesor = Profesor.objects.get(user=request.user)  # Obtener el Profesor asociado al usuario

        if request.method == "POST":
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.email = request.POST['email']
            request.user.save()

            profesor.dni = request.POST['dni']
            profesor.telefono = request.POST['telefono']
            profesor.direccion = request.POST['direccion']
            profesor.save()

            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("home")
        return render(request, "profesores/perfil.html", {"user": request.user, "profesor": profesor})

@login_required
def editar_usuario(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("perfil")
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, "alumnos/editar_usuario.html", {"form": form})

@login_required
def cambiar_contraseña(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa después del cambio
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect("perfil")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "alumnos/cambiar_contraseña.html", {"form": form})

def materias(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    materias = Materia.objects.all()

    # Obtener inscripciones del alumno
    inscripciones = Inscripcion.objects.filter(alumno=alumno)
    comisiones_inscritas = [insc.materia_comision.id for insc in inscripciones]
    materias_inscritas = {insc.materia_comision.materia for insc in inscripciones}
    
    # Obtener materias aprobadas por el alumno
    materias_aprobadas = set()
    for inscripcion in inscripciones:
        if inscripcion.aprobado:
            materias_aprobadas.add(inscripcion.materia_comision.materia)

    # Obtener materias con nota menor a 4
    materias_no_aprobadas = set()
    for inscripcion in inscripciones:
        if inscripcion.nota is not None and inscripcion.nota < 4:
            materias_no_aprobadas.add(inscripcion.materia_comision.materia)

    return render(request, "alumnos/materias.html", {
        "materias": materias,
        "comisiones_inscritas": comisiones_inscritas,
        "materias_inscritas": materias_inscritas,
        "materias_aprobadas": materias_aprobadas,
        "materias_no_aprobadas": materias_no_aprobadas
    })

@login_required
def detalle_materia(request, materia_id):
    materia = Materia.objects.get(id=materia_id)
    comisiones = materia.materia_comisiones.all()
    alumno = Alumno.objects.get(user=request.user)

    # Verificar si el alumno ya está inscrito en alguna comisión de la materia
    if Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=materia).exists():
        inscripcion = Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=materia).first()
        if inscripcion.nota is None:
            messages.info(request, "Ya estás inscrito en una comisión de esta materia.")
            return redirect("materias")

    return render(request, "alumnos/detalle_materia.html", {
        "materia": materia,
        "comisiones": comisiones
    })

def inscribir_comision(request, comision_id):
    comision = get_object_or_404(MateriaComision, id=comision_id)
    alumno = get_object_or_404(Alumno, user=request.user)

    # Verificar si el alumno tiene una nota menor a 4 en alguna comisión de la misma materia
    inscripcion_existente = Inscripcion.objects.filter(alumno=alumno, materia_comision__materia=comision.materia).first()
    if inscripcion_existente:
        if inscripcion_existente.nota is not None and inscripcion_existente.nota < 4:
            inscripcion_existente.delete()
        else:
            messages.info(request, "Ya estás inscrito en una comisión de esta materia.")
            return redirect("materias")


    # Inscribir al alumno en la comisión seleccionada
    inscripcion = Inscripcion(alumno=alumno, materia_comision=comision)
    inscripcion.save()
    messages.success(request, f"Te has inscrito correctamente en {comision.materia.nombre} - {comision.comision.nombre}.")

    return redirect("materias")


@login_required
def desinscribir_materia(request, materia_id):
    """ Permite a un alumno desinscribirse de todas las comisiones de una materia. """
    alumno = get_object_or_404(Alumno, user=request.user)
    materia = get_object_or_404(Materia, id=materia_id)

    # Buscar todas las inscripciones del alumno en cualquier comisión de la materia
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
