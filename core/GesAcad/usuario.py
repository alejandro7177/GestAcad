from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from django.contrib.auth import hashers
from django.db import connection

from .models import Usuarios as UserModel
from .observer import Observador, Sujeto, SujetoConcreto


@dataclass
class Usuario(ABC):
    id_usuario: int
    nombre: str
    apellido: str
    dni: str
    email: str
    password: str

    _model: ClassVar = UserModel

    @classmethod
    @abstractmethod
    def get(cls, id_usuario: int):
        pass

    @staticmethod
    def login(email: str, password: str) -> tuple[Usuario | None, dict]:
        try:
            user = UserModel.objects.get(email=email)

            if not hashers.check_password(
                password,
                user.password_hash,
            ):
                return None, {
                    "error": 1,
                    "description": "Contraseña Incorrecta",
                }

            if str(user.id_perfil) == "Alumno":
                return (
                    Alumno(
                        id_usuario=user.id_usuario,
                        nombre=user.nombre,
                        apellido=user.apellido,
                        dni=user.dni,
                        email=user.email,
                        password=user.password_hash,
                    ),
                    {},
                )

            if str(user.id_perfil) == "Docente":
                return (
                    Docente(
                        id_usuario=user.id_usuario,
                        nombre=user.nombre,
                        apellido=user.apellido,
                        dni=user.dni,
                        email=user.email,
                        password=user.password_hash,
                    ),
                    {},
                )

            return None, {
                "error": 2,
                "description": "Perfil no definido",
            }

        except UserModel.DoesNotExist:
            return None, {
                "error": 3,
                "description": "No existe usuario con ese email",
            }

        except Exception as ex:
            return None, {
                "error": 4,
                "description": f"Error interno del sistema: {ex}",
            }

    def nombreCompleto(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def actualizar_datos(self, nombre, apellido, email):
        pass

    @abstractmethod
    def obtenerPerfil(self) -> str:
        pass


@dataclass
class Alumno(Usuario, Observador):

    @classmethod
    def get(cls, id_usuario: int) -> Alumno | None:
        data = cls._model.objects.filter(
            id_usuario=id_usuario
        ).first()

        if data is None:
            return None

        if str(data.id_perfil) != "Alumno":
            return None

        return cls(
            id_usuario=data.id_usuario,
            nombre=data.nombre,
            apellido=data.apellido,
            dni=data.dni,
            email=data.email,
            password=data.password_hash,
        )

    def obtenerPerfil(self) -> str:
        return "Alumno"

    def inscripciones_materia(self):
        try:
            user = self._model.objects.filter(id_usuario=self.id_usuario).first()
            print(f"{user=}")
            return user.inscripciones_materias.filter(estado="Alta")
        except Exception as ex:
            print(f"{ex=}")
            return []
    
    def inscripciones_aprobados(self):
        return set(
            Inscripcion_Materia.objects.filter(
                id_usuario=self.id_usuario,
                estado="Aprobado"
            ).values_list("id_materia_id", flat=True)
        )
    def ids_inscripciones_materia(self):
        res = self.inscripciones_materia()
        if res:
            return res.values_list("id_materia", flat=True)
        return []

    def obtener_carreras(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM obtener_carreras_usuario(%s)",
                [self.id_usuario],
            )
            return cursor.fetchall()

    def actualizar(self, subject: Sujeto) -> None:
        if isinstance(subject, SujetoConcreto):
            print(f"[Observer] {self.nombre}: {subject.getEstado()}")

@dataclass
class Docente(Usuario):

    @classmethod
    def get(cls, id_usuario: int) -> Docente | None:
        data = cls._model.objects.filter(
            id_usuario=id_usuario
        ).first()

        if data is None:
            return None

        if str(data.id_perfil) != "Docente":
            return None

        return cls(
            id_usuario=data.id_usuario,
            nombre=data.nombre,
            apellido=data.apellido,
            dni=data.dni,
            email=data.email,
            password=data.password_hash,
        )

    def obtenerPerfil(self) -> str:
        return "Docente"

    def materias_asignadas(self):
        pass

    def listar_alumnos(self,id_materia):
        pass

    def cargar_nota(self, id_examen, nota):
        pass
