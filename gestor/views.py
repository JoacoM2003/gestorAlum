from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, AlumnoForm, ProfesorForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Alumno, Materia, Inscripcion, MateriaComision, Profesor, RolProfesor, Horario, Comision
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q

def es_alumno(user):
    return hasattr(user, 'alumno')

def es_profesor(user):
    return hasattr(user, 'profesor')

# ===== HOME Y AUTH =====
def home(request):
    context = {}
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'alumno'):
            alumno = request.user.alumno
            año_actual = datetime.now().year
            inscripciones = Inscripcion.objects.filter(alumno=alumno)
            
            context['total_materias'] = inscripciones.filter(año_cursada=año_actual).count()
            context['materias_aprobadas'] = inscripciones.filter(aprobado=True).count()
            context['materias_cursando'] = inscripciones.filter(nota__isnull=True, año_cursada=año_actual).count()
            context['comisiones_asignadas'] = alumno.comisiones_asignadas.count()
            
            # Calcular promedio
            notas = inscripciones.filter(nota__isnull=False).values_list('nota', flat=True)
            context['promedio'] = round(sum(notas) / len(notas), 2) if notas else 0
            
        elif hasattr(request.user, 'profesor'):
            profesor = request.user.profesor
            context['materias_asignadas'] = profesor.comisiones_dictadas.count()
            context['total_comisiones'] = RolProfesor.objects.filter(profesor=profesor).count()
            
            # Contar alumnos del año actual
            año_actual = datetime.now().year
            comisiones_ids = RolProfesor.objects.filter(profesor=profesor).values_list('materia_comision_id', flat=True)
            context['total_alumnos'] = Inscripcion.objects.filter(
                materia_comision_id__in=comisiones_ids,
                año_cursada=año_actual
            ).values('alumno').distinct().count()
            
        elif request.user.is_superuser:
            context['total_alumnos'] = Alumno.objects.filter(activo=True).count()
            context['total_profesores'] = Profesor.objects.filter(activo=True).count()
            context['total_materias'] = Materia.objects.count()
            context['total_comisiones'] = MateriaComision.objects.count()
    
    return render(request, 'home.html', context)

def signup(request):
    return redirect('home')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            # Verificar si el usuario está activo
            if hasattr(user, 'alumno') and not user.alumno.activo:
                messages.error(request, "Tu cuenta está desactivada. Contacta al administrador.")
                return render(request, 'sign/signin.html')
            if hasattr(user, 'profesor') and not user.profesor.activo:
                messages.error(request, "Tu cuenta está desactivada. Contacta al administrador.")
                return render(request, 'sign/signin.html')
            
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

# ===== PERFIL =====
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

        perfil_obj.telefono = request.POST.get('telefono', '')
        perfil_obj.direccion = request.POST.get('direccion', '')
        perfil_obj.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("perfil")

    return render(request, template, {
        "user": user, 
        "alumno" if es_alumno(user) else "profesor": perfil_obj
    })

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

# ===== MATERIAS (ALUMNO) =====
def materias(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    if hasattr(request.user, 'alumno'):
        alumno = get_object_or_404(Alumno, user=request.user)
        año_actual = datetime.now().year
        inscripciones = Inscripcion.objects.filter(alumno=alumno, año_cursada=año_actual)
        materias = Materia.objects.all()

        comisiones_inscritas = [insc.materia_comision.id for insc in inscripciones]
        materias_inscritas = {insc.materia_comision.materia for insc in inscripciones}
        materias_aprobadas = {i.materia_comision.materia for i in Inscripcion.objects.filter(alumno=alumno, aprobado=True)}
        materias_no_aprobadas = {i.materia_comision.materia for i in inscripciones if i.nota is not None and i.nota < 4}

        return render(request, "alumnos/materias.html", {
            "materias": materias,
            "comisiones_inscritas": comisiones_inscritas,
            "materias_inscritas": materias_inscritas,
            "materias_aprobadas": materias_aprobadas,
            "materias_no_aprobadas": materias_no_aprobadas,
            "año_actual": año_actual
        })

    elif hasattr(request.user, 'profesor'):
        profesor = get_object_or_404(Profesor, user=request.user)
        roles = RolProfesor.objects.filter(profesor=profesor)
        materias_asignadas = {rol.materia_comision.materia for rol in roles}

        return render(request, "profesores/materias.html", {
            "materias_asignadas": materias_asignadas
        })

@login_required
def detalle_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)

    if hasattr(request.user, 'alumno'):
        alumno = get_object_or_404(Alumno, user=request.user)
        año_actual = datetime.now().year
        ya_inscripto = Inscripcion.objects.filter(
            alumno=alumno, 
            materia_comision__materia=materia,
            año_cursada=año_actual
        ).first()

        if ya_inscripto and ya_inscripto.nota is None:
            messages.info(request, "Ya estás inscrito en una comisión de esta materia este año.")
            return redirect("materias")

        comisiones = materia.materia_comisiones.all()
        return render(request, "alumnos/detalle_materia.html", {
            "materia": materia,
            "comisiones": comisiones
        })

    elif hasattr(request.user, 'profesor'):
        profesor = get_object_or_404(Profesor, user=request.user)
        comisiones = materia.materia_comisiones.filter(rolprofesor__profesor=profesor)
        
        # Obtener años disponibles
        años_disponibles = Inscripcion.objects.filter(
            materia_comision__in=comisiones
        ).values_list('año_cursada', flat=True).distinct().order_by('-año_cursada')
        
        return render(request, "profesores/detalle_materia.html", {
            "materia": materia,
            "comisiones": comisiones,
            "años_disponibles": años_disponibles,
            "año_actual": datetime.now().year
        })

