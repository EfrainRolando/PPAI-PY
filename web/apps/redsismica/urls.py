# web/apps/redsismica/urls.py
from django.urls import path
from . import PantallaRevision

urlpatterns = [
    path("", PantallaRevision.home_view, name="home"),
    path("login/", PantallaRevision.login_view, name="login"),
    path("logout/", PantallaRevision.logout_view, name="logout"),
    path("menu/", PantallaRevision.menu_principal_view, name="menu_principal"),

    path("eventos/", PantallaRevision.opcionRegistrarResultado, name="eventos"),

    # ANTES: PantallaRevision.evento_detalle_view
    path("eventos/<int:evento_id>/", PantallaRevision.tomarSeleccionEventoSismico, name="evento_detalle"),

    path("eventos/<int:evento_id>/modificar/", PantallaRevision.evento_modificar_view, name="evento_modificar"),
]
