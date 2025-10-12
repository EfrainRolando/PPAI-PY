from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from Estado import Estado

@dataclass
class CambioEstado:
    estado: Estado
    fechaHoraInicio: datetime
    responsable: Optional[str]
    fechaHoraFin: Optional[datetime] = None
    motivo: Optional[str] = None

    def cerrar(self, fin: datetime) -> None:
        self.fechaHoraFin = fin

    # atajos 'set*' del diagrama
    def setFechaYHoraInicio(self, ts: datetime): self.fechaHoraInicio = ts
    def setEstado(self, estado: Estado): self.estado = estado
    def setResponsable(self, nombre: str): self.responsable = nombre
    def setMotivo(self, texto: str): self.motivo = texto
