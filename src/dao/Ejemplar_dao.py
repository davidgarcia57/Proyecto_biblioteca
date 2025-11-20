from src.config.conexion_db import ConexionBD
from src.model.Ejemplar import Ejemplar

class EjemplarDAO:
    #Es lo mismo que Obra_dao solo que con Ejemplar, no se hagan bolas con esto
    def guardar_ejemplar(self, ejemplar: Ejemplar):
        db = ConexionBD()
        conn = db.conectar()

        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    INSERT INTO ejemplares (
                        no_adquisicion, id_obra, id_usuario_captura, 
                        ejemplar, volumen, tomo, prestado, borrado, fecha_registro
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    ejemplar.no_adquisicion,
                    ejemplar.id_obra,
                    ejemplar.id_usuario_captura,
                    ejemplar.ejemplar,
                    ejemplar.volumen,
                    ejemplar.tomo,
                    ejemplar.prestado,
                    ejemplar.borrado,
                    ejemplar.fecha_registro
                )
                cursor.execute(sql, valores)
                conn.commit()
                print(f"Ejemplar {ejemplar.no_adquisicion} guardado correctamente.")
                return True

            except Exception as e:
                print(f"Error al guardar el ejemplar: {e}")
                return False
            finally:
                cursor.close()
                db.cerrar()
        return False
    
    def existe_adquisicion(self, no_adquisicion):
        """Verifica si ya existe el código de barras/adquisición para evitar duplicados"""
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT no_adquisicion FROM ejemplares WHERE no_adquisicion = %s"
                cursor.execute(sql, (no_adquisicion,))
                return cursor.fetchone() is not None
            finally:
                cursor.close()
                db.cerrar()
        return False