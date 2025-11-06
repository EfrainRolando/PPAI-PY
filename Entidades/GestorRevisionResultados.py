from __future__ import annotations
from typing import List, Any, Optional, Iterable, Type, Dict, Callable
from datetime import datetime

from Entidades.Estado import Estado
from Entidades.EventoSismico import EventoSismico
from Entidades.Sesion import Sesion
from apps.redsismica.repositorio import RepositorioEventosDjango


class GestorRevisionResultados:
    def __init__(self):
        
        self.sesion = Sesion()
        self.repo = RepositorioEventosDjango()
        self.eventoSeleccionado: Optional[EventoSismico] = None
        self.eventos: List[EventoSismico] = self.repo.obtener_eventos()

    #Metodo Inicio Gestor Revision Resultados
    def opcionRegistrarResultado(self, mostrarEventosSismicos: Callable[[List[Dict]], "HttpResponse"]) -> dict:
        self.limpiar_seleccion()
        # 1) Filtra eventos a revisar (el dominio decide qué entra)
        datos = self.buscarSismosARevisar()
        # 2) Ordena (también en el dominio)
        datosOrd = self.ordenarEventosPorFechaOcurrencia(datos)
        # 3) Adaptación de claves para el template (prepara el VM)
        eventos_vm = []
        for d in datosOrd:
            eventos_vm.append({
                "id": d.get("id_evento"),
                "fecha": d.get("fechaHoraOcurrencia"),
                "magnitud": d.get("magnitud"),
                "epicentro": {"lat": d.get("latitudEpicentro"), "lon": d.get("longitudEpicentro")},
                "hipocentro": {"lat": d.get("latitudHipocentro"), "lon": d.get("longitudHipocentro")},
                "estado": d.get("estadoActual"),
            })
        # 4) Devuelve el contexto completo que la vista (Pantalla) necesita
        return mostrarEventosSismicos(eventos_vm)

    #Logica de filtrado y ordenamiento
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
    
    
    def buscarDatosEventoSismico(self) -> Dict[str, Any]:
        # Ya no recibe evento_id, usa self.eventoSeleccionado
        if not self.eventoSeleccionado: 
            return {"evento": {}} # Manejar si no hay nada seleccionado

        return {
            "evento": self.eventoSeleccionado.getDatosEvento()
        }
    
    def buscarDetallesEventoSeleccionado(self) -> dict:
        if not self.eventoSeleccionado:
            return {"evento": {}}

        datos_evento = self.eventoSeleccionado.getDatosEvento()

        return {"evento": datos_evento}
    
    # Metodos propios del gestor
    def getFechaYHoraActual(self) -> datetime:
            return datetime.now()
    

    def obtenerDatosSeriesTemporales(self) -> list[dict]:
        return self.eventoSeleccionado.getDatosSeriesTemporales()
    

    def habilitarOpcionMapa(self) -> bool:
        pass


    def tomarSeleccionMapa(self, Opcion: bool) -> None:
        return  Opcion
    

    def habilitarModificaciones(self):
        if not self.eventoSeleccionado:
            return False
        datos_evento = self.eventoSeleccionado.getDatosEvento()
        if datos_evento and datos_evento.get("estadoActual") == "BloqueadoEnRevision":
            return True

        return False



    def tomarModificaciones(self, nuevoOrigenNombre, nuevoOrigenDescripcion, nuevoAlcanceNombre,
                            nuevoAlcanceDescripcion, nuevoMagnitud) -> dict:
        if not self.eventoSeleccionado: 
            return {} # Manejar si no hay nada seleccionado
        
        self.eventoSeleccionado.setNuevoOrigen(nuevoOrigenNombre, nuevoOrigenDescripcion)
        self.eventoSeleccionado.setNuevoAlcance(nuevoAlcanceNombre, nuevoAlcanceDescripcion)
        self.eventoSeleccionado.setNuevaMagnitud(float(nuevoMagnitud)) 
        
        return {
            "evento": self.eventoSeleccionado.getDatosEvento()
        }
    

    def validarSeleccionAccion(self, Accion: int) -> None:
        if Accion < 0 or Accion > 4:
            print("Accion No valida!")

    def validarDatosEventoSismico(self) -> None:
        # Ya no recibe evento_id, usa self.eventoSeleccionado
        if not self.eventoSeleccionado or self.eventoSeleccionado.getDatosEvento() is None:
            print("Error: Los datos del evento sismico no son validos.")
            # En una app web, esto debería lanzar una excepción
            # raise ValueError("Datos de evento no válidos")


    def buscarUsuario(self) -> str:
        return self.sesion.getUsuario()

    #Logica de cambio de estados

    def cambiarEstadoABloqueadoEnRevision(self) -> None:
        estadoBloqueado = self.buscarEstadoBloqueadoEnRevision()
        if estadoBloqueado:
            self.eventoSeleccionado.bloquearEvento(estadoBloqueado)

    
    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "BloqueadoEnRevision":
                return Estado(n)
            

    def cambiarEstadoARechazado(self, responsable : str) -> None:
        EstadoRechazado = self.buscarEstadoRechazado()
        fechaHoraActual = self.getFechaYHoraActual()
        if EstadoRechazado:
            self.eventoSeleccionado.rechazarEvento(EstadoRechazado, fechaHoraActual, responsable)

                
    def buscarEstadoRechazado(self) -> Estado:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Rechazado":
                return Estado(n)
            
            
    def cambiarEstadoAConfirmado(self, responsable) -> None:
        estado = self.buscarConfirmado()
        fechaHoraActual = self.getFechaYHoraActual()
        if estado:
            self.eventoSeleccionado.confirmar(estado, fechaHoraActual, responsable)

    
    def buscarConfirmado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Confirmado":
                return Estado(n)
            
            
    def cambiarEstadoADerivado(self, responsable) -> None:
        estado = self.buscarDerivado()
        fechaHoraActual = self.getFechaYHoraActual()
        if estado:
            self.eventoSeleccionado.derivar(estado, fechaHoraActual, responsable)

    
    def buscarDerivado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Derivado":
                return Estado(n)
            
