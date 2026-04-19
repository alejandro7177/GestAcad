from django.db import models

# Create your models here.
class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    descripcion = models.CharField()
    
    def __str__(self):
        return self.descripcion

    class Meta():
        db_table = "Perfiles"
        
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField()
    apellido = models.CharField()
    dni = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField()
    id_perfil = models.ForeignKey(Perfiles, on_delete=models.CASCADE)
    class Meta():
        db_table = "Usuarios"

class Materias(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre = models.CharField()
    anio = models.IntegerField()
    cuatrimestre = models.IntegerField()
    class Meta():
        db_table = "Materias"
        
    
class Examenes(models.Model):
    id_examen = models.AutoField(primary_key=True)
    fecha = models.DateField()
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    class Meta():
        db_table = "Examenes"
        

class Carreras(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField()
    class Meta():
        db_table = "Carreras"
        
class Carrera_Materia(models.Model):
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["id_materia","id_carrera"], name="unique_id_materia_carrera")]
        db_table = "Carrera_Materia"
class Inscripcion_Materia(models.Model):
    id_inscripcion_materia = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    estado = models.IntegerField()
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    class Meta():
        db_table = "Inscripcion_Materia"
        
class Inscripcion_Examen(models.Model):
    id_examen = models.ForeignKey(Examenes, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nota = models.FloatField()
    estado = models.IntegerField()
    class Meta:
        constraints = [models.UniqueConstraint(fields=["id_usuario","id_examen"], name="unique_id_usuario_examen")]
        db_table = "Inscripcion_Examen"
