from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Iterable

from EventoSismico import EventoSismico
from Estado import Estado


@dataclass
class GestorRevisionResultados:
    eventos: List[EventoSismico]
    sesion: object | None = None
    eventoSeleccionado: EventoSismico | None = None

    # --- Primera parte del diagrama ---
    def registrarResultado(self) -> None:
        print("Gestor Creado!")

    def buscarSismosARevisar(self):
        # Delego al estático de EventoSismico
        return EventoSismico.buscarSismosARevisar(self.eventos)
