
class Estado:
    def __init__(self, nombre: str):
        self.nombre = nombre

    # ✅ Métodos de consulta
    def sosAutoDetectado(self) -> bool:
        return self.nombre == "AutoDetectado"

    def sosPteRevision(self) -> bool:
        return self.nombre == "PteRevision"
