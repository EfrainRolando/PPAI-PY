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

    AMBITOS_POSIBLES: ClassVar[List[str]] = [
        "EventoSismico",
        "SerieTemporal",
        "MuestraSismica",
    ]

    def __init__(self, nombre: str, ambito: str = "EventoSismico"):
        # Sin validaciones ni normalizaciones
        self.nombre = nombre
        self.ambito = ambito

    # ===== Métodos de clase: devolver listas tal cual =====
    @classmethod
    def nombres_posibles(cls) -> List[str]:
        return cls.NOMBRES_POSIBLES

    @classmethod
    def ambitos_posibles(cls) -> List[str]:
        return cls.AMBITOS_POSIBLES

    # ---------- Métodos de clase que el Gestor va a llamar ----------
    def sosBloqueadoEnRevision(self) -> str:
        if self.nombre == "BloqueadoEnRevision":
            return self.nombre

    def esAmbitoES(self) -> bool:
        return self.ambito == "EventoSismico"

    def sosAutoDetectado(self) -> bool:
        return self.nombre == "AutoDetectado"

    def sosPteRevision(self) -> bool:
        return self.nombre == "PteRevision"
