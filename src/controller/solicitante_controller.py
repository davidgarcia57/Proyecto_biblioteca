from src.view.circulacion.frm_solicitantes import FrmSolicitantes
from src.model.Solicitantes import Solicitante
# Importamos el controlador de reportes aquí, donde pertenece la lógica de orquestación
from src.controller.reportes_controller import ReportesController 
from tkinter import messagebox
import re

class SolicitanteController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close
        # Instanciamos la vista
        self.view = FrmSolicitantes(view_container, self)
        # Carga inicial de datos
        self.cargar_lista()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def cargar_lista(self):
        """Obtiene datos del modelo y actualiza la vista."""
        solicitantes = Solicitante.obtener_todos()
        # Pasamos los objetos o tuplas a la vista para que los pinte
        # (La vista FrmSolicitantes espera objetos Solicitante, ajustamos la vista para recibir tuplas si fuera necesario, 
        # pero aquí FrmSolicitantes.crear_panel_tabla usa atributos, así que pasamos lista de objetos).
        
        # Nota: Para mantener compatibilidad con tu FrmSolicitantes actual, 
        # llenaremos la tabla manualmente aquí o crearemos un método en la vista.
        # Lo ideal es crear un método en la vista:
        self.view.actualizar_tabla(solicitantes)

    def guardar_solicitante(self, datos, id_actual=None):
        """Valida datos y guarda en BD."""
        
        # 1. Validar Email con Regex
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if datos["email"] and not re.match(patron_email, datos["email"]):
            messagebox.showerror("Error", "El formato del correo electrónico no es válido.")
            return
        
        # 2. Validar Teléfono
        if datos["telefono"] and (not datos["telefono"].isdigit() or len(datos["telefono"]) != 10):
            messagebox.showerror("Error", "El teléfono debe ser de 10 dígitos numéricos.")
            return
        
        # 3. Validar Nombre
        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        # 4. Crear Modelo
        nuevo = Solicitante(
            nombre_completo=datos["nombre"],
            telefono=datos["telefono"],
            email=datos["email"],
            direccion=datos["direccion"],
            id_prestatario=id_actual
        )

        # 5. Guardar
        if nuevo.guardar():
            messagebox.showinfo("Éxito", "Solicitante guardado correctamente")
            self.view.limpiar_form()
            self.cargar_lista() # Recargar la tabla
        else:
            messagebox.showerror("Error", "No se pudo guardar en la base de datos")

    def eliminar_solicitante(self, id_solicitante):
        if Solicitante.eliminar(id_solicitante):
            messagebox.showinfo("Eliminado", "Solicitante eliminado.")
            self.view.limpiar_form()
            self.cargar_lista()
        else:
            messagebox.showerror("Error", "No se pudo eliminar (Tal vez tiene préstamos activos).")

    def imprimir_reporte(self):
        """Coordina la generación del reporte PDF."""
        try:
            ReportesController().generar_reporte_solicitantes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")