import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime

class FrmRegistroVisitas(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2") # Beige
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        ctk.CTkButton(header, text="⬅ Volver", width=80, fg_color="#A7744A", command=self.controller.volver_menu).pack(side="left")
        ctk.CTkLabel(header, text="Control de Visitantes", font=("Georgia", 24, "bold"), text_color="#5a3b2e").pack(side="left", padx=20)

        # --- PANEL IZQUIERDO: REGISTRO ---
        p_reg = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        p_reg.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(p_reg, text="Registrar Visita Nueva", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)

        self.entry_nombre = ctk.CTkEntry(p_reg, placeholder_text="Nombre (Opcional)")
        self.entry_nombre.pack(fill="x", padx=20, pady=5)
        
        self.entry_procedencia = ctk.CTkEntry(p_reg, placeholder_text="Procedencia (Escuela/Trabajo)")
        self.entry_procedencia.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(p_reg, text="Seleccione Área:", font=("Arial", 12, "bold")).pack(pady=(15,5))

        # Botones grandes para las áreas
        self.crear_btn_area(p_reg, "📖 Sala de Lectura", "Lectura")
        self.crear_btn_area(p_reg, "💻 Aula Virtual", "Virtual")
        self.crear_btn_area(p_reg, "📝 Sala de Estudio", "Estudio")

        self.lbl_msg = ctk.CTkLabel(p_reg, text="", font=("Arial", 12, "bold"))
        self.lbl_msg.pack(pady=10)

        # --- PANEL DERECHO: REPORTES ---
        p_rep = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        p_rep.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(p_rep, text="Generar Reportes de Visitas", font=("Arial", 16, "bold"), text_color="#A7744A").pack(pady=15)

        # Filtros Fecha
        f_fechas = ctk.CTkFrame(p_rep, fg_color="transparent")
        f_fechas.pack(pady=10)
        
        # Selectores
        self.mi = self.crear_combo_fecha(f_fechas, "De Mes:", 0, 0)
        self.ai = self.crear_combo_fecha(f_fechas, "Año:", 0, 2, ["2024","2025","2026"])
        self.mf = self.crear_combo_fecha(f_fechas, "A Mes:", 1, 0)
        self.af = self.crear_combo_fecha(f_fechas, "Año:", 1, 2, ["2024","2025","2026"])

        ctk.CTkButton(p_rep, text="📄 Reporte por Áreas (Guardar...)", fg_color="#5a3b2e", 
                      command=self.evt_rep_areas).pack(fill="x", padx=30, pady=10)
        
        ctk.CTkButton(p_rep, text="📊 Reporte Total (Guardar...)", fg_color="#5a3b2e", 
                      command=self.evt_rep_total).pack(fill="x", padx=30, pady=10)

    def crear_btn_area(self, parent, texto, valor):
        ctk.CTkButton(parent, text=texto, height=50, fg_color="#A7744A", font=("Arial", 14, "bold"),
                      command=lambda: self.evento_registrar(valor)).pack(fill="x", padx=20, pady=5)

    def crear_combo_fecha(self, parent, txt, r, c, vals=[str(i) for i in range(1,13)]):
        ctk.CTkLabel(parent, text=txt).grid(row=r, column=c, padx=5, pady=5)
        cb = ctk.CTkComboBox(parent, values=vals, width=70)
        cb.set(vals[0])
        cb.grid(row=r, column=c+1, padx=5, pady=5)
        return cb

    def evento_registrar(self, area):
        datos = {
            "nombre": self.entry_nombre.get(),
            "procedencia": self.entry_procedencia.get(),
            "area": area
        }
        self.controller.registrar_entrada(datos)

    def mostrar_exito(self, msg):
        self.lbl_msg.configure(text=msg, text_color="green")
        self.after(3000, lambda: self.lbl_msg.configure(text=""))

    def limpiar_form(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_procedencia.delete(0, 'end')

    def evt_rep_areas(self):
        nombre_default = f"Reporte_Visitas_Areas_{datetime.now().strftime('%H%M')}.pdf"
        ruta = filedialog.asksaveasfilename(
            title="Guardar Reporte Áreas",
            defaultextension=".pdf",
            initialfile=nombre_default,
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if ruta:
            self.controller.imprimir_reporte_areas(self.mi.get(), self.ai.get(), self.mf.get(), self.af.get(), ruta)

    def evt_rep_total(self):
        nombre_default = f"Reporte_Visitas_Total_{datetime.now().strftime('%H%M')}.pdf"
        ruta = filedialog.asksaveasfilename(
            title="Guardar Reporte Total",
            defaultextension=".pdf",
            initialfile=nombre_default,
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if ruta:
            self.controller.imprimir_reporte_total(self.mi.get(), self.ai.get(), self.mf.get(), self.af.get(), ruta)