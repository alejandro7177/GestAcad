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
    pass


class ObservadorConcreto(Observador):
    pass