@login_required
def inscribir_comision(request, comision_id):
    comision = get_object_or_404(MateriaComision, id=comision_id)
    alumno = get_object_or_404(Alumno, user=request.user)
    año_actual = datetime.now().year

    # Verificar cupo
    if comision.cantidad_inscriptos >= comision.cupo_maximo:
        messages.error(request, "La comisión está completa.")
        return redirect('detalle_materia', materia_id=comision.materia.id)

    # Verificar inscripción existente este año
    inscripcion = Inscripcion.objects.filter(
        alumno=alumno, 
        materia_comision__materia=comision.materia,
        año_cursada=año_actual
    ).first()
    
    if inscripcion:
        if inscripcion.nota is not None and inscripcion.nota < 4:
            # Permitir reinscripción si desaprobó
            inscripcion.delete()
        else:
            messages.info(request, "Ya estás inscrito en una comisión de esta materia este año.")
            return redirect("materias")

    Inscripcion.objects.create(alumno=alumno, materia_comision=comision, año_cursada=año_actual)
    messages.success(request, f"Te has inscrito correctamente en {comision.materia.nombre} - {comision.comision.nombre}.")
    return redirect("materias")

@login_required
def desinscribir_materia(request, materia_id):
    alumno = get_object_or_404(Alumno, user=request.user)
    materia = get_object_or_404(Materia, id=materia_id)
    año_actual = datetime.now().year

    inscripciones = Inscripcion.objects.filter(
        alumno=alumno, 
        materia_comision__materia=materia,
        año_cursada=año_actual,
        nota__isnull=True  # Solo sin nota
    )

    if inscripciones.exists():
        inscripciones.delete()
        messages.success(request, f"Te has desinscrito correctamente de {materia.nombre}.")
    else:
        messages.info(request, "No estás inscrito en esta materia este año o ya tienes nota asignada.")

    return redirect("materias")

@login_required
def calificaciones(request):
    alumno = get_object_or_404(Alumno, user=request.user)
    inscripciones = Inscripcion.objects.filter(alumno=alumno).select_related(
        'materia_comision__materia',
        'materia_comision__comision'
    ).order_by('-año_cursada', '-fecha_inscripcion')
    
    # Estadísticas
    total = inscripciones.count()
    aprobadas = inscripciones.filter(aprobado=True).count()
    cursando = inscripciones.filter(nota__isnull=True, año_cursada=datetime.now().year).count()
    
    # Promedio
    notas_list = inscripciones.filter(nota__isnull=False).values_list('nota', flat=True)
    promedio = sum(notas_list) / len(notas_list) if notas_list else 0
    
    return render(request, "alumnos/calificaciones.html", {
        "inscripciones": inscripciones,
        "total": total,
        "aprobadas": aprobadas,
        "cursando": cursando,
        "promedio": round(promedio, 2)
    })

