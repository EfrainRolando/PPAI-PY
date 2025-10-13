from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Iterable
from EventoSismico import EventoSismico
from Estado import Estado


@dataclass
class GestorRevisionResultados:
    def __init__(self, eventos, sesion=None, eventoSeleccionado=None):
        self.eventos = eventos
        self.sesion = sesion
        self.eventoSeleccionado = eventoSeleccionado

    # --- Primera parte del diagrama ---
def registrarResultado(self) -> None:
    gestor = GestorRevisionResultados
    print("Gestor Creado!")


def buscarSismosARevisar(self) -> List[EventoSismico]:
    return [e for e in self.eventos if e.sosAutoDetectado() or e.sosParaRevision()]


def ordenarEventosSismicosFechaOcurrencia(self, eventos: Iterable[EventoSismico]) -> List[EventoSismico]:
    return sorted(eventos, key=lambda e: e.getFechaHoraOcurrencia())


def buscarEstadoBloqueadoEnRevision(self, evento: EventoSismico) -> Optional[Estado]:
    est = evento.estadoActual()
    return est if est.sosBloqueadoEnRevision() else None


def bloquearEvento(self, evento: EventoSismico) -> None:
    evento.bloquearEvento(datetime.now(), self.sesion.getUsuarioLogueado() if self.sesion else "sistema")

    # --- Segunda parte: obtener datos enriquecidos y llamar CU generar sismograma ---


def getDatosEvento(self, evento: EventoSismico) -> dict:
    return evento.getDatosSismo()


def obtenerDatosSeriesTemporales(self, evento: EventoSismico):
    return evento.obtenerDatosSeriesTemporales()

    # --- Tercera parte: acciones ---


def presentarAcciones(self) -> List[str]:
    return ["Rechazar", "Aprobar", "Volver"]


def rechazar(self, motivo: str = "Datos inválidos") -> None:
    if not self.eventoSeleccionado: return
    self.eventoSeleccionado.rechazarEvento(datetime.now(),
                                           self.sesion.getUsuarioLogueado() if self.sesion else "sistema", motivo)


