from typing import Protocol, List, Dict

import GestorRevisionResultados


class PantallaRevision:
    def habilitarPantalla(self) -> None:
        GestorRevisionResultados.registrarResultado(self)
        print("Pantalla habilitada")

    def solicitarSeleccionEventosSismicos(self, eventos: List[Dict]) -> None: ...

    def mostrarDatosEventoSismico(self, datos: Dict) -> None: ...

    def presentarAcciones(self, acciones: List[str]) -> None: ...

    def opcionRegistrarResultado(self):
        self.habilitarPantalla()
