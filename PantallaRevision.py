from __future__ import annotations
from typing import Protocol, List, Dict
from EventoSismico import EventoSismico
from GestorRevisionResultados import GestorRevisionResultados
from repositorio_eventos import obtener_eventos_predeterminados


class PantallaRevision:
    def __init__(self):
        self.gestor: GestorRevisionResultados | None = None

    # ← ÚNICO método que llamará main()
    def opcionRegistrarResultado(self) -> None:
        self.habilitarPantalla()
        eventos: List[EventoSismico] = obtener_eventos_predeterminados()
        self.gestor = GestorRevisionResultados(eventos)
        datos = self.gestor.registrarResultado()
        self.mostrarDatosEventosSismicos(datos)

    def habilitarPantalla(self) -> None:
        print("Pantalla habilitada")

    def mostrarDatosEventosSismicos(self, datos: list[dict]) -> None:
        print("Eventos a revisar:")
        for d in datos:
            if not isinstance(d, dict):
                continue
            print(
                f"- #{d['id_evento']} | {d['fechaHoraOcurrencia']} | M{d['magnitud']} | "
                f"Epi(lat:{d['latitudEpicentro']}, lon:{d['longitudEpicentro']}) | "
                f"Hipo(lat:{d['latitudHipocentro']}, lon:{d['longitudHipocentro']}) |"
            )
