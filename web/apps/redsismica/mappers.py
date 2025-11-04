from typing import Dict, Optional, List
from apps.redsismica import models as orm

# Importá tus entidades de dominio
from Entidades.Estado import Estado
from Entidades.CambioEstado import CambioEstado
from Entidades.AlcanceSismo import AlcanceSismo
from Entidades.ClasificacionSismo import ClasificacionSismo
from Entidades.OrigenGeneracion import OrigenDeGeneracion
from Entidades.TipoDeDato import TipoDeDato
from Entidades.DetalleMuestraSismica import DetalleMuestraSismica
from Entidades.MuestraSismica import MuestraSismica
from Entidades.SerieTemporal import SerieTemporal
from Entidades.EventoSismico import EventoSismico


class _Cache:
    def __init__(self):
        self.estados: Dict[int, Estado] = {}
        self.tipos: Dict[int, TipoDeDato] = {}
        self.series: Dict[int, SerieTemporal] = {}
        self.eventos: Dict[int, EventoSismico] = {}


# ----------- Helpers -----------

def to_dom_estado(o: orm.Estado, cache: _Cache) -> Estado:
    if o.id in cache.estados:
        return cache.estados[o.id]
    d = Estado(o.nombre)
    cache.estados[o.id] = d
    return d


def to_dom_tipo(o: orm.TipoDeDato, cache: _Cache) -> TipoDeDato:
    if o.id in cache.tipos:
        return cache.tipos[o.id]
    d = TipoDeDato(o.denominacion, o.nombreUnidadDeMedida)
    cache.tipos[o.id] = d
    return d


def to_dom_serie(o: orm.SerieTemporal, cache: _Cache) -> SerieTemporal:
    if o.id in cache.series:
        return cache.series[o.id]
    d = SerieTemporal(
        id=o.id,
        condicionMarea=o.condicionMarea,
        fechaHoraInicioRegistroMuestras=o.fechaHoraInicioRegistroMuestras,
        fechaHoraFinRegistroMuestras=o.fechaHoraFinRegistroMuestras,
        frecuenciaMuestreo=o.frecuenciaMuestreo,
        muestras=[],
    )
    cache.series[o.id] = d

    for m in o.muestras.all().order_by("fechaHoraMuestra"):
        dm = MuestraSismica(m.fechaHoraMuestra, [])
        for det in m.detalles.select_related("tipoDato").all():
            dd = DetalleMuestraSismica(det.valor, to_dom_tipo(det.tipoDato, cache))
            dm.agregarDetalle(dd)
        d.muestras.append(dm)

    return d


def to_dom_evento(o: orm.EventoSismico, cache: Optional[_Cache] = None) -> EventoSismico:
    cache = cache or _Cache()

    alcance = AlcanceSismo(o.alcance.nombre, o.alcance.descripcion) if o.alcance_id else None
    clasif = ClasificacionSismo(o.clasificacion.nombre, o.clasificacion.kmProfundidadDesde, o.clasificacion.kmProfundidadHasta) if o.clasificacion_id else None
    origen = OrigenDeGeneracion(o.origen.nombre, o.origen.descripcion) if o.origen_id else None

    cambios: List[CambioEstado] = []
    for ce in o.cambios.select_related("estado").order_by("fechaHoraInicio").all():
        cambios.append(
            CambioEstado(
                estado=to_dom_estado(ce.estado, cache),
                fechaHoraInicio=ce.fechaHoraInicio,
                fechaHoraFin=ce.fechaHoraFin,
                responsable=getattr(ce, "usuario", None),
            )
        )

    series: List[SerieTemporal] = []
    for s in o.series.select_related("sismografo").all():
        series.append(to_dom_serie(s, cache))

    d = EventoSismico(
        id_evento=o.id,
        cambiosEstado=cambios,
        fechaHoraOcurrencia=o.fechaHoraDeteccion,
        latitudEpicentro=o.epi_lat,
        longitudEpicentro=o.epi_lon,
        latitudHipocentro=o.hipo_lat,
        longitudHipocentro=o.hipo_lon,
        valorMagnitud=o.magnitud,
        alcance=alcance,
        clasificacion=clasif,
        origenGeneracion=origen,
        seriesTemporales=series,
    )
    return d
