from conexionBD import conectar

class Autor:
    def __init__(self, id_autor, nombre, tipo_autor):
        self.id_autor = id_autor
        self.nombre = nombre
        self.tipo_autor = tipo_autor

    def guardar(self):
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO autores (Nombre, TipoAutor) VALUES (%s, %s)"
        cursor.execute(sql, (self.nombre, self.tipo_autor))
        conexion.commit()
        conexion.close()
        print(" Autor agregado correctamente.") #Los print son probicionales