from src.config.conexion_db import ConexionBD
from src.view.circulacion.frm_busqueda import FrmBusqueda
from src.view.circulacion.frm_prestamo import FrmPrestamos
from src.view.circulacion.frm_lista_prestamos import FrmListaPrestamos
from src.model.Prestamo import Prestamo
from src.model.Ejemplar import Ejemplar 
from src.model.Solicitantes import Solicitante 
from src.model.Obra import Obra
from datetime import datetime, timedelta
from tkinter import messagebox

class PrestamoController:
    def __init__(self, view_container, usuario_sistema, on_close=None):
        self.view_container = view_container
        self.usuario_sistema = usuario_sistema 
        self.on_close = on_close
        self.db = ConexionBD()
        
        self.view = FrmPrestamos(view_container, self)

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    # =========================================================================
    # LÓGICA DE LA LISTA DE PRÉSTAMOS
    # =========================================================================
    
    def iniciar_lista_prestamos(self):
        for widget in self.view_container.winfo_children():
            widget.destroy()
            
        self.view = FrmListaPrestamos(self.view_container, self)
        self.view.pack(fill="both", expand=True)
        
        self.cargar_lista_activos()

    def cargar_lista_activos(self):
        datos = Prestamo.obtener_activos()
        self.view.actualizar_tabla(datos)

    def procesar_devolucion(self, id_prestamo, id_ejemplar):
        conn = self.db.conectar()
        if conn:
            try:
                # --- CORRECCIÓN AQUÍ ---
                conn.begin() # En PyMySQL se usa begin(), no start_transaction()
                
                Prestamo.finalizar_prestamo(conn, id_prestamo, id_ejemplar)
                
                conn.commit()
                messagebox.showinfo("Éxito", "Libro devuelto correctamente.")
                self.cargar_lista_activos() 
                
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error en devolución: {e}")
            finally:
                conn.close()

    # =========================================================================
    # LÓGICA DE NUEVO PRÉSTAMO
    # =========================================================================

    def verificar_libro(self, id_ejemplar):
        res = Ejemplar.verificar_estado(id_ejemplar)
        if res:
            titulo, estado = res
            is_ok = (estado == 'Disponible')
            msg = f"✔ {titulo}" if is_ok else f"⚠ {titulo} ({estado})"
            
            if hasattr(self.view, 'actualizar_info_libro'):
                self.view.actualizar_info_libro(msg, is_ok)
            return is_ok
        else:
            if hasattr(self.view, 'actualizar_info_libro'):
                self.view.actualizar_info_libro("❌ ID no encontrado", False)
            return False

    def verificar_solicitante(self, id_solicitante):
        nombre = Solicitante.obtener_nombre(id_solicitante)
        if nombre:
            if hasattr(self.view, 'actualizar_info_usuario'):
                self.view.actualizar_info_usuario(f"✔ {nombre}", True)
            return True
        else:
            if hasattr(self.view, 'actualizar_info_usuario'):
                self.view.actualizar_info_usuario("❌ Usuario no encontrado", False)
            return False

    def registrar_prestamo(self, id_ejemplar, id_solicitante, dias):
        if not id_ejemplar or not id_solicitante:
            messagebox.showwarning("Faltan datos", "Ingrese ID de Libro y Solicitante")
            return

        dias = int(dias)
        fecha_dev = datetime.now() + timedelta(days=dias)

        conn = self.db.conectar()
        if conn:
            try:
                # --- CORRECCIÓN AQUÍ ---
                conn.begin() # Cambiado de start_transaction() a begin()
                
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM prestamos WHERE id_prestatario = %s AND estado = 'Activo'", (id_solicitante,))
                if cursor.fetchone()[0] >= 3:
                    messagebox.showwarning("Límite excedido", "El lector ya tiene 3 préstamos activos.")
                    conn.rollback()
                    return

                nuevo = Prestamo(id_solicitante, self.usuario_sistema.id_usuario, id_ejemplar, fecha_dev)
                id_gen = nuevo.guardar(conn)
                
                conn.commit() 
                
                messagebox.showinfo("Éxito", f"Préstamo #{id_gen} registrado.")
                
                if hasattr(self.view, 'limpiar_form'):
                    self.view.limpiar_form() 
                
            except Exception as e:
                conn.rollback()
                print(e) # Imprimimos en consola para ver detalle si falla
                messagebox.showerror("Error", f"Error al prestar: {e}")
            finally:
                conn.close()

    # =========================================================================
    # POPUPS
    # =========================================================================

    def abrir_busqueda_libros(self):
        def al_seleccionar(id_sel):
            self.view.txt_id_libro.delete(0, 'end')
            self.view.txt_id_libro.insert(0, str(id_sel))
            self.verificar_libro(id_sel)

        self.popup = FrmBusqueda(self.view, al_seleccionar, tipo="libro")
        self.popup.configurar_busqueda(self.buscar_libros_bd)

    def buscar_libros_bd(self, termino):
        datos = Obra.buscar_disponibles(termino)
        self.popup.cargar_datos(datos)

    def abrir_busqueda_lectores(self):
        def al_seleccionar(id_sel):
            self.view.txt_id_usuario.delete(0, 'end')
            self.view.txt_id_usuario.insert(0, str(id_sel))
            self.verificar_solicitante(id_sel)

        self.popup_lec = FrmBusqueda(self.view, al_seleccionar, tipo="lector")
        self.popup_lec.configurar_busqueda(self.buscar_lectores_bd)

    def buscar_lectores_bd(self, termino):
        datos = Solicitante.buscar_por_termino(termino)
        self.popup_lec.cargar_datos(datos)