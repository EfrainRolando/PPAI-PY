from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any, Type
from Entidades.CambioEstado import CambioEstado
from Entidades.Estado import Estado
from Entidades.SerieTemporal import SerieTemporal
from Entidades.AlcanceSismo import AlcanceSismo
from Entidades.ClasificacionSismo import ClasificacionSismo
from Entidades.OrigenGeneracion import OrigenDeGeneracion
from Entidades.EstadoEvento import EstadoEvento, PteRevision, BloqueadoEnRevision


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
    def _nombre_de(self, estado_obj) -> str | None:
        if estado_obj is None:
            return None

        n = getattr(estado_obj, "nombre", None)
        if isinstance(n, str):
            return n
        if callable(n):
            try:
                return n()
            except Exception:
                pass

        if hasattr(estado_obj, "NAME"):
            try:
                return getattr(estado_obj, "NAME")
            except Exception:
                pass

        return estado_obj.__class__.__name__


    def getEstadoActual(self) -> str | None:
        for c in reversed(self.cambiosEstado):
            if c.esActual():
                return self._nombre_de(c.estado)

        if self.cambiosEstado:
            return self._nombre_de(self.cambiosEstado[-1].estado)

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

    def bloquear(self, fechaHora: datetime, resp =Optional[str]) -> None:
        PteRevision().bloquear(self, fechaHora, resp)


    def crearCambioEstado(self, estado,fechaHora: Optional[datetime] = None, nombreUsuario: Optional[str] = None,) -> CambioEstado:
        cambio = CambioEstado(estado=estado, fechaHoraInicio=fechaHora, responsable=nombreUsuario)
        self.cambiosEstado.append(cambio)
        self.cambioEstadoActual = cambio
        print("Cambio de estado actualizado!")
        print("Evento:", self.id_evento)
        print("Estado Actual del Evento:", self.cambioEstadoActual.estado.nombre)
        print("Fecha Hora Inicio del Cambio de estado:", self.cambioEstadoActual.fechaHoraInicio)
        return cambio

    def getDatosEvento(self) -> dict:
        def _round_coord(coord: Optional[float]):
            return round(coord, 4) if coord is not None else None

        def _as_array(obj, project=None):
            if not obj:
                return []
            datos = obj.getDatos() if hasattr(obj, "getDatos") else {}
            if callable(project):
                datos = project(datos)
            return [datos]
        def _project_clasif(d: dict) -> dict:
            return {
            "nombre": d.get("nombre"),
            "kmProfundidadDesde": d.get("kmProfundidadDesde"),
            "kmProfundidadHasta": d.get("kmProfundidadHasta"),
            }

        return {
        "id_evento": self.id_evento,
        "fechaHoraOcurrencia": self.fechaHoraOcurrencia,
        "epicentro": {
            "lat": _round_coord(getattr(self, "latitudEpicentro", None)),
            "lon": _round_coord(getattr(self, "longitudEpicentro", None)),
        },
        "hipocentro": {
            "lat": _round_coord(getattr(self, "latitudHipocentro", None)),
            "lon": _round_coord(getattr(self, "longitudHipocentro", None)),
        },
        "magnitud": getattr(self, "valorMagnitud", None),

        # 👉 Arrays para que la Pantalla itere
        # Alcance y Origen: nombre + descripcion
        "alcances": _as_array(getattr(self, "alcance", None)),  # usa alcance.getDatos()
        "origenes": _as_array(getattr(self, "origenGeneracion", None)),  # usa origen.getDatos()

        # Clasificación: nombre + kmProfundidadDesde/Hasta (proyección)
        "clasificaciones": _as_array(getattr(self, "clasificacion", None), project=_project_clasif),

        # Estado actual como string (o el dict que tu getEstadoActual retorne)
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

    def rechazar(self, fechaHora, responsable):
        BloqueadoEnRevision().rechazar(self, fechaHora, responsable)
        
    def confirmar(self, estado, fechaHora, responsable):
        for c in self.cambiosEstado:
            if CambioEstado.esActual(c):
                c.setFechaHoraFin(fechaHora)
        self.crearCambioEstado(estado, fechaHora, responsable)

    def derivar(self, estado, fechaHora, responsable):
        for c in self.cambiosEstado:
            if CambioEstado.esActual(c):
                c.setFechaHoraFin(fechaHora)
        self.crearCambioEstado(estado, fechaHora, responsable)

    def setCambioEstado(self, cambio: CambioEstado) -> None:
        self.cambiosEstado.append(cambio)
        self.cambioEstadoActual = cambio
        return None

    def setEstadoActual(self, estado:EstadoEvento) -> None:
        self.estadoActual = estado
        return None