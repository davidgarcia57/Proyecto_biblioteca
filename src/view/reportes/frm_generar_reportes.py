import customtkinter as ctk
from tkinter import filedialog
from src.controller.reportes_controller import ReportesController
from datetime import datetime

class FrmGenerarReportes(ctk.CTkFrame):
    def __init__(self, master, controller): 
        super().__init__(master)
        self.reportes_ctrl = ReportesController()
        self.main_controller = controller 
        
        self.configure(fg_color="#F3E7D2")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frm_bajas = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        # Lo ponemos en la fila 2, abarcando ambas columnas para que se vea destacado
        self.frm_bajas.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        ctk.CTkLabel(self.frm_bajas, text="🗑️", font=("Arial", 30)).pack(side="left", padx=20)
        ctk.CTkLabel(self.frm_bajas, text="Inventario de Libros de Baja", font=("Georgia", 16, "bold"), text_color="#D32F2F").pack(side="left")
        
        ctk.CTkButton(
            self.frm_bajas, 
            text="Generar PDF de Bajas", 
            fg_color="#D32F2F", # Rojo para indicar alerta/baja
            font=("Arial", 14, "bold"),
            command=self.imprimir_bajas
        ).pack(side="right", padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        ctk.CTkButton(header, text="⬅ Volver", width=80, fg_color="#A7744A", 
                      command=self.main_controller.volver_menu).pack(side="left")
        ctk.CTkLabel(header, text="Generación de Reportes", font=("Georgia", 26, "bold"), text_color="#5a3b2e").pack(side="left", padx=20)

        # --- SECCIÓN 1: REPORTE DE LIBROS (ACERVO) ---
        self.crear_panel_reporte(
            titulo="Reporte de Libros Registrados",
            columna=0,
            comando=self.imprimir_libros,
            icono="📚"
        )

        # --- SECCIÓN 2: REPORTE DE PRÉSTAMOS ---
        self.crear_panel_reporte(
            titulo="Reporte de Préstamos Realizados",
            columna=1,
            comando=self.imprimir_prestamos,
            icono="📑"
        )

    def crear_panel_reporte(self, titulo, columna, comando, icono):
        frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        frame.grid(row=1, column=columna, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(frame, text=icono, font=("Arial", 50)).pack(pady=(30,10))
        ctk.CTkLabel(frame, text=titulo, font=("Georgia", 18, "bold"), text_color="#A7744A").pack(pady=10)
        
        # Filtros de Fecha
        frm_fechas = ctk.CTkFrame(frame, fg_color="transparent")
        frm_fechas.pack(pady=20)
        
        # Fecha Inicio
        ctk.CTkLabel(frm_fechas, text="Desde:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        mes_ini = ctk.CTkComboBox(frm_fechas, values=[str(i) for i in range(1,13)], width=60)
        mes_ini.set("1")
        mes_ini.grid(row=0, column=1, padx=2)
        anio_ini = ctk.CTkComboBox(frm_fechas, values=["2024", "2025", "2026"], width=70)
        anio_ini.set("2025")
        anio_ini.grid(row=0, column=2, padx=2)

        # Fecha Fin
        ctk.CTkLabel(frm_fechas, text="Hasta:", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5, pady=10)
        mes_fin = ctk.CTkComboBox(frm_fechas, values=[str(i) for i in range(1,13)], width=60)
        mes_fin.set(str(datetime.now().month))
        mes_fin.grid(row=1, column=1, padx=2, pady=10)
        anio_fin = ctk.CTkComboBox(frm_fechas, values=["2024", "2025", "2026"], width=70)
        anio_fin.set("2025")
        anio_fin.grid(row=1, column=2, padx=2, pady=10)

        # Guardar referencias para usarlas en el comando
        if "Libros" in titulo:
            self.widgets_libros = (mes_ini, anio_ini, mes_fin, anio_fin)
        else:
            self.widgets_prestamos = (mes_ini, anio_ini, mes_fin, anio_fin)

        # Botón Imprimir
        ctk.CTkButton(frame, text="Guardar PDF...", fg_color="#2E7D32", height=40, font=("Arial", 14, "bold"),
                      command=comando).pack(pady=30, padx=40, fill="x")

    def imprimir_libros(self):
        mi, ai, mf, af = [w.get() for w in self.widgets_libros]
        
        nombre_default = f"Reporte_Libros_{mi}-{ai}_al_{mf}-{af}.pdf"
        ruta = filedialog.asksaveasfilename(
            title="Guardar Reporte de Libros",
            defaultextension=".pdf",
            initialfile=nombre_default,
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if ruta:
            self.reportes_ctrl.generar_reporte_registros(mi, ai, mf, af, ruta)

    def imprimir_prestamos(self):
        mi, ai, mf, af = [w.get() for w in self.widgets_prestamos]
        
        nombre_default = f"Reporte_Prestamos_{mi}-{ai}_al_{mf}-{af}.pdf"
        ruta = filedialog.asksaveasfilename(
            title="Guardar Reporte de Préstamos",
            defaultextension=".pdf",
            initialfile=nombre_default,
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if ruta:
            self.reportes_ctrl.generar_reporte_prestamos(mi, ai, mf, af, ruta)

    def imprimir_bajas(self):
        nombre_default = f"Reporte_Libros_Baja_{datetime.now().strftime('%Y-%m-%d')}.pdf"
        ruta = filedialog.asksaveasfilename(
            title="Guardar Reporte de Bajas",
            defaultextension=".pdf",
            initialfile=nombre_default,
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        
        if ruta:
            # Llamamos al nuevo método del controlador
            self.reportes_ctrl.generar_reporte_bajas(ruta)