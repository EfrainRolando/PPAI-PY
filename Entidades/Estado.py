from typing import List

try:
    from typing_extensions import ClassVar
except ImportError:
    from typing import ClassVar


class Estado:

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

    def __init__(self, NAME: str):

        self.NAME = NAME


    @classmethod
    def nombres_posibles(cls) -> List[str]:
        return cls.NOMBRES_POSIBLES
    
    def sosBloqueadoEnRevision(self) -> bool:
        return self.NAME == "BloqueadoEnRevision"

    def sosAutoDetectado(self) -> bool:
        return self.NAME == "AutoDetectado"

    def sosPteRevision(self) -> bool:
        return self.NAME == "PteRevision"
