class Estado:
    nombreEstado = string

    def sosAutoDetectado(self):
        if Estado.nombreEstado == "AutoDetectado":
            return True