# ===== PROFESORES - GESTIÓN DE ALUMNOS =====
@login_required
def detalle_comision(request, comision_id):
    comision = get_object_or_404(MateriaComision, id=comision_id)
    
    # Filtrar por año si se especifica
    año_filtro = request.GET.get('año', datetime.now().year)
    try:
        año_filtro = int(año_filtro)
    except:
        año_filtro = datetime.now().year
    
    inscripciones = Inscripcion.objects.filter(
        materia_comision=comision,
        año_cursada=año_filtro
    ).select_related('alumno__user').order_by('alumno__legajo')
    
    # Obtener años disponibles
    años_disponibles = Inscripcion.objects.filter(
        materia_comision=comision
    ).values_list('año_cursada', flat=True).distinct().order_by('-año_cursada')
    
    return render(request, "profesores/detalle_comision.html", {
        "comision": comision,
        "inscripciones": inscripciones,
        "años_disponibles": años_disponibles,
        "año_seleccionado": año_filtro
    })

@login_required
def ingresar_nota(request):
    if request.method == "POST":
        inscripcion_id = request.POST.get("inscripcion_id")
        nota = request.POST.get("nota")
        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
        
        try:
            nota_decimal = float(nota)
            if 0 <= nota_decimal <= 10:
                inscripcion.nota = nota_decimal
                inscripcion.save()
                messages.success(request, f"Nota {nota} ingresada correctamente.")
            else:
                messages.error(request, "La nota debe estar entre 0 y 10.")
        except ValueError:
            messages.error(request, "Formato de nota inválido.")
    
    return redirect(request.META.get('HTTP_REFERER', 'materias'))

@login_required
def limpiar_comision(request, comision_id):
    """Elimina inscripciones sin nota del año actual"""
    comision = get_object_or_404(MateriaComision, id=comision_id)
    profesor = get_object_or_404(Profesor, user=request.user)
    
    if not RolProfesor.objects.filter(profesor=profesor, materia_comision=comision).exists():
        messages.error(request, "No tienes permiso para gestionar esta comisión.")
        return redirect('materias')
    
    año_actual = datetime.now().year
    inscripciones_eliminadas = Inscripcion.objects.filter(
        materia_comision=comision,
        nota__isnull=True,
        año_cursada=año_actual
    ).delete()
    
    messages.success(request, f"Se eliminaron {inscripciones_eliminadas[0]} inscripciones del año {año_actual}. Las notas calificadas se mantienen.")
    return redirect('detalle_comision', comision_id=comision_id)

# ===== HORARIOS =====
@login_required
def horarios(request):
    user = request.user

    if hasattr(user, 'alumno'):
        año_actual = datetime.now().year
        inscripciones = Inscripcion.objects.filter(
            alumno__user=user, 
            año_cursada=año_actual,
            nota__isnull=True  # Solo materias cursando
        ).select_related('materia_comision')
        comisiones = [inscripcion.materia_comision for inscripcion in inscripciones]
    elif hasattr(user, 'profesor'):
        roles = RolProfesor.objects.filter(profesor__user=user).select_related('materia_comision')
        comisiones = [rol.materia_comision for rol in roles]
    else:
        return redirect("home")

    horarios_por_dia = {
        "Lunes": [], "Martes": [], "Miércoles": [],
        "Jueves": [], "Viernes": [], "Sábado": [], "Domingo": []
    }

    for comision in comisiones:
        for horario in comision.horarios.all():
            horarios_por_dia[horario.dia].append({
                'horario': horario,
                'comision': comision
            })

    # Ordenar por hora de inicio
    for dia in horarios_por_dia:
        horarios_por_dia[dia].sort(key=lambda h: h['horario'].hora_inicio)

    return render(request, "horarios.html", {"horarios": horarios_por_dia})

# ===== ADMINISTRACIÓN - PROFESORES =====
@login_required
@permission_required('is_superuser')
def profesores(request):
    profesores_list = Profesor.objects.select_related('user').order_by('legajo')
    return render(request, "profesores/profesores.html", {"profesores": profesores_list})

