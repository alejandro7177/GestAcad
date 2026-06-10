from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from django.db import connection

from .academico import Materia
from .models import Inscripcion_Materia as InscriptionMateriaModel
from .usuario import Usuario

@dataclass
class Inscripcion(ABC):
    usuario : Usuario
    fecha_inscripcion : datetime
    estado: str

    @abstractmethod
    def get(self, id):
        pass

    def dar_alta_baja(self):
        pass

@dataclass
class InscripcionMateria(Inscripcion):
    materia: Materia
    _model = InscriptionMateriaModel
    
    @abstractmethod
    def get(cls, id):
        return cls._model.objects.get(id._model)

    def obtener_materia(self)->Materia:
        return self.materia

    @classmethod
    def alta_baja_inscripcion(cls, id_usuario, id_materia):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT alta_baja_inscripcion_materia(%s, %s)
                """,
                [id_usuario, id_materia]
            )

            return cursor.fetchone()[0]

@dataclass
class InscripcionCarrera(Inscripcion):
    def obtener_carrera(self):
        pass

    def dar_baja_carrera(self):
        pass

@dataclass
class InscripcionExamen(Inscripcion):
    def registrar_nota(self, nota:int):
        pass

    def obtener_examen(self):
        pass
