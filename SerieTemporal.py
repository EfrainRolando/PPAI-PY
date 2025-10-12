from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from MuestraSismica import MuestraSismica
from EstacionSismologica import EstacionSismologica


@dataclass
class SerieTemporal:
    condicionMarea: str
    fechaHoraInicioRegistroMuestras: datetime
    fechaHoraFinRegistroMuestras: datetime
    frecuenciaMuestreo: float  # Hz
    estacion: EstacionSismologica
    muestras: List[float] = field(default_factory=list)

    def getDatos(self) -> dict:
        return {
            "condicionMarea": self.condicionMarea,
            "desde": self.fechaHoraInicioRegistroMuestras.isoformat(),
            "hasta": self.fechaHoraFinRegistroMuestras.isoformat(),
            "frecuencia": self.frecuenciaMuestreo,
            "estacion": self.estacion.getCodigoEstacion(),
        }

    def agregarMuestra(self, muestra: MuestraSismica) -> None:
        self.muestras.append(muestra)

    def sosDeMiSerie(self, estacion_codigo: str) -> bool:
        return self.estacion.codigoEstacion == estacion_codigo
