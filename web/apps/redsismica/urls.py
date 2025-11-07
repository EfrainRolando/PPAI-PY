# web/apps/redsismica/urls.py
from django.urls import path
from . import PantallaRevision

urlpatterns = [
    path("", PantallaRevision.home_view, name="home"),
    path("login/", PantallaRevision.login_view, name="login"),
    path("logout/", PantallaRevision.logout_view, name="logout"),
    path("menu/", PantallaRevision.menu_principal_view, name="menu_principal"),

    path("eventos/", PantallaRevision.opcionRegistrarResultado, name="eventos"),
    path("eventos/<int:evento_id>/", PantallaRevision.tomarSeleccionEventoSismico, name="evento_detalle"),
    path("eventos/<int:evento_id>/modificar/", PantallaRevision.tomar_modificaciones, name="tomar_modificaciones"),
    # NUEVA: opción mapa
    path("opcion-mapa/", PantallaRevision.tomarSeleccionOpcionMapa, name="opcion_mapa"),
    path("eventos/<int:evento_id>/accion/", PantallaRevision.tomarOpcionAccion, name="evento_accion"),
    path("eventos/guardar/", PantallaRevision.guardar_cambios_view, name="guardar_cambios"),
]
