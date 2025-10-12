from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
from CambioEstado import CambioEstado
from Estado import Estado
from SerieTemporal import SerieTemporal
from AlcanceSismo import AlcanceSismo
from ClasificacionSismo import ClasificacionSismo
from OrigenGeneracion import OrigenDeGeneracion


@dataclass
class EventoSismico:
    fechaHoraFin: Optional[datetime]
    fechaHoraOcurrencia: datetime
    latitudEpicentro: float
    latitudHipocentro: float
    longitudEpicentro: float
    longitudHipocentro: float
    valorMagnitud: float
    alcance: AlcanceSismo
    clasificacion: ClasificacionSismo
    origenGeneracion: OrigenDeGeneracion
    seriesTemporales: List[SerieTemporal]
    cambiosDeEstado: List[CambioEstado]

    # Consultas/Comandos
    def getDatosSismo(self) -> dict:
        base = asdict(self)
        base["seriesTemporales"] = [s.getDatos() for s in self.seriesTemporales]
        base["estadoActual"] = self.estadoActual().nombre.name if self.cambiosDeEstado else None
        return base

    def estadoActual(self) -> Estado:
        if not self.cambiosDeEstado:
            raise ValueError("Evento sin estado")
        return self.cambiosDeEstado[-1].estado

    def crearCambioEstado(self, estado: Estado, responsable: Optional[str], fecha: datetime) -> CambioEstado:
        # cerrar el actual si existe
        if self.cambiosDeEstado and self.cambiosDeEstado[-1].fechaHoraFin is None:
            self.cambiosDeEstado[-1].cerrar(fecha)
        nuevo = CambioEstado(estado=estado, fechaHoraInicio=fecha, responsable=responsable)
        self.cambiosDeEstado.append(nuevo)
        return nuevo

    # Helpers del diagrama
    def sosAutoDetectado(self) -> bool:
        return self.estadoActual().sosDetectado()

    def sosParaRevision(self) -> bool:
        return self.estadoActual().sosParaRevision()

    def bloquearEvento(self, fecha: datetime, responsable: str) -> None:
        self.crearCambioEstado(Estado.nombre, responsable, fecha)

    def rechazarEvento(self, fecha: datetime, responsable: str, motivo: str) -> None:
        ce = self.crearCambioEstado(Estado.nombre, responsable, fecha)
        ce.motivo = motivo

    # Accesores usados por los lifelines
    def getFechaHoraOcurrencia(self) -> datetime:
        return self.fechaHoraOcurrencia

    def getUbicacionOcurrencia(self) -> tuple:
        return self.latitudEpicentro, self.longitudEpicentro

    def getMagnitud(self) -> float:
        return self.valorMagnitud

    # series
    def obtenerDatosSeriesTemporales(self) -> List[dict]:
        return [s.getDatos() for s in self.seriesTemporales]

    def agregarSerieTemporal(self, serie: SerieTemporal) -> None:
        self.seriesTemporales.append(serie)
