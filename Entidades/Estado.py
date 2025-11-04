from typing import List

try:
    from typing_extensions import ClassVar
except ImportError:
    from typing import ClassVar


class Estado:
    # Disponibles siempre (no lazy). El Gestor puede iterar directo sobre estas listas.
    NOMBRES_POSIBLES: ClassVar[List[str]] = [
        "AutoDetectado",
        "PteRevision",
        "BloqueadoEnRevision",
        "Aprobado",
        "Rechazado",
        "Derivado",
        "Confirmado",
        "Registrado",
        "PteCierre",
        "Cerrado",
    ]

    def __init__(self, nombre: str):
        # Sin validaciones ni normalizaciones
        self.nombre = nombre

    # ===== Métodos de clase: devolver listas tal cual =====
    @classmethod
    def nombres_posibles(cls) -> List[str]:
        return cls.NOMBRES_POSIBLES

    # ---------- Métodos de clase que el Gestor va a llamar ----------
    def sosBloqueadoEnRevision(self) -> bool:
        return self.nombre == "BloqueadoEnRevision"

    def sosAutoDetectado(self) -> bool:
        return self.nombre == "AutoDetectado"

    def sosPteRevision(self) -> bool:
        return self.nombre == "PteRevision"
