import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
from PIL import Image
from src.utils import resource_path

class FrmRegistroVisitas(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # --- CONFIGURACIÓN GENERAL ---
        self.configure(fg_color="#F3E7D2") # Fondo Beige
        
        # Grid: 50% Izquierda (Formularios) | 50% Derecha (Instrucciones)
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        # --- HEADER (Botón Volver Gigante) ---
        self.crear_header()

        # --- PANEL IZQUIERDO: ACCIONES (REGISTRO + REPORTES) ---
        self.crear_panel_izquierdo()

        # --- PANEL DERECHO: AYUDA (LOGO + INSTRUCCIONES) ---
        self.crear_panel_derecho()

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=30, pady=(20, 10))
        
        # BOTÓN VOLVER (MÁS GRANDE)
        btn_volver = ctk.CTkButton(
            header, 
            text="⬅ VOLVER AL MENÚ", 
            width=220,          # Más ancho
            height=55,          # Más alto
            fg_color="#8D6E63", 
            hover_color="#6D4C41",
            font=("Arial", 18, "bold"), # Letra más grande
            command=self.controller.volver_menu
        )
        btn_volver.pack(side="left")
        
        lbl_titulo = ctk.CTkLabel(
            header, 
            text="CONTROL DE ACCESO Y VISITAS", 
            font=("Georgia", 32, "bold"), # Título Gigante
            text_color="#5a3b2e"
        )
        lbl_titulo.pack(side="left", padx=40)

    def crear_panel_izquierdo(self):
        # Usamos un ScrollableFrame por si la pantalla es pequeña, para que quepa todo
        p_izq = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text="")
        p_izq.grid(row=1, column=0, sticky="nsew", padx=(30, 15), pady=20)
        
        # ==========================================
        #           SECCIÓN 1: REGISTRO
        # ==========================================
        frame_reg = ctk.CTkFrame(p_izq, fg_color="white", corner_radius=20)
        frame_reg.pack(fill="x", pady=(0, 20), ipadx=10, ipady=10)
        
        ctk.CTkLabel(frame_reg, text="1. Registrar Nueva Entrada", font=("Arial", 22, "bold"), text_color="#A7744A").pack(pady=(20, 15))

        # Entradas (LETRAS GRANDES)
        self.entry_nombre = ctk.CTkEntry(frame_reg, placeholder_text="Nombre Completo", height=50, font=("Arial", 16))
        self.entry_nombre.pack(fill="x", padx=30, pady=10)
        
        # Combo Sexo
        self.combo_sexo = ctk.CTkComboBox(frame_reg, values=["Hombre", "Mujer", "Otro", "No especificar"], height=50, font=("Arial", 16), state="readonly")
        self.combo_sexo.set("Seleccione Género")
        self.combo_sexo.pack(fill="x", padx=30, pady=10)

        self.entry_procedencia = ctk.CTkEntry(frame_reg, placeholder_text="Procedencia (Escuela / Trabajo)", height=50, font=("Arial", 16))
        self.entry_procedencia.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(frame_reg, text="Seleccione el Área a visitar:", font=("Arial", 18, "bold"), text_color="#555").pack(pady=(20, 10))

        # Botones de Áreas (GIGANTES)
        self.crear_btn_area(frame_reg, "📖  SALA DE LECTURA", "Lectura", "#A7744A")
        self.crear_btn_area(frame_reg, "💻  AULA VIRTUAL", "Virtual", "#8B5E3C") 
        self.crear_btn_area(frame_reg, "📝  SALA DE ESTUDIO", "Estudio", "#6F4E37") 

        # Mensaje Exito/Error
        self.lbl_msg = ctk.CTkLabel(frame_reg, text="", font=("Arial", 16, "bold"))
        self.lbl_msg.pack(pady=10)

        # ==========================================
        #           SECCIÓN 2: REPORTES
        # ==========================================
        frame_rep = ctk.CTkFrame(p_izq, fg_color="white", corner_radius=20)
        frame_rep.pack(fill="x", ipadx=10, ipady=10)

        ctk.CTkLabel(frame_rep, text="2. Generar Reportes PDF", font=("Arial", 22, "bold"), text_color="#A7744A").pack(pady=(20, 15))

        # Filtros Fecha
        f_fechas = ctk.CTkFrame(frame_rep, fg_color="#F9F5EB")
        f_fechas.pack(fill="x", padx=20, pady=10)
        
        self.mi = self.crear_combo_fecha(f_fechas, "De:", 0, 0)
        self.ai = self.crear_combo_fecha(f_fechas, "Año:", 0, 2, ["2024","2025","2026"])
        self.mf = self.crear_combo_fecha(f_fechas, "A:", 1, 0)
        self.af = self.crear_combo_fecha(f_fechas, "Año:", 1, 2, ["2024","2025","2026"])

        # Botones Reporte
        ctk.CTkButton(frame_rep, text="📄 REPORTE POR ÁREAS", height=50, fg_color="#5a3b2e", font=("Arial", 16, "bold"), command=self.evt_rep_areas).pack(fill="x", padx=30, pady=10)
        ctk.CTkButton(frame_rep, text="📊 REPORTE TOTAL", height=50, fg_color="#5a3b2e", font=("Arial", 16, "bold"), command=self.evt_rep_total).pack(fill="x", padx=30, pady=10)

    def crear_panel_derecho(self):
        p_der = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_color="#Decdbb", border_width=2)
        p_der.grid(row=1, column=1, sticky="nsew", padx=(15, 30), pady=20)
        
        # --- LOGO (Arriba) ---
        frame_logo = ctk.CTkFrame(p_der, fg_color="transparent")
        frame_logo.pack(pady=(40, 20))

        try:
            ruta_logo = resource_path("resources/logo.png")
            
            if os.path.exists(ruta_logo):
                img_pil = Image.open(ruta_logo)
                self.logo_img = ctk.CTkImage(light_image=img_pil, size=(200, 200)) 
                ctk.CTkLabel(frame_logo, image=self.logo_img, text="").pack(anchor="center")
            else:
                # Debug
                print(f"Buscando logo en: {ruta_logo}")
                ctk.CTkLabel(frame_logo, text="🏛️", font=("Arial", 100)).pack(anchor="center")
        except Exception as e:
            print(f"Error logo: {e}")
            ctk.CTkLabel(frame_logo, text="🏛️", font=("Arial", 100)).pack(anchor="center")

        # --- INSTRUCCIONES (Abajo) ---
        # Usamos un frame transparente contenedor para forzar el centrado vertical y horizontal
        frame_inst = ctk.CTkFrame(p_der, fg_color="transparent")
        frame_inst.pack(expand=True, fill="both", padx=20)

        ctk.CTkLabel(frame_inst, text="GUÍA RÁPIDA", font=("Arial", 26, "bold"), text_color="#A7744A").pack(pady=(0, 20))
        
        texto_instrucciones = (
            "PASO 1:\n"
            "Escriba el nombre de la persona y seleccione\n"
            "su género y procedencia (Escuela/Trabajo).\n\n"
            "PASO 2:\n"
            "Presione el botón café que corresponda\n"
            "al área que van a visitar (Lectura, Virtual...).\n\n"
            "PASO 3 (Reportes):\n"
            "Para sacar un reporte, seleccione las fechas\n"
            "abajo a la izquierda y presione 'Descargar'."
        )
        
        lbl_inst = ctk.CTkLabel(
            frame_inst, 
            text=texto_instrucciones, 
            font=("Arial", 20), 
            text_color="#333333",
            justify="center" # Centra el texto renglón por renglón
        )
        
        # AJUSTE VISUAL: 'padx' asimétrico para empujarlo visualmente a la derecha si se siente a la izquierda
        # (Izquierda: 80px, Derecha: 20px) -> Esto lo mueve a la derecha
        lbl_inst.pack(anchor="center", padx=(80, 20), pady=10)
        
    # --- UTILIDADES ---
    def crear_btn_area(self, parent, texto, valor, color):
        ctk.CTkButton(
            parent, text=texto, height=60, # Botones más altos
            fg_color=color, hover_color="#4A3B2A",
            font=("Arial", 18, "bold"),
            command=lambda: self.evento_registrar(valor)
        ).pack(fill="x", padx=30, pady=8)

    def crear_combo_fecha(self, parent, txt, r, c, vals=[str(i).zfill(2) for i in range(1,13)]):
        # Combos más grandes
        ctk.CTkLabel(parent, text=txt, font=("Arial", 14, "bold")).grid(row=r, column=c, padx=5, pady=5, sticky="e")
        cb = ctk.CTkComboBox(parent, values=vals, width=80, height=35, font=("Arial", 14), state="readonly")
        cb.set(vals[0])
        cb.grid(row=r, column=c+1, padx=5, pady=5, sticky="w")
        return cb

    def evento_registrar(self, area):
        sexo = self.combo_sexo.get()
        if sexo == "Seleccione Género": sexo = "No especificado"

        datos = {
            "nombre": self.entry_nombre.get(),
            "sexo": sexo,
            "procedencia": self.entry_procedencia.get(),
            "area": area
        }
        
        if not datos["procedencia"]:
            self.lbl_msg.configure(text="⚠ Falta Procedencia", text_color="#b03a2e")
            return

        self.controller.registrar_entrada(datos)

    def mostrar_exito(self, msg, error=False):
        color = "#b03a2e" if error else "#1e8449"
        self.lbl_msg.configure(text=msg, text_color=color)
        self.after(3000, lambda: self.lbl_msg.configure(text=""))

    def limpiar_form(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_procedencia.delete(0, 'end')
        self.combo_sexo.set("Seleccione Género")
        self.focus()

    def evt_rep_areas(self):
        self.guardar_pdf(f"Visitas_Areas", lambda r: self.controller.imprimir_reporte_areas(self.mi.get(), self.ai.get(), self.mf.get(), self.af.get(), r))

    def evt_rep_total(self):
        self.guardar_pdf(f"Visitas_Total", lambda r: self.controller.imprimir_reporte_total(self.mi.get(), self.ai.get(), self.mf.get(), self.af.get(), r))

    def guardar_pdf(self, nombre_base, funcion):
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=f"{nombre_base}.pdf")
        if ruta:
            funcion(ruta)
            messagebox.showinfo("Éxito", "Reporte generado.")