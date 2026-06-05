from __future__ import annotations

from dataclasses import dataclass

from .models import Materias


@dataclass
class Carrera:
    pass


@dataclass
class Materia:
    nombre : str
    anio : int
    cuatrimestre : int

    def get(id:int):
        return Materias.objects.get(id_materia=id)

@dataclass
class Examen:
    pass
