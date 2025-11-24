from datetime import datetime

class Ejemplar:
    def __init__(self, id_obra, numero_copia="Copia 1", ubicacion_fisica="General", estado="Disponible", id_ejemplar=None):
        self.id_ejemplar = id_ejemplar # Este será el No. Adquisición (Auto)
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
        
        # Recuperamos el ID que la BD acaba de crear
        self.id_ejemplar = cursor.lastrowid
        return self.id_ejemplar