from datetime import datetime

from Entidades.PantallaRevision import PantallaRevision
from Entidades.Sesion import Sesion
from Entidades.Usuario import Usuario

if __name__ == "__main__":
    sesion = Sesion()
    sesion.iniciarSesionDesdeTeclado()
    PantallaRevision(sesion).opcionRegistrarResultado()
