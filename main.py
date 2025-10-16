from datetime import datetime
from Estado import Estado
from CambioEstado import CambioEstado
from EventoSismico import EventoSismico

# Simulamos estados
e_auto = Estado("AutoDetectado")
e_rev = Estado("ParaRevision")

# Simulamos eventos
ev1 = EventoSismico(
    id_evento=1,
    cambiosEstado=[CambioEstado(e_auto, datetime.now(), 'User')],
    fechaHoraFin=datetime.now(),
    fechaHoraOcurrencia=datetime.now(),
    latitudEpicentro=-31.4,
    latitudHipocentro=-31.5,
    longitudEpicentro=-64.2,
    longitudHipocentro=-64.3,
    valorMagnitud=5.2,
    alcance=None,
    clasificacion=None,
    origenGeneracion=None,
    seriesTemporales=[]
)

ev2 = EventoSismico(
    id_evento=2,
    cambiosEstado=[CambioEstado(e_rev, datetime.now(), 'User')],
    fechaHoraFin=datetime.now(),
    fechaHoraOcurrencia=datetime.now(),
    latitudEpicentro=-30.1,
    latitudHipocentro=-30.2,
    longitudEpicentro=-63.8,
    longitudHipocentro=-63.9,
    valorMagnitud=3.8,
    alcance=None,
    clasificacion=None,
    origenGeneracion=None,
    seriesTemporales=[]
)

# Prueba del método de clase
lista = [ev1, ev2]
for evento in EventoSismico.buscarSismosARevisar(lista):
    ultimo_Cambio = evento.cambiosEstado[-1]
    print('Evento:', evento.id_evento, '---|  Estado Evento:', ultimo_Cambio.estado.nombre)