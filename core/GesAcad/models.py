from datetime import datetime
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

    @classmethod
    def get(cls, id:int):
        try:
            return cls.objects.filter(id_usuario=id).first()
        except cls.DoesNotExist:
            return None
        except:
            return None

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        db_table = "Usuarios"

class Carreras(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    @classmethod
    def get(cls, id:int):
        return cls.objects.filter(id_carrera=id).first()

    def __str__(self)->str:
        return str(self.nombre)

    class Meta:
        db_table = "Carreras"

    @classmethod
    def carreras_alumno(cls, alumno:Usuarios)->models.QuerySet:
        return cls.objects.filter(inscripcion_carrera__id_usuario=alumno)

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
        
        
class Carrera_Materia(models.Model):
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE, related_name='carreras_rel')
    id_carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    class Meta:
        constraints = (models.UniqueConstraint(fields=["id_materia","id_carrera"], name="unique_id_materia_carrera"),)
        db_table = "Carrera_Materia"
class Inscripcion_Materia(models.Model):
    id_inscripcion_materia = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name="inscripciones_materias")
    estado = models.CharField(
            max_length=20,
            choices=[
                ("Baja", "Baja"),
                ("Alta", "Alta"),
                ("Aprobado", "Aprobado"),
                ("Desaprobado", "Desaprobado"),
            ])
    id_materia = models.ForeignKey(Materias, on_delete=models.CASCADE)

    @classmethod
    def materias_alta(cls, usuario:Usuarios):
        return cls.objects.filter(id_usuario=usuario, estado='Alta')

    @classmethod
    def id_materias_alta(cls, usuario:Usuarios)->list[int]:
        return cls.materias_alta(usuario=usuario).values_list("id_materia", flat=True)

    @classmethod
    def dar_alta_baja_Inscripcion_Materia(cls, materia:Materias, usuario:Usuarios)->bool:
        try:
            
            insc, created = cls.objects.get_or_create(
                id_usuario = usuario,
                id_materia = materia,
                defaults={"estado":"Alta"}
            )

            if not created:
                insc.estado = "Baja" if insc.estado == "Alta" else "Alta"
                insc.save()
            return True
        except Exception as e:
            print(e)
            return False
    
    @classmethod
    def inscriptos_por_materia(cls, materia:Materias, usuario:Usuarios):
        try:
            inscripciones = cls.objects.filter(
                    id_materia=materia,
                    estado__in=["Alta", "Aprobado", "Desaprobado"]
                ).exclude(id_usuario=usuario)
            return inscripciones
        except Exception as e:
            print(e)
            return None
    class Meta:
        db_table = "Inscripcion_Materia"
        
class Inscripcion_Examen(models.Model):
    id_examen = models.ForeignKey(Examenes, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    nota = models.IntegerField()
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nota} - {self.id_examen}"

    
    @classmethod
    def obtener_examenes_agrupados(cls, usuario: Usuarios, carrera: Carreras) -> dict:
        inscripciones = cls.objects.filter(
            id_usuario=usuario,
            id_examen__id_materia__carreras_rel__id_carrera=carrera,
            nota__gte=1
        ).order_by(
            "id_examen__id_materia__nombre",  
            "id_examen__fecha"                
        ) 

        examenes_agrupados = {}
        for insc in inscripciones:
            materia = insc.id_examen.id_materia
            if materia not in examenes_agrupados:
                examenes_agrupados[materia] = []
            examenes_agrupados[materia].append(insc)

        return examenes_agrupados

    class Meta:
        constraints = (models.UniqueConstraint(fields=["id_usuario","id_examen"], name="unique_id_usuario_examen"),)
        db_table = "Inscripcion_Examen"



class Inscripcion_Carrera(models.Model):
    id_usuario= models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    id_carrera= models.ForeignKey(Carreras, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    fecha_inscripcion = models.DateField(default=datetime.now())

    class Meta:
        constraints = (models.UniqueConstraint(fields=["id_usuario", "id_carrera"], name='unique_id_carrera_usuario'),)
        db_table = "Inscripcion_Carrera"
