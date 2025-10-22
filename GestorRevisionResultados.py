from __future__ import annotations
from typing import List, Any, Optional, Iterable, Type, Dict
from datetime import datetime

from Estado import Estado
from EventoSismico import EventoSismico
from repositorio_eventos import obtener_eventos_predeterminados


class GestorRevisionResultados:
    def __init__(self):
        self.eventos: List[EventoSismico] = obtener_eventos_predeterminados()

    def registrarResultado(self) -> None:
        print("Gestor creado → registrando resultado...")
        datos = self.buscarSismosARevisar()
        datos_ordenados = self.ordenarEventosPorFechaOcurrencia(datos)
        from PantallaRevision import PantallaRevision
        PantallaRevision().mostrarDatosEventosSismicos(datos_ordenados)
        EventoSeleccionado = PantallaRevision().solicitarSeleccionEventoSismico()
        EstadoBloqueado = self.buscarEstadoBloqueadoEnRevision()
        fechaHoraActual = self.getFechaYHoraActual()
        self.cambiarEstadoABloqueadoEnRevision(EventoSeleccionado, EstadoBloqueado, fechaHoraActual)
        datos = self.buscarDatosEventoSismico(EventoSeleccionado)
        PantallaRevision().mostrarDatosEventoSismico(datos)
        self.imprimir_series_evento(EventoSeleccionado)  #Metodo que no pertenece al diagrama, pero sirve para mostrar las series temporales en consola o en el front

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

    def cambiarEstadoABloqueadoEnRevision(self, EventoSeleccionado, estadoBloqueado: Estado, fechaHoraInicio) -> None:
        EventoSismico.bloquearEvento(EventoSeleccionado, estadoBloqueado, fechaHoraInicio)

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

            print(f"\n— Serie {i} —")
            print(f"  Condición de marea : {_fmt(condicion)}")
            print(f"  Desde              : {_fmt(desde)}")
            print(f"  Hasta              : {_fmt(hasta)}")
            print(f"  Frecuencia         : {_fmt(freq)} Hz")
            print(f"  Muestras           : {len(muestras)}")

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