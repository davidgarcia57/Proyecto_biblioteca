from datetime import datetime
from src.config.conexion_db import ConexionBD

class Ejemplar:
    def __init__(self, id_obra, numero_copia="Copia 1", ubicacion_fisica="General", estado="Disponible", id_ejemplar=None):
        self.id_ejemplar = id_ejemplar 
        self.id_obra = id_obra
        self.numero_copia = numero_copia
        self.ubicacion_fisica = ubicacion_fisica
        self.estado = estado
        self.fecha_adquisicion = datetime.now()

    def guardar(self, cursor):
        sql = """
            INSERT INTO ejemplares (id_obra, numero_copia, ubicacion_fisica, estado, fecha_adquisicion) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            self.id_obra, 
            self.numero_copia, 
            self.ubicacion_fisica, 
            self.estado, 
            self.fecha_adquisicion
        )
        cursor.execute(sql, valores)
        return cursor.lastrowid
        
    @staticmethod
    def obtener_info(id_ejemplar):
        """Busca título y estado para mostrar antes de borrar"""
        db = ConexionBD()
        conn = db.conectar()
        info = None
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT e.id_ejemplar, o.titulo, e.estado, e.ubicacion_fisica
                    FROM ejemplares e
                    JOIN obras o ON e.id_obra = o.id_obra
                    WHERE e.id_ejemplar = %s
                """
                cursor.execute(sql, (id_ejemplar,))
                row = cursor.fetchone()
                if row:
                    info = {"id": row[0], "titulo": row[1], "estado": row[2], "ubicacion": row[3]}
            finally:
                conn.close()
        return info

    @staticmethod
    def dar_de_baja(id_ejemplar):
        """Cambia el estado a 'Baja'"""
        db = ConexionBD()
        conn = db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # 1. Verificar si está prestado
                cursor.execute("SELECT estado FROM ejemplares WHERE id_ejemplar = %s", (id_ejemplar,))
                estado = cursor.fetchone()
                
                if estado and estado[0] == 'Prestado':
                    return False, "El libro está prestado. No se puede dar de baja."

                # 2. Ejecutar Baja
                sql = "UPDATE ejemplares SET estado = 'Baja' WHERE id_ejemplar = %s"
                cursor.execute(sql, (id_ejemplar,))
                conn.commit()
                return True, "Libro dado de baja correctamente."
            except Exception as e:
                return False, f"Error BD: {e}"
            finally:
                conn.close()
        return False, "Sin conexión."
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        from src.config.conexion_db import ConexionBD
        db = ConexionBD()
        conn = db.conectar()
        datos = []
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT 
                        e.numero_copia,  -- Adquisición
                        o.titulo, 
                        a.nombre_completo, -- Autor
                        o.clasificacion, 
                        e.fecha_adquisicion
                    FROM ejemplares e
                    JOIN obras o ON e.id_obra = o.id_obra
                    LEFT JOIN autores_obras ao ON o.id_obra = ao.id_obra
                    LEFT JOIN autores a ON ao.id_autor = a.id_autor
                    WHERE e.fecha_adquisicion BETWEEN %s AND %s
                    AND e.estado != 'Baja'
                    GROUP BY e.id_ejemplar  -- Evita duplicados si tiene varios autores
                    ORDER BY e.fecha_adquisicion DESC
                """
                cursor.execute(sql, (fecha_inicio, fecha_fin))
                datos = cursor.fetchall()
            finally:
                conn.close()
        return datos

    @staticmethod
    def obtener_libros_baja():
        from src.config.conexion_db import ConexionBD
        db = ConexionBD()
        conn = db.conectar()
        datos = []
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT e.id_ejemplar, o.titulo, o.isbn, e.ubicacion_fisica
                    FROM ejemplares e
                    JOIN obras o ON e.id_obra = o.id_obra
                    WHERE e.estado = 'Baja'
                    ORDER BY e.id_ejemplar DESC
                """
                cursor.execute(sql)
                datos = cursor.fetchall()
            finally:
                conn.close()
        return datos

    def actualizar_estado(self, nuevo_estado):
        db = ConexionBD()
        conn = db.conectar()
        exito = False
        if conn:
            try:
                cursor = conn.cursor()
                if nuevo_estado == 'Prestado':
                    sql = "UPDATE ejemplares SET estado = %s WHERE id_ejemplar = %s AND estado = 'Disponible'"
                else:
                    sql = "UPDATE ejemplares SET estado = %s WHERE id_ejemplar = %s"
                
                cursor.execute(sql, (nuevo_estado, self.id_ejemplar))
                conn.commit()
                
                if cursor.rowcount > 0:
                    self.estado = nuevo_estado
                    exito = True
                else:
                    print("El libro ya no estaba disponible.")
                    exito = False
            except Exception as e:
                print(f"Error actualizar estado: {e}")
            finally:
                conn.close()
        return exito

    @staticmethod
    def obtener_reporte_detallado(fecha_ini, fecha_fin):
        """
        Trae TODOS los datos de los libros para el reporte detallado.
        """
        db = ConexionBD()
        conn = db.conectar()
        datos = []
        if conn:
            try:
                cursor = conn.cursor()
                
                sql = """
                    SELECT 
                        e.id_ejemplar,
                        o.titulo,
                        IFNULL(a.nombre_completo, 'Anónimo') as autor,
                        ed.nombre as editorial,
                        o.isbn,
                        o.anio_publicacion,
                        o.edicion,
                        o.paginas,
                        o.dimensiones,
                        e.ubicacion_fisica,
                        e.estado,
                        DATE_FORMAT(e.fecha_adquisicion, '%%Y-%%m-%%d') as fecha 
                    FROM ejemplares e
                    JOIN obras o ON e.id_obra = o.id_obra
                    LEFT JOIN editoriales ed ON o.id_editorial = ed.id_editorial
                    LEFT JOIN (
                        SELECT ao.id_obra, MIN(aut.nombre_completo) as nombre_completo
                        FROM autores_obras ao
                        JOIN autores aut ON ao.id_autor = aut.id_autor
                        GROUP BY ao.id_obra
                    ) a ON o.id_obra = a.id_obra
                    WHERE e.fecha_adquisicion BETWEEN %s AND %s
                    ORDER BY e.fecha_adquisicion DESC
                """
                
                f_ini = f"{fecha_ini}-01 00:00:00"
                f_fin = f"{fecha_fin}-31 23:59:59" 
                
                cursor.execute(sql, (f_ini, f_fin))
                datos = cursor.fetchall()
            except Exception as e:
                print(f"Error reporte detallado: {e}")
            finally:
                conn.close()
        return datos