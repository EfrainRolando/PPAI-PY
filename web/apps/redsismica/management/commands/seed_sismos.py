from django.core.management.base import BaseCommand
from django.utils import timezone
from random import random, choice
from datetime import timedelta
from apps.redsismica.models import (
    Estado, AlcanceSismo, ClasificacionSismo, OrigenDeGeneracion,
    EstacionSismologica, Sismografo, TipoDeDato,
    EventoSismico, CambioEstado, SerieTemporal, MuestraSismica, DetalleMuestraSismica
)


class Command(BaseCommand):
    help = "Carga una semilla grande de datos sísmicos"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Creando catálogos..."))

        # ------------------- Estados -------------------
        estados = [
            ("AutoDetectado", "EventoSismico"),
            ("PteRevision", "EventoSismico"),
            ("BloqueadoEnRevision", "EventoSismico"),
            ("Aprobado", "EventoSismico"),
            ("Rechazado", "EventoSismico"),
        ]
        for n, a in estados:
            Estado.objects.get_or_create(nombre=n, ambito=a)

        # ------------------- Catálogos -------------------
        AlcanceSismo.objects.get_or_create(nombre="Local", descripcion="Percibido solo en el epicentro")
        AlcanceSismo.objects.get_or_create(nombre="Regional", descripcion="Percibido en varias ciudades")
        AlcanceSismo.objects.get_or_create(nombre="Lejano", descripcion="Percibido a gran distancia")

        ClasificacionSismo.objects.get_or_create(nombre="Leve", kmProfundidadDesde=0, kmProfundidadHasta=20)
        ClasificacionSismo.objects.get_or_create(nombre="Moderado", kmProfundidadDesde=21, kmProfundidadHasta=70)
        ClasificacionSismo.objects.get_or_create(nombre="Fuerte", kmProfundidadDesde=71, kmProfundidadHasta=300)

        OrigenDeGeneracion.objects.get_or_create(nombre="Tectónico", descripcion="Por placas")
        OrigenDeGeneracion.objects.get_or_create(nombre="Volcánico", descripcion="Por actividad magmática")
        OrigenDeGeneracion.objects.get_or_create(nombre="Inducido", descripcion="Por actividad humana")

        for i in range(1, 6):
            est, _ = EstacionSismologica.objects.get_or_create(
                codigoEstacion=f"EST{i}",
                defaults={"latitud": -32.0 - i * 0.1, "longitud": -63.8 - i * 0.1},
            )
            Sismografo.objects.get_or_create(
                codigo=f"SG{i}",
                defaults={"estacion": est, "nroSerie": f"SN-{1000+i}"},
            )

        TipoDeDato.objects.get_or_create(denominacion="Aceleración", nombreUnidadDeMedida="m/s^2")
        TipoDeDato.objects.get_or_create(denominacion="Velocidad", nombreUnidadDeMedida="m/s")

        self.stdout.write(self.style.MIGRATE_HEADING("Creando eventos sísmicos..."))        

        estado_auto = Estado.objects.get(nombre="AutoDetectado", ambito="EventoSismico")
        estado_pte = Estado.objects.get(nombre="PteRevision", ambito="EventoSismico")

        alcances = list(AlcanceSismo.objects.all())
        clasifs = list(ClasificacionSismo.objects.all())
        origenes = list(OrigenDeGeneracion.objects.all())
        sismografos = list(Sismografo.objects.select_related("estacion").all())
        tipo_acc = TipoDeDato.objects.get(denominacion="Aceleración")

        base = timezone.now() - timedelta(days=20)
        creados = 0

        for k in range(1, 41):  # 40 eventos
            ev = EventoSismico.objects.create(
                fechaHoraDeteccion=base + timedelta(hours=k * 4),
                magnitud=round(3.0 + random() * 3.0, 1),
                epi_lat=-32.1 + random() * 0.3,
                epi_lon=-63.8 + random() * 0.3,
                hipo_lat=-32.2 + random() * 0.3,
                hipo_lon=-63.9 + random() * 0.3,
                alcance=choice(alcances),
                clasificacion=choice(clasifs),
                origen=choice(origenes),
                estado_actual=estado_auto,
                estado_actual_desde=base + timedelta(hours=k * 4),
            )
            CambioEstado.objects.create(evento=ev, estado=estado_auto, fechaHoraInicio=ev.estado_actual_desde)

            # Algunos eventos pasan a PteRevision
            if k % 3 == 0:
                CambioEstado.objects.create(
                    evento=ev,
                    estado=estado_pte,
                    fechaHoraInicio=ev.estado_actual_desde + timedelta(hours=1),
                )
                ev.estado_actual = estado_pte
                ev.estado_actual_desde = ev.estado_actual_desde + timedelta(hours=1)
                ev.save(update_fields=["estado_actual", "estado_actual_desde"])

            # Series y muestras
            for s in range(2):  # 2 series por evento
                sg = choice(sismografos)
                st = SerieTemporal.objects.create(
                    evento=ev,
                    condicionMarea=choice(["Alta", "Baja", "Media"]),
                    fechaHoraInicioRegistroMuestras=ev.fechaHoraDeteccion,
                    fechaHoraFinRegistroMuestras=ev.fechaHoraDeteccion + timedelta(minutes=30),
                    frecuenciaMuestreo=20.0,
                    sismografo=sg,
                )
                # 25 muestras por serie
                t0 = st.fechaHoraInicioRegistroMuestras
                for i in range(25):
                    m = MuestraSismica.objects.create(
                        serie=st, fechaHoraMuestra=t0 + timedelta(seconds=i * 3)
                    )
                    DetalleMuestraSismica.objects.create(
                        muestra=m, tipoDato=tipo_acc, valor=round(random() * 0.02, 5)
                    )

            creados += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. Eventos creados: {creados}"))
