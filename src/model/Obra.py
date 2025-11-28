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

    # El método relacionar_autor se queda igual
    def relacionar_autor(self, cursor, id_autor, rol="Autor Principal"):
        sql = "INSERT INTO autores_obras (id_obra, id_autor, rol) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.id_obra, id_autor, rol))
    
    @staticmethod
    def buscar_por_termino(cursosr,termino):
        termino_like = f"%{termino}%"

        sql = """
            SELECT o.id_obra, o.titulo, o.isbn, o.anio_publicacion, a.nombre_completo, e.nombre
            FROM obras o
            LEFT JOIN autores_obras ao ON o.id_obra = ao.id_obra
            LEFT JOIN autores a ON ao.id_autor = a.id_autor
            LEFT JOIN editoriales e ON o.id_editorial = e.id_editorial
            WHERE o.titulo LIKE %s OR o.isbn LIKE %s OR a.nombre_completo LIKE %s
        """
        cursosr.execute(sql, (termino_like, termino_like, termino_like))
        return cursosr.fetchall()

    @staticmethod
    def buscar_disponibles(termino):
        """
        Busca ejemplares que estén DISPONIBLES para préstamo.
        Retorna una lista de tuplas: (id_ejemplar, titulo, autor)
        """
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