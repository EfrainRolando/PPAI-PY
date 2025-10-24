from dataclasses import dataclass, asdict


@dataclass
class OrigenDeGeneracion:
    nombre: str  # p.ej. "Tectónico", "Volcánico"
    descripcion: str = ""

    def getDatos(self) -> dict:
        return asdict(self)
