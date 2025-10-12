from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Iterable
from EventoSismico import EventoSismico
from Estado import Estado
from Sesion import Sesion
from PantallaRevision import PantallaRevision
class GestorRevisionResultados:
    eventos: List[EventoSismico]
    sesion: Optional[Sesion] = None
    pantalla: Optional[PantallaRevision] = None
    eventoSeleccionado: Optional[EventoSismico] = None

    def buscarSismosARevisar(self):
        return [e for e in self.eventos if Estado.nombreEstado(e) in ("detectado", "pararevision")]