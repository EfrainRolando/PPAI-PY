from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any 
from Entidades.MuestraSismica import MuestraSismica


class SerieTemporal:
    def __init__(
        self,
        id: int,
        condicionMarea: Optional[str] = None,
        fechaHoraInicioRegistroMuestras: Optional[datetime] = None,
        fechaHoraFinRegistroMuestras: Optional[datetime] = None,
        frecuenciaMuestreo: Optional[float] = None,
        muestras: Optional[List["MuestraSismica"]] = None,
    ):
        self.id = id
        self.condicionMarea = condicionMarea
        self.fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
        self.fechaHoraFinRegistroMuestras = fechaHoraFinRegistroMuestras
        self.frecuenciaMuestreo = frecuenciaMuestreo
        self.muestras = list(muestras) if muestras else []
        self.sismografo: Optional["Sismografo"] = None  # back-ref opcional

    def setSismografo(self, sismografo: "Sismografo") -> None:
        self.sismografo = sismografo

    def getDatos(self) -> Dict[str, Any]:
        codigo = None
        if self.sismografo:
            # pide el código yendo Serie -> Sismógrafo -> Estación
            codigo = self.sismografo.sosDeMiSerie(self)

        return {
            "condicionMarea": self.condicionMarea,
            "desde": self.fechaHoraInicioRegistroMuestras,
            "hasta": self.fechaHoraFinRegistroMuestras,
            "frecuencia": self.frecuenciaMuestreo,
            "muestras": [m.obtenerDatosMuestraSismica() for m in (self.muestras or [])],
            "CodigoEstacion": codigo,
        }