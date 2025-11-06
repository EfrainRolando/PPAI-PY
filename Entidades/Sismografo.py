from __future__ import annotations
from typing import Optional, List
from Entidades.SerieTemporal import SerieTemporal
from Entidades.EstacionSismologica import EstacionSismologica

class Sismografo:
    def __init__(
        self,
        codigo: Optional[str] = None,
        estacion: Optional[EstacionSismologica] = None,
        nroSerie: Optional[int] = None,
        seriesTemporales: Optional[List[SerieTemporal]] = None,
    ):
        self.codigo = codigo
        self.estacion = estacion
        self.nroSerie = nroSerie
        self.seriesTemporales = list(seriesTemporales) if seriesTemporales else []
        # asegurar back-ref
        for st in self.seriesTemporales:
            if getattr(st, "sismografo", None) is None:
                st.setSismografo(self)

    def getDatosSismografo(self) -> dict:
        return {
            "codigo": self.codigo,
            "estacion": self.estacion.getCodigoEstacion() if self.estacion else None,
        }

    def sosDeMiSerie(self, serie: SerieTemporal) -> Optional[str]:
        if serie is None:
            return None
        if getattr(serie, "sismografo", None) is self:
            return self.estacion.getCodigoEstacion() if self.estacion else None
        if serie in self.seriesTemporales:
            serie.setSismografo(self)
            return self.estacion.getCodigoEstacion() if self.estacion else None
        return None