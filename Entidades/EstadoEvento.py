from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from Entidades.CambioEstado import CambioEstado

class EstadoEvento(ABC):
    def adquirirDatos()-> None:
        pass
    def derivar()-> None:
        pass
    def confirmar()-> None:
        pass
    def rechazar()-> None:
        pass
    def cerrar()-> None:
        pass
    def controlarTiempo()-> None:
        pass
    def bloquear()-> None:
        pass


class AutoDetectado(EstadoEvento):
    NAME = "AutoDetectado"
    def controlarTiempo() -> None:
        pass
    def revisar() -> None:
        pass

class AutoConfirmado(EstadoEvento):
    NAME = "AutoConfirmado"
    def adquirirDatos()-> None:
        pass

class PendienteDeCierre(EstadoEvento):
    NAME = "PendienteDeCierre"
    def cerrar()-> None:
        pass

class Cerrado(EstadoEvento):
    NAME = "Cerrado"

class SinRevision(EstadoEvento):
    NAME = "SinRevision"

class ConfirmadoPorPersonal(EstadoEvento):
    NAME = "ConfirmadoPorPersonal"
    def adquirirDatos()-> None:
        pass

class Derivado(EstadoEvento):
    NAME = "Derivado"
    def confirmar()-> None:
        pass
    def rechazar()-> None:
        pass

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
        pass

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
        return Rechazado()
    
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
    def rechazar()-> None:
        pass