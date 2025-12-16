class Editorial:
    def __init__(self, nombre, ciudad=None, id_editorial=None):
        self.id_editorial = id_editorial
        self.nombre = nombre
        self.ciudad = ciudad

    def guardar(self, cursor):
        # 1. Buscar si existe
        sql_buscar = "SELECT id_editorial FROM editoriales WHERE nombre = %s"
        cursor.execute(sql_buscar, (self.nombre,))
        resultado = cursor.fetchone()

        if resultado:
            self.id_editorial = resultado[0]
        else:
            # 2. Si no existe, insertar
            sql_insertar = "INSERT INTO editoriales (nombre, ciudad) VALUES (%s, %s)"
            cursor.execute(sql_insertar, (self.nombre, self.ciudad))
            self.id_editorial = cursor.lastrowid
        
        return self.id_editorial
    
    @staticmethod
    def obtener_id_por_nombre(cursor, nombre):
        sql = "SELECT id_editorial FROM editoriales WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None