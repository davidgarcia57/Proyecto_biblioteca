import pymysql
from pymysql import Error

class ConexionBD:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "biblioteca_normalizada"
        self.connection = None

    def conectar(self):
        try:
            # Usamos PyMySQL para conectar
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Error al conectar a la BD: {e}")
            return None
        
    def cerrar(self):
        # PyMySQL usa .open en lugar de .is_connected()
        if self.connection and self.connection.open:
            self.connection.close()