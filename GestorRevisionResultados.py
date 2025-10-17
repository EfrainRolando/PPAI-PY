from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Any

from EventoSismico import EventoSismico


class GestorRevisionResultados:
    def __init__(self, eventos: List[EventoSismico], sesion: Optional[object] = None):
        self.eventos = list(eventos)
        self.sesion = sesion
        self.eventoSeleccionado: Optional[EventoSismico] = None

    def registrarResultado(self) -> List[Any]:
        print("Gestor Creado!")
        items = EventoSismico.buscarSismosARevisar(self.eventos)
        return self.ordenarEventoSismicoFechaOcurrencia(items)

    def buscarSismosARevisar(self) -> List[Any]:
        items = EventoSismico.buscarSismosARevisar(self.eventos)
        return self.ordenarEventoSismicoFechaOcurrencia(items)

    def ordenarEventoSismicoFechaOcurrencia(self, items: List[Any], descendente: bool = False) -> List[Any]:
        def key_fn(x):
            if isinstance(x, dict):
                return x.get("fechaHoraOcurrencia", datetime.min)
            return getattr(x, "fechaHoraOcurrencia", datetime.min)

        return sorted(items, key=key_fn, reverse=descendente)
