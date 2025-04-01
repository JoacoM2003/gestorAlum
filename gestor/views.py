from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Alumno, Materia, Inscripcion
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
def perfil_alumno(request):
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

@login_required
def editar_usuario(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("perfil_alumno")
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
            return redirect("perfil_alumno")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "alumnos/cambiar_contraseña.html", {"form": form})

@login_required
def materias(request):
    materias = Materia.objects.all()
    materias_inscritas = Inscripcion.objects.filter(alumno=request.user.alumno).values_list('materia_id', flat=True)
    print(materias_inscritas)
    
    return render(request, "alumnos/materias.html", {
        "materias": materias,
        "materias_inscritas": materias_inscritas
    })

@login_required
def detalle_materia(request, materia_id):
    materia = Materia.objects.get(id=materia_id)
    comisiones = materia.materia_comisiones.all()
    print(comisiones)
    
    return render(request, "alumnos/detalle_materia.html", {
        "materia": materia,
        "comisiones": comisiones
    })

@login_required
def inscribir_materia(request, materia_id):
    materia = Materia.objects.get(id=materia_id)
    alumno = Alumno.objects.get(user=request.user)
    
    if Inscripcion.objects.filter(alumno=alumno, materia=materia).exists():
        messages.info(request, "Ya est s inscrito en esta materia.")
    else:
        inscripcion = Inscripcion(alumno=alumno, materia=materia)
        inscripcion.save()
        messages.success(request, "Te has inscrito correctamente en la materia.")
    
    return redirect("materias")


@login_required
def desinscribir_materia(request, materia_id):
    materia = Materia.objects.get(id=materia_id)
    alumno = Alumno.objects.get(user=request.user)
    
    inscripcion = Inscripcion.objects.filter(alumno=alumno, materia=materia).first()
    if inscripcion:
        inscripcion.delete()
        messages.success(request, "Te has desinscrito correctamente de la materia.")
    else:
        messages.info(request, "No estas inscrito en esta materia.")
    
    return redirect("materias")