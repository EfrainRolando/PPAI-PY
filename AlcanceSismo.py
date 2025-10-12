
from dataclasses import dataclass

@dataclass(frozen=True)
class AlcanceSismo:
    descripcion: str
    nombre: str

    def getDatos(self) -> dict:
        return {"nombre": self.nombre, "descripcion": self.descripcion}
