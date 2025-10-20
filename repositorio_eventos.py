from datetime import datetime
from typing import List

from AlcanceSismo import AlcanceSismo
from ClasificacionSismo import ClasificacionSismo
from Estado import Estado
from CambioEstado import CambioEstado
from EventoSismico import EventoSismico
from OrigenGeneracion import OrigenDeGeneracion

dt = lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M")


def obtener_eventos_predeterminados() -> List[EventoSismico]:
    # Cambios “ya hechos”
    c1 = CambioEstado(Estado("AutoDetectado", "EventoSismico"), dt("2025-10-06 09:14"), "sensor", fechaHoraFin=dt("2025-10-06 09:20"))
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

    e1 = EventoSismico(
        id_evento=1, cambiosEstado=[c1, c2], fechaHoraFin=None,
        fechaHoraOcurrencia=dt("2025-10-06 09:40"),
        latitudEpicentro=-32.10, latitudHipocentro=-32.20,
        longitudEpicentro=-63.80, longitudHipocentro=-63.85,
        valorMagnitud=4.8, alcance=alcances[1], clasificacion=clasificaciones[0],
        origenGeneracion=origenes[1], seriesTemporales=[]
    )

    e2 = EventoSismico(
        id_evento=2, cambiosEstado=[c3, c2], fechaHoraFin=None,
        fechaHoraOcurrencia=dt("2025-10-06 09:25"),
        latitudEpicentro=-32.11, latitudHipocentro=-32.21,
        longitudEpicentro=-63.82, longitudHipocentro=-63.87,
        valorMagnitud=3.9, alcance=alcances[2], clasificacion=clasificaciones[1],
        origenGeneracion=origenes[0], seriesTemporales=[]
    )

    return [e1, e2]
