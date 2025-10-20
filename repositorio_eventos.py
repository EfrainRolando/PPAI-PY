# repositorio_eventos.py
from datetime import datetime
from typing import List
from Estado import Estado
from CambioEstado import CambioEstado
from EventoSismico import EventoSismico

dt = lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M")


def obtener_eventos_predeterminados() -> List[EventoSismico]:
    # Cambios “ya hechos”
    c1 = CambioEstado(Estado("AutoDetectado", "EventoSismico"), dt("2025-10-06 09:14"), "sensor", fechaHoraFin=dt("2025-10-06 09:20"))
    c2 = CambioEstado(Estado("PteRevision", "EventoSismico"), dt("2025-10-06 09:20"), "analista")
    c3 = CambioEstado(Estado("AutoDetectado", "EventoSismico"), dt("2025-10-06 09:26"), "sensor")

    e1 = EventoSismico(
        id_evento=1, cambiosEstado=[c1, c2], fechaHoraFin=None,
        fechaHoraOcurrencia=dt("2025-10-06 09:40"),
        latitudEpicentro=-32.10, latitudHipocentro=-32.20,
        longitudEpicentro=-63.80, longitudHipocentro=-63.85,
        valorMagnitud=4.8, alcance=None, clasificacion=None,
        origenGeneracion=None, seriesTemporales=[]
    )

    e2 = EventoSismico(
        id_evento=2, cambiosEstado=[c3, c2], fechaHoraFin=None,
        fechaHoraOcurrencia=dt("2025-10-06 09:25"),
        latitudEpicentro=-32.11, latitudHipocentro=-32.21,
        longitudEpicentro=-63.82, longitudHipocentro=-63.87,
        valorMagnitud=3.9, alcance=None, clasificacion=None,
        origenGeneracion=None, seriesTemporales=[]
    )

    return [e1, e2]
