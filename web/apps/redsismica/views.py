from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core import signing
from functools import wraps
from datetime import datetime
# views.py
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


from .forms import LoginForm

# Importamos TU Gestor/Sesion/Entidades (gracias al sys.path agregado en manage.py)
from Entidades.GestorRevisionResultados import GestorRevisionResultados
from Entidades.Sesion import Sesion

# ====== Login con COOKIE firmada (sin BD ni django.contrib.auth) ======
COOKIE_NAME = "auth_user"
COOKIE_MAX_AGE = 60 * 60 * 8  # 8 horas

# Usuarios de ejemplo (reemplazá por tu verificación real si quisieras)
USUARIOS = {
    "efra": "1234",
    "admin": "admin",
}

def _set_auth_cookie(resp: HttpResponse, username: str):
    value = signing.dumps({"u": username})
    resp.set_cookie(COOKIE_NAME, value, max_age=COOKIE_MAX_AGE, httponly=True, samesite="Lax")

def _clear_auth_cookie(resp: HttpResponse):
    resp.delete_cookie(COOKIE_NAME)

def _get_user(request: HttpRequest) -> str | None:
    raw = request.COOKIES.get(COOKIE_NAME)
    if not raw:
        return None
    try:
        data = signing.loads(raw, max_age=COOKIE_MAX_AGE)
        return data.get("u")
    except signing.BadSignature:
        return None

def requiere_login(view_func):
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        if not _get_user(request):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped

# ====== Vistas ======
def home_view(request: HttpRequest) -> HttpResponse:
    if _get_user(request):
        return redirect("eventos")
    return redirect("login")

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            if USUARIOS.get(u) == p:
                resp = redirect("eventos")
                _set_auth_cookie(resp, u)
                return resp
            else:
                form.add_error(None, "Usuario o contraseña inválidos")
    else:
        form = LoginForm()
    return render(request, "redsismica/login.html", {"form": form})

def logout_view(request: HttpRequest) -> HttpResponse:
    resp = redirect("login")
    _clear_auth_cookie(resp)
    return resp

@requiere_login
def eventos_view(request: HttpRequest) -> HttpResponse:
    """Lista de eventos usando SOLO el Gestor (filtra y ordena)."""
    usuario = _get_user(request)

    sesion = Sesion()
    gestor = GestorRevisionResultados(sesion)

    # 1) Filtra eventos a revisar (el dominio decide qué entra)
    datos = gestor.buscarSismosARevisar()   # -> list[dict]
    # 2) Ordena (también en el dominio)
    datos = gestor.ordenarEventosPorFechaOcurrencia(datos)

    # 3) Adaptación mínima de claves para el template (no es lógica de negocio)
    eventos_vm = []
    for d in datos:
        eventos_vm.append({
            "id": d.get("id_evento"),
            "fecha": d.get("fechaHoraOcurrencia"),
            "magnitud": d.get("magnitud"),
            "epicentro": {"lat": d.get("latitudEpicentro"), "lon": d.get("longitudEpicentro")},
            "hipocentro": {"lat": d.get("latitudHipocentro"), "lon": d.get("longitudHipocentro")},
            "estado": d.get("estadoActual"),
        })

    return render(request, "redsismica/eventos.html", {"eventos": eventos_vm, "user": usuario})


@requiere_login
def evento_detalle_view(request: HttpRequest, evento_id: int) -> HttpResponse:
    usuario = _get_user(request)
    sesion = Sesion()
    gestor = GestorRevisionResultados(sesion)

    # Carga de evento según tu Gestor
    evento = gestor.tomarSeleccionEventoSismico(evento_id)

    if request.method == "POST":
        accion = request.POST.get("accion", "").strip().lower()

        # Map clásico que ya usabas:
        # aprobar -> 1, rechazar -> 2, guardar -> 3
        # añadí "solicitar" como 3 (no destructivo)
        ACCION_MAP = {"aprobar": 1, "rechazar": 2, "guardar": 3, "solicitar": 3}
        Accion = ACCION_MAP.get(accion)

        nombreUsuario = usuario

        # Aprobación (confirmar) -> no hace cambios y vuelve a eventos
        if Accion == 1:
            messages.info(request, "Confirmado: sin cambios aplicados")
            return redirect("eventos")

        # Rechazar -> cambia estado y vuelve a eventos
        if (Accion == 2):
            EstadoRechazado = gestor.buscarEstadoRechazado()
            fechaHoraActual = gestor.getFechaYHoraActual()
            gestor.cambiarEstadoARechazado(evento, EstadoRechazado, fechaHoraActual, nombreUsuario)
            messages.success(request, "Evento rechazado exitosamente")
            return redirect("eventos")

        # Guardar / Solicitar revisión a experto -> lógica no destructiva que ya tenías
        if Accion == 3:
            # acá podés disparar derivación si lo querés en el futuro
            messages.success(request, "Solicitado: revisión a experto")
            return redirect("eventos")

        # si llega algo raro, cerramos CU y seguimos
        gestor.finCU()

    # GET normal: traer datos
    datos = gestor.buscarDatosEventoSismico(evento)
    series = gestor.obtenerDatosSeriesTemporales(evento)

    return render(request, "redsismica/evento_detalle.html", {
        "evento": datos["evento"],
        "series": series,
        "user": usuario,
        "mensaje": None,
    })