from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.contrib.auth import hashers
from django.db import connection

from .academico import Carrera
from .models import Usuarios, Inscripcion_Materia
from .observer import Observador, Sujeto


@dataclass
class Usuario(ABC):
    id_usuario: int
    nombre: str
    apellido: str
    dni: str
    email: str
    password : str
    
    @staticmethod
    def get(id_usuario:int):
        _model = Usuarios.objects.filter(id_usuario=id_usuario).first()
        if _model.id_perfil.id_perfil == 1:
            return Alumno(
                id_usuario=_model.id_usuario,
                nombre = _model.nombre,
                apellido = _model.apellido,
                dni = _model.dni,
                email = _model.email,
                password = _model.password_hash
            )
        elif _model.id_perfil.id_perfil == 2:
            return Docente(
                 id_usuario=_model.id_usuario,
                nombre = _model.nombre,
                apellido = _model.apellido,
                dni = _model.dni,
                email = _model.email,
                password = _model.password_hash
            )
    @staticmethod
    def login(email:str, password:str)-> tuple[ Usuario | None , dict]:
        try:
            _user = Usuarios.objects.get(email=email)
            if not hashers.check_password(password, _user.password_hash):
                return None, {"error": 1 , "description": "Contraseña Incorrecta"}

            if _user.id_perfil.__str__() == "Alumno":
                return Alumno(
                    id_usuario = _user.id_usuario,
                    nombre = _user.nombre,
                    apellido= _user.apellido,
                    dni = _user.dni,
                    email = _user.email,
                    password = _user.password_hash
                ), {}
            if _user.id_perfil.__str__() == "Docente":
                return Docente(
                    id_usuario = _user.id_usuario,
                    nombre = _user.nombre,
                    apellido= _user.apellido,
                    dni = _user.dni,
                    email = _user.email,
                    password = _user.password_hash
                ), {}
            return None, {"error": 2 , "description" : "Perfil no Definido"}
        except Usuarios.DoesNotExist:
            return None, {"error": 3 , "description": "No existe usuario con ese email"}
        except Exception:
            return None, {"error": 4 , "description": f"Error Interno del Sistema:{ex}"}

    def nombreCompleto(self) -> str:
        return f"{self.nombre} {self.apellido}"
    
    @abstractmethod
    def obtenerPerfil(self) -> str:
        pass
@dataclass
class Alumno(Usuario, Observador):
    def obtenerPerfil(self) -> str:
        return "Alumno"
    
    def inscripciones(self)-> list:
        

    def obtener_carreras(self) -> list[Carrera]:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM obtener_carreras_usuario(%s)", 
                [self.id_usuario]
            )
            return cursor.fetchall()
    def actualizar(self, subject: Sujeto) -> None:
        return super().actualizar(subject)
@dataclass
class Docente(Usuario):
    def obtenerPerfil(self) -> str:
        return "Docente"

if __name__ == "__main__":
    alumno = Alumno.get(1)
    print(f"{alumno=}")
    carreras = alumno.obtener_carreras()
    print(f"{carreras=}")
