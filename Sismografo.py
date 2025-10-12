from dataclasses import dataclass
from EstacionSismologica import EstacionSismologica

@dataclass
class Sismografo:
    codigo: str
    estacion: EstacionSismologica
    nroSerie: int

    def getDatosSismografo(self) -> dict:
        return {"codigo": self.codigo, "estacion": self.estacion.getCodigoEstacion()}