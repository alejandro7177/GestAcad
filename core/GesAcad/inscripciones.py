from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from .models import Inscripcion_Materia
from .usuario import Usuario

@dataclass
class Inscripcion(ABC):
    usuario : Usuario
    fecha_inscripcion : datetime
    estado: str

    @abstractmethod
    def get(self, id):
        pass

@dataclass
class Inscripcion_Materia(Inscripcion):
    def get(self, id):
        return Inscripcion_Materia.get(id=id)

    def inscripciones_alta(self, usuario:Usuario):
        return Inscripcion_Materia.objects.filter(
            id_usuario_id_usuario=usuario.id_usuario,
            estado = "Alta"
        )
