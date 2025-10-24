from dataclasses import dataclass
from typing import Optional

from Entidades.TipoDeDato import TipoDeDato


class DetalleMuestraSismica:
    valor: Optional[float]
    tipoDato: Optional["TipoDeDato"]

    def __init__(self, valor: Optional[float] = None, tipoDato: Optional["TipoDeDato"] = None):
        self.valor = valor
        self.tipoDato = tipoDato

    def obtenerDatosDetalleMuestras(self) -> dict:
        return {
            "valor": self.valor,
            "tipoDeDato": self.tipoDato.obtenerTipoDeDato() if self.tipoDato else None,
        }