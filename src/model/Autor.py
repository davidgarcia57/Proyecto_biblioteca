class Autor:
    def __init__(self, nombre_completo, tipo_autor='Personal', id_autor=None):
        self.id_autor = id_autor
        self.nombre_completo = nombre_completo
        self.tipo_autor = tipo_autor

    def __str__(self):
        return self.nombre_completo