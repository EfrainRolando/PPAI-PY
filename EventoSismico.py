from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
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
    ) -> None:
        # ==== Mismos nombres de atributos que tu dataclass original ====
        self.id_evento: int = id_evento
        self.cambiosEstado: List[CambioEstado] = list(cambiosEstado or [])
        self.fechaHoraFin: Optional[datetime] = fechaHoraFin
        self.fechaHoraOcurrencia: Optional[datetime] = fechaHoraOcurrencia
        self.latitudEpicentro: Optional[float] = latitudEpicentro
        self.latitudHipocentro: Optional[float] = latitudHipocentro
        self.longitudEpicentro: Optional[float] = longitudEpicentro
        self.longitudHipocentro: Optional[float] = longitudHipocentro if (longitudHipocentro is not None) else None
        self.valorMagnitud: Optional[float] = valorMagnitud
        self.alcance: Optional[AlcanceSismo] = alcance
        self.clasificacion: Optional[ClasificacionSismo] = clasificacion
        self.origenGeneracion: Optional[OrigenDeGeneracion] = origenGeneracion
        self.seriesTemporales: List[SerieTemporal] = list(seriesTemporales or [])

    # ✅ Método de clase usado por el Gestor
    @classmethod
    def buscarSismosARevisar(cls, lista_eventos: List["EventoSismico"]) -> list[None]:
        """

        :rtype: object
        """
        eventos_a_revisar = []
        datosEventos = []
        for e in lista_eventos:
            ad = 0
            for cambio in e.cambiosEstado:
                if cambio.sosAutoDetectado():
                    ad = 1
                if cambio.sosPteRevision() and cambio.esActual() and ad == 1:
                    datosEventos.append(e.getDatosSismos())
                    break
        return datosEventos

    def getFechaHoraOcurrencia(self):
        return self.fechaHoraOcurrencia

    def getUbicacionOcurrencia(self):
        return self.longitudHipocentro, self.latitudHipocentro, self.longitudEpicentro, self.latitudEpicentro

    def getMagnitud(self):
        return self.valorMagnitud

    def getDatosSismos(self) -> Dict:
        return {
            "id_evento": self.id_evento,
            "fechaHoraOcurrencia": self.getFechaHoraOcurrencia(),
            "magnitud": self.getMagnitud(),
            # ⬇⬇⬇ claves iguales a las que usás en la pantalla
            "latitudEpicentro": self.latitudEpicentro,
            "longitudEpicentro": self.longitudEpicentro,
            "latitudHipocentro": self.latitudHipocentro,
            "longitudHipocentro": self.longitudHipocentro
        }
