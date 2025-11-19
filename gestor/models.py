from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    dni = models.CharField(max_length=100)
    legajo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)  # NUEVO: Para activar/desactivar

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def materias_inscritas(self):
        return Inscripcion.objects.filter(alumno=self)

    @property
    def comisiones_asignadas(self):
        return MateriaComision.objects.filter(inscripcion__alumno=self).distinct()


class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    legajo = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)  # NUEVO: Para activar/desactivar

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def comisiones_dictadas(self):
        return MateriaComision.objects.filter(rolprofesor__profesor=self).distinct()


class Materia(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    año = models.PositiveIntegerField(blank=True, null=True)
    creditos = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre


class Comision(models.Model):
    nombre = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.nombre


class MateriaComision(models.Model):
    """
    Relación entre una materia y una comisión.
    Una materia puede tener múltiples comisiones.
    """
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="materia_comisiones")
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name="comision_materias")
    cupo_maximo = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.materia.nombre} - {self.comision.nombre}"

    @property
    def cantidad_inscriptos(self):
        # Solo contar inscripciones del año actual
        return self.inscripcion_set.filter(año_cursada=datetime.now().year).count()

    @property
    def profesores(self):
        return Profesor.objects.filter(rolprofesor__materia_comision=self)

    class Meta:
        unique_together = ('materia', 'comision')


class Horario(models.Model):
    """
    Horarios específicos para cada comisión de materia.
    CAMBIADO: Ahora pertenece directamente a MateriaComision
    """
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    materia_comision = models.ForeignKey(
        MateriaComision, 
        on_delete=models.CASCADE, 
        related_name="horarios",
        default=None
    )
    dia = models.CharField(max_length=20, choices=DIAS_SEMANA, default='Lunes')
    hora_inicio = models.TimeField()  # CAMBIADO: De CharField a TimeField
    hora_fin = models.TimeField()     # CAMBIADO: De CharField a TimeField

    def __str__(self):
        return f"{self.materia_comision} - {self.dia} {self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')}"

    class Meta:
        ordering = ['dia', 'hora_inicio']


class RolProfesor(models.Model):
    ROL_CHOICES = [
        ('Titular', 'Titular'),
        ('Ayudante', 'Ayudante'),
    ]
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    materia_comision = models.ForeignKey(MateriaComision, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.profesor} - {self.materia_comision} - {self.rol}"

    class Meta:
        unique_together = ('profesor', 'materia_comision')


class Inscripcion(models.Model):
    """
    Inscripción de un alumno a una comisión específica de una materia.
    NUEVO: Incluye año de cursada para gestión por períodos
    """
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia_comision = models.ForeignKey(MateriaComision, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    año_cursada = models.PositiveIntegerField(default=datetime.now().year)  # NUEVO
    aprobado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.aprobado = self.nota is not None and self.nota >= 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno.legajo} - {self.materia_comision} ({self.año_cursada})"

    @property
    def materia(self):
        return self.materia_comision.materia if self.materia_comision else None

    @property
    def comision(self):
        return self.materia_comision.comision if self.materia_comision else None

    @property
    def horarios(self):
        return self.materia_comision.horarios.all() if self.materia_comision else []

    class Meta:
        # Un alumno solo puede estar inscrito una vez por año en una materia
        unique_together = ('alumno', 'materia_comision', 'año_cursada')