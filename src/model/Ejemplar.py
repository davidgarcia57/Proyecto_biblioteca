from datetime import datetime

class Ejemplar:
    def __init__(self, no_adquisicion, id_obra, id_usuario_captura, 
                 ejemplar=None, volumen=None, tomo=None, 
                 prestado=False, borrado=False, fecha_registro=None):
        
        # Identificadores, estos se los comento por que si se pueden confundir
        self.no_adquisicion = no_adquisicion  # PK 
        self.id_obra = id_obra                # FK a la Obra
        self.id_usuario_captura = id_usuario_captura # FK al Usuario (Auditoría)
        
        # Datos Específicos del Físico
        self.ejemplar = ejemplar 
        self.volumen = volumen
        self.tomo = tomo
        
        # Estado si es presatdo (el if else)
        self.prestado = prestado
        self.borrado = borrado
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()

    def __str__(self):
        return f"Adq: {self.no_adquisicion} - Obra ID: {self.id_obra}"