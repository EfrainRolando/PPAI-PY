import Estado


class CambioEstado:
    def __init__(self, fechaHoraInicio, fechaHoraFin):
        self.fechaHoraInicio = fechaHoraInicio
        self.fechaHoraFin = fechaHoraFin

    def sosAutoDetectado(self):
        if Estado.sosAutoDetectado() == True:
            return True