from src.config.conexion_db import ConexionBD

class Estadisticas:
    @staticmethod
    def obtener_resumen():
        db = ConexionBD()
        conn = db.conectar()
        stats = {
            "libros": 0,
            "prestamos": 0,
            "usuarios": 0
        }
        
        if conn:
            try:
                cursor = conn.cursor()
                # 1. Total de Obras Activas
                sql_obras = "SELECT COUNT(DISTINCT id_obra) FROM ejemplares WHERE estado != 'Baja'"
                cursor.execute(sql_obras)
                stats["libros"] = cursor.fetchone()[0]
                
                # 2. Préstamos Activos (Sin cambios)
                cursor.execute("SELECT COUNT(*) FROM prestamos WHERE estado = 'Activo'")
                stats["prestamos"] = cursor.fetchone()[0]
                
                # 3. Solicitantes (Sin cambios)
                cursor.execute("SELECT COUNT(*) FROM solicitantes")
                stats["usuarios"] = cursor.fetchone()[0]
                
            except Exception as e:
                print(f"Error estadísticas: {e}")
            finally:
                cursor.close()
                conn.close()
                
        return stats