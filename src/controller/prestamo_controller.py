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
        
        # Variables para almacenar los ID
        self.id_libro_seleccionado = None
        self.id_lector_seleccionado = None
        
        # Cargamos la nueva vista
        self.view = FrmPrestamos(view_container, self)

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    # Lista prestamos
    
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
                conn.begin()
                Prestamo.finalizar_prestamo(conn, id_prestamo, id_ejemplar)
                conn.commit()
                messagebox.showinfo("Éxito", "Libro devuelto correctamente.")
                self.cargar_lista_activos() 
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error en devolución: {e}")
            finally:
                conn.close()

    # Prestamo vista

    def abrir_busqueda_libros(self):
        def al_seleccionar(id_sel):
            self.id_libro_seleccionado = id_sel
            
            # Consultamos datos para mostrar título en el Label
            info = Ejemplar.obtener_info(id_sel)
            if info:
                titulo = info['titulo']
                estado = info['estado']
                
                # Advertencia si no está disponible
                if estado != 'Disponible':
                    self.view.actualizar_libro(f"⚠️ {titulo} ({estado})")
                    self.id_libro_seleccionado = None # Invalidamos selección
                    messagebox.showwarning("No disponible", f"El libro seleccionado está {estado}.")
                else:
                    self.view.actualizar_libro(titulo)
            else:
                self.view.actualizar_libro("ID Desconocido")

        self.popup = FrmBusqueda(self.view, al_seleccionar, tipo="libro")
        self.popup.configurar_busqueda(self.buscar_libros_bd)

    def buscar_libros_bd(self, termino):
        datos = Obra.buscar_disponibles(termino)
        self.popup.cargar_datos(datos)

    def abrir_busqueda_lectores(self):
        def al_seleccionar(id_sel):
            self.id_lector_seleccionado = id_sel
            nombre = Solicitante.obtener_nombre(id_sel)
            if nombre:
                self.view.actualizar_usuario(nombre)
            else:
                self.view.actualizar_usuario("Desconocido")

        self.popup_lec = FrmBusqueda(self.view, al_seleccionar, tipo="lector")
        self.popup_lec.configurar_busqueda(self.buscar_lectores_bd)

    def buscar_lectores_bd(self, termino):
        datos = Solicitante.buscar_por_termino(termino)
        self.popup_lec.cargar_datos(datos)

    def realizar_prestamo(self):
        # Validaciones usando las variables internas
        if not self.id_libro_seleccionado:
            messagebox.showwarning("Faltan datos", "Por favor, seleccione un libro.")
            return
        if not self.id_lector_seleccionado:
            messagebox.showwarning("Faltan datos", "Por favor, seleccione un lector.")
            return

        dias = 7 # Plazo de 7 dias
        fecha_dev = datetime.now() + timedelta(days=dias)

        conn = self.db.conectar()
        if conn:
            try:
                conn.begin()
                cursor = conn.cursor()
                
                # 1. Verificar límite de 3 libros
                cursor.execute("SELECT COUNT(*) FROM prestamos WHERE id_prestatario = %s AND estado = 'Activo'", (self.id_lector_seleccionado,))
                count = cursor.fetchone()[0]
                if count >= 3:
                    messagebox.showwarning("Límite excedido", "El lector ya tiene 3 préstamos activos.\nDebe devolver uno antes de solicitar otro.")
                    conn.rollback()
                    return

                # 2. Registrar
                nuevo = Prestamo(self.id_lector_seleccionado, self.usuario_sistema.id_usuario, self.id_libro_seleccionado, fecha_dev)
                id_gen = nuevo.guardar(conn)
                
                conn.commit() 
                messagebox.showinfo("Éxito", f"Préstamo #{id_gen} registrado exitosamente.")
                
                # 3. Limpiar Interfaz
                self.id_libro_seleccionado = None
                self.id_lector_seleccionado = None
                self.view.actualizar_libro("Ningún libro seleccionado")
                self.view.actualizar_usuario("Ningún lector seleccionado")
                
            except Exception as e:
                conn.rollback()
                print(e)
                messagebox.showerror("Error", f"Error al prestar: {e}")
            finally:
                conn.close()