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
    
class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=100)
    legajo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class Materia(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    año = models.PositiveIntegerField(blank=True, null=True)
    creditos = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre
    
class Comision(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='comisiones')
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    cupos = models.PositiveIntegerField()
    alumnos_inscritos = models.ManyToManyField(Alumno, through='Inscripcion')

    def __str__(self):
        return f"{self.materia} - {self.horario}"
    
    def cupos_disponibles(self):
        return self.cupos - self.alumnos_inscritos.count()
    
class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    comision = models.ForeignKey(Comision, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno} - {self.materia}"
    
class Horario(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miercoles', 'Miercoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sabado', 'Sabado')])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.materia} - {self.dia} {self.hora_inicio} - {self.hora_fin}"