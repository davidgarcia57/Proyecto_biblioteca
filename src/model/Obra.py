class Obra:
    def __init__(self, titulo, id_editorial, isbn=None, idioma="Español", 
                 anio_publicacion=None, edicion=None, clasificacion=None, 
                 paginas=None, dimensiones=None, serie=None, 
                 descripcion=None, temas=None, id_obra=None):
        self.id_obra = id_obra
        self.titulo = titulo
        self.id_editorial = id_editorial # FK obligatoria
        self.isbn = isbn
        self.idioma = idioma
        self.anio_publicacion = anio_publicacion
        self.edicion = edicion
        self.clasificacion = clasificacion
        self.paginas = paginas
        self.dimensiones = dimensiones
        self.serie = serie
        self.descripcion = descripcion
        self.temas = temas

    def guardar(self, cursor):
        sql = """
            INSERT INTO obras (
                titulo, isbn, id_editorial, idioma, anio_publicacion, 
                edicion, clasificacion, paginas, dimensiones, serie, 
                descripcion, temas
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            self.titulo, self.isbn, self.id_editorial, self.idioma,
            self.anio_publicacion, self.edicion, self.clasificacion,
            self.paginas, self.dimensiones, self.serie, 
            self.descripcion, self.temas
        )
        cursor.execute(sql, valores)
        self.id_obra = cursor.lastrowid
        return self.id_obra

    def relacionar_autor(self, cursor, id_autor, rol="Autor Principal"):
        sql = "INSERT INTO autores_obras (id_obra, id_autor, rol) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.id_obra, id_autor, rol))