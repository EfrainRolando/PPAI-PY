from datetime import datetime, timedelta
from typing import List, Dict

from datetime import datetime
from typing import List
from EventoSismico import EventoSismico
from Estado import Estado
from PantallaRevision import PantallaRevision
from GestorRevisionResultados import GestorRevisionResultados
from EstacionSismologica import EstacionSismologica
from SerieTemporal import SerieTemporal

def main():
    def habilitarPantalla(self) -> None:
        print("Pantalla habilitada")

    def solicitarSeleccionEventosSismicos(self, eventos: List[Dict]) -> None:
        print(f"Eventos candidatos: {len(eventos)}")

    def mostrarDatosEventoSismico(self, datos: Dict) -> None:
        print("Evento seleccionado:", datos["valorMagnitud"], datos["estadoActual"])

    def presentarAcciones(self, acciones: List[str]) -> None:
        print("Acciones:", acciones)


if __name__ == '__main__':
    main()


def fabricar_evento(lat=-34.6, lon=-58.4, mag=4.2, estado=Estado) -> EventoSismico:
    est = EstacionSismologica("BUE01", "BsAs", 15.0)
    serie = SerieTemporal("baja", datetime.now() - timedelta(hours=1), datetime.now(), 100.0, est)
    e = EventoSismico(
        fechaHoraFin=None,
        fechaHoraOcurrencia=datetime.now() - timedelta(minutes=10),
        latitudEpicentro=lat,
        latitudHipocentro=lat,
        longitudEpicentro=lon,
        longitudHipocentro=lon,
        valorMagnitud=mag,
        seriesTemporales=[serie],
    )
    e.crearCambioEstado(Estado(estado), responsable="sistema", fecha=datetime.now() - timedelta(minutes=9))
    return e


if __name__ == "__main__":
    eventos = [fabricar_evento(mag=3.1, estado"Detectado"),
               fabricar_evento(mag=5.0 = "PteRevision")]*\
    gestor = GestorRevisionResultados(eventos=eventos)
    gestor.registrarResultado(PantallaRevision())
    # Simular rechazo según tercera lámina
    gestor.rechazar("No cumple criterios")
    print("Estado final:", gestor.eventoSeleccionado.estadoActual().nombre)