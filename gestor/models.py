from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    dni = models.CharField(max_length=100)
    legajo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)

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
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    dias = models.CharField(max_length=100, choices=DIAS_SEMANA, blank=True)  # Día único
    hora_inicio = models.CharField(max_length=10)
    hora_fin = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.dias} {self.hora_inicio} - {self.hora_fin}"


class MateriaComision(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="materia_comisiones")
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE, related_name="comision_materias")
    cupo_maximo = models.PositiveIntegerField(default=30)
    horarios = models.ManyToManyField(Horario, blank=True)

    def __str__(self):
        return f"{self.materia.nombre} - {self.comision.nombre}"

    @property
    def cantidad_inscriptos(self):
        return self.inscripcion_set.count()

    @property
    def profesores(self):
        return Profesor.objects.filter(rolprofesor__materia_comision=self)


class RolProfesor(models.Model):
    ROL_CHOICES = [
        ('Titular', 'Titular'),
        ('Ayudante', 'Ayudante'),
    ]
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    materia_comision = models.ForeignKey(MateriaComision, on_delete=models.CASCADE, blank=True, null=True)
    rol = models.CharField(max_length=100, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.profesor} - {self.materia_comision} - {self.rol}"


class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    materia_comision = models.ForeignKey(MateriaComision, on_delete=models.CASCADE, blank=True, null=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.aprobado = self.nota is not None and self.nota >= 4
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno.legajo} - {self.materia_comision}"

    @property
    def alumno_instance(self):
        return self.alumno

    @property
    def materia(self):
        return self.materia_comision.materia if self.materia_comision else None

    @property
    def comision(self):
        return self.materia_comision.comision if self.materia_comision else None

    @property
    def horarios(self):
        return self.materia_comision.horarios.all() if self.materia_comision else []
