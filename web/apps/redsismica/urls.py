from django.urls import path
from .views import home_view, login_view, logout_view, eventos_view, evento_detalle_view, revisar_evento_view

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("eventos/", eventos_view, name="eventos"),
    path("eventos/<int:evento_id>/", evento_detalle_view, name="evento_detalle"),
    path("eventos/<int:evento_id>/revisar/", revisar_evento_view, name="revisar_evento"),
]