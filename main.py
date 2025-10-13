from datetime import datetime, timedelta
from typing import List, Dict

from EventoSismico import EventoSismico
from Estado import Estado
from PantallaRevision import PantallaRevision
from GestorRevisionResultados import GestorRevisionResultados
from EstacionSismologica import EstacionSismologica
from SerieTemporal import SerieTemporal


def fabricar_evento(lat=-34.6, lon=-58.4, mag=4.2, estado="Detectado") -> EventoSismico:
    est = EstacionSismologica(
        codigoEstacion="BUE01",
        nombre="BsAs",
        documentoCertificacion="DOC123",
        fechaSolicitudCertificacion=datetime(2024, 5, 1),
        nroCertificacionAdquisicion=999,
        latitud=121,
        longitud=11,
    )
    serie = SerieTemporal("baja", datetime.now() - timedelta(hours=1), datetime.now(), 100.0, est, muestras=[0.12, 0.15, 0.10, 0.05, -0.02, -0.10, -0.08])
    e = EventoSismico(
        fechaHoraFin=None,
        fechaHoraOcurrencia=datetime.now() - timedelta(minutes=10),
        latitudEpicentro=lat,
        latitudHipocentro=lat,
        longitudEpicentro=lon,
        longitudHipocentro=lon,
        valorMagnitud=mag,
        alcance=None,  # por ahora
        clasificacion=None,  # por ahora
        origenGeneracion=None,  # por ahora
        seriesTemporales=[serie],
        cambiosDeEstado=[]
    )
    e.crearCambioEstado(Estado(estado), responsable="sistema", fecha=datetime.now() - timedelta(minutes=9))
    return e


def main():
    eventos = [
        fabricar_evento(mag=3.1, estado="Detectado"),
        fabricar_evento(mag=5.0, estado="PteRevision")
    ]

    gestor = GestorRevisionResultados(eventos=eventos)
    pantalla = PantallaRevision()

    pantalla.opcionRegistrarResultado()


if __name__ == '__main__':
    main()
