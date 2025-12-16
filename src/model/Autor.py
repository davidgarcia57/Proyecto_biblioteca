class Autor:
    def __init__(self, nombre_completo, tipo='Persona', id_autor=None):
        self.id_autor = id_autor
        self.nombre_completo = nombre_completo
        self.tipo = tipo

    def guardar(self, cursor):
        """Busca si existe o inserta un nuevo autor."""
        # 1. Verificamos si ya existe
        sql_buscar = "SELECT id_autor FROM autores WHERE nombre_completo = %s"
        cursor.execute(sql_buscar, (self.nombre_completo,))
        resultado = cursor.fetchone()

        if resultado:
            # Si existe, tomamos su ID y no duplicamos
            self.id_autor = resultado[0]
        else:
            # Si no existe, lo insertamos
            sql_insertar = "INSERT INTO autores (nombre_completo, tipo) VALUES (%s, %s)"
            cursor.execute(sql_insertar, (self.nombre_completo, self.tipo))
            self.id_autor = cursor.lastrowid
        
        return self.id_autor
    
    @staticmethod
    def obtener_id_por_nombre(cursor, nombre):
        sql = "SELECT id_autor FROM autores WHERE nombre_completo = %s"
        cursor.execute(sql, (nombre,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None