import hashlib
from dataclasses import dataclass


class Usuario:
    def __init__(self, username: str, nombre_mostrar: str, password_plana: str) -> None:
        self.username = username
        self.nombre_mostrar = nombre_mostrar
        self.password_plana = password_plana  # hoy aceptás

    @staticmethod
    def hash_password(clave_plana: str) -> str:
        return hashlib.sha256(clave_plana.encode("utf-8")).hexdigest()

    def getUsuarioLogueado(self: "Usuario") -> str:
        # Devuelve el nombre a mostrar (podés cambiar a return usuario si querés el objeto)
        return self.nombre_mostrar
