from django.db import models

# Create your models here.
class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    descripcion = models.CharField()

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField()
    apellido = models.CharField()
    dni = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField()
    id_perfil = models.ForeignKey(Perfiles, on_delete=models.CASCADE)

class Materias(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre = models.CharField()
    anio = models.IntegerField()
    cuatrimestre = models.IntegerField()
    
class Examenes(models.Model):
    id_examen = models.AutoField(primary_key=True)
    fecha = models.DateField()
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)

class Carreras(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField()

class Carrera_Materia(models.Model):
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["id_materia","id_carrera"], name="unique_id_materia_carrera")]

class Inscripcion_Materia(models.Model):
    id_inscripcion_materia = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    estado = models.IntegerField()
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)

class Inscripcion_Examen(models.Model):
    id_examen = models.ForeignKey(Examenes, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nota = models.FloatField()
    estado = models.IntegerField()
    class Meta:
        constraints = [models.UniqueConstraint(fields=["id_usuario","id_examen"], name="unique_id_usuario_examen")]