@login_required
@permission_required('is_superuser')
def agregar_profesor(request):
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            try:
                # Verificar email único
                if User.objects.filter(email=form.cleaned_data["email"]).exists():
                    messages.error(request, "Ya existe un usuario con ese email.")
                    return render(request, "profesores/agregar_profesor.html", {"form": form})
                
                profesor = form.save(commit=False)
                user = User.objects.create_user(
                    username=form.cleaned_data["email"],
                    email=form.cleaned_data["email"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    password=form.cleaned_data["dni"],
                )
                profesor.user = user
                profesor.save()
                messages.success(request, "Profesor agregado correctamente.")
                return redirect("profesores")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ProfesorForm()
    return render(request, "profesores/agregar_profesor.html", {"form": form})

@login_required
@permission_required('is_superuser')
def detalle_profesor(request, profesor_id):
    profesor = get_object_or_404(Profesor, id=profesor_id)
    return render(request, "profesores/detalle_profesor.html", {"profesor": profesor})

@login_required
@permission_required('is_superuser')
def toggle_profesor(request, profesor_id):
    """Activar/Desactivar profesor"""
    profesor = get_object_or_404(Profesor, id=profesor_id)
    profesor.activo = not profesor.activo
    profesor.save()
    estado = "activado" if profesor.activo else "desactivado"
    messages.success(request, f"Profesor {estado} correctamente.")
    return redirect('detalle_profesor', profesor_id=profesor_id)

@login_required
@permission_required('is_superuser')
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

    materias = Materia.objects.prefetch_related('materia_comisiones__comision').order_by('año', 'nombre')
    comisiones = MateriaComision.objects.select_related('materia', 'comision').order_by('materia__nombre')
    
    return render(request, "asignar_profesor.html", {
        "profesores": Profesor.objects.filter(activo=True).select_related('user'),
        "materias": materias,
        "comisiones": comisiones,
        "roles": RolProfesor.ROL_CHOICES
    })

@login_required
@permission_required('is_superuser')
def eliminar_rol_profesor(request, rol_profesor_id):
    get_object_or_404(RolProfesor, id=rol_profesor_id).delete()
    messages.success(request, "Asignación eliminada correctamente.")
    return redirect(request.META.get('HTTP_REFERER', 'profesores'))

# ===== ADMINISTRACIÓN - ALUMNOS =====
@login_required
@permission_required('is_superuser')
def alumnos(request):
    alumnos_list = Alumno.objects.select_related('user').order_by('legajo')
    return render(request, "alumnos/alumnos.html", {"alumnos": alumnos_list})

@login_required
@permission_required('is_superuser')
def agregar_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            try:
                # Verificar email único
                if User.objects.filter(email=form.cleaned_data["email"]).exists():
                    messages.error(request, "Ya existe un usuario con ese email.")
                    return render(request, "alumnos/agregar_alumno.html", {"form": form})
                
                alumno = form.save(commit=False)
                user = User.objects.create_user(
                    username=form.cleaned_data["email"],
                    email=form.cleaned_data["email"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    password=form.cleaned_data["dni"],
                )
                alumno.user = user
                alumno.save()
                messages.success(request, "Alumno agregado correctamente.")
                return redirect("alumnos")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = AlumnoForm()
    return render(request, "alumnos/agregar_alumno.html", {"form": form})

@login_required
@permission_required('is_superuser')
def toggle_alumno(request, alumno_id):
    """Activar/Desactivar alumno"""
    alumno = get_object_or_404(Alumno, id=alumno_id)
    alumno.activo = not alumno.activo
    alumno.save()
    estado = "activado" if alumno.activo else "desactivado"
    messages.success(request, f"Alumno {estado} correctamente.")
    return redirect('alumnos')

# ===== ADMINISTRACIÓN - MATERIAS =====
@login_required
@permission_required('is_superuser')
def ver_materias(request):
    materias = Materia.objects.all().order_by('año', 'codigo')
    return render(request, "ver_materias.html", {"materias": materias})

@login_required
@permission_required('is_superuser')
def agregar_materia(request):
    if request.method == "POST":
        try:
            materia = Materia(
                codigo=request.POST.get("codigo"),
                nombre=request.POST.get("nombre"),
                descripcion=request.POST.get("descripcion", ""),
                año=int(request.POST.get("año")),
                creditos=int(request.POST.get("creditos"))
            )
            materia.save()
            messages.success(request, "Materia agregada correctamente.")
            return redirect("ver_materias")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "agregar_materia.html")

@login_required
@permission_required('is_superuser')
def ver_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    comisiones = Comision.objects.exclude(
        id__in=materia.materia_comisiones.values_list('comision', flat=True)
    )
    
    if request.method == "POST":
        try:
            materiaComision = MateriaComision(
                materia=materia,
                comision=Comision.objects.get(id=request.POST.get("comision"))
            )
            materiaComision.save()
            messages.success(request, "Comisión agregada correctamente.")
            return redirect("ver_materia", materia_id=materia_id)
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    
    return render(request, "ver_materia.html", {
        "materia": materia,
        "comisiones": comisiones
    })

@login_required
@permission_required('is_superuser')
def agregar_comision(request):
    if request.method == "POST":
        try:
            comision = Comision(nombre=request.POST.get("nombre"))
            comision.save()
            messages.success(request, "Comisión agregada correctamente.")
            return redirect("ver_materias")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, "agregar_comision.html")