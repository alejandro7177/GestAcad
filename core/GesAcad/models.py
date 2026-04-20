from django.db import models


class Perfiles(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=40)
    
    def __str__(self)-> str:
        return str(self.descripcion)

    class Meta:
        db_table = "Perfiles"
        
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    dni = models.CharField(unique=True, max_length=10)
    email = models.EmailField(unique=True, max_length=100)
    password_hash = models.CharField(max_length=128)
    id_perfil = models.ForeignKey(Perfiles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    class Meta:
        db_table = "Usuarios"

class Materias(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    anio = models.IntegerField()
    cuatrimestre = models.IntegerField()

    def __str__(self)->str:
        return f"{self.nombre}"
    class Meta:
        db_table = "Materias"
        
    
class Examenes(models.Model):
    id_examen = models.AutoField(primary_key=True)
    fecha = models.DateField()
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_materia} - {self.fecha}" 
    class Meta:
        db_table = "Examenes"
        
class Carreras(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self)->str:
        return str(self.nombre)

    class Meta:
        db_table = "Carreras"
        
class Carrera_Materia(models.Model):
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    class Meta:
        constraints = (models.UniqueConstraint(fields=["id_materia","id_carrera"], name="unique_id_materia_carrera"),)
        db_table = "Carrera_Materia"
class Inscripcion_Materia(models.Model):
    id_inscripcion_materia = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)
    class Meta:
        db_table = "Inscripcion_Materia"
        
class Inscripcion_Examen(models.Model):
    id_examen = models.ForeignKey(Examenes, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nota = models.IntegerField()
    estado = models.CharField(max_length=20)
    class Meta:
        constraints = (models.UniqueConstraint(fields=["id_usuario","id_examen"], name="unique_id_usuario_examen"),)
        db_table = "Inscripcion_Examen"
