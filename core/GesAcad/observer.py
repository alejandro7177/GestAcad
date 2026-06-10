from __future__ import annotations

from abc import ABC, abstractmethod


class Sujeto(ABC):
    """
    La interfaz Sujeto declara un conjunto de metodos para el manejo de subscritores
    """

    @abstractmethod
    def vincular(self, o: Observador) -> None:
        pass

    @abstractmethod
    def desvincular(self, o: Observador) -> None:
        pass

    @abstractmethod
    def notificar(self) -> None:
        pass


class Observador(ABC):
    """
    La interfaz Observador declara el método de actualización utilizado por el Sujeto
    """

    @abstractmethod
    def actualizar(self, subject: Sujeto) -> None:
        pass


"""
Implementación de las interfaces para el proyecto
"""


class SujetoConcreto(Sujeto):
    def __init__(self):
        self._observadores: list[Observador] = []
        self._estado: str = ""

    def vincular(self, o:Observador) -> None:
        if o not in self._observadores:
            self._observadores.append(o)


    def desvincular(self, o:Observador) -> None:
        self._observadores.remove(o)

    
    def notificar(self) -> None:
        for observador in self._observadores:
            observador.actualizar(self)

    
    def getEstado(self) -> str:
        return self._estado
    

    def setEstado(self, estado:str) -> None:
        self._estado = estado
        self.notificar()


class ObservadorConcreto(Observador):
    def __init__(self):
        self.estadoObservador: str = ""

    
    def actualizar(self, subject:Sujeto) -> None:
        if isinstance(subject, SujetoConcreto):
            self.estadoObservador = subject.getEstado()
