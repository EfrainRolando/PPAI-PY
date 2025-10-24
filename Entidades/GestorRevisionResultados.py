from __future__ import annotations
from typing import List, Any, Optional, Iterable, Type, Dict
from datetime import datetime

from Entidades.Estado import Estado
from Entidades.EventoSismico import EventoSismico
from Entidades.Sesion import Sesion
from Entidades.repositorio_eventos import obtener_eventos_predeterminados


class GestorRevisionResultados:
    def __init__(self, sesion):
        self.eventos: List[EventoSismico] = obtener_eventos_predeterminados()
        self.sesion = sesion

    def registrarResultado(self) -> None:
        print("Gestor creado → registrando resultado...")
        datos = self.buscarSismosARevisar()
        datos_ordenados = self.ordenarEventosPorFechaOcurrencia(datos)
        from Entidades.PantallaRevision import PantallaRevision
        PantallaRevision(self.sesion).mostrarDatosEventosSismicos(datos_ordenados)
        EventoSeleccionado = PantallaRevision(self.sesion).solicitarSeleccionEventoSismico()
        EstadoBloqueado = self.buscarEstadoBloqueadoEnRevision()
        fechaHoraActual = self.getFechaYHoraActual()
        self.cambiarEstadoABloqueadoEnRevision(EventoSeleccionado, EstadoBloqueado, fechaHoraActual)
        datos = self.buscarDatosEventoSismico(EventoSeleccionado)
        PantallaRevision(self.sesion).mostrarDatosEventoSismico(datos)
        self.imprimir_series_evento(
            EventoSeleccionado)  # Metodo que no pertenece al diagrama, pero sirve para mostrar las series temporales en consola o en el front
        # self.llamarCUGenerarSismograma
        self.habilitarOpcionMapa()
        self.habilitarModificaciones(EventoSeleccionado)
        datos = self.buscarDatosEventoSismico(EventoSeleccionado)
        PantallaRevision(self.sesion).mostrarDatosEventoSismico(datos)
        PantallaRevision(self.sesion).presentarAcciones()
        Accion = PantallaRevision(self.sesion).tomarSeleccionAccion()
        self.validarSeleccionAccion(Accion)
        nombreUsuario = self.buscarUsuario()
        if Accion == 2 and EventoSeleccionado.valorMagnitud is not None and EventoSeleccionado.valorMagnitud is not None and EventoSeleccionado.origenGeneracion is not None:
            EstadoRechazado = self.buscarEstadoRechazado()
            fechaHoraActual = self.getFechaYHoraActual()
            self.cambiarEstadoARechazado(EventoSeleccionado, EstadoRechazado, fechaHoraActual, nombreUsuario)
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

    def buscarEstadoBloqueadoEnRevision(self) -> Estado:
        for a in Estado.AMBITOS_POSIBLES:
            if a == "EventoSismico":
                for n in Estado.NOMBRES_POSIBLES:
                    if n == "BloqueadoEnRevision":
                        return Estado(n, a)

    def getFechaYHoraActual(self) -> datetime:
        return datetime.now()

    def cambiarEstadoABloqueadoEnRevision(self, EventoSeleccionado, estadoBloqueado: Estado, fechaHoraInicio,
                                          responsable="Usuario") -> None:
        EventoSismico.bloquearEvento(EventoSeleccionado, estadoBloqueado, fechaHoraInicio, responsable)

    def buscarDatosEventoSismico(self, evento: EventoSismico) -> Dict[str, Any]:
        EventoSismico.eventoSeleccionado = evento
        return {
            "evento": evento.getDatosEvento()
        }

    def obtenerDatosSeriesTemporales(self, evento: EventoSismico) -> list[dict]:
        return evento.getDatosSeriesTemporales()

    def imprimir_series_evento(self, evento):
        def _fmt(x):  # para mostrar None prolijo
            return "-" if x is None else x

        series = self.obtenerDatosSeriesTemporales(evento)

        print("=== SERIES TEMPORALES ASOCIADAS ===")
        if not series:
            print("(Sin series temporales)")
            return

        for i, s in enumerate(series, 1):
            # claves esperadas
            condicion = s.get("condicionMarea")
            desde = s.get("desde")
            hasta = s.get("hasta")
            freq = s.get("frecuencia")
            # soporta tu versión previa ("Muestras")
            muestras = s.get("muestras") or s.get("Muestras") or []
            codigo = (
                    s.get("codigoEstacion")
                    or s.get("Codigo Estacion")
                    or s.get("CodigoEstacion")  # por si en algún lado quedó sin espacio
            )

            print(f"\n— Serie {i} —")
            print(f"  Condición de marea : {_fmt(condicion)}")
            print(f"  Desde              : {_fmt(desde)}")
            print(f"  Hasta              : {_fmt(hasta)}")
            print(f"  Frecuencia         : {_fmt(freq)} Hz")
            print(f"  Muestras           : {len(muestras)}")
            print(f"  Estación           : {_fmt(codigo)}")

            if not muestras:
                print("    (Sin muestras)")
                continue

            for j, m in enumerate(muestras, 1):
                fh = m.get("fechaHoraMuestra")
                # soporta tu typo anterior "detalles:"
                detalles = m.get("detalles") or m.get("detalles:") or []

                print(f"    ▸ Muestra {j}: {_fmt(fh)}  (detalles={len(detalles)})")
                if not detalles:
                    print("        (Sin detalles)")
                    continue

                for k, d in enumerate(detalles, 1):
                    # soporta "valor"/"Valor" y "tipoDeDato"/"TipoDeDato"
                    val = d.get("valor", d.get("Valor"))
                    tipo = d.get("tipoDeDato", d.get("TipoDeDato"))
                    denom = tipo.get("denominacion") if isinstance(tipo, dict) else None
                    unidad = tipo.get("nombreUnidadDeMedida") if isinstance(tipo, dict) else None
                    sufijo_tipo = ""
                    if denom or unidad:
                        sufijo_tipo = f"  → Tipo: {_fmt(denom)} ({_fmt(unidad)})"
                    print(f"        - Detalle {k}: valor={_fmt(val)}{sufijo_tipo}")

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
        for a in Estado.AMBITOS_POSIBLES:
            if a == "EventoSismico":
                for n in Estado.NOMBRES_POSIBLES:
                    if n == "Rechazado":
                        return Estado(n, a)

    def cambiarEstadoARechazado(self, EventoSeleccionado, EstadoRechazado, fechaHoraActual, nombreUsuario) -> None:
        EventoSismico.rechazarEvento(EventoSeleccionado, EstadoRechazado, fechaHoraActual, nombreUsuario)

    def validarSeleccionAccion(self, Accion):
        if Accion >= 0 or Accion <= 4:
            if Accion != 2:
                print("Accion No valida!")

    def buscarUsuario(self) -> str:
        # Usa la misma instancia; si no hay login, Sesion lo pedirá
        return self.sesion.getUsuario()

    def finCU(self):
        print("Llegaste hasta el final, crack")
