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

# --- INSTANCIA ÚNICA (Como pediste) ---
sesion = Sesion()
gestor = GestorRevisionResultados(sesion)

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
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            if USUARIOS.get(u) == p:
                # ✅ Seteamos la sesión real del Gestor
                sesion.iniciarSesion(u, p)
                gestor.sesion = sesion  # el gestor usa esta sesión

                resp = redirect("menu_principal")
                _set_auth_cookie(resp, u)
                return resp
            else:
                form.add_error(None, "Usuario o contraseña inválidos")
    else:
        form = LoginForm()
    return render(request, "redsismica/login.html", {"form": form})


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
        return redirect("menu_principal")
    return redirect("login")


def logout_view(request: HttpRequest) -> HttpResponse:
    resp = redirect("login")
    _clear_auth_cookie(resp)
    sesion.cerrarSesion()
    gestor.sesion = sesion
    return resp

@requiere_login
def menu_principal_view(request: HttpRequest) -> HttpResponse:
    user = gestor.buscarUsuario()
    return render(request, "redsismica/menu_principal.html", {"user": user})
# --------------------
#Logica de Primer parte
@requiere_login
def opcionRegistrarResultado(request: HttpRequest) -> HttpResponse:
    return gestor.opcionRegistrarResultado(
        lambda eventos: mostrarEventosSismicos(request, eventos)  # 👈 la Pantalla es quien muestra
    )

def mostrarEventosSismicos(request: HttpRequest, eventos: list[dict]) -> HttpResponse:
    user = gestor.buscarUsuario()  # ← usar la sesión de dominio
    return render(request, "redsismica/eventos.html", {
        "eventos": eventos,
        "user": user,
    })

@requiere_login
def tomarSeleccionEventoSismico(request: HttpRequest, evento_id: int) -> HttpResponse:
    # Esta view SOLO muestra (GET). Si llega un POST por error, redirige a acciones.
    if request.method == "POST":
        return redirect("evento_accion", evento_id=evento_id)

    # GET → pasamos dos callbacks siguiendo tu secuencia
    return gestor.tomarSeleccionEventoSismico(
        evento_id,
        lambda datos: mostrarDetalleEvento(request, datos),
        lambda payload: mostrarDetalleEvento(request, payload),
    )


@requiere_login
def tomarOpcionAccion(request: HttpRequest, evento_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("eventos")

    accion = (request.POST.get("accion") or "").strip().lower()

    # Aseguramos que el gestor tenga seleccionado el evento
    gestor.tomarSeleccionEventoSismico(
        evento_id,
        lambda _datos: None,   # no mostramos nada acá
        lambda _payload: None  # no mostramos nada acá
    )

    # Ejecutamos la acción en el gestor
    ejecutada = gestor.tomarOpcionAccion(evento_id, accion)

    if accion == "modificar":
        return redirect("evento_modificar", evento_id=evento_id)

    if not ejecutada:
        messages.error(request, "No se pudo ejecutar la acción o el evento no existe.")
        return redirect("evento_detalle", evento_id=evento_id)

    if accion == "rechazar":
        messages.success(request, "Evento rechazado exitosamente.")
    elif accion in ("confirmar", "aprobar"):
        messages.success(request, "Evento confirmado y aprobado.")
    elif accion in ("derivar", "solicitar"):
        messages.info(request, "Evento derivado a experto.")

    return redirect("eventos")


def mostrarDetalleEvento(request: HttpRequest, datos: dict) -> HttpResponse:
    img = datos.get("sismograma_img_url") or "redsismica/sismografo.jpeg"
    series = datos.get("series_por_estacion")
    if not series:
        ev = datos.get("evento")
        try:
            # Si 'evento' es un objeto de dominio con atributo 'seriesTemporales'
            st_list = getattr(ev, "seriesTemporales", None)
            if st_list:
                series = [st.getDatos() for st in st_list]    # usa SerieTemporal.getDatos()
        except Exception:
            pass

        # Si 'evento' ya viene como dict con seriesTemporales (dicts), las usamos igual
        if not series and isinstance(ev, dict) and "seriesTemporales" in ev:
            series = ev["seriesTemporales"]

    # Si aún es None, que al menos sea lista
    if series is None:
        series = []

    return render(request, "redsismica/evento_detalle.html", {
        "evento": datos.get("evento", {}),
        "sismograma_img_url": img,
        "series_por_estacion": series,
    })
    
@requiere_login
def tomar_modificaciones(request: HttpRequest, evento_id: int) -> HttpResponse:
    usuario = _get_user(request)
    if request.method == "POST":
        magnitud = request.POST.get("magnitud")
        alcance_nombre = request.POST.get("alcance_nombre")
        alcance_desc = request.POST.get("alcance_desc")
        origen_nombre = request.POST.get("origen_nombre")
        origen_detalle = request.POST.get("origen_detalle")

        if not magnitud or not alcance_nombre or not origen_nombre:
            datos = gestor.buscarDatosEventoSismico()
            return render(request, "redsismica/evento_modificar.html", {
                "evento": datos["evento"],
                "user": usuario,
                "form_error": "Error: Magnitud, Alcance y Origen no pueden estar vacíos."
            })

        gestor.tomarModificaciones(
            nuevoMagnitud=float(magnitud),
            nuevoAlcanceNombre=alcance_nombre,
            nuevoAlcanceDescripcion=alcance_desc,
            nuevoOrigenNombre=origen_nombre,
            nuevoOrigenDescripcion=origen_detalle
        )
        messages.success(request, "Datos modificados correctamente.")
        return redirect('evento_detalle', evento_id=evento_id)

    datos = gestor.buscarDatosEventoSismico()
    return render(request, "redsismica/evento_modificar.html", {
        "evento": datos["evento"],
        "user": usuario,
        "form_error": None
    })
@requiere_login
def tomarSeleccionOpcionMapa(request) -> HttpResponse:
    usuario = _get_user(request)
    return gestor.tomarSeleccionOpcionMapa(
        lambda datos: render(request, "redsismica/opcion_mapa.html", {
            "evento": datos.get("evento", {}),
            "mapa_img_url": datos.get("mapa_img_url", "redsismica/sismo-mapa.jpg"),
            "user": usuario,
        })
    )

@requiere_login
@require_POST
def guardar_cambios_view(request: HttpRequest) -> HttpResponse:
    try:
        gestor.finCU()
        messages.success(request, "Cambios guardados correctamente.")
    except Exception as e:
        messages.error(request, f"No se pudieron guardar los cambios: {e}")
    return redirect("menu_principal")