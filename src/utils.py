import os
import sys

def resource_path(relative_path):
    """
    Devuelve la ruta correcta para recursos empaquetados con PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        # Cuando ya está en .exe
        return os.path.join(sys._MEIPASS, relative_path)
    # Cuando está en modo desarrollo
    return os.path.join(os.path.dirname(__file__), relative_path)
