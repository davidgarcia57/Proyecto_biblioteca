from src.config.conexion_db import ConexionBD

class Usuario:
    def __init__(self, id_usuario=None, nombre=None, usuario=None, rol=None, activo=1):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.rol = rol
        self.activo = activo

    @staticmethod
    def autenticar(usuario, password):
        """Método estático que busca en la BD y devuelve un objeto Usuario si es válido"""
        db = ConexionBD()
        conn = db.conectar()
        usuario_obj = None
        
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT id_usuario, nombre, usuario, rol, activo FROM usuarios_sistema WHERE usuario = %s AND password_hash = %s"
                cursor.execute(sql, (usuario, password))
                row = cursor.fetchone()

                if row:
                    # Creamos la instancia con los datos de la BD
                    usuario_obj = Usuario(row[0], row[1], row[2], row[3], row[4])
            except Exception as e:
                print(f"Error SQL Usuario: {e}")
            finally:
                cursor.close()
                db.cerrar()
        
        return usuario_obj

    def __str__(self):
        return f"{self.usuario} ({self.rol})"