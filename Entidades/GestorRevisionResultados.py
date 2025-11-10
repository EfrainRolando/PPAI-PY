from __future__ import annotations
from typing import List, Any, Optional, Iterable, Type, Dict, Callable
from datetime import datetime

from Entidades.Estado import Estado
from Entidades.EventoSismico import EventoSismico
from Entidades.Sesion import Sesion
from apps.redsismica.repositorio import RepositorioEventosDjango


class GestorRevisionResultados:
    def __init__(self, sesion):
        
        self.sesion = sesion
        self.repo = RepositorioEventosDjango()
        self.eventoSeleccionado: Optional[EventoSismico] = None
        self.eventos: List[EventoSismico] = self.repo.obtener_eventos()
    def opcionRegistrarResultado(self, mostrarEventosSismicos: Callable[[List[Dict]], "HttpResponse"]) -> dict:
        self.limpiar_seleccion()
        datos = self.buscarSismosARevisar()
        datosOrd = self.ordenarEventosPorFechaOcurrencia(datos)
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
        if not self.eventoSeleccionado: 
            return {"evento": {}} 

        return {
            "evento": self.eventoSeleccionado.getDatosEvento()
        }
    
    def buscarDetallesEventoSeleccionado(self) -> dict:
        if not self.eventoSeleccionado:
            return {"evento": {}}

        datos_evento = self.eventoSeleccionado.getDatosEvento()

        return {"evento": datos_evento}
    
    # Metodos propios del gestor
    def getFechaHoraActual(self) -> datetime:
            return datetime.now()
    

    def obtenerDatosSeriesTemporales(self) -> list[dict]:
        return self.eventoSeleccionado.getDatosSeriesTemporales()
    

    def habilitarOpcionMapa(self) -> bool:
        return self.eventoSeleccionado is not None

    def tomarSeleccionOpcionMapa(self, mostrarMapa_cb: Callable[[Dict[str, Any]] , "HttpResponse"]) -> "HttpResponse":
        if not self.eventoSeleccionado:
            payload = {"evento": {},"mapa_img_url": "redsismica/sismo-mapa.jpg", 
                       }
            return mostrarMapa_cb(payload)

        detalles_evento = self.eventoSeleccionado.getDatosEvento()
        payload = {"evento": detalles_evento,
                    "mapa_img_url": "redsismica/sismo-mapa.jpg",
                    }
        return mostrarMapa_cb(payload)

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
            return {}
        
        self.eventoSeleccionado.setNuevoOrigen(nuevoOrigenNombre, nuevoOrigenDescripcion)
        self.eventoSeleccionado.setNuevoAlcance(nuevoAlcanceNombre, nuevoAlcanceDescripcion)
        self.eventoSeleccionado.setNuevaMagnitud(float(nuevoMagnitud)) 
        
        return {
            "evento": self.eventoSeleccionado.getDatosEvento()
        }
    

    def tomarOpcionAccion(self, evento_id: int, accion: str) -> bool:
        a = (accion or "").strip().lower()

        if (not self.eventoSeleccionado) or (self.eventoSeleccionado.id_evento != evento_id):
            self.eventoSeleccionado = next((e for e in self.eventos if e.id_evento == evento_id), None)

        if not self.eventoSeleccionado:
            return False

        if a == "rechazar":
            self.validarDatosEventoSismico()
            self.cambiarEstadoARechazado()
            return True

        if a in ("confirmar", "aprobar"):
            self.cambiarEstadoAConfirmado()
            return True

        if a in ("derivar", "solicitar"):
            self.cambiarEstadoADerivado()
            return True

        return False


    def validarDatosEventoSismico(self) -> None:
        if not self.eventoSeleccionado or self.eventoSeleccionado.getDatosEvento() is None:
            print("Error: Los datos del evento sismico no son validos.")

    def buscarUsuario(self) -> str:
        if self.sesion is None or self.sesion.getUsuario() is None:
            return "Desconocido"
        return self.sesion.getUsuario()

    #Logica de cambio de estados

    def cambiarEstadoABloqueadoEnRevision(self) -> None:
        fechaHoraActual = self.getFechaHoraActual()
        self.eventoSeleccionado.bloquear(fechaHoraActual)
            

    def cambiarEstadoARechazado(self) -> None:
        fechaHoraActual = self.getFechaHoraActual()
        responsable = self.buscarUsuario()
        self.eventoSeleccionado.rechazar(fechaHoraActual, responsable)
            
            
    def cambiarEstadoAConfirmado(self) -> None:
        estado = self.buscarConfirmado()
        fechaHoraActual = self.getFechaHoraActual()
        responsable = self.buscarUsuario()
        if estado:
            self.eventoSeleccionado.confirmar(estado, fechaHoraActual, responsable)

    
    def buscarConfirmado(self) -> None:
        for n in Estado.NOMBRES_POSIBLES:
            if n == "Confirmado":
                return Estado(n)
            
            
    def cambiarEstadoADerivado(self) -> None:
        estado = self.buscarDerivado()
        fechaHoraActual = self.getFechaHoraActual()
        responsable = self.buscarUsuario()
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

    def tomarSeleccionEventoSismico(
        self,
        eleccion: int,
        mostrarDetalleEvento_cb: Callable[[Dict[str, Any]], None],
        mostrarSismograma_cb: Callable[[Dict[str, Any]], "HttpResponse"],
    ) -> "HttpResponse":
        self.eventoSeleccionado = None
        for e in self.eventos:
            if eleccion == e.id_evento:
                self.eventoSeleccionado = e
                break
        if not self.eventoSeleccionado:
            payload = {
                "evento": {},
                "sismograma_img_url": "redsismica/sismografo.jpeg", 
                "series_por_estacion": [],
            }
            return self.llamarCUGenerarSismograma(payload, mostrarSismograma_cb)
        self.cambiarEstadoABloqueadoEnRevision()
        detalles_evento = self.eventoSeleccionado.getDatosEvento()
        mostrarDetalleEvento_cb({"evento": detalles_evento})

        series: List[Dict[str, Any]] = self.obtenerDatosSeriesTemporales()
        series_ordenadas = self.ordenarPorCodigoEstacion(series)

        payload = {
            "evento": detalles_evento,
            "sismograma_img_url": "redsismica/sismografo.jpeg", 
            "series_por_estacion": series_ordenadas,
        }
        return self.llamarCUGenerarSismograma(payload, mostrarSismograma_cb)


    def ordenarPorCodigoEstacion(self, datos: List[dict]) -> List[dict]:
        return sorted(datos, key=lambda d: (d.get("CodigoEstacion") or ""))


    def llamarCUGenerarSismograma(self,payload: Dict[str, Any],mostrarSismograma_cb: Callable[[Dict[str, Any]], "HttpResponse"],) -> "HttpResponse":
        return mostrarSismograma_cb(payload)

     
    def finCU(self):

        responsable = self.buscarUsuario() if hasattr(self, 'buscarUsuario') else 'sistema'
        if getattr(self, 'eventoSeleccionado', None) is not None:
            eventos = [self.eventoSeleccionado]
        elif hasattr(self, 'eventos'):
            eventos = list(self.eventos)
        else:
            eventos = []
        def _estado_final_mem(e) -> Optional[str]:

            try:
                if getattr(e, "cambiosEstado", None):
                    ult = e.cambiosEstado[-1]
                    nombre = getattr(ult.estado, "nombre", None)
                    if not nombre:
                        nombre = ult.estado.__class__.__name__
                    return nombre
            except Exception:
                pass
            try:
                return e.getEstadoActual()
            except Exception:
                return None

        NORMALIZA = {
            "PteRevision": "PteRevision",
            "BloqueadoEnRevision": "BloqueadoEnRevision",
            "Rechazado": "Rechazado",
            "Confirmado": "Confirmado",
            "Derivado": "Derivado",
            "PteRevisionState": "PteRevision",
            "BloqueadoEnRevisionState": "BloqueadoEnRevision",
            "RechazadoState": "Rechazado",
            "ConfirmadoState": "Confirmado",
            "DerivadoState": "Derivado",
    }
        for e in eventos:
            if not hasattr(e, "id_evento") or e.id_evento is None:
                continue

            estado_final = _estado_final_mem(e)
            if not estado_final:
                continue

            estado_final = NORMALIZA.get(estado_final, estado_final)

            try:
                estado_db = self.repo.get_estado_actual(e.id_evento)
            except Exception:
                estado_db = None
            if estado_db != estado_final:
                try:
                    self.repo.cambiar_estado(e.id_evento, estado_final, responsable)
                except Exception:
                    continue

        return True