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
        db = ConexionBD()
        conn = db.conectar()
        
        if conn:
            try:
                cursor = conn.cursor()
                if self.id_prestatario:
                    sql = """
                        UPDATE solicitantes SET nombre_completo=%s, telefono=%s, email=%s, direccion=%s 
                        WHERE id_prestatario=%s
                    """
                    valores = (self.nombre_completo, self.telefono, self.email, self.direccion, self.id_prestatario)
                    cursor.execute(sql, valores)
                else:
                    # INSERTAR NUEVO
                    sql = """
                        INSERT INTO solicitantes (nombre_completo, telefono, email, direccion, fecha_registro) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
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
        db = ConexionBD()
        conn = db.conectar()
        lista = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM solicitantes ORDER BY nombre_completo ASC")
                datos = cursor.fetchall()
                for fila in datos:
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

    @staticmethod
    def obtener_nombre(id_prestatario):
        db = ConexionBD()
        conn = db.conectar()
        nombre = None
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT nombre_completo FROM solicitantes WHERE id_prestatario = %s"
                cursor.execute(sql, (id_prestatario,))
                res = cursor.fetchone()
                if res:
                    nombre = res[0]
            finally:
                conn.close()
        return nombre

    @staticmethod
    def buscar_por_termino(termino):

        """Busca solicitantes por nombre o ID para el popup"""
        db = ConexionBD()
        conn = db.conectar()
        resultados = []
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT id_prestatario, nombre_completo, telefono 
                    FROM solicitantes 
                    WHERE nombre_completo LIKE %s OR id_prestatario LIKE %s
                    LIMIT 20
                """
                like = f"%{termino}%"
                cursor.execute(sql, (like, like))
                resultados = cursor.fetchall()
            finally:
                conn.close()
        return resultados
    
    @staticmethod
    def obtener_todos_reporte():
        """Retorna lista para el reporte PDF"""
        db = ConexionBD()
        conn = db.conectar()
        datos = []
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT id_prestatario, nombre_completo, telefono, email, direccion FROM solicitantes ORDER BY nombre_completo"
                cursor.execute(sql)
                datos = cursor.fetchall()
            finally:
                conn.close()
        return datos
