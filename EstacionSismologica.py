class EstacionSismologica:
    def __init__(self, codigoEstacion, latitud, longitud, nombre, documentoCertificacionAdq, fechaSolicitudCertificacion, nroCertificacionAdquisicion):
        self.codigoEstacion = codigoEstacion
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.documentoCertificacionAdq = documentoCertificacionAdq
        self.fechaSolicitudCertificacion = fechaSolicitudCertificacion
        self.nroCertificacionAdquisicion = nroCertificacionAdquisicion