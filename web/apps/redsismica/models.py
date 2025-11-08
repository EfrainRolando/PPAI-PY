from django.db import models
from django.utils import timezone


# ================================================================
# === C A T Á L O G O S  /  E S T Á T I C O S ====================
# ================================================================

class Estado(models.Model):
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre


class AlcanceSismo(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class ClasificacionSismo(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    kmProfundidadDesde = models.FloatField()
    kmProfundidadHasta = models.FloatField()

    def __str__(self):
        return self.nombre


class OrigenDeGeneracion(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class TipoDeDato(models.Model):
    denominacion = models.CharField(max_length=40, unique=True)
    nombreUnidadDeMedida = models.CharField(max_length=20)

    def __str__(self):
        return self.denominacion


# ================================================================
# ===  E S T R U C T U R A  D E  L A  R E D  ====================
# ================================================================

class EstacionSismologica(models.Model):
    codigoEstacion = models.CharField(max_length=20, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    nombre = models.CharField(max_length=60, blank=True, null=True)
    documentoCertificacion = models.JSONField(blank=True, null=True)
    fechaSolicitudCertificacion = models.DateTimeField(blank=True, null=True)
    nroCertificacionAdquisicion = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.codigoEstacion


class Sismografo(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    estacion = models.ForeignKey(
        EstacionSismologica, on_delete=models.CASCADE, related_name="sismografos"
    )
    nroSerie = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.codigo} ({self.estacion.codigoEstacion})"


# ================================================================
# ===  E V E N T O S  S Í S M I C O S  ===========================
# ================================================================

class EventoSismico(models.Model):
    fechaHoraDeteccion = models.DateTimeField(default=timezone.now)
    magnitud = models.FloatField()
    epi_lat = models.FloatField()
    epi_lon = models.FloatField()
    hipo_lat = models.FloatField()
    hipo_lon = models.FloatField()

    alcance = models.ForeignKey(
        AlcanceSismo, on_delete=models.SET_NULL, null=True, related_name="eventos"
    )
    clasificacion = models.ForeignKey(
        ClasificacionSismo, on_delete=models.SET_NULL, null=True, related_name="eventos"
    )
    origen = models.ForeignKey(
        OrigenDeGeneracion, on_delete=models.SET_NULL, null=True, related_name="eventos"
    )
    estado_actual = models.ForeignKey(
        Estado, on_delete=models.SET_NULL, null=True, related_name="eventos_actuales"
    )
    estado_actual_desde = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Evento {self.id} - Mag {self.magnitud}"


class CambioEstado(models.Model):
    evento = models.ForeignKey(
        EventoSismico, on_delete=models.CASCADE, related_name="cambios"
    )
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=60, blank=True, null=True)
    fechaHoraInicio = models.DateTimeField(default=timezone.now)
    fechaHoraFin = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.evento} → {self.estado.nombre}"


# ================================================================
# ===  S E R I E S  &  M U E S T R A S  ==========================
# ================================================================

class SerieTemporal(models.Model):
    evento = models.ForeignKey(
        EventoSismico, on_delete=models.CASCADE, related_name="series"
    )
    condicionMarea = models.CharField(max_length=30)
    fechaHoraInicioRegistroMuestras = models.DateTimeField()
    fechaHoraFinRegistroMuestras = models.DateTimeField()
    frecuenciaMuestreo = models.FloatField()
    sismografo = models.ForeignKey(
        Sismografo, on_delete=models.CASCADE, related_name="series_temporales"
    )

    def __str__(self):
        return f"Serie {self.id} - {self.evento}"


class MuestraSismica(models.Model):
    serie = models.ForeignKey(
        SerieTemporal, on_delete=models.CASCADE, related_name="muestras"
    )
    fechaHoraMuestra = models.DateTimeField()

    def __str__(self):
        return f"Muestra {self.id} ({self.fechaHoraMuestra})"


class DetalleMuestraSismica(models.Model):
    muestra = models.ForeignKey(
        MuestraSismica, on_delete=models.CASCADE, related_name="detalles"
    )
    tipoDato = models.ForeignKey(
        TipoDeDato, on_delete=models.SET_NULL, null=True, related_name="detalles"
    )
    valor = models.FloatField()

    def __str__(self):
        return f"{self.tipoDato} = {self.valor}"


# ================================================================
# ===  U S U A R I O  &  S E S I Ó N  ============================
# ================================================================

class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    nombre_mostrar = models.CharField(max_length=80)
    password_hash = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre_mostrar
