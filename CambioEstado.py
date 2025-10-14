from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from Estado import Estado


@dataclass
class CambioEstado:
    def __init__(self, estado, fechaHoraInicio, responsable, motivo=None, fechaHoraFin=None):
        self.estado = estado
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin
        self.responsable = responsable
        self.motivo = motivo

    def sosActual(self) -> bool:
        return self.fechaHoraFin is None

    @classmethod
    def sosAutoDetectado(cls, evento) -> bool:
        """ Devuelve True si algún cambio del evento tiene estado AutoDetectado """
        for cambio in evento.cambiosEstado:
            if cambio.estado.sosAutoDetectado():
                return True
        return False

