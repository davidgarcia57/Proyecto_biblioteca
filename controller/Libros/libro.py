from conexionBD import conectar

class Libro:
    def __init__(self, id_libro, titulo, id_autor, id_editorial, fecha_publicacion, isbn):
        self.id_libro = id_libro
        self.titulo = titulo
        self.id_autor = id_autor
        self.id_editorial = id_editorial
        self.fecha_publicacion = fecha_publicacion
        self.isbn = isbn

    def guardar(self):
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO libros (Titulo, IdAutor, IdEditorial, FechaPublicacion, ISBN) VALUES (%s, %s, %s, %s, %s)"
        valores = (self.titulo, self.id_autor, self.id_editorial, self.fecha_publicacion, self.isbn)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        print(" Libro guardado correctamente.") #Los print son provicionales
