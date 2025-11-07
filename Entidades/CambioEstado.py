from datetime import datetime
from typing import Optional, Any

class CambioEstado:
    def __init__(self, estado: Any, fechaHoraInicio: datetime,
                 responsable: str, motivo: Optional[str] = None,
                 fechaHoraFin: Optional[datetime] = None):
        # estado puede ser un STATE (PteRevision(), BloqueadoEnRevision(), etc.)
        # o una ENTIDAD Estado(nombre="...") —compatibilidad
        self.estado = estado
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin
        self.responsable = responsable
        self.motivo = motivo

    def esActual(self) -> bool:
        return self.fechaHoraFin is None

    # ===== Helpers de compatibilidad =====
    def _estado_tiene(self, attr: str) -> bool:
        return hasattr(self.estado, attr)

    def _estado_nombre(self) -> Optional[str]:
        # STATE con atributo NAME (convención) o método nombre()
        if self._estado_tiene("NAME"):
            return getattr(self.estado, "NAME")
        if self._estado_tiene("nombre"):
            val = getattr(self.estado, "nombre")
            # nombre puede ser callable (método) o str
            return val() if callable(val) else val
        return None

    def sosAutoDetectado(self) -> bool:
        if self._estado_tiene("sosAutoDetectado"):
            return self.estado.sosAutoDetectado()
        return self._estado_nombre() == "AutoDetectado"

    def sosPteRevision(self) -> bool:
        if self._estado_tiene("sosPteRevision"):
            return self.estado.sosPteRevision()
        return self._estado_nombre() == "PteRevision"

    def setFechaHoraFin(self, fechaHoraFin):
        self.fechaHoraFin = fechaHoraFin

    def setFechaHoraInicio(self, fechaHoraInicio):
        self.fechaHoraInicio = fechaHoraInicio

    def setEstado(self, nuevo_estado: Any):
        self.estado = nuevo_estado
