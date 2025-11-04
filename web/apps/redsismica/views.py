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

@requiere_login
def eventos_view(request: HttpRequest) -> HttpResponse:
    """Lista de eventos usando SOLO el Gestor (filtra y ordena)."""
    usuario = _get_user(request)

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
def evento_modificar_view(request: HttpRequest, evento_id: int) -> HttpResponse:
    usuario = _get_user(request)
    evento = gestor.tomarSeleccionEventoSismico(evento_id)

    if request.method == "POST":
        # --- PASO 12 (Guardar): Capturar modificaciones ---
        magnitud = request.POST.get("magnitud")
        alcance_nombre = request.POST.get("alcance_nombre")
        alcance_desc = request.POST.get("alcance_desc")
        origen_nombre = request.POST.get("origen_nombre")
        origen_detalle = request.POST.get("origen_detalle")

        # --- PASO 16: Validación (simple) ---
        if not magnitud or not alcance_nombre or not origen_nombre:
            # Si hay error, volvemos a mostrar el formulario con un mensaje
            datos = gestor.buscarDatosEventoSismico(evento)
            return render(request, "redsismica/evento_modificar.html", {
                "evento": datos["evento"],
                "user": usuario,
                "form_error": "Error: Magnitud, Alcance y Origen no pueden estar vacíos."
            })
        
        # Si la validación es OK, actualizamos el objeto evento en memoria
        gestor.tomarModificaciones(
            evento=evento,
            nuevoMagnitud=float(magnitud),
            nuevoAlcanceNombre=alcance_nombre,
            nuevoAlcanceDescripcion=alcance_desc,
            nuevoOrigenNombre=origen_nombre,
            nuevoOrigenDescripcion=origen_detalle
        )
        
        # Redirigimos DE VUELTA a la página de detalle
        messages.success(request, "Datos modificados correctamente.")
        return redirect('evento_detalle', evento_id=evento.id_evento)

    # --- GET (Mostrar el formulario por primera vez) ---
    datos = gestor.buscarDatosEventoSismico(evento)
    return render(request, "redsismica/evento_modificar.html", {
        "evento": datos["evento"],
        "user": usuario,
        "form_error": None
    })


@requiere_login
def evento_detalle_view(request: HttpRequest, evento_id: int) -> HttpResponse:
    usuario = _get_user(request)
    evento = gestor.tomarSeleccionEventoSismico(evento_id)
    
    # --- PASO 8: Bloquear evento (Se ejecuta al Cargar la vista GET) ---
    if request.method == "GET":
        gestor.cambiarEstadoABloqueadoEnRevision(evento, usuario)

    # -----------------------------------------------------------------
    # --- PASOS 14, 15, 17: Se ejecutan en el POST ---
    # -----------------------------------------------------------------
    if request.method == "POST":
        accion = request.POST.get("accion", "").strip().lower()

        # --- YA NO SE CAPTURAN MODIFICACIONES AQUÍ ---
        # --- YA NO SE VALIDA NADA AQUÍ (excepto la acción) ---

        # --- PASO 14, 15, 17: Procesar la acción seleccionada ---
        
        # PASO 15: AS Selecciona "Rechazar"
        if accion == "rechazar":
            gestor.validarDatosEventoSismico(evento)
            gestor.cambiarEstadoARechazado(evento, usuario)
            messages.success(request, "Evento rechazado exitosamente")
            return redirect("eventos")

        # Flujo Alternativo A6: AS selecciona "Confirmar"
        if accion == "aprobar":
            # (Usando los métodos que creamos en la respuesta anterior)
            gestor.cambiarEstadoAConfirmado(evento, usuario)
            messages.success(request, "Evento confirmado y aprobado.")
            return redirect("eventos")

        # Flujo Alternativo A7: AS selecciona "Solicitar revisión"
        if accion == "solicitar":
            gestor.cambiarEstadoADerivado(evento, usuario)
            messages.info(request, "Evento derivado a experto.")
            return redirect("eventos")

    # --- GET normal: traer datos y mostrar la pág. ---
    datos = gestor.buscarDatosEventoSismico(evento)
    
    # Recogemos mensajes de éxito (ej. "Datos modificados correctamente")
    page_messages = messages.get_messages(request)

    return render(request, "redsismica/evento_detalle.html", {
        "evento": datos["evento"],
        "user": usuario,
        "messages": page_messages, # Pasamos los mensajes a la plantilla
    })