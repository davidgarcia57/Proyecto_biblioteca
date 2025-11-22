class AutorObra:
    def __init__(self, id_obra, id_autor, rol='Autor Principal'):
        self.id_obra = id_obra
        self.id_autor = id_autor
        self.rol = rol # 'Autor Principal', 'Coautor', 'Traductor', etc.

    def __str__(self):
        return f"Obra {self.id_obra} - Autor {self.id_autor} ({self.rol})"