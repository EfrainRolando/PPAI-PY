from dataclasses import dataclass


@dataclass(frozen=True)
class TipoDeDato:
    denominacion: str
    nombreUnidadDeMedida: str

    def obtenerTipoDeDato(self) -> str:
        return f"{self.denominacion} [{self.nombreUnidadDeMedida}]"