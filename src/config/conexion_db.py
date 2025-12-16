import pymysql
from pymysql import Error
import configparser
import os
import sys

class ConexionBD:
    def __init__(self):
        self.connection = None
        self.host = None
        self.user = None
        self.password = None
        self.database = None
        self.leer_configuracion()

    def leer_configuracion(self):
        config = configparser.ConfigParser()
        
        # LÓGICA HÍBRIDA ROBUSTA:
        # 1. Primero buscamos junto al ejecutable/script principal
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            # 2. Si estamos desarrollando, subimos niveles desde este archivo
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
        ruta_config = os.path.join(base_dir, 'config.ini')

        if os.path.exists(ruta_config):
            config.read(ruta_config)
            try:
                self.host = config['mysql']['host']
                self.user = config['mysql']['user']
                self.password = config['mysql']['password']
                self.database = config['mysql']['db']
            except KeyError:
                print("❌ Error: Faltan claves en config.ini")
                self._usar_default()
        else:
            print(f"⚠️ No se encontró {ruta_config}, usando valores por defecto.")
            self._usar_default()

    def _usar_default(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "biblioteca_normalizada"

    # --- ESTE ES EL MÉTODO QUE FALTABA ---
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

    # Soporte para 'with ConexionBD() as conn:'
    def __enter__(self):
        return self.conectar()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar()