from __future__ import annotations
from typing import List
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
