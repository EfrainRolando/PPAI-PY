from __future__ import annotations
from typing import List, Dict, Any

from EventoSismico import EventoSismico
from GestorRevisionResultados import GestorRevisionResultados


class PantallaRevision:
    def __init__(self) -> None:
        self.gestor: GestorRevisionResultados = GestorRevisionResultados()

    def opcionRegistrarResultado(self) -> None:
        """Método principal invocado por el actor AS"""
        self.habilitarPantalla()
        self.gestor.registrarResultado()

    def habilitarPantalla(self) -> None:
        print("Pantalla habilitada")

    def mostrarDatosEventosSismicos(self, datos: List[dict]) -> None:
        """Muestra los eventos que cumplen el criterio"""
        print("Eventos a revisar:")
        for d in datos:
            print(
                f"- #{d['id_evento']} | {d['fechaHoraOcurrencia']} | M{d['magnitud']} | "
                f"Epi(lat:{d['latitudEpicentro']}, lon:{d['longitudEpicentro']}) | "
                f"Hipo(lat:{d['latitudHipocentro']}, lon:{d['longitudHipocentro']})"
            )

    def solicitarSeleccionEventoSismico(self) -> EventoSismico:
        eleccion = int(input('Seleccione un evento a modificar:'))
        return GestorRevisionResultados.tomarSeleccionEventoSismico(self.gestor, eleccion)

    def mostrarDatosEventoSismico(self, datos: Dict[str, Any], *, devolver_str: bool = False):
        evento = datos.get("evento", {}) or {}
        series = datos.get("series_temporales", []) or []

        lineas = ["=== EVENTO SÍSMICO SELECCIONADO ===", f"ID: {evento.get('id_evento')}",
                  f"Fecha/Hora ocurrencia: {evento.get('fechaHoraOcurrencia')}"]
        coords = evento.get("coordenadas", {}) or {}
        lineas.append(f"Coordenadas: lat={coords.get('lat')}  lon={coords.get('lon')}")
        lineas.append(f"Magnitud: {evento.get('magnitud')}")

        alc = evento.get("alcance") or {}
        cla = evento.get("clasificacion") or {}
        org = evento.get("origen") or {}

        lineas.append("\n-- Alcance --")
        lineas.append(f"Nombre: {alc.get('nombre', '(sin datos)')} | Descripción: {alc.get('descripcion', '')}")

        lineas.append("\n-- Clasificación --")
        lineas.append(
            f"Nombre: {cla.get('nombre', '(sin datos)')} | KMdesde: {cla.get('kmProfundidadDesde', '')} | KMhasta: {cla.get('kmProfundidadHasta', '')}")

        lineas.append("\n-- Origen de Generación --")
        lineas.append(f"Nombre: {org.get('nombre', '(sin datos)')} | Detalle: {org.get('descripcion', '')}")

        texto = "\n".join(lineas)
        if devolver_str:
            return texto
        print(texto)

    def solicitarOpcionMapa(self):
        OpMapa = input("Desea Visualizar el mapa?")  # Agregar botones de si o no en el front
        return GestorRevisionResultados.tomarSeleccionMapa(GestorRevisionResultados(), OpMapa)

    def solicitarModificaciones(self, evento: EventoSismico):
        opcion = input("Desea Modificar los datos del Evento? (S-N)")
        if opcion == "S":
            nuevoMagnitud = input("Ingrese la magnitud del evento")
            nuevoAlcanceNombre = input("Ingrese el nombre del alcance del evento")
            nuevoAlcanceDescripcion = input("Ingrese la descripcion del alcance del evento")
            nuevoOrigenNombre = input("Ingrese el Nombre del Origen del evento")
            nuevoOrigenDescripcion = input("Ingrese la descripcion del Origen del evento")
            return self.gestor.tomarModificaciones(nuevoOrigenNombre, nuevoOrigenDescripcion, nuevoAlcanceNombre,nuevoAlcanceDescripcion, nuevoMagnitud, evento)
        else:
            return print("Sin Modificaciones")


