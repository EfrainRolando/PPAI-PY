from typing import Protocol, List, Dict

from GestorRevisionResultados import GestorRevisionResultados


class PantallaRevision:
    def __init__(self, gestor: GestorRevisionResultados):
        self.gestor = gestor

    def habilitarPantalla(self) -> None:
        GestorRevisionResultados.registrarResultado(self)
        print("Pantalla habilitada")

    def solicitarSeleccionEventosSismicos(self, eventos: List[Dict]) -> None: ...

    def mostrarDatosEventoSismico(self, datos: Dict) -> None: ...

    def presentarAcciones(self, acciones: List[str]) -> None: ...

    def opcionRegistrarResultado(self):
        self.habilitarPantalla()
