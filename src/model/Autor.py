class Autor:
    def __init__(self, nombre_completo, tipo='Persona', id_autor=None):
        self.id_autor = id_autor
        self.nombre_completo = nombre_completo
        self.tipo = tipo

    def guardar(self, cursor):
        """Busca si existe o inserta un nuevo autor."""
        sql_buscar = "SELECT id_autor FROM autores WHERE nombre_completo = %s"
        cursor.execute(sql_buscar, (self.nombre_completo,))
        resultado = cursor.fetchone()

        if resultado:
            self.id_autor = resultado[0]
        else:
            sql_insertar = "INSERT INTO autores (nombre_completo, tipo) VALUES (%s, %s)"
            cursor.execute(sql_insertar, (self.nombre_completo, self.tipo))
            self.id_autor = cursor.lastrowid
        
        return self.id_autor