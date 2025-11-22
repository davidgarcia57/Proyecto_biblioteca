from datetime import datetime

class Solicitante:
    def __init__(self, nombre_completo, telefono=None, email=None, direccion=None, fecha_registro=None, id_prestatario=None):
        self.id_prestatario = id_prestatario
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()

    def __str__(self):
        return f"{self.nombre_completo} (ID: {self.id_prestatario})"