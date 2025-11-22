import mysql.connector
from mysql.connector import Error

class ConexionBD:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "biblioteca_normalizada" # Aqui el nombre de la BD
        self.connection = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
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
        if self.connection and self.connection.is_connected():
            self.connection.close()