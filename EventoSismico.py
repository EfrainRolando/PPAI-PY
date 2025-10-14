from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List
from CambioEstado import CambioEstado
from SerieTemporal import SerieTemporal
from AlcanceSismo import AlcanceSismo
from ClasificacionSismo import ClasificacionSismo
from OrigenGeneracion import OrigenDeGeneracion


@dataclass
class EventoSismico:
    id_evento: int
    cambiosEstado: List[CambioEstado]
    fechaHoraFin: datetime
    fechaHoraOcurrencia: datetime
    latitudEpicentro: float
    latitudHipocentro: float
    longitudEpicentro: float
    longitudHipocentro: float
    valorMagnitud: float
    alcance: AlcanceSismo
    clasificacion: ClasificacionSismo
    origenGeneracion: OrigenDeGeneracion
    seriesTemporales: List[SerieTemporal]

    # ✅ Método de clase usado por el Gestor
    @classmethod
    def buscarSismosARevisar(cls, lista_eventos: List[EventoSismico]) -> List[EventoSismico]:
        eventos_a_revisar = []
        for e in lista_eventos:
            if CambioEstado.sosAutoDetectado(e):
                eventos_a_revisar.append(e)
                return eventos_a_revisar


