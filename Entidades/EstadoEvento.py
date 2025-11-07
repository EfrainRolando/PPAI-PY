from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from Entidades.CambioEstado import CambioEstado

class EstadoEvento(ABC):

    # Predicados por defecto (para filtros tipo sosPteRevision())
    def sosAutoDetectado(self) -> bool: return False
    def sosPteRevision(self) -> bool:   return False
    def sosBloqueadoEnRevision(self) -> bool: return False

    def nombre(self) -> str:
        # Por si alguien quiere pedir nombre() en lugar de NAME
        return self.NAME
    def bloquear(
        self,
        evento: "EventoSismico",
        fecha_hora: datetime,
        responsable: Optional[str] = None,
    ) -> CambioEstado:
        ...


class PteRevision(EstadoEvento):
    NAME = "PteRevision"
    def sosPteRevision(self) -> bool: return True

    def bloquear(
        self,
        evento: "EventoSismico",
        fecha_hora: datetime,
        responsable: Optional[str] = None,
    ) -> None:
        # 1) cerrar vigente
        cambio_actual = next((c for c in reversed(evento.cambiosEstado) if c.esActual()), None)
        if cambio_actual is None:
            raise ValueError("No hay CambioEstado vigente para cerrar.")
        cambio_actual.setFechaHoraFin(fecha_hora)
        estado_bloq = BloqueadoEnRevision()
        nuevo = evento.crearCambioEstado(
            estado=estado_bloq,
            fechaHora=fecha_hora,
            nombreUsuario=responsable,
        )
        evento.setCambioEstado(nuevo)
        if hasattr(evento, "setEstadoActual"):
            evento.setEstadoActual(estado_bloq)
        else:
            evento.estadoActual = estado_bloq


class BloqueadoEnRevision(EstadoEvento):
    NAME = "BloqueadoEnRevision"
    def sosBloqueadoEnRevision(self) -> bool: return True
    def bloquear(self, evento, fecha_hora, responsable = None):
        return super().bloquear(evento, fecha_hora, responsable)

    def rechazar(self,evento: "EventoSismico",fecha_hora: datetime,responsable: Optional[str] = None,
    ) -> None:
        cambio_actual = next((c for c in reversed(evento.cambiosEstado) if c.esActual()), None)
        if cambio_actual is None:
            raise ValueError("No hay CambioEstado vigente para cerrar.")
        cambio_actual.setFechaHoraFin(fecha_hora)
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