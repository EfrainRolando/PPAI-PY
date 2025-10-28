from django.urls import path
from . import views 

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("eventos/", views.eventos_view, name="eventos"),
    path("eventos/<int:evento_id>/", views.evento_detalle_view, name="evento_detalle"),
]