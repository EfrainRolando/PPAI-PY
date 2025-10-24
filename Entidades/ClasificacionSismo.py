from dataclasses import dataclass, asdict


@dataclass
class ClasificacionSismo:
    nombre: str
    kmProfundidadDesde: float
    kmProfundidadHasta: float

    def getDatos(self) -> dict:
        return asdict(self)
