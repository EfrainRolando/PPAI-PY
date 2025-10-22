from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List


class EstacionSismologica:
    def __init__(
        self,
        codigoEstacion: Optional[str] = None,
        latitud: Optional[float] = None,
        longitud: Optional[float] = None,
        nombre: Optional[str] = None,
        documentoCertificacion: Optional[List[str]] = None,
        fechaSolicitudCertificacion: Optional[datetime] = None,
        nroCertificacionAdquisicion: Optional[int] = None
    ):
        self.codigoEstacion = codigoEstacion
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.documentoCertificacion = documentoCertificacion or []
        self.fechaSolicitudCertificacion = fechaSolicitudCertificacion
        self.nroCertificacionAdquisicion = nroCertificacionAdquisicion

    # +otros atributos omitidos del diagrama

    def getCodigoEstacion(self) -> str:
        return self.codigoEstacion
