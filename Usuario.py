from dataclasses import dataclass


@dataclass
class Usuario:
    nombreUsuario: str
    contrasena: str

    def getUsuario(self) -> str:
        return self.nombreUsuario
