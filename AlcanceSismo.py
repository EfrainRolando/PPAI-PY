from dataclasses import dataclass, asdict


@dataclass
class AlcanceSismo:
    nombre: str
    descripcion: str = ""

    def getDatos(self) -> dict:
        return asdict(self)
