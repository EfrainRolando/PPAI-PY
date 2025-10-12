from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    nombreUsuario: str
    contrasena: str

    def getUsuario(self) -> str:
        return self.nombreUsuario


@dataclass
class Sesion:
    usuario: Usuario
    fechaHoraDesde: datetime
    fechaHoraHasta: Optional[datetime] = None

    def getUsuarioLogueado(self) -> str:
        return self.usuario.getUsuario()