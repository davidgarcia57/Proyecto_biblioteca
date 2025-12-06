from src.config.conexion_db import ConexionBD
from src.view.inventario.frm_buscar_libro import FrmBuscarLibro
from src.view.inventario.popup_ficha import PopupFicha
from src.model.Obra import Obra
from src.model.Ejemplar import Ejemplar
from tkinter import messagebox

class BusquedaController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close

        # Instanciamos la vista y le pasamos 'self'
        self.view = FrmBuscarLibro(view_container, self)
        self.db = ConexionBD()
        
        # Carga inicial
        self.realizar_busqueda("")

    def realizar_busqueda(self, termino):
        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                resultados = Obra.buscar_por_termino(cursor, termino)
                self.view.mostrar_resultados(resultados)
            except Exception as e:
                print(f"Error en búsqueda: {e}")
            finally:
                conn.close()

    def volver_al_menu(self):
        if self.on_close:
            self.on_close()

    # =========================================================================
    #  NUEVA LÓGICA: FICHA TÉCNICA Y GESTIÓN
    # =========================================================================
    def abrir_ficha_libro(self, id_obra):
        # 1. Obtener datos
        data = Obra.obtener_detalle_completo(id_obra)
        if not data: return

        # --- FUNCIÓN 1: GUARDAR EDICIÓN ---
        def guardar_cambios_obra(datos_nuevos):
            conn = self.db.conectar()
            if conn:
                try:
                    cursor = conn.cursor()
                    # Creamos un objeto Obra temporal para usar su método guardar/actualizar
                    # O usamos un método estático si preferimos. 
                    # Aquí instanciamos para facilitar el pase de argumentos
                    obra_tmp = Obra(
                        id_obra=datos_nuevos['id_obra'],
                        titulo=datos_nuevos['titulo'],
                        id_editorial=None, # No editamos esto por ahora
                        isbn=datos_nuevos['isbn'],
                        idioma=datos_nuevos['idioma'],
                        anio_publicacion=datos_nuevos['anio'],
                        edicion=datos_nuevos['edicion'],
                        clasificacion=datos_nuevos['clasificacion'],
                        paginas=datos_nuevos['paginas'],
                        dimensiones=datos_nuevos['dimensiones'],
                        descripcion=datos_nuevos['descripcion']
                        # Los demás campos se mantienen o ignoran en la query de update simple
                    )
                    
                    if obra_tmp.actualizar(cursor):
                        conn.commit()
                        messagebox.showinfo("Éxito", "Ficha del libro actualizada correctamente.")
                        # Refrescamos la vista principal
                        self.realizar_busqueda(self.view.txt_busqueda.get())
                    else:
                        messagebox.showerror("Error", "No se pudieron guardar los cambios.")
                        
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Error Crítico", f"Fallo al actualizar: {e}")
                finally:
                    conn.close()

        # --- FUNCIÓN 2: VALIDACIÓN ROBUSTA DE BAJA ---
        def callback_baja(id_ejemplar, estado_actual, etiqueta_copia):
            # 1. Validación de Estado
            if estado_actual == 'Prestado':
                messagebox.showerror("Acción Denegada", f"La {etiqueta_copia} está PRESTADA.\nDebe realizar la devolución antes de darla de baja.")
                return
            
            if estado_actual == 'Baja':
                messagebox.showinfo("Información", "Este ejemplar ya se encuentra dado de baja.")
                return

            # 2. Confirmación de Seguridad
            confirmacion = messagebox.askyesno(
                "Confirmación de Baja", 
                f"¿Está SEGURO de dar de baja el ejemplar ID {id_ejemplar}?\n\n"
                f"Detalle: {etiqueta_copia}\n"
                "Esta acción lo eliminará del inventario activo."
            )
            
            if confirmacion:
                exito, msg = Ejemplar.dar_de_baja(id_ejemplar)
                if exito:
                    messagebox.showinfo("Baja Exitosa", f"El ejemplar ha sido procesado.\nEstado: {msg}")
                    self.popup.destroy()
                    self.abrir_ficha_libro(id_obra) # Recargar ficha
                    self.realizar_busqueda(self.view.txt_busqueda.get()) # Recargar tabla principal
                else:
                    messagebox.showerror("Error", msg)

        # Abrir Popup pasando ambas funciones
        self.popup = PopupFicha(self.view, data, callback_baja, guardar_cambios_obra)