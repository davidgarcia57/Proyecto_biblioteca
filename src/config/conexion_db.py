import pymysql
from pymysql import Error
import configparser
import os

class ConexionBD:
    def __init__(self):
        self.connection = None
        self.leer_configuracion()

    def leer_configuracion(self):

        config = configparser.ConfigParser()
        
        # --- TRUCO DE LAS RUTAS ---
        # Este archivo está en: src/config/conexion_db.py
        # Queremos llegar a:    config.ini (que está en la raíz)
        # Tenemos que subir 3 niveles: conexion_db.py -> config -> src -> RAIZ
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ruta_config = os.path.join(base_dir, 'config.ini')

        # Leemos el archivo
        config.read(ruta_config)

        try:
            # Sacamos los datos de la sección [mysql] del archivo .ini
            self.host = config['mysql']['host']
            self.user = config['mysql']['user']
            self.password = config['mysql']['password']
            self.database = config['mysql']['db']
        except KeyError:
            print("❌ ERROR: No se encontró el archivo config.ini o faltan datos.")
            # Valores por defecto de emergencia
            self.host = "localhost"
            self.user = "root"
            self.password = ""
            self.database = "biblioteca_normalizada"

    def conectar(self):
        try:
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
        if self.connection and self.connection.open:
            self.connection.close()