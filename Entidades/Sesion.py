from datetime import datetime
from typing import Optional

from Entidades.Usuario import Usuario


class Sesion:
    def __init__(self) -> None:
        self.usuario_actual: Optional[Usuario] = None
        self.inicio: Optional[datetime] = None

    def iniciarSesionDesdeTeclado(self) -> None:
        username = input("Usuario: ").strip()
        clave = input("Clave: ")

        # Acepta cualquier cosa
        self.usuario_actual = Usuario(
            username=username or "invitado",
            nombre_mostrar=(username.capitalize() if username else "Invitado"),
            password_plana=clave  # si guardás hash, cambialo adentro de Usuario
        )
        self.inicio = datetime.now()

    def getUsuario(self) -> str:
        # 👇 CAMBIO CLAVE: si no hay sesión, pide user/clave ahora
        if self.usuario_actual is None:
            self.iniciarSesionDesdeTeclado()
        # si tu Usuario tiene getNombreMostrar(), usalo; si no, accedé al atributo
        return self.usuario_actual.nombre_mostrar

    def getUsuarioActual(self) -> Optional[Usuario]:
        return self.usuario_actual

    def cerrarSesion(self) -> None:
        self.usuario_actual = None
        self.inicio = None
