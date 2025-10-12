from dataclasses import dataclass


@dataclass
class Estado:
    nombre: str
    ambitoES: bool = True  # True = del CU 'ES' (gestor), False = de otro módulo

    def esAmbitoES(self) -> bool:
        return self.ambitoES

    # Consultas del diagrama
    def sosDetectado(self) -> bool: return self.nombre == "Detectado"
    def sosParaRevision(self) -> bool: return self.nombre == "PteRevision"
    def sosBloqueadoEnRevision(self) -> bool: return self.nombre == "BloqEnRevision"
    def sosRechazado(self) -> bool: return self.nombre == "Rechazado"
