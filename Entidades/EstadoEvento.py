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

    def bloquear(
        self,
        evento: "EventoSismico",
        fecha_hora: datetime,
        responsable: Optional[str] = None,
    ) -> None:
        for c in evento.cambiosEstado:
            if c.esActual():
                c.setFechaHoraFin(fecha_hora)
        estadoBloqueado = BloqueadoEnRevision()
        nuevo = evento.crearCambioEstado(
            estado=estadoBloqueado,
            fechaHora=fecha_hora,
            nombreUsuario=responsable,
        )
        evento.setCambioEstado(nuevo)
        if hasattr(evento, "setEstadoActual"):
            evento.setEstadoActual(estadoBloqueado)
        else:
            evento.estadoActual = estadoBloqueado


class BloqueadoEnRevision(EstadoEvento):
    NAME = "BloqueadoEnRevision"
    def sosBloqueadoEnRevision(self) -> bool: return True
    def bloquear(self, evento, fecha_hora, responsable = None):
        return super().bloquear(evento, fecha_hora, responsable)

    def rechazar(self,evento: "EventoSismico",fecha_hora: datetime,responsable: Optional[str] = None,
    ) -> None:
        for c in evento.cambiosEstado:
            if c.esActual():
                c.setFechaHoraFin(fecha_hora)
        estado_rechazado = Rechazado()
        nuevo = evento.crearCambioEstado(
            estado=estado_rechazado,
            fechaHora=fecha_hora,
            nombreUsuario=responsable,
        )
        evento.setCambioEstado(nuevo)
        if hasattr(evento, "setEstadoActual"):
            evento.setEstadoActual(estado_rechazado)
        else:
            evento.estadoActual = estado_rechazado

class Rechazado(EstadoEvento):
    NAME = "Rechazado"
    def rechazar():
        pass