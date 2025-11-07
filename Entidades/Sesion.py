
from typing import Optional
from Entidades.Usuario import Usuario

class Sesion:
    def __init__(self) -> None:
        self.usuario: Optional[Usuario] = None
        self.activa: bool = False

    def iniciarSesion(self, username: str, password: str) -> bool:
        # (tu lógica de autenticación)
        # si ok:
        self.usuario = Usuario(username)  # o como lo estés construyendo
        self.activa = True
        return True

    def cerrarSesion(self) -> None:
        self.usuario = None
        self.activa = False

    def getUsuario(self) -> str:
        """
        Devuelve SIEMPRE el nombre para mostrar, o 'Invitado' si no hay sesión.
        """
        if self.usuario:
            return self.usuario.getUsuarioLogueado()
        return "Invitado"