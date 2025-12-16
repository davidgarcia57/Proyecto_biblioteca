from src.config.conexion_db import ConexionBD
from datetime import datetime

class Visita:
    def __init__(self, area, nombre=None, procedencia=None, sexo=None, fecha=None, id_visita=None):
        self.id_visita = id_visita
        self.area = area # 'Lectura', 'Virtual', 'Estudio'
        self.nombre = nombre
        self.procedencia = procedencia
        self.sexo = sexo
        self.fecha = fecha if fecha else datetime.now()

    def guardar(self):
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    INSERT INTO visitantes (area, nombre_completo, procedencia, sexo, fecha_entrada)
                    VALUES (%s, %s, %s, %s, NOW())
                """
                cursor.execute(sql, (self.area, self.nombre, self.procedencia, self.sexo))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error guardar visita: {e}")
                return False
            finally:
                conn.close()
        return False

    @staticmethod
    def obtener_conteo_por_area(fecha_ini, fecha_fin):
        db = ConexionBD()
        conn = db.conectar()
        datos = []
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT area, COUNT(*) as total 
                    FROM visitantes 
                    WHERE fecha_entrada BETWEEN %s AND %s
                    GROUP BY area
                """
                cursor.execute(sql, (fecha_ini, fecha_fin))
                datos = cursor.fetchall()
            finally:
                conn.close()
        return datos

    @staticmethod
    def obtener_conteo_total(fecha_ini, fecha_fin):
        db = ConexionBD()
        conn = db.conectar()
        total = 0
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT COUNT(*) FROM visitantes WHERE fecha_entrada BETWEEN %s AND %s"
                cursor.execute(sql, (fecha_ini, fecha_fin))
                row = cursor.fetchone()
                if row: total = row[0]
            finally:
                conn.close()
        return total