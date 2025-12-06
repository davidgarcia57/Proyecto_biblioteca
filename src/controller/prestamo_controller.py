from src.config.conexion_db import ConexionBD
from src.view.circulacion.popup_busqueda import PopupBusqueda
from src.view.circulacion.frm_prestamo import FrmPrestamos
from src.model.Prestamo import Prestamo
from src.model.Obra import Obra 
from src.model.Ejemplar import Ejemplar
from src.model.Solicitantes import Solicitante
from datetime import datetime, timedelta

class PrestamoController:
    def __init__(self, view_container, usuario_sistema, on_close=None):
        self.view_container = view_container
        self.usuario_sistema = usuario_sistema 
        self.on_close = on_close
        
        self.view = FrmPrestamos(view_container, self)
        self.db = ConexionBD()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def verificar_libro(self, id_ejemplar):
        res = Ejemplar.verificar_estado(id_ejemplar)
        
        if res:
            titulo, estado = res
            if estado == 'Disponible':
                self.view.actualizar_info_libro(f"✔ {titulo} (Disponible)", True)
                return True
            else:
                self.view.actualizar_info_libro(f"⚠ {titulo} ({estado})", False)
                return False
        else:
            self.view.actualizar_info_libro("❌ ID no encontrado", False)
            return False

    def verificar_solicitante(self, id_solicitante):
        # MVC CORRECTO: Delegamos la consulta al Modelo
        nombre = Solicitante.obtener_nombre(id_solicitante)

        if nombre:
            self.view.actualizar_info_usuario(f"✔ {nombre}", True)
            return True
        else:
            self.view.actualizar_info_usuario("❌ Usuario no encontrado", False)
            return False

    def registrar_prestamo(self, id_ejemplar, id_solicitante, dias):
        if not id_ejemplar or not id_solicitante:
            self.view.mostrar_mensaje("Ingrese ID de Libro y Solicitante", True)
            return

        # Calcular fechas
        dias = int(dias)
        fecha_dev = datetime.now() + timedelta(days=dias)

        conn = self.db.conectar()
        if conn:
            try:
                # IMPORTANTE: Iniciar Transacción
                conn.start_transaction()
                
                # Crear objeto préstamo
                nuevo_prestamo = Prestamo(
                    id_prestatario=id_solicitante,
                    id_usuario_sistema=self.usuario_sistema.id_usuario,
                    id_ejemplar=id_ejemplar,
                    fecha_devolucion_esperada=fecha_dev
                )
                
                # El modelo se encarga del INSERT
                id_generado = nuevo_prestamo.guardar(conn)
                
                conn.commit() # Confirmar cambios
                self.view.mostrar_mensaje(f"Préstamo #{id_generado} registrado con éxito.")
                
                # Limpiar campos
                self.view.txt_id_libro.delete(0, 'end')
                self.view.lbl_info_libro.configure(text="[Esperando libro...]", text_color="gray")
                
            except Exception as e:
                conn.rollback() # Deshacer si hay error
                self.view.mostrar_mensaje(f"Error al prestar: {e}", True)
            finally:
                conn.close()

    def abrir_popup_libros(self):
        """
        Abre el popup de búsqueda y maneja la selección del libro.
        Respeta MVC delegando la búsqueda al Modelo (Obra).
        """
        def al_seleccionar_libro(id_ejemplar):
            self.view.txt_id_libro.delete(0, 'end')
            self.view.txt_id_libro.insert(0, str(id_ejemplar))
            self.verificar_libro(id_ejemplar) 

        popup = PopupBusqueda(self.view, al_seleccionar_libro, tipo="libro")
        
        def ejecutar_busqueda(event=None):
            termino = popup.entry_busqueda.get()
            resultados = Obra.buscar_disponibles(termino)
            popup.cargar_datos(resultados)

        popup.entry_busqueda.bind("<Return>", ejecutar_busqueda)
        
        if hasattr(popup, 'btn_buscar'):
             popup.btn_buscar.configure(command=ejecutar_busqueda)

    def mostrar_lista_activos(self):
        for widget in self.view_container.winfo_children():
            widget.destroy()
            
        from src.view.circulacion.frm_lista_prestamos import FrmListaPrestamos
        self.view = FrmListaPrestamos(self.view_container, self)
        self.view.pack(fill="both", expand=True)