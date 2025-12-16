from src.view.circulacion.frm_solicitantes import FrmSolicitantes
from src.model.Solicitantes import Solicitante
from src.controller.reportes_controller import ReportesController 
from tkinter import messagebox
import re

class SolicitanteController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close
        self.view = FrmSolicitantes(view_container, self)
        self.listar_solicitantes()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def listar_solicitantes(self):
        try:
            solicitantes = Solicitante.obtener_todos()
            self.view.actualizar_tabla(solicitantes)
        except Exception as e:
            print(f"Error al listar: {e}")

    def agregar_solicitante(self, data):
        self._procesar_guardado(data)

    def actualizar_solicitante(self, data):
        self._procesar_guardado(data, id_actual=data.get('id'))

    def _procesar_guardado(self, datos, id_actual=None):
        
        # 1. Validar Email con Regex
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if datos["email"] and not re.match(patron_email, datos["email"]):
            messagebox.showerror("Error", "El formato del correo electrónico no es válido.")
            return
        
        # 2. Validar Teléfono (Solo números, 10 dígitos)
        if datos["telefono"] and (not datos["telefono"].isdigit() or len(datos["telefono"]) != 10):
            messagebox.showerror("Error", "El teléfono debe ser de 10 dígitos numéricos.")
            return
        
        # 3. Validar Nombre
        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        # 4. Crear Modelo
        try:
            nuevo = Solicitante(
                nombre_completo=datos["nombre"],
                telefono=datos["telefono"],
                email=datos["email"],
                direccion=datos["direccion"],
                id_prestatario=id_actual
            )

            # 5. Guardar
            if nuevo.guardar(): 
                accion = "actualizado" if id_actual else "registrado"
                messagebox.showinfo("Éxito", f"Lector {accion} correctamente")
                self.view.limpiar_form()
                self.listar_solicitantes()
            else:
                messagebox.showerror("Error", "No se pudo guardar en la base de datos")
        except Exception as e:
            messagebox.showerror("Error crítico", f"Ocurrió un error: {e}")

    def eliminar_solicitante(self, id_solicitante):
        if Solicitante.eliminar(id_solicitante):
            messagebox.showinfo("Eliminado", "Solicitante eliminado.")
            self.view.limpiar_form()
            self.listar_solicitantes()
        else:
            messagebox.showerror("Error", "No se pudo eliminar (Tal vez tiene préstamos activos).")

    def imprimir_reporte(self):
        try:
            ReportesController().generar_reporte_solicitantes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")