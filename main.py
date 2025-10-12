from datetime import datetime

from Estado import Estado
from EventoSismico import EventoSismico
from GestorRevisionResultados import GestorRevisionResultados


def dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M")

# Asegurate que existen:
# class Estado: def __init__(self, nombre: str): self.nombre = nombre
# class CambioEstado: (estado, fechaHoraInicio, fechaHoraFin=None, responsable=None, motivo=None)
# class EventoSismico: tiene lista cambiosDeEstado y método crearCambioEstado(estado, responsable, fecha)

# ---- Crear 4 eventos "seed" ----
evento1 = EventoSismico(
    fechaHoraFin=None,
    fechaHoraOcurrencia=dt("2025-10-06 09:13"),
    latitudEpicentro=-32.10, latitudHipocentro=-32.20,
    longitudEpicentro=-63.80, longitudHipocentro=-63.85,
    valorMagnitud=3.5,
)
evento1.crearCambioEstado(Estado("Evento","Detectado"),    "sensor",    dt("2025-10-06 09:14"))
evento1.crearCambioEstado(Estado("Evento","ParaRevision"), "analista1", dt("2025-10-06 09:20"))

evento2 = EventoSismico(
    fechaHoraFin=None,
    fechaHoraOcurrencia=dt("2025-10-06 09:25"),
    latitudEpicentro=-32.11, latitudHipocentro=-32.21,
    longitudEpicentro=-63.82, longitudHipocentro=-63.87,
    valorMagnitud=4.8,
)
evento2.crearCambioEstado(Estado("Evento","Detectado"),   "sensor",    dt("2025-10-06 09:26"))
evento2.crearCambioEstado(Estado("Evento","Rechazado"),   "analista2", dt("2025-10-06 09:35"))

evento3 = EventoSismico(
    fechaHoraFin=None,
    fechaHoraOcurrencia=dt("2025-10-06 09:40"),
    latitudEpicentro=-32.12, latitudHipocentro=-32.22,
    longitudEpicentro=-63.83, longitudHipocentro=-63.88,
    valorMagnitud=5.1,
)
evento3.crearCambioEstado(Estado("Evento", "Detectado"),            "sensor",    dt("2025-10-06 09:41"))
evento3.crearCambioEstado(Estado("Evento", "ParaRevision"),         "analista1", dt("2025-10-06 09:50"))
evento3.crearCambioEstado(Estado("Evento", "BloqueadoEnRevision"),  "analista1", dt("2025-10-06 09:55"))

evento4 = EventoSismico(
    fechaHoraFin=None,
    fechaHoraOcurrencia=dt("2025-10-06 09:55"),
    latitudEpicentro=-32.13, latitudHipocentro=-32.23,
    longitudEpicentro=-63.84, longitudHipocentro=-63.89,
    valorMagnitud=4.2,
)
evento4.crearCambioEstado(Estado("Evento", "Detectado"),    "sensor",    dt("2025-10-06 09:56"))
evento4.crearCambioEstado(Estado("Evento", "ParaRevision"), "analista1", dt("2025-10-06 10:00"))
evento4.crearCambioEstado(Estado("Evento", "Aprobado"),     "jefe",      dt("2025-10-06 10:10"))

eventos = [evento1, evento2, evento3, evento4]
gestor = GestorRevisionResultados
candidatos = gestor.buscarSismosARevisar(eventos)
print(candidatos)