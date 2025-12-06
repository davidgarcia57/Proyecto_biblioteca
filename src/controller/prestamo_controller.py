from src.config.conexion_db import ConexionBD
from src.view.circulacion.frm_busqueda import FrmBusqueda
from src.view.circulacion.frm_prestamo import FrmPrestamos
from src.model.Prestamo import Prestamo
from src.model.Obra import Obra 
from src.model.Ejemplar import Ejemplar 
from src.model.Solicitantes import Solicitante 
from datetime import datetime, timedelta
from tkinter import messagebox

class PrestamoController:
    def __init__(self, view_container, usuario_sistema, on_close=None):
        self.view_container = view_container
        self.usuario_sistema = usuario_sistema 
        self.on_close = on_close
        
        # NOTA: Por defecto cargamos la vista de Crear Préstamo.
        # Si el Router nos llama para "Lista de Préstamos", él reemplaza la vista manualmente.
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
                conn.start_transaction()
                
                # Validar límite de préstamos
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM prestamos WHERE id_prestatario = %s AND estado = 'Activo'", (id_solicitante,))
                if cursor.fetchone()[0] >= 3:
                    self.view.mostrar_mensaje("El lector ya tiene 3 préstamos activos.", True)
                    conn.rollback()
                    return

                nuevo_prestamo = Prestamo(
                    id_prestatario=id_solicitante,
                    id_usuario_sistema=self.usuario_sistema.id_usuario,
                    id_ejemplar=id_ejemplar,
                    fecha_devolucion_esperada=fecha_dev
                )
                
                id_generado = nuevo_prestamo.guardar(conn)
                conn.commit() 
                
                self.view.mostrar_mensaje(f"Préstamo #{id_generado} registrado con éxito.")
                self.view.txt_id_libro.delete(0, 'end')
                self.view.lbl_info_libro.configure(text="[Esperando libro...]", text_color="gray")
                
            except Exception as e:
                conn.rollback()
                self.view.mostrar_mensaje(f"Error al prestar: {e}", True)
            finally:
                conn.close()

    # --- NUEVO: Procesar Devolución ---
    def procesar_devolucion(self, id_prestamo, id_ejemplar):
        conn = self.db.conectar()
        if conn:
            try:
                conn.start_transaction()
                
                # Llamamos al método estático del modelo pasando la conexión
                Prestamo.finalizar_prestamo(conn, id_prestamo, id_ejemplar)
                
                conn.commit()
                messagebox.showinfo("Éxito", "Libro devuelto correctamente.\nAhora está Disponible.")
                
                # Refrescamos la tabla
                self.view.cargar_datos()
                
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo procesar la devolución: {e}")
            finally:
                conn.close()

    # --- LÓGICA DE BÚSQUEDA DE LIBROS ---
    def abrir_busqueda_libros(self):
        def al_seleccionar(id_sel):
            self.view.txt_id_libro.delete(0, 'end')
            self.view.txt_id_libro.insert(0, str(id_sel))
            self.verificar_libro(id_sel) 

        self.popup = FrmBusqueda(self.view, al_seleccionar, tipo="libro")
        
        def buscar_bd(event=None):
            termino = self.popup.entry_busqueda.get()
            datos = Obra.buscar_disponibles(termino)
            self.popup.cargar_datos(datos)

        self.popup.ejecutar_busqueda_evento = buscar_bd
        self.popup.entry_busqueda.bind("<Return>", buscar_bd)
        
        for widget in self.popup.winfo_children(): 
            for child in widget.winfo_children():
                if isinstance(child, type(self.popup.entry_busqueda.master.winfo_children()[1])): 
                     child.configure(command=buscar_bd)

    # --- LÓGICA DE BÚSQUEDA DE LECTORES ---
    def abrir_busqueda_lectores(self):
        def al_seleccionar(id_sel):
            self.view.txt_id_usuario.delete(0, 'end')
            self.view.txt_id_usuario.insert(0, str(id_sel))
            self.verificar_solicitante(id_sel)

        self.popup_lec = FrmBusqueda(self.view, al_seleccionar, tipo="lector")
        
        def buscar_bd(event=None):
            termino = self.popup_lec.entry_busqueda.get()
            datos = Solicitante.buscar_por_termino(termino)
            self.popup_lec.cargar_datos(datos)

        self.popup_lec.ejecutar_busqueda_evento = buscar_bd
        self.popup_lec.entry_busqueda.bind("<Return>", buscar_bd)
        
        for widget in self.popup_lec.winfo_children(): 
            for child in widget.winfo_children():
                if isinstance(child, type(self.popup_lec.entry_busqueda.master.winfo_children()[1])): 
                     child.configure(command=buscar_bd)