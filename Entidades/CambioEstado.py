from datetime import datetime
from typing import Optional
from Entidades.Estado import Estado


class CambioEstado:
    def __init__(self, estado: Estado, fechaHoraInicio: datetime,
                 responsable: str, motivo: Optional[str] = None,
                 fechaHoraFin: Optional[datetime] = None):
        self.estado = estado
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin
        self.responsable = responsable
        self.motivo = motivo

    def esActual(self) -> bool:  # o sosActual, como prefieras
        # actual si no tiene fin (o si usás “vigente”, ajustá lógica aquí)
        return self.fechaHoraFin is None

    def sosAutoDetectado(self) -> bool:
    # ANTES: return self.estado.nombre.sosAutoDetectado()
        return self.estado.sosAutoDetectado()

    def sosPteRevision(self) -> bool:
    # ANTES: return self.estado.nombre.sosPteRevision()
        return self.estado.sosPteRevision()

    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin

    def setFechaHoraInicio(self, fechaHoraInicio):
        self.fechaHoraInicio = fechaHoraInicio

    def setEstadoBloqueado(self, estadoBloqueado):
        self.estado = estadoBloqueado
