from src.config.conexion_db import ConexionBD

class Usuario:
    def __init__(self, id_usuario=None, nombre=None, usuario=None, password_hash=None, rol=None, activo=1):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.usuario = usuario
        self.password_hash = password_hash
        self.rol = rol
        self.activo = activo

    @staticmethod
    def autenticar(usuario, password):
        """Login: Busca usuario y contraseña"""
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
                    usuario_obj = Usuario(row[0], row[1], row[2], None, row[3], row[4])
            finally:
                conn.close()
        return usuario_obj

    def guardar(self):
        """Guarda nuevo o actualiza existente"""
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                if self.id_usuario:
                    sql = "UPDATE usuarios_sistema SET nombre=%s, usuario=%s, rol=%s, activo=%s WHERE id_usuario=%s"
                    cursor.execute(sql, (self.nombre, self.usuario, self.rol, self.activo, self.id_usuario))
                else:
                    sql = "INSERT INTO usuarios_sistema (nombre, usuario, password_hash, rol, activo) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.nombre, self.usuario, self.password_hash, self.rol, self.activo))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error guardar usuario: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def obtener_todos():
        db = ConexionBD()
        conn = db.conectar()
        lista = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id_usuario, nombre, usuario, rol, activo FROM usuarios_sistema")
                for row in cursor.fetchall():
                    lista.append(Usuario(row[0], row[1], row[2], None, row[3], row[4]))
            finally:
                conn.close()
        return lista

    @staticmethod
    def cambiar_password(id_usuario, nueva_pass):
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE usuarios_sistema SET password_hash=%s WHERE id_usuario=%s", (nueva_pass, id_usuario))
                conn.commit()
                return True
            finally:
                conn.close()
        return False
    
    @staticmethod
    def eliminar(id_usuario):
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuarios_sistema WHERE id_usuario = %s", (id_usuario,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar usuario: {e}")
                return False
            finally:
                conn.close()
        return False

    def __str__(self):
        return f"{self.usuario} ({self.rol})"