from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any, Type
from Entidades.CambioEstado import CambioEstado
from Entidades.Estado import Estado
from Entidades.SerieTemporal import SerieTemporal
from Entidades.AlcanceSismo import AlcanceSismo
from Entidades.ClasificacionSismo import ClasificacionSismo
from Entidades.OrigenGeneracion import OrigenDeGeneracion


class EventoSismico:
    def __init__(
            self,
            id_evento: int,
            cambiosEstado: Optional[List[CambioEstado]] = None,
            fechaHoraFin: Optional[datetime] = None,
            fechaHoraOcurrencia: Optional[datetime] = None,
            latitudEpicentro: Optional[float] = None,
            latitudHipocentro: Optional[float] = None,
            longitudEpicentro: Optional[float] = None,
            longitudHipocentro: Optional[float] = None,
            valorMagnitud: Optional[float] = None,
            alcance: Optional[AlcanceSismo] = None,
            clasificacion: Optional[ClasificacionSismo] = None,
            origenGeneracion: Optional[OrigenDeGeneracion] = None,
            seriesTemporales: Optional[List[SerieTemporal]] = None,
            cambioEstadoActual: Optional[CambioEstado] = None,
            estadoActual: Optional[Estado] = None,
    ) -> None:
        self.id_evento = id_evento
        self.cambiosEstado: List[CambioEstado] = list(cambiosEstado or [])
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudEpicentro = longitudEpicentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud
        self.alcance = alcance
        self.clasificacion = clasificacion
        self.origenGeneracion = origenGeneracion
        self.seriesTemporales: List[SerieTemporal] = list(seriesTemporales or [])
        self.cambioEstadoActual = cambioEstadoActual
        self.estadoActual = self.getEstadoActual()

    # ---------- reglas locales ----------
    def getEstadoActual(self) -> str | None:
        """
        Devuelve el nombre del estado del ÚLTIMO CambioEstado 'vigente' (sin fechaHoraFin).
        Si por alguna razón no hay ninguno vigente (no debería pasar con el fix),
        como fallback devuelve el nombre del último cambio de la lista.
        """
        # Buscar el más reciente vigente
        for c in reversed(self.cambiosEstado):
            if c.esActual():
                return c.estado.nombre
        # Fallback: último estado registrado
        if self.cambiosEstado:
            return self.cambiosEstado[-1].estado.nombre
        return None
        
    def buscarSismosARevisar(self) -> bool:
        # ⬇️ si el estado vigente es Rechazado, NO va a la lista
        if self.getEstadoActual() == "Rechazado":
            return False

        vio_AD = False
        for c in self.cambiosEstado:
            if c.sosAutoDetectado():
                vio_AD = True
            elif vio_AD and c.sosPteRevision():
                return True
        return False
    
    def getFechaHoraOcurrencia(self):
        return self.fechaHoraOcurrencia

    def getMagnitud(self):
        return self.valorMagnitud

    def getDatosSismos(self) -> Dict:
        return {
            "id_evento": self.id_evento,
            "fechaHoraOcurrencia": self.getFechaHoraOcurrencia(),
            "magnitud": self.getMagnitud(),
            "latitudEpicentro": self.latitudEpicentro,
            "longitudEpicentro": self.longitudEpicentro,
            "latitudHipocentro": self.latitudHipocentro,
            "longitudHipocentro": self.longitudHipocentro,
    # ANTES: "EstadoActual": self.getEstadoActual()
            "estadoActual": self.getEstadoActual(),
        }

    def bloquearEvento(self, estadoBloqueado, fechaHora, responsable):
        for c in self.cambiosEstado:
            if CambioEstado.esActual(c):
                c.setFechaHoraFin(fechaHora)
        self.crearCambioEstado(estadoBloqueado, fechaHora, responsable)


    def crearCambioEstado(self, estado, fechaHora, nombreUsuario: Optional[str]) -> CambioEstado:
        cambio = CambioEstado(estado=estado, fechaHoraInicio=fechaHora, responsable=nombreUsuario)
        self.cambiosEstado.append(cambio)
        self.cambioEstadoActual = cambio
        print("Cambio de estado actualizado!")
        print("Evento:", self.id_evento)
        print("Estado Actual del Evento:", self.cambioEstadoActual.estado.nombre)
        print("Fecha Hora Inicio del Cambio de estado:", self.cambioEstadoActual.fechaHoraInicio)
        return cambio

    def getDatosEvento(self) -> dict:
        def _d(obj, base): return obj.getDatos() if obj else base

        return {
            "id_evento": self.id_evento,
            "fechaHoraOcurrencia": self.fechaHoraOcurrencia,
            "coordenadas": {"lat": self.latitudEpicentro, "lon": self.longitudEpicentro},
            "magnitud": self.valorMagnitud,
            "alcance": _d(self.alcance, {"nombre": "(sin datos)", "descripcion": ""}),
            "clasificacion": _d(self.clasificacion, {"nombre": "(sin datos)", "escala": ""}),
            "origen": _d(self.origenGeneracion, {"nombre": "(sin datos)", "detalle": ""}),
            "estadoActual": self.getEstadoActual() or "(sin datos)",
        }

    def getDatosSeriesTemporales(self) -> list[dict]:
        return [s.getDatos() for s in (self.seriesTemporales or [])]

    def setNuevoOrigen(self, nuevoOrigenNombre, nuevoOrigenDescripcion):
        self.origenGeneracion.nombre = nuevoOrigenNombre
        self.origenGeneracion.descripcion = nuevoOrigenDescripcion

    def setNuevoAlcance(self, nuevoAlcanceNombre, nuevoAlcanceDescripcion):
        self.alcance.nombre = nuevoAlcanceNombre
        self.alcance.descripcion = nuevoAlcanceDescripcion

    def setNuevaMagnitud(self, nuevoMagnitud):
        self.valorMagnitud = nuevoMagnitud

    def rechazarEvento(self, estadoRechazado: Estado, fechaHora, responsable):
        for c in self.cambiosEstado:
            if CambioEstado.esActual(c):
                c.setFechaHoraFin(fechaHora)
        self.crearCambioEstado(estadoRechazado, fechaHora, responsable)
