
from dataclasses import dataclass

@dataclass(frozen=True)
class ClasificacionSismo:
    nombre: str
    kmProfundidadDesde: float
    kmProfundidadHasta: float

    def getDatos(self) -> dict:
        return {
            "nombre": self.nombre,
            "profundidadKm": [self.kmProfundidadDesde, self.kmProfundidadHasta],
        }