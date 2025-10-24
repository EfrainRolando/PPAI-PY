from datetime import datetime, date
from typing import List

from Entidades.AlcanceSismo import AlcanceSismo
from Entidades.ClasificacionSismo import ClasificacionSismo
from Entidades.DetalleMuestraSismica import DetalleMuestraSismica
from Entidades.EstacionSismologica import EstacionSismologica
from Entidades.Estado import Estado
from Entidades.CambioEstado import CambioEstado
from Entidades.EventoSismico import EventoSismico
from Entidades.MuestraSismica import MuestraSismica
from Entidades.OrigenGeneracion import OrigenDeGeneracion
from Entidades.SerieTemporal import SerieTemporal
from Entidades.Sismografo import Sismografo

dt = lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M")


def obtener_eventos_predeterminados() -> List[EventoSismico]:
    # Cambios “ya hechos”
    c1 = CambioEstado(Estado("AutoDetectado", "EventoSismico"), dt("2025-10-06 09:14"), "sensor",
                      fechaHoraFin=dt("2025-10-06 09:20"))
    c2 = CambioEstado(Estado("PteRevision", "EventoSismico"), dt("2025-10-06 09:20"), "analista")
    c3 = CambioEstado(Estado("AutoDetectado", "EventoSismico"), dt("2025-10-06 09:26"), "sensor")
    alcances = [
        AlcanceSismo("Local", "Percibido solo en el epicentro"),
        AlcanceSismo("Regional", "Percibido en varias ciudades"),
        AlcanceSismo("Lejano", "Percibido a gran distancia"),
    ]

    clasificaciones = [
        ClasificacionSismo("Leve", 18.5, 20.9),
        ClasificacionSismo("Moderado", 74.1, 78),
        ClasificacionSismo("Fuerte", 10.5, 15),
    ]

    origenes = [
        OrigenDeGeneracion("Tectónico", "Por movimientos de placas"),
        OrigenDeGeneracion("Volcánico", "Por actividad magmática"),
        OrigenDeGeneracion("Inducido", "Por actividad humana"),
    ]

    # Construcción de Series/Muestras/Detalles
    st1 = SerieTemporal(
        id=1,
        condicionMarea="Normal",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:14"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:20"),
        frecuenciaMuestreo=100.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:15"), [
                DetalleMuestraSismica(0.012),
                DetalleMuestraSismica(0.20),
            ]),
            MuestraSismica(dt("2025-10-06 09:16"), [
                DetalleMuestraSismica(0.018),
                DetalleMuestraSismica(0.50),
            ]),
        ],
    )
    st2 = SerieTemporal(
        id=2,
        condicionMarea="Normal",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:20"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:26"),
        frecuenciaMuestreo=200.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:21"), [DetalleMuestraSismica(0.009)]),
            MuestraSismica(dt("2025-10-06 09:22"), [DetalleMuestraSismica(0.12)]),
        ],
    )
    st3 = SerieTemporal(
        id=3,
        condicionMarea="Alta",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:26"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:30"),
        frecuenciaMuestreo=50.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:26"), [DetalleMuestraSismica(0.35)]),
        ],
    )
    st4 = SerieTemporal(
        id=4,
        condicionMarea="Baja",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:17"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:19"),
        frecuenciaMuestreo=100.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:18"), [DetalleMuestraSismica(0.006)]),
        ]
    )

    e1 = EventoSismico(
        id_evento=1, cambiosEstado=[c1, c2], fechaHoraFin=None,
        fechaHoraOcurrencia=dt("2025-10-06 09:40"),
        latitudEpicentro=-32.10, latitudHipocentro=-32.20,
        longitudEpicentro=-63.80, longitudHipocentro=-63.85,
        valorMagnitud=4.8, alcance=alcances[1], clasificacion=clasificaciones[0],
        origenGeneracion=origenes[1], seriesTemporales=[st1, st2]
    )

    e2 = EventoSismico(
        id_evento=2, cambiosEstado=[c3, c2], fechaHoraFin=None,
        fechaHoraOcurrencia=dt("2025-10-06 09:25"),
        latitudEpicentro=-32.11, latitudHipocentro=-32.21,
        longitudEpicentro=-63.82, longitudHipocentro=-63.87,
        valorMagnitud=3.9, alcance=alcances[2], clasificacion=clasificaciones[1],
        origenGeneracion=origenes[0], seriesTemporales=[st1, st3, st4]
    )

    return [e1, e2]


def obtenerSismografos() -> list[Sismografo]:
    estaciones = [
        EstacionSismologica("CBA-01", -31.41, -64.19),
        EstacionSismologica("CBA-02", -31.35, -64.21),
        EstacionSismologica("CBA-03", -31.46, -64.20)
    ]
    st1 = SerieTemporal(
        id=1,
        condicionMarea="Normal",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:14"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:20"),
        frecuenciaMuestreo=100.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:15"), [
                DetalleMuestraSismica(0.012),
                DetalleMuestraSismica(0.20),
            ]),
            MuestraSismica(dt("2025-10-06 09:16"), [
                DetalleMuestraSismica(0.018),
                DetalleMuestraSismica(0.50),
            ]),
        ],
    )
    st2 = SerieTemporal(
        id=2,
        condicionMarea="Normal",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:20"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:26"),
        frecuenciaMuestreo=200.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:21"), [DetalleMuestraSismica(0.009)]),
            MuestraSismica(dt("2025-10-06 09:22"), [DetalleMuestraSismica(0.12)]),
        ],
    )
    st3 = SerieTemporal(
        id=3,
        condicionMarea="Alta",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:26"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:30"),
        frecuenciaMuestreo=50.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:26"), [DetalleMuestraSismica(0.35)]),
        ],
    )
    st4 = SerieTemporal(
        id=4,
        condicionMarea="Baja",
        fechaHoraInicioRegistroMuestras=dt("2025-10-06 09:17"),
        fechaHoraFinRegistroMuestras=dt("2025-10-06 09:19"),
        frecuenciaMuestreo=100.0,
        muestras=[
            MuestraSismica(dt("2025-10-06 09:18"), [DetalleMuestraSismica(0.006)]),
        ]
    )

    s1 = Sismografo("SG-001", estaciones[1], seriesTemporales=[st1, st3])
    s2 = Sismografo("SG-002", estaciones[0], seriesTemporales=[st4])
    s3 = Sismografo("SG-003", estaciones[2], seriesTemporales=[st2])
    return [s1, s2, s3]
