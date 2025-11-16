from src.config.conexion_db import ConexionBD
from src.model.Libro import Libro

class LibroDAO:
    def guardar(self, libro: Libro):
        db = ConexionBD()
        conn = db.conectar()

        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO libros (titulo, isbn, clasificacion_lc, id_editorial) VALUES (%s, %s, %s, %s)"
                valores = (libro.titulo, libro.isbn, libro.clasificacion, libro.id_editorial)

                cursor.execute(sql,valores)
                conn.commit()
                print("Libro guardado exitosamente")
                return True
            except Exception as e:
                print(f"Error al guarda el libro: {e}")
                return False
            finally:
                cursor.close()
                db.cerrar()
        return False