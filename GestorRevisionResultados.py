from __future__ import annotations
from typing import List, Any, Optional, Iterable, Type, Dict
from datetime import datetime

from Estado import Estado
from EventoSismico import EventoSismico
from repositorio_eventos import obtener_eventos_predeterminados


class GestorRevisionResultados:
    def __init__(self):
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
        datos = self.buscarDatosEventoSismico(EventoSeleccionado)
        PantallaRevision().mostrarDatosEventoSismico(datos)

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

    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for a in Estado.AMBITOS_POSIBLES:
            if a == "EventoSismico":
                for n in Estado.NOMBRES_POSIBLES:
                    if n == "BloqueadoEnRevision":
                        return Estado(n, a)

    def getFechaYHoraActual(self) -> datetime:
        return datetime.now()

    def cambiarEstadoABloqueadoEnRevision(self, EventoSeleccionado, estadoBloqueado: Estado, fechaHoraInicio) -> None:
        EventoSismico.bloquearEvento(EventoSeleccionado, estadoBloqueado, fechaHoraInicio)

    def buscarDatosEventoSismico(self, evento: EventoSismico) -> Dict[str, Any]:
        EventoSismico.eventoSeleccionado = evento
        return {
            "evento": evento.getDatosEvento()
        }
