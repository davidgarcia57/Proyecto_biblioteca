from src.config.conexion_db import ConexionBD
from src.model.Usuario import Usuario

class UsuarioDAO:
    def autenticar(self, usuario, password):
        db = ConexionBD()
        conn = db.conectar()
        usuario_encontrado = None

        if conn:
            try:
                cursor = conn.cursor()
                # Consulta simple (Para producción real, las contraseñas deberían estar encriptadas)
                sql = "SELECT id_usuario_sistema, nombre, usuario, rol FROM usuarios_sistema WHERE usuario = %s AND password_hash = %s"
                cursor.execute(sql, (usuario, password))
                row = cursor.fetchone()

                if row:
                    # Si existe, creamos el objeto Usuario
                    usuario_encontrado = Usuario(
                        id_usuario=row[0],
                        nombre_completo=row[1],
                        usuario=row[2],
                        rol=row[3]
                    )
            except Exception as e:
                print(f"Error en login: {e}")
            finally:
                cursor.close()
                db.cerrar()
        
        return usuario_encontrado