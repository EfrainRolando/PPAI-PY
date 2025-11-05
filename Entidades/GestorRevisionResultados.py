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
        self.eventoSeleccionado: Optional[EventoSismico] = None
        self.eventos: List[EventoSismico] = self.repo.obtener_eventos()

    def registrarResultado(self) -> None: #Logica no usada por la web
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
    def limpiar_seleccion(self) -> None:
        """Limpia el evento sísmico seleccionado de la memoria del gestor."""
        self.eventoSeleccionado = None

    def tomarSeleccionEventoSismico(self, eleccion) -> EventoSismico:
        for e in self.eventos:
            if eleccion == e.id_evento:
                self.eventoSeleccionado = e
                return e

    def cambiarEstadoABloqueadoEnRevision(self, responsable) -> None:
        estadoBloqueado = self.buscarEstadoBloqueadoEnRevision()
        fechaHoraInicio = self.getFechaYHoraActual()
        if estadoBloqueado:
            self.eventoSeleccionado.bloquearEvento(estadoBloqueado, fechaHoraInicio, responsable)

    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "BloqueadoEnRevision":
                return Estado(n)

    def getFechaYHoraActual(self) -> datetime:
            return datetime.now()

    def buscarDatosEventoSismico(self) -> Dict[str, Any]:
        # Ya no recibe evento_id, usa self.eventoSeleccionado
        if not self.eventoSeleccionado: 
            return {"evento": {}} # Manejar si no hay nada seleccionado

        return {
            "evento": self.eventoSeleccionado.getDatosEvento()
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
                            nuevoAlcanceDescripcion, nuevoMagnitud):
        # Ya no recibe evento, usa self.eventoSeleccionado
        if not self.eventoSeleccionado: 
            return {}

        # Actualiza el objeto en memoria
        self.eventoSeleccionado.setNuevoOrigen(nuevoOrigenNombre, nuevoOrigenDescripcion)
        self.eventoSeleccionado.setNuevoAlcance(nuevoAlcanceNombre, nuevoAlcanceDescripcion)
        self.eventoSeleccionado.setNuevaMagnitud(float(nuevoMagnitud))
        
        # (Aquí faltaría persistir los cambios en el repositorio,
        # pero el repo actual no tiene un método para "actualizar"
        # datos maestros del evento, solo para cambiar estado).
        
        return {
            "evento": self.eventoSeleccionado.getDatosEvento()
        }

    def buscarEstadoRechazado(self) -> Estado:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Rechazado":
                return Estado(n)

    def cambiarEstadoARechazado(self, responsable : str) -> None:
        EstadoRechazado = self.buscarEstadoRechazado()
        fechaHoraActual = self.getFechaYHoraActual()
        if EstadoRechazado:
            self.eventoSeleccionado.rechazarEvento(EstadoRechazado, fechaHoraActual, responsable)

    def validarSeleccionAccion(self, Accion):
        if Accion >= 0 or Accion <= 4:
            if Accion != 2:
                print("Accion No valida!")

    def validarDatosEventoSismico(self):
        # Ya no recibe evento_id, usa self.eventoSeleccionado
        if not self.eventoSeleccionado or self.eventoSeleccionado.getDatosEvento() is None:
            print("Error: Los datos del evento sismico no son validos.")
            # En una app web, esto debería lanzar una excepción
            # raise ValueError("Datos de evento no válidos")

    def buscarUsuario(self) -> str:
        # Usa la misma instancia; si no hay login, Sesion lo pedirá
        return self.sesion.getUsuario()

    def finCU(self):
        print("Llegaste hasta el final, crack")
    
    def buscarConfirmado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Confirmado":
                return Estado(n)
            
    def cambiarEstadoAConfirmado(self, responsable) -> None:
        estado = self.buscarConfirmado()
        fechaHoraActual = self.getFechaYHoraActual()
        if estado:
            self.eventoSeleccionado.confirmar(estado, fechaHoraActual, responsable)
            
    def buscarDerivado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Derivado":
                return Estado(n)
            
    def cambiarEstadoADerivado(self, responsable) -> None:
        estado = self.buscarDerivado()
        fechaHoraActual = self.getFechaYHoraActual()
        if estado:
            # El gestor original llamaba a 'rechazarEvento'
            # Lo corrijo para que llame a 'derivar'
            self.eventoSeleccionado.derivar(estado, fechaHoraActual, responsable)