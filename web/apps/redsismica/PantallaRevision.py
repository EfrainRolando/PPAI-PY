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
gestor = GestorRevisionResultados()

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
        return redirect("menu_principal")
    return redirect("login")

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data["username"]
            p = form.cleaned_data["password"]
            if USUARIOS.get(u) == p:
                resp = redirect("menu_principal")
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
def menu_principal_view(request: HttpRequest) -> HttpResponse:
    """Muestra la 'carátula' o menú principal."""
    usuario = _get_user(request)
    return render(request, "redsismica/menu_principal.html", {"user": usuario})
# --------------------
#Logica de Primer parte
@requiere_login
def opcionRegistrarResultado(request: HttpRequest) -> HttpResponse:
    return gestor.opcionRegistrarResultado(
        lambda eventos: mostrarEventosSismicos(request, eventos)  # 👈 la Pantalla es quien muestra
    )

def mostrarEventosSismicos(request: HttpRequest, eventos: list[dict]) -> HttpResponse:
    usuario = _get_user(request)
    return render(request, "redsismica/eventos.html", {
        "eventos": eventos,
        "user": usuario,
    })

@requiere_login
def tomarSeleccionEventoSismico(request: HttpRequest, evento_id: int) -> HttpResponse:
    usuario = _get_user(request)

    if request.method == "POST":
        accion = request.POST.get("accion", "").strip().lower()
        if accion == "rechazar":
            gestor.validarDatosEventoSismico()
            gestor.cambiarEstadoARechazado(usuario)
            messages.success(request, "Evento rechazado exitosamente")
            return redirect("eventos")
        if accion == "aprobar":
            gestor.cambiarEstadoAConfirmado(usuario)
            messages.success(request, "Evento confirmado y aprobado.")
            return redirect("eventos")
        if accion == "solicitar":
            gestor.cambiarEstadoADerivado(usuario)
            messages.info(request, "Evento derivado a experto.")
            return redirect("eventos")
        if accion == "modificar":
            return redirect("evento_modificar", evento_id=evento_id)
        messages.error(request, "Acción no válida.")
        return redirect("evento_detalle", evento_id=evento_id)

    # GET → pasamos DOS callbacks siguiendo tu secuencia
    return gestor.tomarSeleccionEventoSismico(
        evento_id,
        # 3) “mostrar” detalle (paso lógico)
        lambda detalles: None,  # si querés, podríamos hacer messages.info(...) acá
        # 5) mostrar sismograma (render final que incluye detalle + sismograma)
        lambda payload: mostrarDetalleEvento(request, payload),
    )


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
def evento_modificar_view(request: HttpRequest, evento_id: int) -> HttpResponse:
    usuario = _get_user(request)
    if not gestor.eventoSeleccionado or gestor.eventoSeleccionado.id_evento != evento_id:
        if not gestor.tomarSeleccionEventoSismico(evento_id):
            messages.error(request, "Evento no encontrado o no disponible.")
            return redirect("eventos")
    if request.method == "POST":
        magnitud = request.POST.get("magnitud")
        alcance_nombre = request.POST.get("alcance_nombre")
        alcance_desc = request.POST.get("alcance_desc")
        origen_nombre = request.POST.get("origen_nombre")
        origen_detalle = request.POST.get("origen_detalle")

        # --- PASO 16: Validación (simple) ---
        if not magnitud or not alcance_nombre or not origen_nombre:
            # Si hay error, volvemos a mostrar el formulario con un mensaje
            # --- MODIFICADO ---
            datos = gestor.buscarDatosEventoSismico() # Usa el evento en memoria
            return render(request, "redsismica/evento_modificar.html", {
                "evento": datos["evento"],
                "user": usuario,
                "form_error": "Error: Magnitud, Alcance y Origen no pueden estar vacíos."
            })

        # Si la validación es OK, actualizamos el objeto evento en memoria
        # --- MODIFICADO ---
        gestor.tomarModificaciones(
            # evento=evento, <-- Argumento removido
            nuevoMagnitud=float(magnitud),
            nuevoAlcanceNombre=alcance_nombre,
            nuevoAlcanceDescripcion=alcance_desc,
            nuevoOrigenNombre=origen_nombre,
            nuevoOrigenDescripcion=origen_detalle
        )

        # Redirigimos DE VUELTA a la página de detalle
        messages.success(request, "Datos modificados correctamente.")
        # Usamos el evento_id del parámetro de la URL
        return redirect('evento_detalle', evento_id=evento_id)

    # --- GET (Mostrar el formulario por primera vez) ---
    # --- MODIFICADO ---
    datos = gestor.buscarDatosEventoSismico() # Usa el evento en memoria
    return render(request, "redsismica/evento_modificar.html", {
        "evento": datos["evento"],
        "user": usuario,
        "form_error": None
    })
