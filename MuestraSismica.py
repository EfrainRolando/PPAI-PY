from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from TipoDeDato import TipoDeDato


@dataclass
class DetalleMuestraSismica:
    valor: float
    tipoDato: TipoDeDato

    def obtenerDatosDetalleMuestra(self) -> dict:
        return {"valor": self.valor, "tipo": self.tipoDato.obtenerTipoDeDato()}


@dataclass
class MuestraSismica:
    fechaHoraMuestra: datetime
    detalles: List[DetalleMuestraSismica] = field(default_factory=list)

    def obtenerDatosMuestraSismica(self) -> dict:
        return {
            "fechaHoraMuestra": self.fechaHoraMuestra.isoformat(),
            "detalles": [d.obtenerDatosDetalleMuestra() for d in self.detalles]
        }

    def agregarDetalle(self, detalle: DetalleMuestraSismica) -> None:
        self.detalles.append(detalle)