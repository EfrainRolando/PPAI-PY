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

    def estaAbierto(self) -> bool:
        return self.fechaHoraFin is None

    # ⚠️ NO @classmethod, NO @staticmethod
    def sosAutoDetectado(self) -> bool:
        # si Estado tiene helpers:
        try:
            return self.estado.sosDetectado()
        except AttributeError:
            # si Estado solo tiene .nombre (string)
            return (getattr(self.estado, "nombre", "") or "").strip().lower() == "detectado"

    def sosParaRevision(self) -> bool:
        try:
            return self.estado.sosParaRevision()
        except AttributeError:
            return (getattr(self.estado, "nombre", "") or "").strip().lower() == "pararevision"