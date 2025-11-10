from django.db import transaction
from django.utils import timezone
from typing import List, Optional
from . import models as orm
from .mappers import _Cache, to_dom_evento

class RepositorioEventosDjango:
    def obtener_eventos(self) -> List[object]:
        qs = (orm.EventoSismico.objects
          .select_related("alcance","clasificacion","origen","estado_actual")
          .prefetch_related(
              "cambios__estado",
              "series__sismografo__estacion", 
              "series__muestras__detalles__tipoDato"
          ))

        cache = _Cache()
        return [to_dom_evento(e, cache) for e in qs]


    @transaction.atomic
    def cambiar_estado(self, id_evento: int, nuevo_estado: str, responsable: str = "sistema",
                   motivo: Optional[str] = None) -> bool:
        try:
            ev = orm.EventoSismico.objects.select_for_update().get(pk=id_evento)
        except orm.EventoSismico.DoesNotExist:
            return False

        ahora = timezone.now()


        prev = ev.cambios.order_by("-fechaHoraInicio").first()
        if prev and prev.fechaHoraFin is None:
            prev.fechaHoraFin = ahora
            prev.save(update_fields=["fechaHoraFin"])

            estado, _ = orm.Estado.objects.get_or_create(nombre=nuevo_estado)

        orm.CambioEstado.objects.create(
            evento=ev, estado=estado, fechaHoraInicio=ahora,
            usuario=responsable
        )

        ev.estado_actual = estado
        ev.estado_actual_desde = ahora
        ev.save(update_fields=["estado_actual", "estado_actual_desde"])
        return True



    def bloquear_en_revision(self, id_evento: int, responsable: str = "sistema") -> bool:
        return self.cambiar_estado(id_evento, "BloqueadoEnRevision", responsable)

    def rechazar_evento(self, id_evento: int, responsable: str = "sistema", motivo: Optional[str] = None) -> bool:
        return self.cambiar_estado(id_evento, "Rechazado", responsable, motivo)

_singleton = None
def repositorio_eventos_django():
    global _singleton
    if _singleton is None:
        _singleton = RepositorioEventosDjango()
    return _singleton

def get_estado_actual(self, id_evento: int) -> Optional[str]:
    try:
        ev = orm.EventoSismico.objects.select_related("estado_actual").get(pk=id_evento)
    except orm.EventoSismico.DoesNotExist:
        return None
    if ev.estado_actual_id and ev.estado_actual:
        return ev.estado_actual.nombre
    return None
