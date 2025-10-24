from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from Entidades.DetalleMuestraSismica import DetalleMuestraSismica


class MuestraSismica:
    fechaHoraMuestra: Optional[datetime]
    detalles: List["DetalleMuestraSismica"]

    def __init__(self,
                 fechaHoraMuestra: Optional[datetime] = None,
                 detalles: Optional[List["DetalleMuestraSismica"]] = None):
        self.fechaHoraMuestra = fechaHoraMuestra
        self.detalles = list(detalles) if detalles is not None else []

    def obtenerDatosMuestraSismica(self) -> dict:
        return {
            "fechaHoraMuestra": self.fechaHoraMuestra.isoformat() if self.fechaHoraMuestra else None,
            "detalles": [d.obtenerDatosDetalleMuestras() for d in (self.detalles or [])],
        }

    def agregarDetalle(self, detalle: DetalleMuestraSismica) -> None:
        self.detalles.append(detalle)
