class Editorial:
    def __init__(self, nombre_editorial, lugar_publicacion=None, id_editorial=None):
        self.id_editorial = id_editorial
        self.nombre_editorial = nombre_editorial
        self.lugar_publicacion = lugar_publicacion

    def __str__(self):
        return self.nombre_editorial