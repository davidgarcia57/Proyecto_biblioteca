class Usuario:
    def __init__(self, id_usuario, nombre_completo, usuario, rol):
        self.id_usuario = id_usuario
        self.nombre_completo = nombre_completo
        self.usuario = usuario
        self.rol = rol

    def __str__(self):
        return f"{self.usuario} ({self.rol})"