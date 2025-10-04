class EventoSismico:
    def __init__(self, fechaHoraFin, fechaHoraOcurrencia, latitudEpicentro, latitudHipocentro, longitudEpicentro, longitudHipocentro, valorMagnitud):
        self.fechaHoraFin = fechaHoraFin
        self.fechaHoraOcurrencia = fechaHoraOcurrencia
        self.latitudEpicentro = latitudEpicentro
        self.latitudHipocentro = latitudHipocentro
        self.longitudEpicentro = longitudEpicentro
        self.longitudHipocentro = longitudHipocentro
        self.valorMagnitud = valorMagnitud

Evento1 = EventoSismico("11:08/09/2025","10:25/09/2025", -32.1532, -32.1567, -68.5321, -68.5289, 5.7)
print(Evento1.fechaHoraOcurrencia)