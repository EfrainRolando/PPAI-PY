from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Iterable
from CambioEstado import CambioEstado
from Estado import Estado
from SerieTemporal import SerieTemporal
from AlcanceSismo import AlcanceSismo
from ClasificacionSismo import ClasificacionSismo
from OrigenGeneracion import OrigenDeGeneracion


@dataclass
class EventoSismico:
    fechaHoraFin: Optional[datetime]
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
    cambiosDeEstado: List[CambioEstado]

    # Consultas/Comandos
    def getActualCambioDeEstado(self):
        for ce in reversed(self.cambiosDeEstado):
            # tolerante si olvidás estaAbierto en algún lado
            if hasattr(ce, "estaAbierto"):
                if ce.estaAbierto():
                    return ce
            else:
                if getattr(ce, "fechaHoraFin", None) is None:
                    return ce
        return self.cambiosDeEstado[-1] if self.cambiosDeEstado else None

    def estadoActual(self):
        ce = self.getActualCambioDeEstado()
        return ce.estado if ce else None

    @staticmethod
    def buscarSismosARevisar(eventos):
        candidatos = []
        for e in eventos:
            ce = e.getActualCambioDeEstado()
            if not ce:
                continue
            # 👇 Llamadas de **instancia**, no a la clase
            if ce.sosAutoDetectado() or ce.sosParaRevision():
                candidatos.append(e)
        # si existe:
        try:
            candidatos.sort(key=lambda x: x.getFechaHoraOcurrencia())
        except Exception:
            pass
        return candidatos

    def crearCambioEstado(self, param, responsable, fecha):
        pass
