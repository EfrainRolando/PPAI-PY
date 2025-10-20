from typing import ClassVar, List


class Estado:
    # Se inicializan la PRIMERA vez que se crea un Estado (desde __init__)
    NOMBRES_POSIBLES: ClassVar[List[str]] = []
    AMBITOS_POSIBLES: ClassVar[List[str]] = []

    def __init__(self, nombre: str, ambito: str = "EventoSismico"):
        # --- Catálogos definidos adentro del init, SIN validaciones ---
        if not Estado.NOMBRES_POSIBLES:
            Estado.NOMBRES_POSIBLES = [
                "AutoDetectado",
                "PteRevision",            # o "ParaRevision" si usás ese
                "BloqueadoEnRevision",
                "Aprobado",
                "Rechazado",
                "Derivado",
                "Confirmado",
                "Registrado",
                "PteCierre",
                "Cerrado",
            ]
        if not Estado.AMBITOS_POSIBLES:
            Estado.AMBITOS_POSIBLES = [
                "EventoSismico",
                "SerieTemporal",
                "MuestraSismica",
            ]

        # Se asigna TAL CUAL llega (sin validar, sin normalizar)
        self.nombre: str = nombre
        self.ambito = ambito

    # ---------- Métodos de clase que el Gestor va a llamar ----------
    @classmethod
    def sosBloqueadoEnRevision(cls) -> List[str]:
        """Lista de nombres que consideramos 'bloqueado'."""
        # No requiere instancias previas:
        if not cls.NOMBRES_POSIBLES:
            # misma lista del __init__ para asegurar disponibilidad
            cls.NOMBRES_POSIBLES = [
                "AutoDetectado", "PteRevision", "BloqueadoEnRevision",
                "Aprobado", "Rechazado", "Derivado", "Confirmado",
                "Registrado", "PteCierre", "Cerrado",
            ]
        return ["BloqueadoEnRevision"]

    @classmethod
    def esAmbitoES(cls) -> List[str]:
        """Lista de etiquetas de ámbito que representan 'EventoSismico'."""
        if not cls.AMBITOS_POSIBLES:
            cls.AMBITOS_POSIBLES = ["EventoSismico", "SerieTemporal", "MuestraSismica"]
        return ["EventoSismico"]

    @classmethod
    def nombres_posibles(cls) -> List[str]:
        if not cls.NOMBRES_POSIBLES:
            cls.NOMBRES_POSIBLES = [
                "AutoDetectado", "PteRevision", "BloqueadoEnRevision",
                "Aprobado", "Rechazado", "Derivado", "Confirmado",
                "Registrado", "PteCierre", "Cerrado",
            ]
        return cls.NOMBRES_POSIBLES

    @classmethod
    def ambitos_posibles(cls) -> List[str]:
        if not cls.AMBITOS_POSIBLES:
            cls.AMBITOS_POSIBLES = ["EventoSismico", "SerieTemporal", "MuestraSismica"]
        return cls.AMBITOS_POSIBLES

    def sosAutoDetectado(self) -> bool:
        return self.nombre == "AutoDetectado"

    def sosPteRevision(self) -> bool:
        return self.nombre == "PteRevision"

    def esAmbitoES(self) -> bool:
        if self.ambito == 'EventoSismico':
            return True

    def sosBloqueadoEnRevision(self):
        if self.nombre == "BloqueadoEnRevision":
            return self.nombre