#Logica de seleccion De Evento Sismico
    def limpiar_seleccion(self) -> None:
        """Limpia el evento sísmico seleccionado de la memoria del gestor."""
        self.eventoSeleccionado = None

    def tomarSeleccionEventoSismico(self,eleccion: int,mostrarDetalleEvento_cb: Callable[[Dict[str, Any]], None],mostrarSismograma_cb: Callable[[Dict[str, Any]], "HttpResponse"],) -> "HttpResponse":
        for e in self.eventos:
            if eleccion == e.id_evento:
                self.eventoSeleccionado = e
                break

        if not self.eventoSeleccionado:
            payload_vacio = {
                "evento": {},
                "sismograma_img_url": "redsismica/sismografo.jpg",
                "series_por_estacion":  series_ordenadas,
            }
            return self.llamarCUGenerarSismograma(payload_vacio, mostrarSismograma_cb)

    
        self.cambiarEstadoABloqueadoEnRevision()
        detalles_evento = self.eventoSeleccionado.getDatosEvento()
        mostrarDetalleEvento_cb({"evento": detalles_evento})
        series: List[Dict[str, Any]] = self.obtenerDatosSeriesTemporales()
        series_ordenadas = self.ordenarPorCodigoEstacion(series)
        payload = {
            "evento": detalles_evento,
            "sismograma_img_url": "/static/redsismica/sismografo.jpg",  # asegurate de tener la imagen en estáticos
            "series_por_estacion": series_ordenadas,
        }
        return self.llamarCUGenerarSismograma(payload, mostrarSismograma_cb)


    def ordenarPorCodigoEstacion(self, datos: List[dict]) -> List[dict]:
        return sorted(datos, key=lambda d: (d.get("CodigoEstacion") or ""))


    def llamarCUGenerarSismograma(self,payload: Dict[str, Any],mostrarSismograma_cb: Callable[[Dict[str, Any]], "HttpResponse"],) -> "HttpResponse":
        return mostrarSismograma_cb(payload)

     
    def finCU(self):
         pass