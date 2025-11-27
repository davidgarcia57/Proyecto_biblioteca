from src.config.conexion_db import ConexionBD
from src.view.circulacion.popup_busqueda import PopupBusqueda
from src.view.circulacion.frm_prestamo import FrmPrestamos
from src.model.Prestamo import Prestamo
from datetime import datetime, timedelta

class PrestamoController:
    def __init__(self, view_container, usuario_sistema, on_close=None):
        self.view_container = view_container
        self.usuario_sistema = usuario_sistema # El bibliotecario logueado
        self.on_close = on_close
        
        self.view = FrmPrestamos(view_container, self)
        self.db = ConexionBD()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def verificar_libro(self, id_ejemplar):
        conn = self.db.conectar()
        if conn:
            cursor = conn.cursor()
            # Buscamos título y estado uniendo tablas
            sql = """
                SELECT o.titulo, e.estado 
                FROM ejemplares e 
                JOIN obras o ON e.id_obra = o.id_obra 
                WHERE e.id_ejemplar = %s
            """
            cursor.execute(sql, (id_ejemplar,))
            res = cursor.fetchone()
            conn.close()

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
        conn = self.db.conectar()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT nombre_completo FROM solicitantes WHERE id_prestatario = %s"
            cursor.execute(sql, (id_solicitante,))
            res = cursor.fetchone()
            conn.close()

            if res:
                self.view.actualizar_info_usuario(f"✔ {res[0]}", True)
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
        # Función que se ejecuta al seleccionar un libro en el popup
        def al_seleccionar_libro(id_ejemplar):
            self.view.txt_id_libro.delete(0, 'end')
            self.view.txt_id_libro.insert(0, id_ejemplar)
            self.verificar_libro(id_ejemplar) # Valida visualmente

        popup = PopupBusqueda(self.view, al_seleccionar_libro, tipo="libro")
        
        # Monkey patch o inyección simple para la búsqueda del popup
        # Lo ideal es que el popup tenga su propio mini-controller, pero para hacerlo rápido:
        def buscar_en_bd(event=None):
            termino = popup.entry_busqueda.get()
            conn = self.db.conectar()
            cursor = conn.cursor()
            # OJO: Buscamos ejemplares DISPONIBLES
            sql = """
                SELECT e.id_ejemplar, o.titulo, a.nombre_completo
                FROM ejemplares e
                JOIN obras o ON e.id_obra = o.id_obra
                JOIN autores_obras ao ON o.id_obra = ao.id_obra
                JOIN autores a ON ao.id_autor = a.id_autor
                WHERE (o.titulo LIKE %s OR o.isbn LIKE %s)
                AND e.estado = 'Disponible'
                GROUP BY e.id_ejemplar
            """
            like = f"%{termino}%"
            cursor.execute(sql, (like, like))
            res = cursor.fetchall()
            popup.cargar_datos(res)
            conn.close()

        popup.entry_busqueda.bind("<Return>", buscar_en_bd)