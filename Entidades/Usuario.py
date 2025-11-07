class Usuario:
    def __init__(self, username: str, nombre_mostrar: str | None = None) -> None:
        self.username = username
        self.nombre_mostrar = nombre_mostrar or username.capitalize()

    def getUsuarioLogueado(self) -> str:
        """
        Nombre a mostrar en la UI.
        """
        return self.nombre_mostrar
