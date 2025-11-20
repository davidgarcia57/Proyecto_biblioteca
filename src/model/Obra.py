class Obra:
    def __init__(self, titulo, id_editorial=None, codigo_idioma=None, isbn=None, 
                 clasificacion_lc=None, edicion=None, fecha_publicacion=None, 
                 paginas=None, dimensiones=None, serie=None, codigo_ilustracion=None, 
                 notas_generales=None, nota_historial_bib=None, encabezado_temas=None, 
                 id_obra=None):
        
        self.id_obra = id_obra
        
        # Relaciones o las FK
        self.id_editorial = id_editorial
        self.codigo_idioma = codigo_idioma
        
        # Datos
        self.titulo = titulo
        self.isbn = isbn
        self.clasificacion_lc = clasificacion_lc
        self.edicion = edicion
        self.fecha_publicacion = fecha_publicacion
        self.paginas = paginas
        self.dimensiones = dimensiones
        self.serie = serie
        
        # Otros lo divido más que nada por que tienen su apartado no por otra cosa
        self.codigo_ilustracion = codigo_ilustracion
        self.notas_generales = notas_generales
        self.nota_historial_bib = nota_historial_bib
        self.encabezado_temas = encabezado_temas

    def __str__(self):
        return f"{self.titulo} (ID: {self.id_obra})"