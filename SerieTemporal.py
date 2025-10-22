from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from MuestraSismica import MuestraSismica
from EstacionSismologica import EstacionSismologica


class SerieTemporal:
    condicionMarea: Optional[str]
    fechaHoraInicioRegistroMuestras: Optional[datetime]
    fechaHoraFinRegistroMuestras: Optional[datetime]
    frecuenciaMuestreo: Optional[float]  # Hz
    muestras: List["MuestraSismica"]

    def __init__(
            self,
            condicionMarea: Optional[str] = None,
            fechaHoraInicioRegistroMuestras: Optional[datetime] = None,
            fechaHoraFinRegistroMuestras: Optional[datetime] = None,
            frecuenciaMuestreo: Optional[float] = None,
            muestras: Optional[List["MuestraSismica"]] = None,
    ):
        self.condicionMarea = condicionMarea
        self.fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
        self.fechaHoraFinRegistroMuestras = fechaHoraFinRegistroMuestras
        self.frecuenciaMuestreo = frecuenciaMuestreo
        self.muestras = list(muestras) if muestras else []

    def getDatos(self) -> dict:
        return {
            "condicionMarea": self.condicionMarea,
            "desde": self.fechaHoraInicioRegistroMuestras.isoformat()
                     if self.fechaHoraInicioRegistroMuestras else None,
            "hasta": self.fechaHoraFinRegistroMuestras.isoformat()
                     if self.fechaHoraFinRegistroMuestras else None,
            "frecuencia": self.frecuenciaMuestreo,
            "muestras": [m.obtenerDatosMuestraSismica() for m in (self.muestras or [])],
        }

    def agregarMuestra(self, muestra: MuestraSismica) -> None:
        self.muestras.append(muestra)
