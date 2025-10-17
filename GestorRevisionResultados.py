from __future__ import annotations
from typing import List, Any, Optional
from datetime import datetime
from EventoSismico import EventoSismico
from repositorio_eventos import obtener_eventos_predeterminados


class GestorRevisionResultados:
    def __init__(self) -> None:
        self.eventos: List[EventoSismico] = obtener_eventos_predeterminados()
        self.vista: Optional[object] = None

    def registrarResultado(self) -> None:
        print("Gestor creado → registrando resultado...")
        datos = self.buscarSismosARevisar()
        datos_ordenados = self.ordenarEventosPorFechaOcurrencia(datos)
        from PantallaRevision import PantallaRevision
        PantallaRevision().mostrarDatosEventosSismicos(datos_ordenados)

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
