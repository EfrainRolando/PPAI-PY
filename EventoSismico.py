from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any
from CambioEstado import CambioEstado
from SerieTemporal import SerieTemporal
from AlcanceSismo import AlcanceSismo
from ClasificacionSismo import ClasificacionSismo
from OrigenGeneracion import OrigenDeGeneracion


class EventoSismico:
    def __init__(
            self,
            id_evento: int,
            cambiosEstado: Optional[List[CambioEstado]] = None,
            fechaHoraFin: Optional[datetime] = None,
            fechaHoraOcurrencia: Optional[datetime] = None,
            latitudEpicentro: Optional[float] = None,
            latitudHipocentro: Optional[float] = None,
            longitudEpicentro: Optional[float] = None,
            longitudHipocentro: Optional[float] = None,
            valorMagnitud: Optional[float] = None,
            alcance: Optional[AlcanceSismo] = None,
            clasificacion: Optional[ClasificacionSismo] = None,
            origenGeneracion: Optional[OrigenDeGeneracion] = None,
            seriesTemporales: Optional[List[SerieTemporal]] = None,
            cambioEstadoActual: Optional[CambioEstado] = None
    ) -> None:
        self.id_evento = id_evento
        self.cambiosEstado: List[CambioEstado] = list(cambiosEstado or [])
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudEpicentro = longitudEpicentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud
        self.alcance = alcance
        self.clasificacion = clasificacion
        self.origenGeneracion = origenGeneracion
        self.seriesTemporales: List[SerieTemporal] = list(seriesTemporales or [])
        self.cambioEstadoActual = cambioEstadoActual

    # ---------- reglas locales ----------
    def buscarSismosARevisar(self) -> bool:
        AD = 0
        for c in self.cambiosEstado:
            if CambioEstado.sosAutoDetectado(c):
                AD = 1
            if CambioEstado.sosPteRevision(c) and CambioEstado.esActual(c) and AD == 1:
                return True

    def getFechaHoraOcurrencia(self):
        return self.fechaHoraOcurrencia

    def getMagnitud(self):
        return self.valorMagnitud

    def getDatosSismos(self) -> Dict:
        return {
            "id_evento": self.id_evento,
            "fechaHoraOcurrencia": self.getFechaHoraOcurrencia(),
            "magnitud": self.getMagnitud(),
            "latitudEpicentro": self.latitudEpicentro,
            "longitudEpicentro": self.longitudEpicentro,
            "latitudHipocentro": self.latitudHipocentro,
            "longitudHipocentro": self.longitudHipocentro
        }

    def bloquearEvento(self, estadoBloqueado, fechaHora):
        for c in self.cambiosEstado:
            if CambioEstado.esActual(c):
                self.cambioEstadoActual = c
        self.cambioEstadoActual.setFechaHoraFin(fechaHora)
        bloqueado = CambioEstado(
            estado=estadoBloqueado,
            fechaHoraInicio=fechaHora,
            responsable="User"
        )
        self.cambiosEstado.append(bloqueado)
        self.cambioEstadoActual = bloqueado
        print("Cambio de estado actualizado!")
        print("Evento:", self.id_evento)
        print("Estado Actual del Evento:", self.cambioEstadoActual.estado)
        print("Fecha Hora Inicio del Cambio de estado:", self.cambioEstadoActual.fechaHoraInicio)
