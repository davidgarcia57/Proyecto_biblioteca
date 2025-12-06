from src.view.circulacion.frm_registro_visitas import FrmRegistroVisitas
from src.model.Visita import Visita
from src.controller.reportes_controller import ReportesController
from tkinter import messagebox

class VisitasController:
    def __init__(self, view_container, on_close=None):
        self.view_container = view_container
        self.on_close = on_close
        self.reportes = ReportesController()
        
        # Inicializar vista
        self.view = FrmRegistroVisitas(view_container, self)

    def volver_menu(self):
        if self.on_close:
            self.on_close()

    def registrar_entrada(self, datos):
        # El área es obligatoria, el nombre puede ser opcional (anónimo)
        if not datos["area"]:
            messagebox.showwarning("Aviso", "Seleccione un área.")
            return

        visita = Visita(
            area=datos["area"],
            nombre=datos.get("nombre", "Anónimo"),
            procedencia=datos.get("procedencia", "General"),
            sexo=datos.get("sexo", "N/A")
        )

        if visita.guardar():
            self.view.mostrar_exito(f"Visita registrada en: {datos['area']}")
            self.view.limpiar_form()
        else:
            messagebox.showerror("Error", "No se pudo registrar la visita.")

    def imprimir_reporte_areas(self, mi, ai, mf, af, ruta_archivo):
        # Convertir a fechas SQL
        fi = f"{ai}-{mi}-01"
        ff = f"{af}-{mf}-28" 
        self.reportes.generar_reporte_visitas_areas(fi, ff, ruta_archivo)

    def imprimir_reporte_total(self, mi, ai, mf, af, ruta_archivo):
        fi = f"{ai}-{mi}-01"
        ff = f"{af}-{mf}-28"
        self.reportes.generar_reporte_visitas_total(fi, ff, ruta_archivo)