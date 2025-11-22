from datetime import datetime

class Ejemplar:
    def __init__(self, codigo_barras, id_obra, estado="Disponible", ubicacion_fisica=None):
        self.codigo_barras = codigo_barras #PK
        self.id_obra = id_obra             #FK
        self.estado = estado
        self.ubicacion_fisica = ubicacion_fisica
        self.fecha_adquisicion = datetime.now()

    def existe(self, cursor):
        sql = "SELECT codigo_barras FROM ejemplares WHERE codigo_barras = %s"
        cursor.execute(sql, (self.codigo_barras,))
        return cursor.fetchone() is not None

    def guardar(self, cursor):
        sql = """
            INSERT INTO ejemplares (codigo_barras, id_obra, estado, ubicacion_fisica, fecha_adquisicion) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (self.codigo_barras, self.id_obra, self.estado, self.ubicacion_fisica, self.fecha_adquisicion)
        cursor.execute(sql, valores)