from src.config.conexion_db import ConexionBD
from src.view.inventario.frm_buscar_libro import FrmBuscarLibro
from src.model.Obra import Obra

class BusquedaController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close

        #Instanciamos la vista y le pasamos 'self' (Que es este controlador)
        self.view = FrmBuscarLibro(view_container, self)

        self.db = ConexionBD()

    def realizar_busqueda(self, termino):
        if not termino:
            return
        
        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                #Llamamos al método estático
                resultados = Obra.buscar_por_termino(cursor, termino)

                #Enviamos los datos a la vistaa para que los pinte
                self.view.mostrar_resultados(resultados)

            except Exception as e:
                print(f"Error en búsqueda: {e}")
            finally:
                conn.close()

    def volver_al_menu(self):
        if self.on_close:
            self.on_close()
