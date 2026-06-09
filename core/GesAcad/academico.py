from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from .models import Materias as MateriaModel


@dataclass
class Carrera:
    pass


@dataclass
class Materia:
    id_materia : int
    nombre : str
    anio : int
    cuatrimestre : int
    _model : ClassVar = MateriaModel

    @classmethod
    def get(cls, id:int):
        try:
            data = MateriaModel.objects.filter(id_materia=id).first()
            return cls(
                id_materia = data.id_materia,
                nombre = data.nombre,
                anio = data.anio,
                cuatrimestre = data.cuatrimestre
            )
        except Exception:
            return None

    @staticmethod
    def materias_cuatrimestre(
        cuatrimestre: int,
        id_carrera: int
    ):
        try:
            return MateriaModel.objects.filter(
                cuatrimestre=cuatrimestre,
                carreras_rel__id_carrera__id_carrera=id_carrera
            )
        except Exception as ex:
            print(f"{ex=}")
            return None
    
    @classmethod
    def obtener_materias_agrupadas(
        cls,
        id_carrera: int
    ):
        from datetime import datetime
        from itertools import groupby

        if id_carrera is None:
            return None

        today = datetime.now()
        materias_alumno = cls.materias_cuatrimestre(
            cuatrimestre= 1 if today.month <= 6 else 2,
            id_carrera=id_carrera
        )
        materias_agrupadas = {}
        for anio, grupo in groupby(materias_alumno, key=lambda x:x.anio):
            materias_agrupadas[anio] = list(grupo)
        
        return materias_agrupadas
@dataclass
class Examen:
    pass
