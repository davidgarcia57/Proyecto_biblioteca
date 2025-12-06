from src.view.circulacion.frm_solicitantes import FrmSolicitantes
from src.model.Solicitantes import Solicitante
from tkinter import messagebox

class SolicitanteController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close
        self.view = FrmSolicitantes(view_container, self)
        self.cargar_lista()

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def cargar_lista(self):
        """Pide al modelo todos los solicitantes y actualiza la tabla"""
        solicitantes = Solicitante.obtener_todos()
        
        # Limpiar tabla
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
            
        # Llenar tabla
        for s in solicitantes:
            self.view.tree.insert("", "end", values=(s.id_prestatario, s.nombre_completo, s.telefono, s.email))

    def guardar_solicitante(self, datos, id_actual=None):
        if not datos["nombre"]:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        nuevo = Solicitante(
            nombre_completo=datos["nombre"],
            telefono=datos["telefono"],
            email=datos["email"],
            direccion=datos["direccion"],
            id_prestatario=id_actual
        )

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