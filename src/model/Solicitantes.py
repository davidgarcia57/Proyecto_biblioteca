from src.config.conexion_db import ConexionBD
from datetime import datetime

class Solicitante:
    def __init__(self, nombre_completo, telefono=None, email=None, direccion=None, fecha_registro=None, id_prestatario=None):
        self.id_prestatario = id_prestatario
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now()

    def guardar(self):
        """Guarda un nuevo solicitante o actualiza uno existente"""
        db = ConexionBD()
        conn = db.conectar()
        
        if conn:
            try:
                cursor = conn.cursor()
                if self.id_prestatario:
                    # ACTUALIZAR
                    sql = """
                        UPDATE solicitantes SET nombre_completo=%s, telefono=%s, email=%s, direccion=%s 
                        WHERE id_prestatario=%s
                    """
                    # CORRECCIÓN: Fíjate en el doble paréntesis ((...))
                    valores = (self.nombre_completo, self.telefono, self.email, self.direccion, self.id_prestatario)
                    cursor.execute(sql, valores)
                else:
                    # INSERTAR NUEVO
                    sql = """
                        INSERT INTO solicitantes (nombre_completo, telefono, email, direccion, fecha_registro) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    # CORRECCIÓN: Fíjate en el doble paréntesis ((...))
                    valores = (self.nombre_completo, self.telefono, self.email, self.direccion, self.fecha_registro)
                    cursor.execute(sql, valores)
                
                conn.commit()
                return True
            except Exception as e:
                print(f"Error al guardar solicitante: {e}")
                return False
            finally:
                conn.close()
        return False
    
    @staticmethod
    def obtener_todos():
        """Devuelve una list de todos los solicitantes para la tabla"""
        db = ConexionBD()
        conn = db.conectar()
        lista = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM solicitantes ORDER BY nombre_completo ASC")
                datos = cursor.fetchall()
                for fila in datos:
                    # Fila: (id, nombre, tel, email, dir, fecha)
                    lista.append(Solicitante(fila[1], fila[2], fila[3], fila[4], fila[5], fila[0]))
            finally:
                conn.close()
        return lista
    
    @staticmethod
    def eliminar(id_prestatario):
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM solicitantes WHERE id_prestatario = %s", (id_prestatario,))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error al eliminar: {e}")
                return False
            finally:
                conn.close()
        return False