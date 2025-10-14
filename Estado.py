
class Estado:
    def __init__(self, nombre: str):
        self.nombre = nombre

    # ✅ Métodos de consulta
    def sosAutoDetectado(self) -> bool:
        return self.nombre == "AutoDetectado"

    def sosParaRevision(self) -> bool:
        return self.nombre == "ParaRevision"
