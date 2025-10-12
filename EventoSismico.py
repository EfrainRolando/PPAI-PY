from __future__ import annotations

import CambioEstado


class EventoSismico:
    def __init__(self, fechaHoraFin, fechaHoraOcurrencia, latitudEpicentro, latitudHipocentro, longitudEpicentro, longitudHipocentro, valorMagnitud, CambioDeEstado):
        self.cambiosDeEstado = []
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudEpicentro = longitudEpicentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud
        self.serieTemporal = []
        self.estadoActual = []
        self.cambiosEstado = []
        self.alcanceSismo = []
        self.clasificacion = []
        self.origenGeneracion = []



    def buscarSismosARevisar(self):
        for Evento in EventoSismico:
            if CambioEstado.sosAutoDetectado() == True:
                return [Evento]

    def crearCambioEstado(self, estado, responsable: str, fecha, motivo: str | None = None):
        nuevo = CambioEstado