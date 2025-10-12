from datetime import datetime
from dataclasses import dataclass


@dataclass
class EstacionSismologica:
    codigoEstacion: str
    laltitud: float
    longitud: float
    nombre: str
    documentoCertificacion: []
    fechaSolicitudCertificacion: datetime
    nroCertificacionAdquisicion: int

    # +otros atributos omitidos del diagrama

    def getCodigoEstacion(self) -> str:
        return self.codigoEstacion
