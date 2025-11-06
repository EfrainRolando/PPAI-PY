from typing import Dict, Optional, List
from apps.redsismica import models as orm

# Entidades de dominio
from Entidades.Estado import Estado
from Entidades.CambioEstado import CambioEstado
from Entidades.AlcanceSismo import AlcanceSismo
from Entidades.ClasificacionSismo import ClasificacionSismo
from Entidades.OrigenGeneracion import OrigenDeGeneracion as OrigenGeneracion
from Entidades.TipoDeDato import TipoDeDato
from Entidades.DetalleMuestraSismica import DetalleMuestraSismica
from Entidades.MuestraSismica import MuestraSismica
from Entidades.SerieTemporal import SerieTemporal
from Entidades.EventoSismico import EventoSismico
from Entidades.Sismografo import Sismografo
from Entidades.EstacionSismologica import EstacionSismologica


class _Cache:
    def __init__(self):
        self.estados: Dict[int, Estado] = {}
        self.tipos: Dict[int, TipoDeDato] = {}
        self.series: Dict[int, SerieTemporal] = {}
        self.eventos: Dict[int, EventoSismico] = {}


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


def to_dom_estacion(o: orm.EstacionSismologica) -> EstacionSismologica:
    return EstacionSismologica(
        codigoEstacion=o.codigoEstacion,
        latitud=getattr(o, "latitud", None),
        longitud=getattr(o, "longitud", None),
        nombre=getattr(o, "nombre", None),
    )


def to_dom_sismografo(o: orm.Sismografo) -> Sismografo:
    est_dom = to_dom_estacion(o.estacion) if getattr(o, "estacion_id", None) else None
    return Sismografo(
        codigo=o.codigo,
        estacion=est_dom,
        nroSerie=getattr(o, "nroSerie", None),
        seriesTemporales=[],
    )


def _get_rel_qs(obj, *names):
    for n in names:
        if hasattr(obj, n):
            attr = getattr(obj, n)
            if hasattr(attr, "all"):
                return attr
    return None

def _get_fk(obj, *names):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return None

def to_dom_serie(o: orm.SerieTemporal, cache: _Cache) -> SerieTemporal:
    if o.id in cache.series:
        return cache.series[o.id]

    d = SerieTemporal(
        id=o.id,
        condicionMarea=o.condicionMarea,
        fechaHoraInicioRegistroMuestras=o.fechaHoraInicioRegistroMuestras,
        fechaHoraFinRegistroMuestras=o.fechaHoraFinRegistroMuestras,
        frecuenciaMuestreo=float(o.frecuenciaMuestreo) if o.frecuenciaMuestreo is not None else None,
        muestras=[],
    )
    cache.series[o.id] = d

    # Sismógrafo (con Estación) para CodigoEstacion en getDatos()
    if getattr(o, "sismografo_id", None):
        sg = _get_fk(o, "sismografo")
        if sg is not None:
            d.setSismografo(to_dom_sismografo(sg))

    # MUESTRAS (tolerante a related_name)
    m_qs = _get_rel_qs(o, "muestras", "muestrasismica_set")
    if m_qs is not None:
        try:
            m_iter = m_qs.all().order_by("fechaHoraMuestra")
        except Exception:
            m_iter = m_qs.all()
        for m in m_iter:
            dm = MuestraSismica(getattr(m, "fechaHoraMuestra", None), [])
            # DETALLES (tolerante a related_name)
            d_qs = _get_rel_qs(m, "detalles", "detallemuestrasismica_set")
            if d_qs is not None:
                for det in d_qs.all():
                    td = _get_fk(det, "tipoDato", "tipo_dato")
                    if td is not None:
                        dd = DetalleMuestraSismica(getattr(det, "valor", None), to_dom_tipo(td, cache))
                    else:
                        dd = DetalleMuestraSismica(getattr(det, "valor", None), None)
                    dm.agregarDetalle(dd)
            d.muestras.append(dm)

    return d

def to_dom_evento(o: orm.EventoSismico, cache: Optional[_Cache] = None) -> EventoSismico:
    cache = cache or _Cache()

    alcance = AlcanceSismo(o.alcance.nombre, o.alcance.descripcion) if o.alcance_id else None #
    clasif = ClasificacionSismo(
        o.clasificacion.nombre,
        o.clasificacion.kmProfundidadDesde,
        o.clasificacion.kmProfundidadHasta
    ) if o.clasificacion_id else None #
    origen = OrigenGeneracion(o.origen.nombre, o.origen.descripcion) if o.origen_id else None #

    cambios: List[CambioEstado] = []
    for ce in o.cambios.select_related("estado").order_by("fechaHoraInicio").all(): #
        cambios.append(
            CambioEstado(
                estado=to_dom_estado(ce.estado, cache),
                fechaHoraInicio=ce.fechaHoraInicio, #
                fechaHoraFin=ce.fechaHoraFin, #
                responsable=getattr(ce, "usuario", None), #
            )
        )

    # --- INICIO DE LA CORRECCIÓN ---
    # Aquí cargamos eficientemente las series y sus relaciones anidadas
    # (muestras -> detalles -> tipoDato) usando prefetch_related.
    
    series: List[SerieTemporal] = []
    
    series_qs = o.series.select_related(
        "sismografo", "sismografo__estacion"  # select_related para FK (1-a-1)
    ).prefetch_related(
        "muestras",                         # prefetch para related_name="muestras"
        "muestras__detalles",               # prefetch para related_name="detalles"
        "muestras__detalles__tipoDato"    # prefetch del FK tipoDato en Detalle
    )

    # ANTES: for s in o.series.select_related("sismografo", "sismografo__estacion").all():
    for s in series_qs.all():
        series.append(to_dom_serie(s, cache))
    
    # --- FIN DE LA CORRECCIÓN ---

    d = EventoSismico(
        id_evento=o.id, #
        cambiosEstado=cambios, #
        fechaHoraOcurrencia=o.fechaHoraDeteccion, #
        latitudEpicentro=o.epi_lat, #
        longitudEpicentro=o.epi_lon, #
        latitudHipocentro=o.hipo_lat, #
        longitudHipocentro=o.hipo_lon, #
        valorMagnitud=o.magnitud, #
        alcance=alcance, #
        clasificacion=clasif, #
        origenGeneracion=origen, #
        seriesTemporales=series, #
    )
    return d
