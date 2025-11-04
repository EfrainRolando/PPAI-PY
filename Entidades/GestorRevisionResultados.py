from __future__ import annotations
from typing import List, Any, Optional, Iterable, Type, Dict
from datetime import datetime

from Entidades.Estado import Estado
from Entidades.EventoSismico import EventoSismico
from Entidades.Sesion import Sesion
from Entidades.repositorio_eventos import obtener_eventos_predeterminados
from apps.redsismica.repositorio import RepositorioEventosDjango


class GestorRevisionResultados:
    def __init__(self, sesion):
        
        self.sesion = sesion
        self.repo = RepositorioEventosDjango()
        self.eventoSeleccionado = None
        self.eventos: List[EventoSismico] = self.repo.obtener_eventos()

    def registrarResultado(self) -> None:
        print("Gestor creado → registrando resultado...")
        datos = self.buscarSismosARevisar()
        datos_ordenados = self.ordenarEventosPorFechaOcurrencia(datos)
        from Entidades.PantallaRevision import PantallaRevision
        PantallaRevision(self.sesion).mostrarDatosEventosSismicos(datos_ordenados)
        EventoSeleccionado = PantallaRevision(self.sesion).solicitarSeleccionEventoSismico()
        self.cambiarEstadoABloqueadoEnRevision(EventoSeleccionado)
        datos = self.buscarDatosEventoSismico(EventoSeleccionado)
        PantallaRevision(self.sesion).mostrarDatosEventoSismico(datos)
        self.habilitarOpcionMapa()
        self.habilitarModificaciones(EventoSeleccionado)
        datos = self.buscarDatosEventoSismico(EventoSeleccionado)
        PantallaRevision(self.sesion).mostrarDatosEventoSismico(datos)
        PantallaRevision(self.sesion).presentarAcciones()
        Accion = PantallaRevision(self.sesion).tomarSeleccionAccion()
        self.validarSeleccionAccion(Accion)
        self.validarDatosEventoSismico(EventoSeleccionado)
        self.cambiarEstadoARechazado(EventoSeleccionado)
        self.finCU()

    def buscarSismosARevisar(self) -> List[dict]:
        """Filtra los eventos que deben ser revisados"""
        eventos_a_revisar = []
        for e in self.eventos:
            if e.buscarSismosARevisar():
                eventos_a_revisar.append(e.getDatosSismos())
        return eventos_a_revisar

    def ordenarEventosPorFechaOcurrencia(self, datos: List[dict]) -> List[dict]:
        """Ordena los eventos según su fechaHoraOcurrencia"""
        return sorted(
            datos,
            key=lambda d: d.get("fechaHoraOcurrencia", datetime.min)
        )

    def tomarSeleccionEventoSismico(self, eleccion) -> EventoSismico:
        for e in self.eventos:
            if eleccion == e.id_evento:
                return e

    def cambiarEstadoABloqueadoEnRevision(self, evento_id, responsable) -> None:
        EventoSeleccionado = self.tomarSeleccionEventoSismico(evento_id)
        if not EventoSeleccionado: return
        estadoBloqueado = self.buscarEstadoBloqueadoEnRevision()
        fechaHoraInicio = self.getFechaYHoraActual()
        EventoSeleccionado.bloquearEvento(estadoBloqueado, fechaHoraInicio, responsable)

    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "BloqueadoEnRevision":
                return Estado(n)

    def getFechaYHoraActual(self) -> datetime:
            return datetime.now()

    def buscarDatosEventoSismico(self, evento_id: EventoSismico) -> Dict[str, Any]:
        evento = self.tomarSeleccionEventoSismico(evento_id)
        if not evento: return {"evento": {}} # Manejar si no lo encuentra

        return {
            "evento": evento.getDatosEvento()
        }

    def obtenerDatosSeriesTemporales(self, evento: EventoSismico) -> list[dict]:
        return evento.getDatosSeriesTemporales()

    def habilitarOpcionMapa(self) -> bool:
        from Entidades.PantallaRevision import PantallaRevision
        PantallaRevision(self.sesion).solicitarOpcionMapa()

    def tomarSeleccionMapa(self, Opcion):
        return print("Opcion Elegida:", Opcion)

    def habilitarModificaciones(self, evento: EventoSismico):
        from Entidades.PantallaRevision import PantallaRevision
        PantallaRevision(self.sesion).solicitarModificaciones(evento)

    def tomarModificaciones(self, nuevoOrigenNombre, nuevoOrigenDescripcion, nuevoAlcanceNombre,
                            nuevoAlcanceDescripcion, nuevoMagnitud, evento: EventoSismico):
        EventoSismico.EventoSeleccionado = evento
        evento.setNuevoOrigen(nuevoOrigenNombre, nuevoOrigenDescripcion)
        evento.setNuevoAlcance(nuevoAlcanceNombre, nuevoAlcanceDescripcion)
        evento.setNuevaMagnitud(nuevoMagnitud)
        return {
            "evento": evento.getDatosEvento()
        }

    def buscarEstadoRechazado(self) -> Estado:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Rechazado":
                return Estado(n)

    def cambiarEstadoARechazado(self, evento_id, responsable) -> None:
            EventoSeleccionado = self.tomarSeleccionEventoSismico(evento_id) # <-- LÓGICA MOVIDA AQUÍ
            if not EventoSeleccionado: return
            EstadoRechazado = self.buscarEstadoRechazado()
            fechaHoraActual = self.getFechaYHoraActual()
            EventoSeleccionado.rechazarEvento(EstadoRechazado, fechaHoraActual, responsable)

    def validarSeleccionAccion(self, Accion):
        if Accion >= 0 or Accion <= 4:
            if Accion != 2:
                print("Accion No valida!")

    def validarDatosEventoSismico(self, evento_id):
        EventoSeleccionado = self.tomarSeleccionEventoSismico(evento_id)
        if EventoSeleccionado.getDatosEvento() is None:
            print("Error: Los datos del evento sismico no son validos.")

    def buscarUsuario(self) -> str:
        # Usa la misma instancia; si no hay login, Sesion lo pedirá
        return self.sesion.getUsuario()

    def finCU(self):
        print("Llegaste hasta el final, crack")
    
    def buscarConfirmado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Confirmado":
                return Estado(n)
            
    def cambiarEstadoAConfirmado(self, evento_id, responsable) -> None:
        EventoSeleccionado = self.tomarSeleccionEventoSismico(evento_id) # <-- LÓGICA MOVIDA AQUÍ
        if not EventoSeleccionado: return
        Estado = self.buscarConfirmado()
        fechaHoraActual = self.getFechaYHoraActual()
        EventoSeleccionado.confirmar(Estado, fechaHoraActual, responsable)
            
    def buscarDerivado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Derivado":
                return Estado(n)
            
    def cambiarEstadoADerivado(self, evento_id, responsable) -> None:
        EventoSeleccionado = self.tomarSeleccionEventoSismico(evento_id) # <-- LÓGICA MOVIDA AQUÍ
        if not EventoSeleccionado: return
        Estado = self.buscarDerivado()
        fechaHoraActual = self.getFechaYHoraActual()
        EventoSeleccionado.rechazarEvento(Estado, fechaHoraActual, responsable)