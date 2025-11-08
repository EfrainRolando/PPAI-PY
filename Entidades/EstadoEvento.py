from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from Entidades.CambioEstado import CambioEstado

class EstadoEvento(ABC):

    def nombre(self) -> str:
        # Por si alguien quiere pedir nombre() en lugar de NAME
        return self.NAME
    def bloquear(
    ) -> None:
        print("bloqueando")


class PteRevision(EstadoEvento):
    NAME = "PteRevision"
    def sosPteRevision(self) -> bool: return True

    def bloquear(self, evento: "EventoSismico", fechaHora: datetime, responsable: Optional[str] = None,) -> None:
        self.buscarCEActual(evento, fechaHora)
        estadoBloqueado = self.crearProxEstado()
        nuevo = self.crearCE(evento, estadoBloqueado, fechaHora, responsable)
        evento.setCambioEstado(nuevo)
        if hasattr(evento, "setEstadoActual"):
            evento.setEstadoActual(estadoBloqueado)
        else:
            evento.estadoActual = estadoBloqueado

    def crearProxEstado(self)-> EstadoEvento:
        return  BloqueadoEnRevision()
    
    def buscarCEActual(self, evento, fechaHora)-> None:
        for c in evento.cambiosEstado:
            if c.esActual():
                c.setFechaHoraFin(fechaHora)

    def crearCE(self, evento, estadoBloqueado, fechaHora, responsable) -> CambioEstado:
            nuevo = evento.crearCambioEstado(
            estado=estadoBloqueado,
            fechaHora=fechaHora,
            nombreUsuario=responsable,
            )
            return nuevo



class BloqueadoEnRevision(EstadoEvento):
    NAME = "BloqueadoEnRevision"
    def sosBloqueadoEnRevision(self) -> bool: return True
    def bloquear(self, evento, fecha_hora, responsable = None):
        return super().bloquear(evento, fecha_hora, responsable)

    def rechazar(self,evento: "EventoSismico",fechaHora: datetime,responsable: Optional[str] = None,
    ) -> None:
        self.buscarCEActual(evento, fechaHora)
        estado_rechazado = self.crearProxEstado()
        nuevo = self.crearCE(evento, estado_rechazado, fechaHora, responsable)
        evento.setCambioEstado(nuevo)
        if hasattr(evento, "setEstadoActual"):
            evento.setEstadoActual(estado_rechazado)
        else:
            evento.estadoActual = estado_rechazado

    def crearProxEstado(self)-> EstadoEvento:
        return Rechazado
    
    def buscarCEActual(self, evento, fechaHora) -> None:

        for c in evento.cambiosEstado:
            if c.esActual():
                c.setFechaHoraFin(fechaHora)

    def crearCE(self, evento, estadoRechazado, fechaHora, responsable):
            nuevo = evento.crearCambioEstado(
            estado=estadoRechazado,
            fechaHora=fechaHora,
            nombreUsuario=responsable,
        )
            return nuevo


class Rechazado(EstadoEvento):
    NAME = "Rechazado"
    def rechazar():
        pass