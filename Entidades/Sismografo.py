from dataclasses import dataclass
from typing import Optional

import repositorio_eventos
from EstacionSismologica import EstacionSismologica
from SerieTemporal import SerieTemporal


class Sismografo:
    codigo: Optional[str]
    estacion: Optional["EstacionSismologica"]
    nroSerie: Optional[int]
    seriesTemporales: list["SerieTemporal"]

    def __init__(self,
                 codigo: Optional[str] = None,
                 estacion: Optional["EstacionSismologica"] = None,
                 nroSerie: Optional[int] = None,
                 seriesTemporales: Optional[list["SerieTemporal"]] = None):
        self.codigo = codigo
        self.estacion = estacion
        self.nroSerie = nroSerie
        self.seriesTemporales = list(seriesTemporales) if seriesTemporales else []

    def getDatosSismografo(self) -> dict:
        return {
            "codigo": self.codigo,
            "estacion": self.estacion.getCodigoEstacion() if self.estacion else None
        }

    # (Opcional, para paso 13 del diagrama)
    def sosDeMiSerie(self: "SerieTemporal") -> Optional[str]:
        sismografos = repositorio_eventos.obtenerSismografos()
        for s in sismografos:
            for a in s.seriesTemporales:
                if getattr(a, "id", None) == getattr(self, "id", None):
                    # más claro y pitónico:
                    return s.estacion.getCodigoEstacion()
        return None
