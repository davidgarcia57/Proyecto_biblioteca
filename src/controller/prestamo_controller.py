from src.config.conexion_db import ConexionBD
from src.view.circulacion.popup_busqueda import PopupBusqueda
from src.view.circulacion.frm_prestamo import FrmPrestamos
from src.model.Prestamo import Prestamo
from src.model.Obra import Obra  # Importamos el modelo para la búsqueda
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
        # Nota: Idealmente, este SQL también debería ir al Modelo (Ejemplar.py),
        # pero lo dejamos aquí para no cambiar todo el código de golpe.
        conn = self.db.conectar()
        if conn:
            try:
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
            finally:
                conn.close()

    def verificar_solicitante(self, id_solicitante):
        # Nota: Idealmente, mover al Modelo (Solicitante.py)
        conn = self.db.conectar()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT nombre_completo FROM solicitantes WHERE id_prestatario = %s"
                cursor.execute(sql, (id_solicitante,))
                res = cursor.fetchone()

                if res:
                    self.view.actualizar_info_usuario(f"✔ {res[0]}", True)
                    return True
                else:
                    self.view.actualizar_info_usuario("❌ Usuario no encontrado", False)
                    return False
            finally:
                conn.close()

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
        """
        Abre el popup de búsqueda y maneja la selección del libro.
        Respeta MVC delegando la búsqueda al Modelo (Obra).
        """
        # 1. Definimos qué hacer cuando el usuario seleccione un libro en el popup
        def al_seleccionar_libro(id_ejemplar):
            self.view.txt_id_libro.delete(0, 'end')
            self.view.txt_id_libro.insert(0, str(id_ejemplar))
            # Validamos visualmente que sea correcto
            self.verificar_libro(id_ejemplar) 

        # 2. Creamos la vista del Popup pasándole nuestra función callback
        popup = PopupBusqueda(self.view, al_seleccionar_libro, tipo="libro")
        
        # 3. Definimos la lógica de búsqueda (Puente entre Vista y Modelo)
        def ejecutar_busqueda(event=None):
            termino = popup.entry_busqueda.get()
            
            # El controlador NO hace SQL. Le pide los datos al Modelo.
            resultados = Obra.buscar_disponibles(termino)
            
            # El controlador recibe los datos limpios y se los da a la Vista.
            popup.cargar_datos(resultados)

        # 4. Conectamos el evento 'Enter' del popup a nuestra función
        popup.entry_busqueda.bind("<Return>", ejecutar_busqueda)
        
        # Si agregaste un botón 'Buscar' en el popup, conéctalo también:
        if hasattr(popup, 'btn_buscar'):
             popup.btn_buscar.configure(command=ejecutar_busqueda)