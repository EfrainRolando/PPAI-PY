from datetime import datetime

from PantallaRevision import PantallaRevision
from Sesion import Sesion
from Usuario import Usuario

if __name__ == "__main__":
    sesion = Sesion()
    sesion.iniciarSesionDesdeTeclado()
    PantallaRevision(sesion).opcionRegistrarResultado()
