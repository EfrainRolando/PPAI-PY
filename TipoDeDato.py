from dataclasses import dataclass
from typing import Optional


class TipoDeDato:
    denominacion: Optional[str]
    nombreUnidadDeMedida: Optional[str]

    def __init__(self, denominacion: Optional[str] = None, nombreUnidadDeMedida: Optional[str] = None):
        self.denominacion = denominacion
        self.nombreUnidadDeMedida = nombreUnidadDeMedida

    def obtenerTipoDeDato(self) -> dict:
        return {
            "denominacion": self.denominacion,
            "nombreUnidadDeMedida": self.nombreUnidadDeMedida,
        }