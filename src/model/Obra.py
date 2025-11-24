class Obra:
    def __init__(self, titulo, id_editorial, isbn=None, idioma="Español", 
                 anio_publicacion=None, edicion=None, clasificacion=None, 
                 paginas=None, dimensiones=None, serie=None, 
                 tomo=None, volumen=None, descripcion=None, temas=None,
                 ficha_no=None, autor_corporativo=None, asientos_secundarios=None,
                 codigo_ilustracion=None, analizo=None, reviso=None, lugar_publicacion=None,
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
        self.temas = temas
        self.ficha_no = ficha_no
        self.autor_corporativo = autor_corporativo
        self.asientos_secundarios = asientos_secundarios
        self.codigo_ilustracion = codigo_ilustracion
        self.analizo = analizo
        self.reviso = reviso
        self.lugar_publicacion = lugar_publicacion

    def guardar(self, cursor):
        sql = """
            INSERT INTO obras (
                titulo, isbn, id_editorial, idioma, anio_publicacion, 
                edicion, clasificacion, paginas, dimensiones, serie, 
                tomo, volumen, descripcion, temas,
                ficha_no, autor_corporativo, asientos_secundarios,
                codigo_ilustracion, analizo, reviso, lugar_publicacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            self.titulo, self.isbn, self.id_editorial, self.idioma,
            self.anio_publicacion, self.edicion, self.clasificacion,
            self.paginas, self.dimensiones, self.serie, 
            self.tomo, self.volumen, self.descripcion, self.temas,
            self.ficha_no, self.autor_corporativo, self.asientos_secundarios,
            self.codigo_ilustracion, self.analizo, self.reviso, self.lugar_publicacion
        )
        cursor.execute(sql, valores)
        self.id_obra = cursor.lastrowid
        return self.id_obra

    # El método relacionar_autor se queda igual
    def relacionar_autor(self, cursor, id_autor, rol="Autor Principal"):
        sql = "INSERT INTO autores_obras (id_obra, id_autor, rol) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.id_obra, id_autor, rol))