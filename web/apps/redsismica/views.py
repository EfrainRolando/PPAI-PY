from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core import signing
from functools import wraps
from datetime import datetime

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
    """
    Lista de eventos a revisar usando SOLO métodos del Gestor/Entidades.
    No se llama a buscarDatosEventoSismico() aquí porque los elementos son dicts.
    """
    # Recuperar usuario (según tu esquema de login; usa cookie o session)
    usuario = _get_user(request) if '_get_user' in globals() else request.session.get("user")

    sesion = Sesion()
    gestor = GestorRevisionResultados(sesion)

    # 1) El gestor devuelve LISTA DE DICTS:
    datos = gestor.buscarSismosARevisar()  # [{ id_evento, fechaHoraOcurrencia, ... }]
    # 2) Ordenar con el propio gestor (también espera dicts):
    datos_ordenados = gestor.ordenarEventosPorFechaOcurrencia(datos)

    # 3) Adaptar las claves a lo que usa el template (no es lógica de dominio, solo “rename”):
    eventos_vm = []
    for d in datos_ordenados:
        eventos_vm.append({
            "id": d.get("id_evento"),
            "fecha": d.get("fechaHoraOcurrencia"),
            "magnitud": d.get("magnitud"),
            "epicentro": {
                "lat": d.get("latitudEpicentro"),
                "lon": d.get("longitudEpicentro"),
            },
            "hipocentro": {
                "lat": d.get("latitudHipocentro"),
                "lon": d.get("longitudHipocentro"),
            },
            "estado": d.get("estadoActual"),
        })

    context = {"eventos": eventos_vm, "user": usuario}
    return render(request, "redsismica/eventos.html", context)

@requiere_login
def evento_detalle_view(request: HttpRequest, evento_id: int) -> HttpResponse:
    """
    Detalle de un evento: se obtiene el evento seleccionado, sus datos y sus series
    únicamente con métodos provistos por el Gestor y las entidades.
    """
    usuario = _get_user(request)
    sesion = Sesion()
    gestor = GestorRevisionResultados(sesion)

    # 1) Seleccionar el evento por id usando el GESTOR
    evento = gestor.tomarSeleccionEventoSismico(evento_id)

    # 2) Obtener datos del evento (dict del dominio)
    datos = gestor.buscarDatosEventoSismico(evento)

    # 3) Obtener series temporales (lista de dicts del dominio)
    series = gestor.obtenerDatosSeriesTemporales(evento)

    context = {
        "evento": datos["evento"],  # trae lo que defina tu dominio
        "series": series,
        "user": usuario,
    }
    return render(request, "redsismica/evento_detalle.html", context)

@requiere_login
def revisar_evento_view(request: HttpRequest, evento_id: int) -> HttpResponse:
    """
    Revisión 100% en front:
    - GET: muestra detalle + formulario editable (sin prints).
    - POST: aplica cambios (solo usando métodos de dominio/gestor) y
            ejecuta la acción elegida (aprobar / rechazar / guardar).
    """
    usuario = _get_user(request)
    # Si tu Sesion necesita user:
    sesion = Sesion()
    gestor = GestorRevisionResultados(sesion)

    # 1) Traemos el evento seleccionado desde el gestor (objeto del dominio)
    evento = gestor.tomarSeleccionEventoSismico(evento_id)

    if request.method == "POST":
        # ==== APLICAR MODIFICACIONES (solo con métodos del dominio) ====
        # Campos que editás en el formulario (ajusta nombres si hace falta)
        nueva_magnitud = request.POST.get("magnitud")
        nuevo_alcance_nombre = request.POST.get("alcance_nombre")
        nuevo_alcance_desc = request.POST.get("alcance_desc")

        # Aplicar magnitud si vino
        if nueva_magnitud is not None and nueva_magnitud != "":
            try:
                # setter del dominio
                evento.setNuevaMagnitud(float(nueva_magnitud))
            except ValueError:
                pass  # si no es numérico, lo ignoramos; podrías mostrar un mensaje

        # Aplicar alcance si vino
        if (nuevo_alcance_nombre or nuevo_alcance_desc):
            # setter del dominio (ya está en tu EventoSismico)
            evento.setNuevoAlcance(
                nuevo_alcance_nombre or "",
                nuevo_alcance_desc or ""
            )

        # ==== ACCIÓN: aprobar / rechazar / solo guardar ====
        accion = request.POST.get("accion")  # "aprobar" | "rechazar" | "guardar"
        ahora = datetime.now()

        # Para cambiar estado necesitamos un Estado, que en tu dominio
        # seguramente lo resolves por catálogo. Si tu Gestor ya trae
        # el objeto Estado por nombre/ámbito, usá eso. Dejo helpers
        # a modo de ejemplo: reemplazalos por tus funciones reales.
        estado = gestor.buscarEstadoRechazado()

        if accion == "rechazar":
            estado_rechazado = estado("Rechazado", "EventoSismico")
            # tu Gestor YA tiene cambiarEstadoARechazado(...)
            gestor.cambiarEstadoARechazado(evento, estado_rechazado, ahora, usuario)
            mensaje = "Evento rechazado exitosamente"

        else:
            # Solo guardamos cambios sin cambiar de estado
            mensaje = "Cambios guardados"

        # Después de aplicar, volvemos a leer los datos desde el dominio/gestor
        datos = gestor.buscarDatosEventoSismico(evento)       # {'evento': {...}}
        series = gestor.obtenerDatosSeriesTemporales(evento)  # lista dicts/objetos

        context = {
            "evento": datos["evento"],
            "series": series,
            "user": usuario,
            "mensaje": mensaje,
        }
        return render(request, "redsismica/evento_detalle.html", context)

    # ==== GET: mostrar el detalle editable (sin prints) ====
    datos = gestor.buscarDatosEventoSismico(evento)
    series = gestor.obtenerDatosSeriesTemporales(evento)

    context = {
        "evento": datos["evento"],
        "series": series,
        "user": usuario,
    }
    return render(request, "redsismica/evento_detalle.html", context)