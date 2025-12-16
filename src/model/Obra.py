from src.config.conexion_db import ConexionBD

class Obra:
    def __init__(self, titulo, id_editorial, isbn=None, idioma="Español", 
                 anio_publicacion=None, edicion=None, clasificacion=None, 
                 paginas=None, dimensiones=None, serie=None, 
                 tomo=None, volumen=None, descripcion=None,
                 ficha_no=None, autor_corporativo=None, asientos_secundarios=None,
                 codigo_ilustracion=None,lugar_publicacion=None,
                 id_obra=None):
        
        self.id_obra = id_obra
        self.titulo = titulo
        self.id_editorial = id_editorial
        self.isbn = isbn
        self.idioma = idioma
        self.anio_publicacion = anio_publicacion
        self.edicion = edicion
        self.clasificacion = clasificacion
        self.paginas = paginas
        self.dimensiones = dimensiones
        self.serie = serie
        self.tomo = tomo
        self.volumen = volumen
        self.descripcion = descripcion
        self.ficha_no = ficha_no
        self.autor_corporativo = autor_corporativo
        self.asientos_secundarios = asientos_secundarios
        self.codigo_ilustracion = codigo_ilustracion
        self.lugar_publicacion = lugar_publicacion

    def guardar(self, cursor):
        sql = """
            INSERT INTO obras (
                titulo, isbn, id_editorial, idioma, anio_publicacion, 
                edicion, clasificacion, paginas, dimensiones, serie, 
                tomo, volumen, descripcion,
                ficha_no, autor_corporativo, asientos_secundarios,
                codigo_ilustracion, lugar_publicacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            self.titulo, self.isbn, self.id_editorial, self.idioma,
            self.anio_publicacion, self.edicion, self.clasificacion,
            self.paginas, self.dimensiones, self.serie, 
            self.tomo, self.volumen, self.descripcion,
            self.ficha_no, self.autor_corporativo, self.asientos_secundarios,
            self.codigo_ilustracion, self.lugar_publicacion
        )
        cursor.execute(sql, valores)
        self.id_obra = cursor.lastrowid
        return self.id_obra

    def relacionar_autor(self, cursor, id_autor, rol="Autor Principal"):
        sql = "INSERT INTO autores_obras (id_obra, id_autor, rol) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.id_obra, id_autor, rol))

    @staticmethod
    def buscar_por_termino(cursor, termino):
        termino_like = f"%{termino}%"
        
        sql = """
            SELECT 
                o.id_obra, 
                o.titulo, 
                o.isbn, 
                a.nombre_completo, 
                o.anio_publicacion, 
                e.nombre, 
                (SELECT COUNT(*) FROM ejemplares ej WHERE ej.id_obra = o.id_obra AND ej.estado = 'Disponible') as disponibles,
                (SELECT COUNT(*) FROM ejemplares ej WHERE ej.id_obra = o.id_obra AND ej.estado != 'Baja') as total
            FROM obras o
            LEFT JOIN autores_obras ao ON o.id_obra = ao.id_obra
            LEFT JOIN autores a ON ao.id_autor = a.id_autor
            LEFT JOIN editoriales e ON o.id_editorial = e.id_editorial
            WHERE (o.titulo LIKE %s OR o.isbn LIKE %s OR a.nombre_completo LIKE %s)
            
            -- AGREGAMOS ESTA CONDICIÓN PARA FILTRAR LOS DADOS DE BAJA:
            AND EXISTS (
                SELECT 1 FROM ejemplares ej_filtro 
                WHERE ej_filtro.id_obra = o.id_obra 
                AND ej_filtro.estado != 'Baja'
            )
            
            GROUP BY o.id_obra
        """
        
        cursor.execute(sql, (termino_like, termino_like, termino_like))
        return cursor.fetchall()

    @staticmethod
    def buscar_disponibles(termino):
        """
        Busca ejemplares que estén DISPONIBLES para préstamo.
        Retorna una lista de tuplas: (id_ejemplar, titulo, autor)
        """
        from src.config.conexion_db import ConexionBD # Import local para evitar ciclos
        db = ConexionBD()
        conn = db.conectar()
        resultados = []
        
        if conn:
            try:
                cursor = conn.cursor()
                sql = """
                    SELECT e.id_ejemplar, o.titulo, a.nombre_completo
                    FROM ejemplares e
                    JOIN obras o ON e.id_obra = o.id_obra
                    LEFT JOIN autores_obras ao ON o.id_obra = ao.id_obra
                    LEFT JOIN autores a ON ao.id_autor = a.id_autor
                    WHERE (o.titulo LIKE %s OR o.isbn LIKE %s)
                    AND e.estado = 'Disponible'
                    GROUP BY e.id_ejemplar
                """
                like = f"%{termino}%"
                cursor.execute(sql, (like, like))
                resultados = cursor.fetchall()
            except Exception as e:
                print(f"Error al buscar disponibles: {e}")
            finally:
                conn.close()
        
        return resultados

    @staticmethod
    def obtener_detalle_completo(id_obra):
        from src.config.conexion_db import ConexionBD
        db = ConexionBD()
        conn = db.conectar()
        detalle = {}
        
        if conn:
            try:
                cursor = conn.cursor()
                
                # --- AGREGAMOS: idioma, edicion, serie ---
                sql_obra = """
                    SELECT o.titulo, o.isbn, o.anio_publicacion, o.clasificacion, 
                           o.descripcion, o.paginas, o.dimensiones,
                           e.nombre as editorial, a.nombre_completo as autor,
                           o.idioma, o.edicion, o.serie
                    FROM obras o
                    LEFT JOIN editoriales e ON o.id_editorial = e.id_editorial
                    LEFT JOIN autores_obras ao ON o.id_obra = ao.id_obra
                    LEFT JOIN autores a ON ao.id_autor = a.id_autor
                    WHERE o.id_obra = %s
                """
                cursor.execute(sql_obra, (id_obra,))
                row = cursor.fetchone()
                
                if row:
                    detalle['obra'] = {
                        'id_obra': id_obra, # Importante para guardar después
                        'titulo': row[0], 
                        'isbn': row[1], 
                        'anio': row[2], 
                        'clasificacion': row[3], 
                        'descripcion': row[4], 
                        'paginas': row[5], 
                        'dimensiones': row[6],
                        'editorial': row[7], 
                        'autor': row[8],
                        # Nuevos campos mapeados por índice (orden del SELECT)
                        'idioma': row[9],
                        'edicion': row[10],
                        'serie': row[11]
                    }

                # (El resto de la función para 'ejemplares' sigue igual...)
                sql_ejemplares = "SELECT id_ejemplar, numero_copia, ubicacion_fisica, estado FROM ejemplares WHERE id_obra = %s"
                cursor.execute(sql_ejemplares, (id_obra,))
                detalle['ejemplares'] = [{'id': r[0], 'copia': r[1], 'ubicacion': r[2], 'estado': r[3]} for r in cursor.fetchall()]
                
            finally:
                conn.close()
        return detalle

    def actualizar(self, cursor):
        """Actualiza los datos básicos de la obra"""
        sql = """
            UPDATE obras SET 
                titulo=%s, isbn=%s, anio_publicacion=%s, clasificacion=%s,
                paginas=%s, dimensiones=%s, descripcion=%s,
                edicion=%s, idioma=%s, serie=%s
            WHERE id_obra=%s
        """
        vals = (
            self.titulo, self.isbn, self.anio_publicacion, self.clasificacion,
            self.paginas, self.dimensiones, self.descripcion,
            self.edicion, self.idioma, self.serie, 
            self.id_obra
        )
        cursor.execute(sql, vals)
        return True