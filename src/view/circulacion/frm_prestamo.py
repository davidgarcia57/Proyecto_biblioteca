import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

class FrmPrestamos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.configure(fg_color="#F3E7D2") # Beige de fondo

        # Layout principal: 2 columnas
        # Columna 0 (Formulario) un poco más ancha para acomodar los inputs grandes
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # =================================================
        #                   HEADER
        # =================================================
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        # Botón Volver grande
        self.btn_volver = ctk.CTkButton(
            self.header, 
            text="⬅ Volver", 
            width=150, 
            height=50,
            font=("Arial", 18, "bold"),
            fg_color="#A7744A", 
            command=self.controller.volver_menu
        )
        self.btn_volver.pack(side="left")
        
        # Título grande y limpio
        ctk.CTkLabel(
            self.header, 
            text="Gestión de Préstamos", 
            font=("Arial", 32, "bold"), # CAMBIO: Arial 32px
            text_color="#000000"
        ).pack(side="left", padx=30)

        # =================================================
        #               ZONA DE FORMULARIO
        # =================================================
        self.frm_form = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.frm_form.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            self.frm_form, 
            text="Nuevo Préstamo", 
            font=("Arial", 22, "bold"), 
            text_color="#A7744A"
        ).pack(pady=20)

        # --- 1. SECCIÓN LIBRO ---
        ctk.CTkLabel(self.frm_form, text="1. Código del Libro:", font=("Arial", 18, "bold")).pack(pady=(10,0), padx=30, anchor="w")
        
        frm_input_libro = ctk.CTkFrame(self.frm_form, fg_color="transparent")
        frm_input_libro.pack(fill="x", padx=30, pady=5)
        
        # Input grande
        self.txt_id_libro = ctk.CTkEntry(
            frm_input_libro, 
            placeholder_text="Escriba ID aquí...",
            height=50,              # CAMBIO: Altura para facilitar clic
            font=("Arial", 18)      # CAMBIO: Texto legible
        )
        self.txt_id_libro.pack(side="left", fill="x", expand=True)
        self.txt_id_libro.bind("<Return>", lambda e: self.buscar_libro())
        
        # Botón Lupa grande
        self.btn_buscar_libro = ctk.CTkButton(
            frm_input_libro, 
            text="🔍 Buscar", 
            width=100,              # CAMBIO: Más ancho
            height=50, 
            font=("Arial", 16, "bold"),
            fg_color="#A7744A",
            command=self.controller.abrir_busqueda_libros 
        )
        self.btn_buscar_libro.pack(side="left", padx=(10,0))

        # Etiqueta de estado (Feedback)
        self.lbl_info_libro = ctk.CTkLabel(
            self.frm_form, 
            text="[ Ingrese un libro ]", 
            font=("Arial", 16),
            text_color="#555555", 
            wraplength=400
        )
        self.lbl_info_libro.pack(pady=5)

        # --- 2. SECCIÓN SOLICITANTE ---
        ctk.CTkFrame(self.frm_form, height=2, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10) # Separador

        ctk.CTkLabel(self.frm_form, text="2. ID del Solicitante:", font=("Arial", 18, "bold")).pack(pady=(5,0), padx=30, anchor="w")
        
        frm_input_user = ctk.CTkFrame(self.frm_form, fg_color="transparent")
        frm_input_user.pack(fill="x", padx=30, pady=5)

        self.txt_id_usuario = ctk.CTkEntry(
            frm_input_user, 
            placeholder_text="ID del lector...",
            height=50, 
            font=("Arial", 18)
        )
        self.txt_id_usuario.pack(side="left", fill="x", expand=True)
        self.txt_id_usuario.bind("<Return>", lambda e: self.buscar_solicitante())

        self.btn_buscar_sol = ctk.CTkButton(
            frm_input_user, 
            text="🔍 Buscar", 
            width=100, 
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#A7744A",
            command=self.controller.abrir_busqueda_lectores 
        )
        self.btn_buscar_sol.pack(side="left", padx=(10,0))

        self.lbl_info_usuario = ctk.CTkLabel(
            self.frm_form, 
            text="[ Ingrese un lector ]", 
            font=("Arial", 16),
            text_color="#555555"
        )
        self.lbl_info_usuario.pack(pady=5)

        # --- 3. DÍAS Y ACCIÓN ---
        ctk.CTkFrame(self.frm_form, height=2, fg_color="#E0E0E0").pack(fill="x", padx=20, pady=10) # Separador

        frm_footer = ctk.CTkFrame(self.frm_form, fg_color="transparent")
        frm_footer.pack(fill="x", padx=30, pady=10)

        # Combo de días más grande
        ctk.CTkLabel(frm_footer, text="Días:", font=("Arial", 18, "bold")).pack(side="left")
        
        self.combo_dias = ctk.CTkComboBox(
            frm_footer, 
            values=["3", "5", "7", "15"], 
            state="readonly",
            width=100,
            height=40,
            font=("Arial", 18),
            dropdown_font=("Arial", 18) # Importante: la lista desplegable también grande
        )
        self.combo_dias.set("3")
        self.combo_dias.pack(side="left", padx=15)

        # BOTÓN FINAL GIGANTE
        self.btn_prestar = ctk.CTkButton(
            self.frm_form, 
            text="CONFIRMAR PRÉSTAMO ✅", 
            fg_color="#2E7D32", 
            hover_color="#1B5E20",
            height=70,                  # CAMBIO: Altura máxima
            font=("Arial", 22, "bold"), # CAMBIO: Letra muy legible
            command=self.evento_prestar
        )
        self.btn_prestar.pack(pady=20, padx=30, fill="x", side="bottom")

        # =================================================
        #             PANEL DERECHO (INSTRUCCIONES)
        # =================================================
        self.frm_lista = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.frm_lista.grid(row=1, column=1, sticky="nsew", padx=(0,20), pady=(0, 20))
        
        ctk.CTkLabel(self.frm_lista, text="Instrucciones", font=("Arial", 24, "bold"), text_color="#A7744A").pack(pady=(30, 20))
        
        # Texto de instrucciones con tamaño 18px
        instrucciones = (
            "1. LIBRO:\n"
            "   Escriba el ID del libro o use la lupa 🔍 para buscarlo en el catálogo.\n\n"
            "2. LECTOR:\n"
            "   Ingrese el ID del usuario o búsquelo con la lupa.\n\n"
            "3. FINALIZAR:\n"
            "   Verifique que los nombres sean correctos y presione el botón verde."
        )
        
        lbl_inst = ctk.CTkLabel(
            self.frm_lista, 
            text=instrucciones, 
            justify="left", 
            font=("Arial", 18), # CAMBIO: Letra grande para lectura fácil
            text_color="#333333",
            wraplength=350      # Ajuste de wrap para columna derecha
        )
        lbl_inst.pack(padx=30, anchor="w")

        # Imagen decorativa o espacio extra si sobra
        # 




    # --- MÉTODOS (Lógica intacta, solo ajustes visuales) ---
    def buscar_libro(self):
        id_libro = self.txt_id_libro.get()
        if id_libro:
            self.controller.verificar_libro(id_libro)

    def buscar_solicitante(self):
        id_sol = self.txt_id_usuario.get()
        if id_sol:
            self.controller.verificar_solicitante(id_sol)

    def evento_prestar(self):
        self.controller.registrar_prestamo(
            self.txt_id_libro.get(),
            self.txt_id_usuario.get(),
            self.combo_dias.get()
        )
        
    def mostrar_mensaje(self, msg, error=False):
        if error:
            messagebox.showerror("Atención", msg)
        else:
            messagebox.showinfo("Éxito", msg)
        
    def actualizar_info_libro(self, texto, disponible=True):
        # CAMBIO: Usamos colores oscuros pero distinguibles para accesibilidad
        color = "#2E7D32" if disponible else "#C62828" # Verde oscuro / Rojo oscuro
        self.lbl_info_libro.configure(text=texto, text_color=color, font=("Arial", 16, "bold"))
        
    def actualizar_info_usuario(self, texto, valido=True):
        color = "#2E7D32" if valido else "#C62828"
        self.lbl_info_usuario.configure(text=texto, text_color=color, font=("Arial", 16, "bold"))