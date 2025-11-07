from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from Entidades.CambioEstado import CambioEstado

class EstadoEvento(ABC):
    NAME: str = "ABSTRACT"

    # Predicados por defecto (para filtros tipo sosPteRevision())
    def sosAutoDetectado(self) -> bool: return False
    def sosPteRevision(self) -> bool:   return False
    def sosBloqueadoEnRevision(self) -> bool: return False

    def nombre(self) -> str:
        # Por si alguien quiere pedir nombre() en lugar de NAME
        return self.NAME

    @abstractmethod
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
    ) -> CambioEstado:
        # 1) cerrar vigente
        cambio_actual = next((c for c in reversed(evento.cambiosEstado) if c.esActual()), None)
        if cambio_actual is None:
            raise ValueError("No hay CambioEstado vigente para cerrar.")
        cambio_actual.setFechaHoraFin(fecha_hora)

        # 2) crear el nuevo STATE de destino
        estado_bloq = BloqueadoEnRevision()

        # 3) crear el nuevo cambio (espera STATE)
        nuevo = evento.crearCambioEstado(
            estado=estado_bloq,
            fechaHora=fecha_hora,
            nombreUsuario=responsable,
        )

        # (opcional) si el evento mantiene un estadoActual como referencia al STATE
        if hasattr(evento, "setEstadoActual"):
            evento.setEstadoActual(estado_bloq)
        else:
            evento.estadoActual = estado_bloq

        return nuevo


class BloqueadoEnRevision(EstadoEvento):
    NAME = "BloqueadoEnRevision"
    def sosBloqueadoEnRevision(self) -> bool: return True

    def bloquear(
        self,
        evento: "EventoSismico",
        fecha_hora: datetime,
        responsable: Optional[str] = None,
    ) -> CambioEstado:
        # En bloqueado, bloquear de nuevo no cambia nada; devolvemos vigente
        cambio_actual = next((c for c in reversed(evento.cambiosEstado) if c.esActual()), None)
        if cambio_actual is None:
            raise ValueError("No hay CambioEstado vigente.")
        return cambio_actual
