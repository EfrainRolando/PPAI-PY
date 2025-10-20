from __future__ import annotations
from typing import List, Any, Optional, Iterable
from datetime import datetime

from Estado import Estado
from EventoSismico import EventoSismico
from repositorio_eventos import obtener_eventos_predeterminados


class GestorRevisionResultados:
    def __init__(self) -> None:
        self.eventos: List[EventoSismico] = obtener_eventos_predeterminados()

    def registrarResultado(self) -> None:
        print("Gestor creado → registrando resultado...")
        datos = self.buscarSismosARevisar()
        datos_ordenados = self.ordenarEventosPorFechaOcurrencia(datos)
        from PantallaRevision import PantallaRevision
        PantallaRevision().mostrarDatosEventosSismicos(datos_ordenados)
        EventoSeleccionado = PantallaRevision().solicitarSeleccionEventoSismico()
        EstadoBloqueado = self.buscarEstadoBloqueadoEnRevision()
        fechaHoraActual = self.getFechaYHoraActual()
        self.cambiarEstadoABloqueadoEnRevision(EventoSeleccionado, EstadoBloqueado, fechaHoraActual)
        #self.buscarDatosEventoSismico()

    def buscarSismosARevisar(self) -> List[dict]:
        """Filtra los eventos que deben ser revisados"""
        eventos_a_revisar = []
        for e in self.eventos:
            if e.buscarSismosARevisar():
                eventos_a_revisar.append(e.getDatosSismos())
        return eventos_a_revisar

    def ordenarEventosPorFechaOcurrencia(self, datos: List[dict]) -> List[dict]:
        """Ordena los eventos según su fechaHoraOcurrencia"""
        return sorted(
            datos,
            key=lambda d: d.get("fechaHoraOcurrencia", datetime.min)
        )

    def tomarSeleccionEventoSismico(self, eleccion) -> EventoSismico:
        for e in self.eventos:
            if eleccion == e.id_evento:
                return e

    def buscarEstadoBloqueadoEnRevision(self) -> str:
        for a in Estado.AMBITOS_POSIBLES:
            AEV = 0
            if a == "EventoSismico":
                AEV = 1
            for n in Estado.NOMBRES_POSIBLES:
                if AEV == 1 and n == "BloqueadoEnRevision":
                    return n

    def getFechaYHoraActual(self) -> datetime:
        return datetime.now()

    def cambiarEstadoABloqueadoEnRevision(self, EventoSeleccionado, estadoBloqueado, fechaHoraInicio) -> None:
        EventoSismico.bloquearEvento(EventoSeleccionado, estadoBloqueado, fechaHoraInicio)

   # def buscarDatosEventoSismico(self):

