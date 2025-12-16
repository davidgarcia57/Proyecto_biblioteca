import customtkinter as ctk
from tkinter import filedialog, messagebox
from src.controller.reportes_controller import ReportesController
from datetime import datetime

class FrmGenerarReportes(ctk.CTkFrame):
    def __init__(self, master, controller): 
        super().__init__(master)
        self.reportes_ctrl = ReportesController()
        self.main_controller = controller 
        
        self.configure(fg_color="#F3E7D2")
        
        # Grid Asimétrico: 40% Instrucciones | 60% Botones
        self.grid_columnconfigure(0, weight=4) 
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(1, weight=1) 
        
        # ==================================================
        #                 1. ENCABEZADO
        # ==================================================
        frm_header = ctk.CTkFrame(self, fg_color="transparent")
        frm_header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        # BOTÓN VOLVER
        self.btn_volver = ctk.CTkButton(
            frm_header,
            text="⬅ VOLVER AL MENÚ",
            font=("Arial", 16, "bold"),
            width=200, height=50,
            fg_color="#8D6E63", hover_color="#6D4C41",
            command=self.volver_menu
        )
        self.btn_volver.pack(side="left")
        
        ctk.CTkLabel(
            frm_header, 
            text="CENTRAL DE REPORTES", 
            font=("Arial", 32, "bold"), 
            text_color="#5a3b2e"
        ).pack(side="left", padx=40)

        # ==================================================
        #           2. PANEL IZQUIERDO: INSTRUCCIONES
        # ==================================================
        self.crear_panel_instrucciones(row=1, col=0)

        # ==================================================
        #           3. PANEL DERECHO: BOTONES
        # ==================================================
        self.crear_panel_botones(row=1, col=1)

    def volver_menu(self):
        if hasattr(self.main_controller, 'volver_menu'):
            self.main_controller.volver_menu()

    def crear_panel_instrucciones(self, row, col):
        frame_inst = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        frame_inst.grid(row=row, column=col, sticky="nsew", padx=(20, 10), pady=10)
        
        ctk.CTkLabel(
            frame_inst, 
            text="¿Cómo generar un reporte?", 
            font=("Arial", 26, "bold"), 
            text_color="#A7744A"
        ).pack(pady=(40, 30), padx=20)
        
        texto_instrucciones = (
            "1. Seleccione las fechas 'Desde' y 'Hasta'\n"
            "   en el reporte que desea consultar.\n\n"
            "2. Haga clic en el botón 'Descargar PDF'.\n\n"
            "3. Elija dónde guardar el archivo en su\n"
            "   computadora.\n\n"
            "4. El documento se abrirá automáticamente."
        )
        
        lbl_texto = ctk.CTkLabel(
            frame_inst, 
            text=texto_instrucciones, 
            font=("Arial", 22), # Letra Muy Grande
            text_color="#333333",
            justify="left"
        )
        lbl_texto.pack(pady=10, padx=30, anchor="w")
        
        ctk.CTkLabel(frame_inst, text="📄", font=("Arial", 120)).pack(side="bottom", pady=40)

    def crear_panel_botones(self, row, col):
        # Frame desplazable por si hay muchos reportes
        frame_btns = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="")
        frame_btns.grid(row=row, column=col, sticky="nsew", padx=(10, 20), pady=10)
        
        # 1. LIBROS
        self.crear_tarjeta_reporte(frame_btns, "📚 Inventario de Libros", 
                                   self.crear_filtros_fecha, self.imprimir_libros)

        # 2. PRÉSTAMOS
        self.crear_tarjeta_reporte(frame_btns, "⏳ Historial de Préstamos", 
                                   self.crear_filtros_fecha, self.imprimir_prestamos)

        # 3. LECTORES
        self.crear_tarjeta_simple(frame_btns, "👥 Directorio de Lectores", 
                                  "Generar Lista de Usuarios", self.imprimir_lectores)

        # 4. BAJAS
        self.crear_tarjeta_simple(frame_btns, "🗑️ Libros dados de Baja", 
                                  "Generar Reporte de Bajas", self.imprimir_bajas)

    # --- UTILIDADES DE DISEÑO ---
    def crear_tarjeta_reporte(self, parent, titulo, funcion_widgets, comando_btn):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=10, ipadx=10, ipady=10)
        
        ctk.CTkLabel(card, text=titulo, font=("Arial", 20, "bold"), text_color="#5a3b2e").pack(pady=10)
        widgets = funcion_widgets(card)
        
        ctk.CTkButton(
            card, text="DESCARGAR PDF", 
            font=("Arial", 16, "bold"), height=50,
            fg_color="#A7744A", hover_color="#8c5e3c",
            command=lambda: comando_btn(widgets)
        ).pack(pady=10)

    def crear_tarjeta_simple(self, parent, titulo, texto_btn, comando_btn):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        card.pack(fill="x", pady=10, ipadx=10, ipady=10)
        
        ctk.CTkLabel(card, text=titulo, font=("Arial", 20, "bold"), text_color="#5a3b2e").pack(pady=10)
        
        ctk.CTkButton(
            card, text=texto_btn.upper(), 
            font=("Arial", 16, "bold"), height=50,
            fg_color="#A7744A", hover_color="#8c5e3c",
            command=comando_btn
        ).pack(pady=10)

    def crear_filtros_fecha(self, parent):
        f = ctk.CTkFrame(parent, fg_color="#F9F5EB")
        f.pack(pady=5)
        meses = [str(i).zfill(2) for i in range(1, 13)]
        anios = [str(i) for i in range(2023, 2030)]
        
        ctk.CTkLabel(f, text="Desde:", font=("Arial", 14)).pack(side="left", padx=5)
        mi = ctk.CTkComboBox(f, values=meses, width=70, font=("Arial", 14)); mi.pack(side="left", padx=2); mi.set("01")
        ai = ctk.CTkComboBox(f, values=anios, width=80, font=("Arial", 14)); ai.pack(side="left", padx=2); ai.set("2024")
        
        ctk.CTkLabel(f, text=" Hasta:", font=("Arial", 14)).pack(side="left", padx=10)
        mf = ctk.CTkComboBox(f, values=meses, width=70, font=("Arial", 14)); mf.pack(side="left", padx=2); mf.set("12")
        af = ctk.CTkComboBox(f, values=anios, width=80, font=("Arial", 14)); af.pack(side="left", padx=2); af.set("2024")
        return (mi, ai, mf, af)

    # --- FUNCIONES DE IMPRESIÓN ---
    def imprimir_libros(self, widgets):
        mi, ai, mf, af = [w.get() for w in widgets]
        self.guardar_pdf(f"Libros_{mi}-{ai}", lambda r: self.reportes_ctrl.generar_reporte_registros(mi, ai, mf, af, r))

    def imprimir_prestamos(self, widgets):
        mi, ai, mf, af = [w.get() for w in widgets]
        self.guardar_pdf(f"Prestamos_{mi}-{ai}", lambda r: self.reportes_ctrl.generar_reporte_prestamos(mi, ai, mf, af, r))

    def imprimir_lectores(self):
        self.guardar_pdf("Lista_Lectores", self.reportes_ctrl.generar_reporte_solicitantes)

    def imprimir_bajas(self):
        self.guardar_pdf("Bajas", self.reportes_ctrl.generar_reporte_bajas)

    def guardar_pdf(self, nombre_base, funcion_generadora):
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"{nombre_base}.pdf")
        if ruta:
            try:
                funcion_generadora(ruta)
                messagebox.showinfo("Éxito", "Reporte generado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")