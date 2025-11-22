from datetime import datetime

class Ejemplar:
    def __init__(self, codigo_barras, id_obra, numero_copia="Copia 1", ubicacion_fisica="General", estado="Disponible"):
        self.codigo_barras = codigo_barras # PK
        self.id_obra = id_obra             # FK
        self.numero_copia = numero_copia   # Nuevo campo (ej. "Copia 1")
        self.ubicacion_fisica = ubicacion_fisica # ej. "Pasillo 3"
        self.estado = estado
        self.fecha_adquisicion = datetime.now()

    def existe(self, cursor):
        sql = "SELECT codigo_barras FROM ejemplares WHERE codigo_barras = %s"
        cursor.execute(sql, (self.codigo_barras,))
        return cursor.fetchone() is not None

    def guardar(self, cursor):
        sql = """
            INSERT INTO ejemplares (codigo_barras, id_obra, numero_copia, ubicacion_fisica, estado, fecha_adquisicion) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            self.codigo_barras, 
            self.id_obra, 
            self.numero_copia, 
            self.ubicacion_fisica, 
            self.estado, 
            self.fecha_adquisicion
        )
        cursor.execute(sql, valores)