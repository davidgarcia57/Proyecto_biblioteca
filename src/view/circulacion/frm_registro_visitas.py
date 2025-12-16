import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
import os
from PIL import Image # Requiere: pip install pillow

class FrmRegistroVisitas(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        # Configuración principal del frame
        self.configure(fg_color="#F3E7D2") # Fondo Beige
        self.grid_columnconfigure(0, weight=1) # Panel Izquierdo
        self.grid_columnconfigure(1, weight=1) # Panel Derecho
        self.grid_rowconfigure(1, weight=1)    # Expansión vertical

        # --- HEADER (Título y Botón Volver) ---
        self.crear_header()

        # --- PANEL IZQUIERDO: FORMULARIO DE REGISTRO ---
        self.crear_panel_registro()

        # --- PANEL DERECHO: LOGO Y REPORTES ---
        self.crear_panel_reportes()

    def crear_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 10))
        
        btn_volver = ctk.CTkButton(
            header, text="⬅ Volver", width=90, height=35,
            fg_color="#A7744A", hover_color="#8c5e3a",
            font=("Arial", 13, "bold"),
            command=self.controller.volver_menu
        )
        btn_volver.pack(side="left")
        
        lbl_titulo = ctk.CTkLabel(
            header, text="Control de Acceso y Visitas", 
            font=("Georgia", 26, "bold"), text_color="#5a3b2e"
        )
        lbl_titulo.pack(side="left", padx=20)

    def crear_panel_registro(self):
        # Frame contenedor
        p_reg = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=1, border_color="#Decdbb")
        p_reg.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Título del panel
        ctk.CTkLabel(p_reg, text="Registrar Nueva Entrada", font=("Arial", 18, "bold"), text_color="#A7744A").pack(pady=(25, 15))

        # --- CAMPO 1: NOMBRE ---
        self.entry_nombre = ctk.CTkEntry(p_reg, placeholder_text="Nombre del Visitante (Opcional)", height=40, font=("Arial", 14))
        self.entry_nombre.pack(fill="x", padx=30, pady=(5, 10))
        
        # --- CAMPO 2: GÉNERO (NUEVO) ---
        # Usamos un ComboBox para que seleccionen el sexo
        self.combo_sexo = ctk.CTkComboBox(
            p_reg, 
            values=["Hombre", "Mujer", "Otro", "No especificar"], 
            height=40, 
            font=("Arial", 14),
            state="readonly" # Para que no puedan escribir texto libre
        )
        self.combo_sexo.set("Seleccione Género") # Texto inicial
        self.combo_sexo.pack(fill="x", padx=30, pady=10)

        # --- CAMPO 3: PROCEDENCIA ---
        self.entry_procedencia = ctk.CTkEntry(p_reg, placeholder_text="Procedencia (Escuela / Trabajo)", height=40, font=("Arial", 14))
        self.entry_procedencia.pack(fill="x", padx=30, pady=10)

        # SELECCIÓN DE ÁREA
        ctk.CTkLabel(p_reg, text="Seleccione el Área a visitar:", font=("Arial", 13, "bold"), text_color="gray").pack(pady=(20, 5))

        # Botones de Áreas
        self.crear_btn_area(p_reg, "📖  Sala de Lectura", "Lectura", "#A7744A")
        self.crear_btn_area(p_reg, "💻  Aula Virtual", "Virtual", "#8B5E3C") 
        self.crear_btn_area(p_reg, "📝  Sala de Estudio", "Estudio", "#6F4E37") 

        # Mensaje de estado
        self.lbl_msg = ctk.CTkLabel(p_reg, text="", font=("Arial", 14, "bold"))
        self.lbl_msg.pack(pady=20, side="bottom")

    def evento_registrar(self, area):
        # Obtenemos el valor del combo de sexo
        sexo_seleccionado = self.combo_sexo.get()
        
        # Validación: Si no ha seleccionado sexo, podemos poner un default o pedirlo
        if sexo_seleccionado == "Seleccione Género":
            sexo_seleccionado = "No especificado"

        datos = {
            "nombre": self.entry_nombre.get(),
            "sexo": sexo_seleccionado,  # <--- AQUI AGREGAMOS EL DATO FALTANTE
            "procedencia": self.entry_procedencia.get(),
            "area": area
        }
        
        # Validación simple
        if not datos["procedencia"]:
            self.mostrar_exito("⚠ Falta Procedencia", error=True)
            return

        self.controller.registrar_entrada(datos)

    def crear_panel_reportes(self):
            # Frame contenedor
            p_rep = ctk.CTkFrame(self, fg_color="white", corner_radius=20, border_width=1, border_color="#Decdbb")
            p_rep.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

            # --- SECCIÓN LOGO CORREGIDA ---
            frame_logo = ctk.CTkFrame(p_rep, fg_color="transparent")
            frame_logo.pack(pady=(20, 10), fill="x")

            try:
                import os
                # Ajuste de ruta: Subimos 3 niveles (view -> circulacion -> src)
                # __file__ = src/view/circulacion/frm_registro_visitas.py
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                        
                # Ahora buscamos en src/resources/logo.png
                ruta_real_logo = os.path.join(base_dir, "resources", "logo.png")
                        
                if os.path.exists(ruta_real_logo):
                    img_pil = Image.open(ruta_real_logo)
                    self.logo_img = ctk.CTkImage(light_image=img_pil, size=(150, 150)) 
                            
                    lbl_img = ctk.CTkLabel(frame_logo, image=self.logo_img, text="")
                    lbl_img.pack()
                else:
                    # Debug visual si falla
                    print(f"Buscando en: {ruta_real_logo}")
                    ctk.CTkLabel(frame_logo, text="🏛️", font=("Arial", 80)).pack()

            except Exception as e:
                print(f"Error cargando imagen: {e}")

            # --- RESTO DEL CÓDIGO (BOTONES DE REPORTES) ---
            # (Esto se queda igual que como lo tenías)
            ctk.CTkLabel(p_rep, text="Generación de Reportes", font=("Arial", 18, "bold"), text_color="#A7744A").pack(pady=10)
            
            # Filtros de fecha y botones...
            f_fechas = ctk.CTkFrame(p_rep, fg_color="#F9F5EB", corner_radius=10)
            f_fechas.pack(pady=15, padx=20, fill="x")
            f_fechas.grid_columnconfigure((0,1,2,3), weight=1)

            self.mi = self.crear_combo_fecha(f_fechas, "De Mes:", 0, 0)
            self.ai = self.crear_combo_fecha(f_fechas, "Año:", 0, 2, ["2024","2025","2026"])
            self.mf = self.crear_combo_fecha(f_fechas, "A Mes:", 1, 0)
            self.af = self.crear_combo_fecha(f_fechas, "Año:", 1, 2, ["2024","2025","2026"])

            ctk.CTkFrame(p_rep, height=2, fg_color="#E0E0E0").pack(fill="x", padx=40, pady=15)

            ctk.CTkButton(p_rep, text="📄 Guardar Reporte por Áreas", height=45, fg_color="#5a3b2e", hover_color="#3e281f",
                        font=("Arial", 14), command=self.evt_rep_areas).pack(fill="x", padx=30, pady=10)
            
            ctk.CTkButton(p_rep, text="📊 Guardar Reporte Total", height=45, fg_color="#5a3b2e", hover_color="#3e281f",
                        font=("Arial", 14), command=self.evt_rep_total).pack(fill="x", padx=30, pady=10)
            
    def crear_btn_area(self, parent, texto, valor, color):
        ctk.CTkButton(
            parent, text=texto, height=50, 
            fg_color=color, hover_color="#4A3B2A",
            font=("Arial", 15, "bold"),
            command=lambda: self.evento_registrar(valor)
        ).pack(fill="x", padx=30, pady=8)

    def crear_combo_fecha(self, parent, txt, r, c, vals=[str(i) for i in range(1,13)]):
        ctk.CTkLabel(parent, text=txt, font=("Arial", 11)).grid(row=r, column=c, padx=5, pady=10, sticky="e")
        cb = ctk.CTkComboBox(parent, values=vals, width=65, height=28, state="readonly")
        cb.set(vals[0])
        cb.grid(row=r, column=c+1, padx=5, pady=10, sticky="w")
        return cb

    def evento_registrar(self, area):
        datos = {
            "nombre": self.entry_nombre.get(),
            "procedencia": self.entry_procedencia.get(),
            "area": area
        }
        # Validación simple
        if not datos["procedencia"]:
            self.mostrar_exito("⚠ Falta Procedencia", error=True)
            return

        self.controller.registrar_entrada(datos)

    def mostrar_exito(self, msg, error=False):
        color = "#b03a2e" if error else "#1e8449" # Rojo o Verde
        self.lbl_msg.configure(text=msg, text_color=color)
        self.after(3000, lambda: self.lbl_msg.configure(text=""))

    def limpiar_form(self):
            self.entry_nombre.delete(0, 'end')
            self.entry_procedencia.delete(0, 'end')
            self.combo_sexo.set("Seleccione Género")
            self.focus()

    def evt_rep_areas(self):
        nombre_default = f"Reporte_Areas_{datetime.now().strftime('%Y%m%d')}.pdf"
        ruta = filedialog.asksaveasfilename(title="Guardar PDF", defaultextension=".pdf", initialfile=nombre_default)
        if ruta:
            self.controller.imprimir_reporte_areas(self.mi.get(), self.ai.get(), self.mf.get(), self.af.get(), ruta)

    def evt_rep_total(self):
        nombre_default = f"Reporte_Total_{datetime.now().strftime('%Y%m%d')}.pdf"
        ruta = filedialog.asksaveasfilename(title="Guardar PDF", defaultextension=".pdf", initialfile=nombre_default)
        if ruta:
            self.controller.imprimir_reporte_total(self.mi.get(), self.ai.get(), self.mf.get(), self.af.get(), ruta)