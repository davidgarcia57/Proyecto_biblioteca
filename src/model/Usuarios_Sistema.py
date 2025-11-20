class UsuarioSistema:
    def __init__(self, nombre, usuario, password_hash, rol, activo=True, id_usuario_sistema=None):
        self.id_usuario_sistema = id_usuario_sistema
        self.nombre = nombre
        self.usuario = usuario
        self.password_hash = password_hash
        self.rol = rol 
        self.activo = activo

    def __str__(self):
        return f"{self.usuario} ({self.rol})"